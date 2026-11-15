"""Capture Milestone 1 with a real model and a temporary loopback HTTP server."""
import json
import subprocess
import sys
import threading
from pathlib import Path
from werkzeug.serving import make_server
import requests
import app
import audit
import detector


def main():
    print(detector.warm_up(), flush=True)
    start = len(audit.read_entries())
    server = make_server('127.0.0.1', 0, app.app)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    base = f'http://127.0.0.1:{server.server_port}'
    try:
        subprocess.run([sys.executable, 'run_attacks.py', '--flood', '15', '--url', base], check=True)
        samples = json.loads(Path('samples.json').read_text(encoding='utf-8'))
        responses = []
        for index, sample in enumerate(samples[:3]):
            response = requests.post(base+'/submit', json={'text': sample['text'], 'creator_id': f'part2-log-check-{index}'}, timeout=180)
            responses.append({'status': response.status_code, 'response': response.json()})
        response = requests.post(base+'/submit', json={'creator_id': 'part2-invalid'}, timeout=10)
        rejected = {'status': response.status_code, 'response': response.json()}
        entries = requests.get(base+'/log', timeout=10).json()['entries'][start:]
        health = requests.get(base+'/health', timeout=10).json()
        assert health['rate_limiting'] is True
        assert all(r['status'] == 200 for r in responses)
        assert rejected['status'] == 400
        assert any(e.get('reason') == 'rate_limited' for e in entries)
        assert len([e for e in entries if e.get('status') == 'decided']) == 13
        Path('results/part2_instrumentation.json').write_text(json.dumps({'health': health, 'submissions': responses, 'invalid_request': rejected, 'audit_entries': entries}, indent=2), encoding='utf-8')
    finally:
        server.shutdown()
        worker.join(timeout=5)


if __name__ == '__main__':
    main()
