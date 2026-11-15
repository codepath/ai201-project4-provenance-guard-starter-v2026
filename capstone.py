"""Single-command local deployment of the original service and its operations UI."""
import os

os.environ['AI201_DEBUG'] = '0'

from flask import jsonify, render_template, request
from werkzeug.serving import make_server
import app as service
import telemetry

app = service.app
telemetry.install(app)


@app.get('/')
def dashboard():
    return render_template('dashboard.html')


@app.get('/ops/traces')
def traces():
    rows = telemetry.read_traces(500)
    return jsonify(entries=rows, window=500, scope='most recent 500 persisted API requests')


@app.get('/ops/export')
def export():
    import json
    body = '\n'.join(json.dumps(row) for row in telemetry.read_traces(500))
    return app.response_class(body + ('\n' if body else ''), mimetype='application/x-ndjson',
                              headers={'Content-Disposition': 'attachment; filename=request-traces.jsonl'})


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5050)
    args = parser.parse_args()
    # Bounded CPU parallelism also makes per-request process-time attribution useful.
    import torch
    torch.set_num_threads(2)
    print(f'Provenance Guard Capstone: http://127.0.0.1:{args.port}', flush=True)
    print('Local only. First analysis loads GPT-2. Ctrl+C stops the service.', flush=True)
    make_server('127.0.0.1', args.port, app, threaded=False).serve_forever()


if __name__ == '__main__':
    main()
