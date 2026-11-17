# Capstone criteria run: after_threads

- Produced by: `run_capstone_criteria.py::main` (3 trials)
- Code under test: clean clone at commit `fd9b4ab`
- Run: 2026-11-17 02:21
- Each trial starts fresh gunicorn servers with RUNNING.md's command, logs in a throwaway dir

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every request leaves a log line | 20/20 lines each trial | ok: 20/20 lines | ok: 20/20 lines | ok: 20/20 lines | MET |
| 2. Starts from RUNNING.md alone | ready within 60s, 3 of 3 | ok: 10s | ok: 7s | ok: 7s | MET |
| 3. First request not slow | first < 1s, next-50 median < 250ms | ok: first 0.083s, median 0.083s | ok: first 0.084s, median 0.085s | ok: first 0.081s, median 0.091s | MET |
| 4. Overload: refusal and a record | no 5xx, 40-50 x429, 60/60 logged | ok: 50 x429, 0 x5xx, 60/60 logged | ok: 50 x429, 0 x5xx, 60/60 logged | ok: 50 x429, 0 x5xx, 60/60 logged | MET |
| 5. Memory and CPU ceiling | < 1000 MB, < 0.5s CPU per request | ok: 919 MB, 0.357s CPU | ok: 947 MB, 0.326s CPU | ok: 918 MB, 0.33s CPU | MET |

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
      "ready_s": 9.56256590198609,
      "ok": true
    },
    "3": {
      "first_s": 0.083,
      "first_status": 200,
      "median_next50_s": 0.083,
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
      "rss_mb": 919,
      "cpu_s_per_request": 0.357,
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
      "ready_s": 7.3757879530021455,
      "ok": true
    },
    "3": {
      "first_s": 0.084,
      "first_status": 200,
      "median_next50_s": 0.085,
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
      "rss_mb": 947,
      "cpu_s_per_request": 0.326,
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
      "ready_s": 6.835289616981754,
      "ok": true
    },
    "3": {
      "first_s": 0.081,
      "first_status": 200,
      "median_next50_s": 0.091,
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
      "rss_mb": 918,
      "cpu_s_per_request": 0.33,
      "ok": true
    }
  }
]
```
