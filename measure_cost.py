"""
Cost of one run: start the service, then report memory, first-request latency
and CPU seconds per request.   python measure_cost.py [label]
"""
import json, subprocess, sys, time, urllib.request, os

label = sys.argv[1] if len(sys.argv) > 1 else "run"
TEXT = ("The meeting ran long because nobody had read the notes beforehand, "
        "so we spent the first twenty minutes catching up and the rest arguing "
        "about a deadline that had already passed.")
env = dict(os.environ, AI201_RATE_LIMITS="0")
p = subprocess.Popen([".venv/bin/gunicorn", "-c", "gunicorn.conf.py", "app:app"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)

def kids():
    out = subprocess.run(["pgrep", "-P", str(p.pid)], capture_output=True, text=True).stdout.split()
    return out

def ps(pid):
    r = subprocess.run(["ps", "-o", "rss=,time=", "-p", str(pid)], capture_output=True, text=True).stdout.split()
    m, s = r[1].split(":"); return int(r[0]) / 1024, int(m) * 60 + float(s)

def post(i):
    req = urllib.request.Request("http://127.0.0.1:5000/submit",
        json.dumps({"text": TEXT, "creator_id": f"c{i}"}).encode(), {"Content-Type": "application/json"})
    t = time.perf_counter(); urllib.request.urlopen(req).read(); return time.perf_counter() - t

try:
    for _ in range(120):
        try: urllib.request.urlopen("http://127.0.0.1:5000/health"); break
        except Exception: time.sleep(1)
    w = kids()[0]
    mb0, cpu0 = ps(w)
    first = post(0)
    rest = [post(i) for i in range(1, 51)]
    mb1, cpu1 = ps(w)
    print(f"[{label}] worker RSS after warm-up {mb0:.0f} MB, after 51 requests {mb1:.0f} MB")
    print(f"[{label}] first request {first:.2f} s; next 50 median {sorted(rest)[25]:.3f} s")
    print(f"[{label}] CPU {cpu1-cpu0:.1f} s for 51 requests = {(cpu1-cpu0)/51*1000:.0f} ms CPU per request")
finally:
    p.terminate(); p.wait()
