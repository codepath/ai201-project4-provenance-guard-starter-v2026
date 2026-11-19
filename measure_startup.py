#!/usr/bin/env python3
"""
Before/after for model preload: start the service cold, then time the first
real /submit.   python measure_startup.py --trials 3

For each mode (AI201_PRELOAD=0 = before, 1 = after) and trial it records:
  ready_s   process start until /ping answers
  first_ms  the first /submit, as a caller sees it
  score     the combined_score for a fixed text, to prove scoring is unchanged
  total_s   process start until the first scored answer
"""
import json, os, statistics, subprocess, sys, tempfile, time, urllib.request
from datetime import datetime
from load_test import post, TEXT

PORT = 5058
URL = f"http://127.0.0.1:{PORT}"


def trial(preload):
    env = dict(os.environ, AI201_PRELOAD=preload, AI201_LOG_DIR=tempfile.mkdtemp())
    t0 = time.perf_counter()
    p = subprocess.Popen([sys.executable, "-m", "gunicorn", "app:app", "--bind", f"127.0.0.1:{PORT}",
                          "--workers", "1", "--threads", "4", "--timeout", "120"],
                         env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        while True:
            try:
                urllib.request.urlopen(URL + "/health", timeout=1); break
            except Exception:
                time.sleep(0.1)
                if time.perf_counter() - t0 > 180: raise SystemExit("never came up")
        ready = time.perf_counter() - t0
        body = json.dumps({"creator_id": "startup_probe", "text": TEXT}).encode()
        req = urllib.request.Request(URL + "/submit", body, {"Content-Type": "application/json"})
        t1 = time.perf_counter()
        score = json.load(urllib.request.urlopen(req, timeout=180))["combined_score"]
        first = (time.perf_counter() - t1) * 1000
        return ready, first, score, time.perf_counter() - t0
    finally:
        p.terminate(); p.wait(timeout=30); time.sleep(1)


def main():
    n = int(sys.argv[sys.argv.index("--trials") + 1]) if "--trials" in sys.argv else 3
    out = {}
    for name, flag in (("before (no preload)", "0"), ("after (preload)", "1")):
        out[name] = [trial(flag) for _ in range(n)]
        print(name, [tuple(round(x, 2) for x in r) for r in out[name]])
    md = ["# Model preload: before and after", "",
          f"- Produced by: `measure_startup.py` · {datetime.now():%Y-%m-%d %H:%M} · {n} cold starts per mode", "",
          "| mode | ready (s) | first /submit (ms) | start to first score (s) | combined_score |",
          "|---|---|---|---|---|"]
    for name, rows in out.items():
        m = lambda i: statistics.median(r[i] for r in rows)
        md.append(f"| {name} | {m(0):.1f} | {m(1):.0f} | {m(3):.1f} | {sorted(set(r[2] for r in rows))} |")
    md += ["", "Per-trial (ready s, first ms, score, total s):", ""]
    for name, rows in out.items():
        md.append(f"- {name}: " + "; ".join(f"({r[0]:.1f}, {r[1]:.0f}, {r[2]}, {r[3]:.1f})" for r in rows))
    path = f"results/preload_{datetime.now():%Y-%m-%d_%H%M}.md"
    open(path, "w").write("\n".join(md) + "\n"); print("wrote", path)


if __name__ == "__main__":
    main()
