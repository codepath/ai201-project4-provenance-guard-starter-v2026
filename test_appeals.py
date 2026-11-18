import json
from pathlib import Path
from datetime import datetime

import requests

BASE_URL = "http://127.0.0.1:5000"
RESULTS = []

for trial in range(1, 4):
    trial_results = []

    for appeal_number in range(1, 4):
        content_id = None

        response = requests.post(
            f"{BASE_URL}/submit",
            json={
                "creator_id": "unit8_appeal_tester",
                "text": (
                    "This paragraph is a controlled test submission "
                    "used to verify that the provenance system records "
                    "appeals for previously submitted content."
                ),
            },
            timeout=90,
        )

        submission_ok = response.status_code == 200
        if submission_ok:
            content_id = response.json().get("content_id")

        appeal_response = requests.post(
            f"{BASE_URL}/appeal",
            json={
                "content_id": content_id,
                "reasoning": "I request a human review of this classification.",
            },
            timeout=30,
        )

        appeal_data = appeal_response.json()

        passed = (
            submission_ok
            and appeal_response.status_code == 200
            and appeal_data.get("status") == "under_review"
        )

        trial_results.append({
            "content_id": content_id,
            "submission_status": response.status_code,
            "appeal_status": appeal_response.status_code,
            "appeal_response": appeal_data,
            "passed": passed,
        })

    RESULTS.append({
        "trial": trial,
        "results": trial_results,
    })

log_response = requests.get(
    f"{BASE_URL}/log",
    params={"limit": 1000},
    timeout=30,
)
log_response.raise_for_status()
audit_entries = log_response.json().get("entries", [])

for trial in RESULTS:
    for item in trial["results"]:
        matches = [
            entry for entry in audit_entries
            if entry.get("content_id") == item["content_id"]
            and entry.get("status") == "under_review"
        ]
        item["audit_verified"] = bool(matches)
        item["passed"] = item["passed"] and item["audit_verified"]

timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
output = Path("results") / f"appeals_{timestamp}_before.json"
output.parent.mkdir(exist_ok=True)
output.write_text(json.dumps(RESULTS, indent=2), encoding="utf-8")

for trial in RESULTS:
    passed = sum(item["passed"] for item in trial["results"])
    print(f"Trial {trial['trial']}: {passed}/3 appeals verified — "
          f"{'MET' if passed == 3 else 'MISSED'}")

print(f"Evidence saved: {output}")
