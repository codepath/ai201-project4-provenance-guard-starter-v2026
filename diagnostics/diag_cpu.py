"""Capstone diagnosis of criterion 5 (CPU per request). See README, The Improvement."""
import sys, subprocess, tempfile, statistics, os, time
from pathlib import Path
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))
import run_capstone_criteria as rc
ROOT = rc.ROOT
t = Path(tempfile.mkdtemp())
for name, ref in (("after", None), ("before", "bb0a8ba")):
    subprocess.run(["git","clone","-q",str(ROOT),str(t/name)],check=True)
    if ref: subprocess.run(["git","checkout","-q",ref,"--","detector.py"],cwd=t/name,check=True)
rows = {"before": [], "after": []}
for rnd in range(5):
    for name in ("before", "after") if rnd % 2 == 0 else ("after", "before"):
        s = rc.Server(t/name, t/f"logs{rnd}{name}")
        s.wait_ready()
        for i in range(5): rc.submit(f"w{i}")          # settle
        rss0, c0 = s.ps(); w0 = time.perf_counter()
        for i in range(30): rc.submit(f"m{i}")
        wall = (time.perf_counter()-w0)/30
        rss, c1 = s.ps()
        load = os.getloadavg()[0]
        rows[name].append(((c1-c0)/30, wall, rss, load))
        print(f"round {rnd} {name:6} cpu/req {(c1-c0)/30:.3f}s wall/req {wall:.3f}s rss {rss:.0f}MB load1 {load:.1f}", flush=True)
        s.stop()
for name in rows:
    cpu=[r[0] for r in rows[name]]; wall=[r[1] for r in rows[name]]
    print(f"{name}: cpu median {statistics.median(cpu):.3f} range {min(cpu):.3f}-{max(cpu):.3f}; wall median {statistics.median(wall):.3f}")
