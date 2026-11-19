"""
Load observation: send requests at a steady rate and report latency.

    python load_test.py --rate 60 --seconds 60

Normal use is taken as ~6 submissions a minute; ten times that is 60 a minute.
Each request uses its own creator_id so the per-creator rate limit doesn't hide
the load. Latency per stage comes from logs/requests.jsonl, not from here.
"""
import argparse, json, statistics, threading, time, urllib.request

TEXT = ("The meeting ran long because nobody had read the notes beforehand, "
        "so we spent the first twenty minutes catching up and the rest arguing "
        "about a deadline that had already passed.")

def one(i, url, out):
    body = json.dumps({"text": TEXT, "creator_id": f"load-{i}"}).encode()
    req = urllib.request.Request(url, body, {"Content-Type": "application/json"})
    t = time.perf_counter()
    try:
        code = urllib.request.urlopen(req, timeout=300).status
    except urllib.error.HTTPError as e:
        code = e.code
    except Exception:
        code = "err"
    out.append((code, time.perf_counter() - t))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rate", type=float, default=60, help="requests per minute")
    ap.add_argument("--seconds", type=int, default=60)
    ap.add_argument("--url", default="http://127.0.0.1:5000/submit")
    a = ap.parse_args()
    out, threads = [], []
    n = int(a.rate * a.seconds / 60)
    start = time.perf_counter()
    for i in range(n):
        time.sleep(max(0, start + i * 60 / a.rate - time.perf_counter()))
        th = threading.Thread(target=one, args=(i, a.url, out)); th.start(); threads.append(th)
    for th in threads: th.join()
    lat = sorted(l for _, l in out)
    codes = {}
    for c, _ in out: codes[c] = codes.get(c, 0) + 1
    q = lambda p: lat[min(len(lat) - 1, int(p * len(lat)))]
    print(f"sent {n} at {a.rate}/min over {a.seconds}s; wall {time.perf_counter()-start:.0f}s")
    print("status counts:", codes)
    print(f"latency s: median {statistics.median(lat):.2f}  p95 {q(.95):.2f}  max {lat[-1]:.2f}")

if __name__ == "__main__":
    main()
