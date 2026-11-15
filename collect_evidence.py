"""Run real local-model HTTP requests and save the exact responses."""
import json
import threading
import subprocess
from pathlib import Path
from werkzeug.serving import make_server
import requests
import app
import detector

if __name__ == "__main__":
    print(detector.warm_up(), flush=True)
    server = make_server("127.0.0.1", 0, app.app)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    base = f"http://127.0.0.1:{server.server_port}"
    results = []
    try:
        print("ping",requests.post(base+"/ping",json={"message":"hello"},timeout=10).json(),flush=True)
        for sample in json.loads(Path("samples.json").read_text(encoding="utf-8")):
            payload = {"text":sample["text"],"creator_id":"demo-writer"}
            # curl.exe receives JSON through stdin, avoiding PowerShell quote escaping.
            captured = subprocess.run(["curl.exe", "--silent", "--show-error", "-X", "POST", base+"/submit", "-H", "Content-Type: application/json", "--data-binary", "@-", "-w", "\\n%{http_code}"], input=json.dumps(payload), capture_output=True, text=True, check=True, timeout=180)
            body, status = captured.stdout.rsplit("\n",1)
            class Response:
                status_code = int(status)
                def json(self):
                    return json.loads(body)
            response = Response()
            row = {**sample,"request":payload,"status_code":response.status_code,"response":response.json()}
            results.append(row)
            print(sample["name"],response.status_code,response.json(),flush=True)
        success = next(row for row in results if row["status_code"] == 200)
        appeal_request = {"content_id":success["response"]["content_id"],"reasoning":"I dispute this automated assessment and request a human review."}
        appeal = requests.post(base+"/appeal",json=appeal_request,timeout=10)
        evidence = {"samples":results,"appeal_request":appeal_request,"appeal_status":appeal.status_code,"appeal_response":appeal.json(),"log_response":requests.get(base+"/log",timeout=10).json(),"health":requests.get(base+"/health",timeout=10).json()}
        Path("results/sample_run.json").write_text(json.dumps(evidence,indent=2),encoding="utf-8")
        print("Saved results/sample_run.json",flush=True)
    finally:
        server.shutdown()
        worker.join(timeout=5)
