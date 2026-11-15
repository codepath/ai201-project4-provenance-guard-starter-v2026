# Running the AI201 Capstone

The capstone extends this same Provenance Guard repository on branch
`capstone/observability`. This Downloads folder is a linked Git worktree; keep
the original project folder because it owns the shared Git metadata.

## Start on this computer

Double-click **Start Capstone.cmd**, or run this single command in this folder:

```powershell
& ".\Start Capstone.cmd"
```

Open http://127.0.0.1:5050. The launcher uses this folder's `.venv` first, then
the existing sibling Provenance Guard environment if available. If neither
exists, it creates a Python 3.13 environment and installs the pinned direct
dependencies. Python 3.13 must already be installed. First-time setup requires
internet. A browser can open before startup completes; refresh after the
terminal prints the local URL. Ctrl+C in the server terminal stops it.

## Reproduce from a clean checkout

```powershell
git clone --branch capstone/observability <YOUR-EXISTING-REPOSITORY-URL>
cd <CLONED-FOLDER>
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-capstone-lock.txt
.\.venv\Scripts\python.exe capstone.py
```

`capstone.py` is the single server start command after environment setup.
The complete freeze includes gunicorn inherited from the original environment;
the Windows capstone does not use it. Direct requirements are separately pinned
in `requirements-capstone.txt`. Use `--port 5051` if 5050 is occupied.

Tested interpreter: CPython 3.13.2, Windows. Flask 3.1.3, Flask-Limiter 3.12,
requests 2.34.2, transformers 4.57.6, torch 2.15.0, certifi 2026.10.23.
GPT-2 downloads approximately 550 MB on first analysis; allow several GB for
Python, PyTorch, dependency caches and model files. No API key is needed.
Warm model state is process-local, so restarting incurs initialization again.

## Evidence and tests

With the server running, in a second terminal:

```powershell
.\.venv\Scripts\python.exe evaluate_capstone.py --phase after
.\.venv\Scripts\python.exe -m unittest test_service test_capstone -v
node --check static/capstone.js
```

If using the sibling environment, replace the Python executable with
`..\ai201-project4-provenance-guard-starter-v2026\.venv\Scripts\python.exe`.
The HTTP evaluator uses the **real GPT-2**, three trials per criterion plus ten
warm cost requests; contract tests use explicit model mocks. The evaluator
appends synthetic audit/trace entries and replaces the named phase evidence
file. Preserve committed evidence before deliberately collecting another run.

The before-fix version is commit `35460ab`; its evaluator uses the same cases
and targets. To reproduce the comparison, use a temporary checkout of that
commit on another port. Do not reset or rewrite the project history.

## Files and operational limits

`logs/requests.jsonl`: operational traces. `logs/audit.jsonl`: original decisions,
rejections and appeals. `results/capstone/`: real responses and cost samples.
`GET /ops/traces` and `/ops/export` expose the latest 500 request traces.
`POST /submit`, `/appeal`, `/ping`, `GET /log` and `/health` remain available.
Dashboard and asset requests are excluded from operational telemetry.

The server binds only to 127.0.0.1, disables the debugger and serializes requests.
This is a documented local deployment, not a production multiworker server.
The in-memory limiter resets at restart; creator IDs are asserted identities.
The original audit retains creator IDs and appeal reasons. Logs have no
retention policy or rotation; do not use personal material in committed demos.
Per-request wall timing excludes trace persistence and network transfer; the
evaluator separately measures HTTP client elapsed time.

If the model is unavailable, the original service returns 503 and records its
failure trace. Check internet/model-cache availability and dependency installation.
If trace storage fails, the service preserves the original response, emits an
operator error, and adds `X-Telemetry-Status: write_failed`; durability is not
claimed during disk failure. Browser visual verification was unavailable in
the authoring session; verify the UI locally before a presentation.
