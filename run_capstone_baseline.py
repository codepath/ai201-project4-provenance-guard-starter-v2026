import json
import time
import uuid
from pathlib import Path

import requests

URL = "http://127.0.0.1:5000/submit"
RESULTS = Path("results")
RESULTS.mkdir(exist_ok=True)

cases = [
    ("oversized", "word " * 2500, 400, "submission_too_large"),
    ("control_character", "This contains \x00 a control character", 400, "unsupported_control_character"),
    ("punctuation_only", "!!! ??? ###", 400, "no_meaningful_words"),
    ("valid_submission", "This is a normal paragraph written to test the classification service.", 200, None),
]

records = []

for trial in range(1, 4):
    for name, text, expected_status, expected_error in cases:
        creator_id = f"baseline_{uuid.uuid4().hex[:12]}"
        start = time.perf_counter()

        try:
            response = requests.post(
                URL,
                json={"creator_id": creator_id, "text": text},
                timeout=200,
            )
            duration = round(time.perf_counter() - start, 3)

            try:
                body = response.json()
            except ValueError:
                body = {}

            passed = (
                response.status_code == expected_status
                and (
                    body.get("error") == expected_error
                    if expected_error
                    else body.get("guess") in {"human", "ai", "unsure"}
                )
            )

            record = {
                "trial": trial,
                "criterion": name,
                "creator_id": creator_id,
                "http_status": response.status_code,
                "error": body.get("error"),
                "guess": body.get("guess"),
                "duration_seconds": duration,
                "passed": passed,
            }

        except requests.RequestException as exc:
            record = {
                "trial": trial,
                "criterion": name,
                "creator_id": creator_id,
                "passed": False,
                "error": str(exc),
            }

        records.append(record)
        print(
            f"Trial {trial} | {name}: "
            f"{'PASS' if record['passed'] else 'FAIL'}"
        )

output = RESULTS / "capstone_baseline.json"
output.write_text(json.dumps(records, indent=2))
print(f"\nSaved {len(records)} records to {output}")
