"""Operational traces, separate from the unchanged decision/appeal audit log."""
import hashlib
import json
import os
import threading
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from flask import g, has_request_context, request

TRACE_PATH = Path(os.getenv('CAPSTONE_TRACE_PATH', Path(__file__).parent / 'logs' / 'requests.jsonl'))
_lock = threading.Lock()
# Include unsuccessful responses: baseline trials exposed missing rejection traces.
INCLUDE_FAILURES = True


@contextmanager
def stage(name):
    start = time.perf_counter()
    try:
        yield
    finally:
        if has_request_context() and hasattr(g, 'stage_ms'):
            g.stage_ms[name + '_ms'] = round((time.perf_counter() - start) * 1000, 4)


def read_traces(limit=500):
    from collections import deque
    if not TRACE_PATH.exists():
        return []
    with _lock, TRACE_PATH.open(encoding='utf-8') as stream:
        lines = list(deque(stream, maxlen=limit))
    rows = []
    for line in lines:
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def install(app):
    @app.before_request
    def begin_trace():
        g.request_id = str(uuid.uuid4())
        g.wall_start = time.perf_counter()
        g.cpu_start = time.process_time()
        g.stage_ms = {}
        g.trace_timestamp = datetime.now(timezone.utc).isoformat()

    @app.after_request
    def finish_trace(response):
        response.headers['X-Request-ID'] = g.request_id
        if request.path.startswith('/static/') or request.path.startswith('/ops') or request.path == '/':
            return response
        if response.status_code >= 400 and not INCLUDE_FAILURES:
            return response
        payload = request.get_json(silent=True)
        summary = {'json_type': type(payload).__name__, 'body_bytes': request.content_length}
        if isinstance(payload, dict):
            summary['fields'] = sorted(payload)
            for key in ('text', 'reasoning'):
                value = payload.get(key)
                if isinstance(value, str):
                    summary[key + '_characters'] = len(value)
                    summary[key + '_sha256'] = hashlib.sha256(value.encode()).hexdigest()
            for key in ('creator_id', 'content_id'):
                if isinstance(payload.get(key), str):
                    summary[key] = payload[key][:200]
        output = response.get_json(silent=True)
        # /log can grow indefinitely; never recursively replicate its contents.
        if request.path == '/log' and isinstance(output, dict):
            output = {'count': output.get('count'), 'entries_omitted': True}
        row = {
            'timestamp': g.trace_timestamp, 'request_id': g.request_id,
            'method': request.method, 'route': request.path, 'input': summary,
            'output': output, 'status': response.status_code,
            'wall_ms': round((time.perf_counter() - g.wall_start) * 1000, 4),
            'cpu_ms': round((time.process_time() - g.cpu_start) * 1000, 4),
            'stages': g.stage_ms,
        }
        try:
            with _lock:
                TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
                with TRACE_PATH.open('a', encoding='utf-8') as stream:
                    stream.write(json.dumps(row, ensure_ascii=False) + '\n')
        except OSError:
            app.logger.exception('Request telemetry could not be persisted')
            response.headers['X-Telemetry-Status'] = 'write_failed'
        return response
