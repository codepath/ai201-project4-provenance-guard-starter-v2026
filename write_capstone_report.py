"""Render the capstone write-up from actual saved measurements."""
import json
from pathlib import Path

root=Path(__file__).parent
before=json.loads((root/'results/capstone/before.json').read_text(encoding='utf-8'))
after=json.loads((root/'results/capstone/after.json').read_text(encoding='utf-8'))
names=['Successful request trace','Rejected request trace','Stage attribution','Warm local latency','Original workflow preserved']
targets=[3,5,3,3,1]

def table(data):
    rows=['| Criterion | Target per trial | Run 1 | Run 2 | Run 3 | Verdict |','|---|---|---|---|---|---|']
    for i,name in enumerate(names):
        counts=[f"{t['counts'][i]}/{targets[i]}" for t in data['trials']]
        rows.append(f"| {i+1}. {name} | {targets[i]}/{targets[i]} | "+' | '.join(counts)+f" | {data['verdicts'][i]} |")
    return '\n'.join(rows)

allrows=after['trials'][-1]['traces']+after['cost_samples']
by_id={row['request_id']:row for row in allrows}
ids=[r['request_id'] for r in after['requests'] if r['request_id'] in by_id]
examples=[by_id[rid] for rid in ids[:11]]
trial=after['trials'][0]
success=trial['successes'][0]
stage_row=by_id[success['request_id']]
cpu=after['mean_cpu_seconds']; wall=after['mean_wall_seconds']
comparison=['| Criterion | Before: trials 1 / 2 / 3 | After: trials 1 / 2 / 3 | Change |','|---|---|---|---|']
for i,name in enumerate(names):
    b=' / '.join(str(t['counts'][i]) for t in before['trials'])
    a=' / '.join(str(t['counts'][i]) for t in after['trials'])
    comparison.append(f"| {i+1}. {name} (out of {targets[i]}) | {b} | {a} | {before['verdicts'][i]} → {after['verdicts'][i]} |")

report=f'''

## Capstone

**What This Extends**

This extends the existing Provenance Guard at `d0efd19`, preserving its GPT-2
signal, stylometry, combination rule, thresholds, submission API and manual
appeal workflow. The extension adds a local operational run path, request-level
JSONL telemetry, stage timing, measured compute costs and an operator dashboard.
The folder `AI201 Capstone` is a linked worktree of the original repository on
`capstone/observability`; its shared history makes the extension inspectable.
Original project criteria are preserved in `criteria-project4.md`.

**The Shape**

Shape A — deploy and instrument. Scope was recorded in `SCOPE.md` before running
the criteria. Out of scope: a replacement detector, altered thresholds,
new retrieval/search systems, automated review decisions, authentication and
public hosting. The UI is an operator view of the operational layer and existing
workflow. Declared stretch: latency breakdown across the existing scoring stages.

**Running It**

Path B — local with logs. See [RUNNING.md](RUNNING.md). Start with
`python capstone.py` after environment setup, or double-click `Start Capstone.cmd`.
The service binds to `127.0.0.1:5050`, disables the debugger and serves one request
at a time. The Windows launcher can reuse the existing sibling environment;
standalone environment setup and the full package freeze are documented.
No remote deployment, repository push or course submission is claimed.

**Instrumentation**

`telemetry.install` in `telemetry.py` records UTC timestamp, generated request ID,
HTTP method/route, input summary (type, field names, lengths and SHA-256 rather
than full prose), output JSON, response status, wall milliseconds, process CPU
milliseconds and stage milliseconds. The response includes `X-Request-ID`.
The unchanged audit log holds decisions and appeals separately. `/log` telemetry
summarizes its count rather than recursively copying history. Dashboard/assets
are excluded so observing the system does not dominate its measurements.
Traces are appended to `logs/requests.jsonl`; latest-500 views and JSONL export
are available in the dashboard. This is single-process local persistence, not
a tamper-proof log or a multiworker observability platform.

Eleven actual post-improvement records follow, including rejected inputs:

```jsonl
{chr(10).join(json.dumps(row,ensure_ascii=False) for row in examples)}
```

The complete original response objects and per-trial trace snapshots are in
`results/capstone/before.json` and `after.json`. Failed runs are retained; no
successes were substituted for errors. Disk-write failure is covered separately
by an isolated operational contract test and exposes `X-Telemetry-Status`.

**What It Costs**

Ten real, warm `/submit` requests after the fix averaged **{cpu:.7f} seconds of
process CPU** and **{wall:.7f} seconds of server wall time** per request.
The before-fix ten-run measurements were {before['mean_cpu_seconds']:.7f} CPU
seconds and {before['mean_wall_seconds']:.7f} wall seconds. These are separate
batches on one laptop, not evidence that failure logging caused a CPU change.
`time.process_time` and `time.perf_counter` surround each handler; the evaluator
correlates each response to its persisted trace and averages the ten samples.
No hosted model API is called, so measured API spend is $0. Electricity,
hardware depreciation, setup and model download are not priced here.

At 100 people/day and one warm submission each: 100 × {cpu:.7f} =
**{100*cpu:.5f} CPU seconds/day**, and 100 × {wall:.7f} =
**{100*wall:.5f} seconds/day of serial handler wall time**. This is arithmetic
under the stated workload, not a load-capacity claim. Initial real-model requests
took {before['warmup']['client_ms']/1000:.3f}s before and
{after['warmup']['client_ms']/1000:.3f}s after restart (client elapsed, including
initialization). Cold initialization is excluded from the warm latency target.
Trace persistence, network transfer and time queued before the handler are
excluded from server wall time; client timings include HTTP overhead.

**Run Log and Verdicts**

Criteria were committed at `da9969a`, before the first results commit `35460ab`.
Five targets were held unchanged. `evaluate_capstone.py::run` issued new HTTP
requests against real GPT-2 for every trial; it did not replay responses or mock
model scores. Three varied texts are reused as controlled fixtures across trials;
deterministic inference explains repeated scores. Criteria 1, 3 and 4 share each
trial's three successful requests because the properties concern the same runs.
Each trial also has five distinct invalid cases and one complete appeal workflow.
This is operational validation, not an authorship accuracy evaluation.

Before improvement:

{table(before)}

Criterion 2 MISSED in every trial. The initial telemetry implementation
explicitly filtered out HTTP statuses >=400 in `telemetry.install::finish_trace`.
The original routes correctly rejected each invalid case, and their existing
rejection audit still worked, but the new request telemetry omitted them. This
is a response-filter mechanism, not a detector failure. The initial design's
success-only coverage and planned coverage improvement were disclosed in scope.
Criteria 1, 3, 4 and 5 MET their stated targets; they do not establish accuracy.

Actual output supporting each criterion, trial 1 after the fix:

1. `app.py::submit` and `telemetry.install::finish_trace`, correlated response:

```json
{json.dumps(success,indent=2)}
```

2. `app.py::submit` through `evaluate_capstone.py::run`, malformed JSON:

```json
{json.dumps(trial['failures'][0],indent=2)}
```

3. `telemetry.stage`, actual stage measurements from that submission:

```json
{json.dumps({'request_id':stage_row['request_id'],'wall_ms':stage_row['wall_ms'],'stages':stage_row['stages']},indent=2)}
```

4. `evaluate_capstone.py::run`, three client-measured warm elapsed times:

```json
{json.dumps({'client_ms':[r['client_ms'] for r in trial['successes']]},indent=2)}
```

5. `app.py::appeal`, actual response; the evaluator independently compares the
original decided event before/after the appeal and checks the appended event:

```json
{json.dumps(trial['appeal'],indent=2)}
```

**The Improvement**

One measured change: include unsuccessful responses in the request telemetry.
Commit `c7fdbcd` changes `INCLUDE_FAILURES` from false to true. It preserves the
original rejection status and message, scoring and decision log. After restarting,
the entire evaluation ran again, three trials per criterion plus ten cost runs:

{table(after)}

Both sets side by side:

{chr(10).join(comparison)}

The change recovered all 15 missing invalid-request traces in the repeated
trials while the four other targets remained met. Rejected request logging adds
disk writes for errors, an intentional visibility cost. Stage timings show where
time went; these trials do not establish concurrent throughput or disk-failure
durability. Contract tests use explicit mocks for model failure/rate limiting and
are separate from this real-model evidence.

**What's Still Broken**

All five final targets were met, but the 5,000ms warm latency limit is loose for
these short fixtures. Next evaluation would tighten it to 1,000ms and add texts
near the 400-token cap; current results are retained against the original target.
The initial 65–69s model startup is substantial. The first operational follow-up
would be explicit model warm-up/readiness so a writer can see initialization
before submitting; it was left out to keep this capstone bounded.

Logging is unrotated and unauthenticated; in-memory rate limits reset at restart.
The last-500 dashboard does not show all-time totals. CPU attribution relies on
the serial single-process run path. No concurrency, recovery under full disk,
public hosting or security hardening claim is made. GPT-2 predictability and
style are uncalibrated authorship heuristics; errors and uneven treatment of
plain-language writers remain unresolved. Appeals only record review requests.
Browser access was unavailable during authoring, so visual and interactive
browser QA remains unverified; HTTP assets and contract behavior are checked.

**How I Used AI**

1. The initial request asked AI to create the strongest capstone from prior
AI201 work. The assistant initially proposed combining several projects; after
reading the supplied assignment, the implementation changed to a bounded
operational extension of Provenance Guard in the existing repository history.
2. The assistant requested student-authored criteria. The user explicitly replied
“write them and make them acceptable.” AI then drafted all five criteria, wrote
the extension and evaluator, collected actual outputs and generated this report
from those outputs. The missing-error-trace diagnosis led to the recorded filter
fix and full rerun. No student-authored criteria, unaided diagnosis or personal
reflection is claimed. **This does not satisfy the assignment's unaided criteria
requirement.** The student needs to review, disclose and defend this work; later
editing cannot retroactively establish unaided pre-evaluation authorship.
'''
readme=root/'README.md'
text=readme.read_text(encoding='utf-8')
if '\n## Capstone\n' in text:
    text=text.split('\n## Capstone\n')[0].rstrip()
readme.write_text(text.rstrip()+report,encoding='utf-8')
print('Appended measured capstone report to README.md')
