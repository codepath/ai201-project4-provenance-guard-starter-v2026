"""
Run my five capstone criteria (criteria.md) against the real service.

    python run_capstone_criteria.py --label before --trials 3
    python run_capstone_criteria.py --label after  --trials 3

Each trial starts fresh gunicorn servers from a CLEAN CLONE of the committed
code (so uncommitted edits are never what gets tested), using the command in
RUNNING.md. Logs go to a throwaway directory through AI201_LOG_DIR, so the
committed logs/ are untouched. Results are written to
results/capstone_run_<label>.md.

Per trial, three servers:
  A  criteria 2, 3, 5  (ready time, first request, median, memory, CPU)
  B  criterion 1       (20 mixed requests, each must leave one log line)
  C  criterion 4       (one creator floods: 429s, no 5xx, all logged)

Two things this does not do, said plainly:
  * It reuses this repo's .venv for the clone instead of building a new venv
    and reinstalling every trial, so criterion 2 tests the start command and
    the committed code, not the pip install.
  * Criterion 5's "10 runs" is 10 consecutive requests after the 51 of
    criterion 3, measured for CPU, with memory read at the end.
"""

import argparse
import json
import os
import statistics
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
PORT = 5057
BASE = f"http://127.0.0.1:{PORT}"
TEXT = ("The meeting ran long because nobody had read the notes beforehand, "
        "so we spent the first twenty minutes catching up and the rest arguing "
        "about a deadline that had already passed.")
GUNICORN = str(ROOT / ".venv" / "bin" / "gunicorn")


# ── helpers ───────────────────────────────────────────────────────────────────

def post(body, raw=False):
    """POST to /submit. Returns (status, seconds). Never raises on HTTP errors."""
    data = body.encode() if raw else json.dumps(body).encode()
    req = urllib.request.Request(f"{BASE}/submit", data, {"Content-Type": "application/json"})
    t = time.perf_counter()
    try:
        status = urllib.request.urlopen(req, timeout=300).status
    except urllib.error.HTTPError as e:
        status = e.code
    except Exception:
        status = "err"
    return status, time.perf_counter() - t


def submit(creator):
    return post({"text": TEXT, "creator_id": creator})


class Server:
    """A gunicorn started the way RUNNING.md says, from a clean clone."""

    def __init__(self, clone, log_dir):
        env = dict(os.environ, PORT=str(PORT), AI201_LOG_DIR=str(log_dir),
                   AI201_RATE_LIMITS="1")
        self.log_dir = Path(log_dir)
        self.started = time.perf_counter()
        self.proc = subprocess.Popen(
            [GUNICORN, "-c", "gunicorn.conf.py", "app:app"],
            cwd=clone, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.ready_s = None

    def wait_ready(self, limit=180):
        while time.perf_counter() - self.started < limit:
            try:
                with urllib.request.urlopen(f"{BASE}/health", timeout=2) as r:
                    if json.load(r).get("detector_loaded"):
                        self.ready_s = time.perf_counter() - self.started
                        return self.ready_s
            except Exception:
                pass
            time.sleep(0.5)
        return None

    def worker(self):
        out = subprocess.run(["pgrep", "-P", str(self.proc.pid)],
                             capture_output=True, text=True).stdout.split()
        return out[0] if out else None

    def ps(self):
        """(resident MB, cumulative CPU seconds) of the worker."""
        r = subprocess.run(["ps", "-o", "rss=,time=", "-p", self.worker()],
                           capture_output=True, text=True).stdout.split()
        m, s = r[1].split(":")
        return int(r[0]) / 1024, int(m) * 60 + float(s)

    def request_lines(self, path="/submit"):
        f = self.log_dir / "requests.jsonl"
        if not f.exists():
            return []
        rows = [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
        return [r for r in rows if r.get("path") == path]

    def stop(self):
        self.proc.terminate()
        try:
            self.proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        time.sleep(1)


# ── the five criteria, one trial each ─────────────────────────────────────────

def trial_a(clone, tmp):
    """Criteria 2, 3 and 5 on one freshly started server."""
    srv = Server(clone, tmp / "logs_a")
    try:
        ready = srv.wait_ready()
        c2 = {"ready_s": ready, "ok": ready is not None and ready <= 60}

        first_status, first = submit("a-0")
        rest = [submit(f"a-{i}")[1] for i in range(1, 51)]
        median = statistics.median(rest)
        c3 = {"first_s": round(first, 3), "first_status": first_status,
              "median_next50_s": round(median, 3),
              "ok": first_status == 200 and first < 1.0 and median < 0.25}

        _, cpu0 = srv.ps()
        for i in range(51, 61):
            submit(f"a-{i}")
        rss, cpu1 = srv.ps()
        cpu_each = (cpu1 - cpu0) / 10
        c5 = {"rss_mb": round(rss), "cpu_s_per_request": round(cpu_each, 3),
              "ok": rss < 1000 and cpu_each < 0.5}
        return c2, c3, c5
    finally:
        srv.stop()


def trial_b(clone, tmp):
    """Criterion 1: 20 mixed requests, each leaves exactly one well-formed line."""
    srv = Server(clone, tmp / "logs_b")
    try:
        srv.wait_ready()
        sent = []
        for _ in range(10):                       # 10 valid, one creator, within the limit
            sent.append(submit("b-valid")[0])
        malformed = [                              # 5 malformed
            ({"creator_id": "b-m1"}, False),
            ({"text": "", "creator_id": "b-m2"}, False),
            ("not json at all", True),
            ("[1, 2, 3]", True),
            ({"text": 123, "creator_id": "b-m5"}, False),
        ]
        for body, raw in malformed:
            sent.append(post(body, raw=raw)[0])
        for _ in range(5):                         # 5 over the limit: same creator again
            sent.append(submit("b-valid")[0])

        time.sleep(1)
        lines = srv.request_lines()
        need = {"ts", "path", "status", "total_ms"}
        complete = all(need <= r.keys() for r in lines)
        errors_ok = all("error" in r for r in lines if r["status"] >= 400)
        ok = len(sent) == 20 and len(lines) == 20 and complete and errors_ok
        return {"requests": len(sent), "log_lines": len(lines),
                "fields_complete": complete, "errors_named": errors_ok,
                "statuses": {s: sent.count(s) for s in sorted(set(sent), key=str)},
                "ok": ok}
    finally:
        srv.stop()


def trial_c(clone, tmp):
    """Criterion 4: one creator sends 60 requests; limit is 10 a minute."""
    srv = Server(clone, tmp / "logs_c")
    try:
        srv.wait_ready()
        statuses = [submit("c-flood")[0] for _ in range(60)]
        time.sleep(1)
        lines = srv.request_lines()
        n429 = statuses.count(429)
        n5xx = sum(1 for s in statuses if isinstance(s, int) and s >= 500) \
            + statuses.count("err")
        return {"status_counts": {s: statuses.count(s) for s in sorted(set(statuses), key=str)},
                "n429": n429, "n5xx": n5xx, "log_lines": len(lines),
                "ok": n5xx == 0 and 40 <= n429 <= 50 and len(lines) == 60}
    finally:
        srv.stop()


# ── the run ───────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True, help="e.g. before or after")
    ap.add_argument("--trials", type=int, default=3)
    a = ap.parse_args()

    results = []
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        clone = tmp / "clone"
        subprocess.run(["git", "clone", "-q", str(ROOT), str(clone)], check=True)
        head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=clone,
                              capture_output=True, text=True).stdout.strip()
        for n in range(1, a.trials + 1):
            print(f"trial {n} ...", flush=True)
            c2, c3, c5 = trial_a(clone, tmp / f"t{n}a")
            c1 = trial_b(clone, tmp / f"t{n}b")
            c4 = trial_c(clone, tmp / f"t{n}c")
            results.append({1: c1, 2: c2, 3: c3, 4: c4, 5: c5})
            print("  ", {k: v["ok"] for k, v in results[-1].items()}, flush=True)

    write_report(a, head, results)


def cell(k, r):
    if k == 1: return f"{r['log_lines']}/20 lines"
    if k == 2: return f"{r['ready_s']:.0f}s" if r["ready_s"] else "never ready"
    if k == 3: return f"first {r['first_s']}s, median {r['median_next50_s']}s"
    if k == 4: return f"{r['n429']} x429, {r['n5xx']} x5xx, {r['log_lines']}/60 logged"
    return f"{r['rss_mb']} MB, {r['cpu_s_per_request']}s CPU"


TARGETS = {
    1: ("Every request leaves a log line", "20/20 lines each trial"),
    2: ("Starts from RUNNING.md alone", "ready within 60s, 3 of 3"),
    3: ("First request not slow", "first < 1s, next-50 median < 250ms"),
    4: ("Overload: refusal and a record", "no 5xx, 40-50 x429, 60/60 logged"),
    5: ("Memory and CPU ceiling", "< 1000 MB, < 0.5s CPU per request"),
}


def write_report(a, head, results):
    out = ROOT / "results" / f"capstone_run_{a.label}.md"
    L = [f"# Capstone criteria run: {a.label}", "",
         f"- Produced by: `run_capstone_criteria.py::main` ({a.trials} trials)",
         f"- Code under test: clean clone at commit `{head}`",
         f"- Run: {datetime.now():%Y-%m-%d %H:%M}",
         "- Each trial starts fresh gunicorn servers with RUNNING.md's command, logs in a throwaway dir", "",
         "| Criterion | Target | " + " | ".join(f"Run {i}" for i in range(1, a.trials + 1)) + " | Verdict |",
         "|---|---|" + "---|" * a.trials + "---|"]
    for k in range(1, 6):
        name, target = TARGETS[k]
        oks = [r[k]["ok"] for r in results]
        verdict = "MET" if all(oks) else "MISSED"
        cells = " | ".join(f"{'ok' if r[k]['ok'] else 'FAIL'}: {cell(k, r[k])}" for r in results)
        L.append(f"| {k}. {name} | {target} | {cells} | {verdict} |")
    L += ["", "The target has to hold in every trial, not on average.", "",
          "## Raw output", "", "```json", json.dumps(results, indent=2), "```", ""]
    out.write_text("\n".join(L))
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
