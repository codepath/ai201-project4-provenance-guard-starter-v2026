# Capstone criteria run: before

- Produced by: `run_capstone_criteria.py::main` (3 trials)
- Code under test: clean clone at commit `785c625`, with `detector.py` taken from `bb0a8ba`
- Run: 2026-11-17 02:09
- Each trial starts fresh gunicorn servers with RUNNING.md's command, logs in a throwaway dir

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every request leaves a log line | 20/20 lines each trial | ok: 20/20 lines | ok: 20/20 lines | ok: 20/20 lines | MET |
| 2. Starts from RUNNING.md alone | ready within 60s, 3 of 3 | ok: 10s | ok: 6s | ok: 7s | MET |
| 3. First request not slow | first < 1s, next-50 median < 250ms | FAIL: first 2.138s, median 0.077s | ok: first 0.259s, median 0.075s | ok: first 0.283s, median 0.073s | MISSED |
| 4. Overload: refusal and a record | no 5xx, 40-50 x429, 60/60 logged | ok: 50 x429, 0 x5xx, 60/60 logged | ok: 50 x429, 0 x5xx, 60/60 logged | ok: 50 x429, 0 x5xx, 60/60 logged | MET |
| 5. Memory and CPU ceiling | < 1000 MB, < 0.5s CPU per request | ok: 932 MB, 0.441s CPU | ok: 922 MB, 0.438s CPU | ok: 931 MB, 0.479s CPU | MET |

The target has to hold in every trial, not on average.

## Raw output

```json
[
  {
    "1": {
      "requests": 20,
      "log_lines": 20,
      "fields_complete": true,
      "errors_named": true,
      "statuses": {
        "200": 10,
        "400": 5,
        "429": 5
      },
      "ok": true
    },
    "2": {
      "ready_s": 9.581862626990187,
      "ok": true
    },
    "3": {
      "first_s": 2.138,
      "first_status": 200,
      "median_next50_s": 0.077,
      "ok": false
    },
    "4": {
      "status_counts": {
        "200": 10,
        "429": 50
      },
      "n429": 50,
      "n5xx": 0,
      "log_lines": 60,
      "ok": true
    },
    "5": {
      "rss_mb": 932,
      "cpu_s_per_request": 0.441,
      "ok": true
    }
  },
  {
    "1": {
      "requests": 20,
      "log_lines": 20,
      "fields_complete": true,
      "errors_named": true,
      "statuses": {
        "200": 10,
        "400": 5,
        "429": 5
      },
      "ok": true
    },
    "2": {
      "ready_s": 6.363829178997548,
      "ok": true
    },
    "3": {
      "first_s": 0.259,
      "first_status": 200,
      "median_next50_s": 0.075,
      "ok": true
    },
    "4": {
      "status_counts": {
        "200": 10,
        "429": 50
      },
      "n429": 50,
      "n5xx": 0,
      "log_lines": 60,
      "ok": true
    },
    "5": {
      "rss_mb": 922,
      "cpu_s_per_request": 0.438,
      "ok": true
    }
  },
  {
    "1": {
      "requests": 20,
      "log_lines": 20,
      "fields_complete": true,
      "errors_named": true,
      "statuses": {
        "200": 10,
        "400": 5,
        "429": 5
      },
      "ok": true
    },
    "2": {
      "ready_s": 6.616345465998165,
      "ok": true
    },
    "3": {
      "first_s": 0.283,
      "first_status": 200,
      "median_next50_s": 0.073,
      "ok": true
    },
    "4": {
      "status_counts": {
        "200": 10,
        "429": 50
      },
      "n429": 50,
      "n5xx": 0,
      "log_lines": 60,
      "ok": true
    },
    "5": {
      "rss_mb": 931,
      "cpu_s_per_request": 0.479,
      "ok": true
    }
  }
]
```
