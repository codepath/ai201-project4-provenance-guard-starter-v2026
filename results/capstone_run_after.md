# Capstone criteria run: after

- Produced by: `run_capstone_criteria.py::main` (3 trials)
- Code under test: clean clone at commit `785c625`
- Run: 2026-11-17 02:12
- Each trial starts fresh gunicorn servers with RUNNING.md's command, logs in a throwaway dir

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every request leaves a log line | 20/20 lines each trial | ok: 20/20 lines | ok: 20/20 lines | ok: 20/20 lines | MET |
| 2. Starts from RUNNING.md alone | ready within 60s, 3 of 3 | ok: 7s | ok: 8s | ok: 8s | MET |
| 3. First request not slow | first < 1s, next-50 median < 250ms | ok: first 0.085s, median 0.095s | ok: first 0.075s, median 0.099s | ok: first 0.089s, median 0.08s | MET |
| 4. Overload: refusal and a record | no 5xx, 40-50 x429, 60/60 logged | ok: 50 x429, 0 x5xx, 60/60 logged | ok: 50 x429, 0 x5xx, 60/60 logged | ok: 50 x429, 0 x5xx, 60/60 logged | MET |
| 5. Memory and CPU ceiling | < 1000 MB, < 0.5s CPU per request | FAIL: 967 MB, 0.537s CPU | FAIL: 951 MB, 0.553s CPU | ok: 930 MB, 0.485s CPU | MISSED |

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
      "ready_s": 7.140304696004023,
      "ok": true
    },
    "3": {
      "first_s": 0.085,
      "first_status": 200,
      "median_next50_s": 0.095,
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
      "rss_mb": 967,
      "cpu_s_per_request": 0.537,
      "ok": false
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
      "ready_s": 8.027909832002479,
      "ok": true
    },
    "3": {
      "first_s": 0.075,
      "first_status": 200,
      "median_next50_s": 0.099,
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
      "rss_mb": 951,
      "cpu_s_per_request": 0.553,
      "ok": false
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
      "ready_s": 8.025819992995821,
      "ok": true
    },
    "3": {
      "first_s": 0.089,
      "first_status": 200,
      "median_next50_s": 0.08,
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
      "rss_mb": 930,
      "cpu_s_per_request": 0.485,
      "ok": true
    }
  }
]
```
