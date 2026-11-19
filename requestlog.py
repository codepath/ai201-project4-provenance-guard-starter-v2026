"""
The request log: one structured line for EVERY request the service handles.

This is separate from the audit log on purpose. The audit log records decisions
(who was judged what, and appeals) and its shape is fixed by the unit 8 rubric.
This one records what the *service* did: what was asked, what came back, how
long it took, and where the time went. Rejected, rate-limited and crashed
requests all get a line — a request that leaves no trace is the one you can't
diagnose.

Fields per line (logs/requests.jsonl):

    timestamp, request_id, method, path, status, outcome,
    duration_ms, stages_ms, creator_id, body_bytes

`stages_ms` is only filled for routes that time their stages (/submit):
model, style, combine, audit. Text itself is never logged.
"""

import json
import threading
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone

from flask import g, jsonify, request
from werkzeug.exceptions import HTTPException

import config

_lock = threading.Lock()


def _write(entry: dict) -> None:
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = json.dumps(entry, ensure_ascii=False)
    with _lock:
        with config.REQUEST_LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")


@contextmanager
def stage(name: str):
    """Time a block and add it to this request's stage breakdown."""
    start = time.perf_counter()
    try:
        yield
    finally:
        stages = getattr(g, "stages_ms", None)
        if stages is not None:
            stages[name] = round(stages.get(name, 0.0) + (time.perf_counter() - start) * 1000, 2)


def note(**fields) -> None:
    """Attach facts (creator_id, outcome) to this request's log line."""
    if hasattr(g, "req_info"):
        g.req_info.update({k: v for k, v in fields.items() if v is not None})


def _outcome(status: int, info: dict) -> str:
    if info.get("outcome"):
        return info["outcome"]
    if status == 429:
        return "rate_limited"
    if status >= 500:
        return "error"
    if status >= 400:
        return "rejected"
    return "ok"


def init_app(app) -> None:
    @app.before_request
    def _start():
        g.t0 = time.perf_counter()
        g.request_id = uuid.uuid4().hex[:12]
        g.stages_ms = {}
        g.req_info = {}

    @app.after_request
    def _finish(response):
        # before_request may not have run (it always does in practice, but a
        # logging bug must never turn a good response into a failure)
        try:
            if hasattr(g, "t0"):
                info = g.req_info
                _write({
                    "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
                    "request_id": g.request_id,
                    "method": request.method,
                    "path": request.path,
                    "status": response.status_code,
                    "outcome": _outcome(response.status_code, info),
                    "duration_ms": round((time.perf_counter() - g.t0) * 1000, 2),
                    "stages_ms": g.stages_ms,
                    "creator_id": info.get("creator_id"),
                    "body_bytes": request.content_length or 0,
                })
                response.headers["X-Request-ID"] = g.request_id
        except Exception:  # noqa: BLE001 — logging must not break serving
            app.logger.exception("request log write failed")
        return response

    @app.errorhandler(Exception)
    def _unhandled(exc):
        """A crash answers with JSON and still gets logged (via after_request)."""
        if isinstance(exc, HTTPException):
            return exc
        app.logger.exception("unhandled error on %s %s", request.method, request.path)
        note(outcome="error")
        return jsonify({"error": "internal_error",
                        "message": "Something went wrong on our side."}), 500
