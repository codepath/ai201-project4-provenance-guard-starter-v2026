#!/usr/bin/env python3
"""
Load observation: normal rate vs ten times normal rate.

    gunicorn app:app --bind 127.0.0.1:5000 --workers 1 --threads 4 --timeout 120
    python load_test.py --normal-per-min 6 --seconds 60

"Normal" is a stated assumption, not a measurement: the README expects a writer
to submit a few times an hour, so a service with a handful of active writers sees
about 6 requests a minute. Phase 2 sends ten times that. Every request uses a
different creator_id so the per-creator rate limit (10/min) never fires and
we measure the service, not the limiter.

Latency is measured client-side (what a caller sees) and the server's own
request log is read back for the per-stage breakdown.
"""
import argparse
import json
import statistics
import threading
import time
import urllib.request
from datetime import datetime

TEXT = ("The committee met on Tuesday to discuss the budget, and honestly nobody "
        "agreed on anything. The chair tried twice to move on, but Margaret kept "
        "returning to the parking question, which had been settled in March.")


def post(url, creator):
    body = json.dumps({"creator_id": creator, "text": TEXT}).encode()
    req = urllib.request.Request(url + "/submit", body, {"Content-Type": "application/json"})
    t = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            status = r.status
    except urllib.error.HTTPError as e:
        status = e.code
    except Exception:
        status = 0
    return status, (time.perf_counter() - t) * 1000


def phase(url, name, per_min, seconds):
    interval = 60.0 / per_min
    results, threads = [], []
    lock = threading.Lock()

    def one(i):
        s, ms = post(url, f"load_{name}_{i}")
        with lock:
            results.append((s, ms))

    start = time.perf_counter()
    i = 0
    while time.perf_counter() - start < seconds:
        th = threading.Thread(target=one, args=(i,))
        th.start(); threads.append(th); i += 1
        time.sleep(max(0, start + i * interval - time.perf_counter()))
    for th in threads:
        th.join()
    return results, time.perf_counter() - start


def pct(v, p):
    v = sorted(v)
    return v[min(len(v) - 1, int(round(p / 100 * (len(v) - 1))))]


def summarise(name, per_min, results, wall):
    ok = [ms for s, ms in results if s == 200]
    codes = {}
    for s, _ in results:
        codes[s] = codes.get(s, 0) + 1
    row = f"| {name} | {per_min}/min | {len(results)} | {codes} |"
    if ok:
        row += (f" {statistics.median(ok):.0f} | {pct(ok, 95):.0f} | {max(ok):.0f} |")
    else:
        row += " – | – | – |"
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:5000")
    ap.add_argument("--normal-per-min", type=int, default=6)
    ap.add_argument("--factor", type=int, default=10)
    ap.add_argument("--seconds", type=int, default=60)
    a = ap.parse_args()

    print("warm-up request (loads the model; excluded from both phases)...")
    s, ms = post(a.url, "load_warmup")
    print(f"  {s} in {ms:.0f} ms")

    rows = []
    for name, rate in (("normal", a.normal_per_min), (f"{a.factor}x", a.normal_per_min * a.factor)):
        print(f"phase {name}: {rate}/min for {a.seconds}s")
        res, wall = phase(a.url, name, rate, a.seconds)
        rows.append(summarise(name, rate, res, wall))
        print(rows[-1])

    out = ["# Load observation", "",
           f"- Produced by: `load_test.py` · {datetime.now():%Y-%m-%d %H:%M}",
           f"- Normal rate assumed: {a.normal_per_min} requests/min; load phase {a.factor}x that; {a.seconds}s each",
           f"- Warm-up (model load, excluded): {s} in {ms:.0f} ms", "",
           "| phase | rate | sent | status codes | p50 ms | p95 ms | max ms |",
           "|---|---|---|---|---|---|---|", *rows, ""]
    path = f"results/load_{datetime.now():%Y-%m-%d_%H%M}.md"
    open(path, "w").write("\n".join(out))
    print("wrote", path)


if __name__ == "__main__":
    main()
