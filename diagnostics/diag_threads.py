"""Capstone diagnosis of criterion 5 (CPU per request). See README, The Improvement."""
import sys, subprocess, tempfile, os, time
from pathlib import Path
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))
import run_capstone_criteria as rc
t = Path(tempfile.mkdtemp())
subprocess.run(["git","clone","-q",str(rc.ROOT),str(t/"c")],check=True)
res = {}
for rnd in range(2):
    for th in ("default", "1", "2", "4"):
        if th == "default": os.environ.pop("OMP_NUM_THREADS", None)
        else: os.environ["OMP_NUM_THREADS"] = th
        s = rc.Server(t/"c", t/f"l{rnd}{th}"); s.wait_ready()
        for i in range(5): rc.submit(f"w{i}")
        _, c0 = s.ps(); w0 = time.perf_counter()
        for i in range(30): rc.submit(f"m{i}")
        wall = (time.perf_counter()-w0)/30; _, c1 = s.ps()
        res.setdefault(th, []).append(((c1-c0)/30, wall))
        print(f"round {rnd} threads={th:7} cpu/req {(c1-c0)/30:.3f}s wall/req {wall:.3f}s load1 {os.getloadavg()[0]:.1f}", flush=True)
        s.stop()
