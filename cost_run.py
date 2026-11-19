#!/usr/bin/env python3
"""
Cost per run: what one /submit costs in compute on this machine.

    AI201_LOG_DIR=/tmp/ai201_cost gunicorn app:app --bind 127.0.0.1:5057 --workers 1 --threads 4 --timeout 120 &
    python cost_run.py --url http://127.0.0.1:5057 --n 100

Sends N sequential requests (distinct creator_ids, so the limiter stays out of
it), reading the worker's CPU time and memory from `ps` before and after.
CPU time, not wall time, is what you'd pay for on a host: wall time includes
waiting. Dollar figures use a stated assumed price, not a quote.
"""
import argparse, subprocess, time
from datetime import datetime
from load_test import post


def worker_pid():
    pids = subprocess.check_output(["pgrep", "-f", "gunicorn app:app"], text=True).split()
    best = max(pids, key=lambda p: rss_mb(p))      # the worker holds the model
    return best


def rss_mb(pid):
    return int(subprocess.check_output(["ps", "-o", "rss=", "-p", str(pid)], text=True)) / 1024


def cpu_s(pid):
    t = subprocess.check_output(["ps", "-o", "time=", "-p", str(pid)], text=True).strip()
    mins, secs = t.split(":")
    return int(mins) * 60 + float(secs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:5000")
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--price-per-vcpu-hour", type=float, default=0.05,
                    help="ASSUMED cloud price, $ per vCPU-hour")
    ap.add_argument("--attack-rows", type=int, default=0, help="rows in the attack set")
    a = ap.parse_args()

    pid = worker_pid()
    post(a.url, "cost_warmup")                         # model load, excluded
    idle_rss = rss_mb(pid)
    cpu0, t0 = cpu_s(pid), time.perf_counter()
    codes = [post(a.url, f"cost_{i}")[0] for i in range(a.n)]
    wall = time.perf_counter() - t0
    cpu = cpu_s(pid) - cpu0
    ok = codes.count(200)
    per_cpu, per_wall = cpu / ok, wall / ok
    usd = per_cpu / 3600 * a.price_per_vcpu_hour
    lines = [
        "# Cost per run", "",
        f"- Produced by: `cost_run.py` · {datetime.now():%Y-%m-%d %H:%M}",
        f"- Machine: Intel i9-8950HK, 12 logical cores; one gunicorn worker, GPT-2, Python 3.11",
        f"- {ok}/{a.n} sequential warm `/submit` calls succeeded", "",
        "| measure | value |", "|---|---|",
        f"| CPU time per request | {per_cpu*1000:.0f} ms |",
        f"| Wall time per request | {per_wall*1000:.0f} ms |",
        f"| Worker memory (resident), loaded | {rss_mb(pid):.0f} MB |",
        f"| Marginal $ per request, local | $0 (no API, no per-call fee) |",
        f"| Equivalent $ per request on a cloud vCPU at ${a.price_per_vcpu_hour}/vCPU-hr (ASSUMED) | ${usd:.7f} |",
        f"| Equivalent $ per 1,000 requests | ${usd*1000:.4f} |",
    ]
    if a.attack_rows:
        lines.append(f"| One attack run ({a.attack_rows} rows) | {a.attack_rows*per_cpu:.1f} CPU-s, {a.attack_rows*per_wall:.1f} s wall |")
    lines += ["", "The first request after a start costs far more (model load, about 12-15 s of wall time); "
              "that is a one-time cost per process start, excluded above."]
    path = f"results/cost_{datetime.now():%Y-%m-%d_%H%M}.md"
    open(path, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines)); print("wrote", path)


if __name__ == "__main__":
    main()
