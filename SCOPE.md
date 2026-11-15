# Capstone scope

Base: Provenance Guard, existing repository commit d0efd19.
Shape A: deploy locally and instrument the existing service.
Path B: a loopback-only, single-process server with durable JSONL request traces,
stage timing, CPU/wall cost measurement, and an operator dashboard over those traces.
The dashboard presents the operational layer; it does not change detection.

Out of scope: new detector, changed thresholds, classifier accuracy claims,
authentication, public hosting, automated appeal decisions, other AI201 systems.
Declared stretch: measured latency breakdown across existing request stages.
One planned improvement after baseline: diagnose and correct telemetry coverage
if error responses are absent. All five criteria will be rerun unchanged.

This folder is a Git worktree sharing the original repository, not a new repo.
AI drafted criteria at the user's request; unaided authorship is not claimed.
