"""
Check my five acceptance criteria (criteria.md) against the real routes, using
Flask's test client — no server needed, but it does run the real model and
writes to a throwaway audit log, not logs/audit.jsonl.

    python check_criteria.py
"""

import tempfile
from pathlib import Path

import config

config.AUDIT_LOG = Path(tempfile.mkdtemp()) / "audit.jsonl"

import audit  # noqa: E402
import calibration as cal  # noqa: E402
from app import app  # noqa: E402

client = app.test_client()


def submit(text, creator="checker"):
    return client.post("/submit", json={"text": text, "creator_id": creator})


def verdict(ok):
    return "PASS" if ok else "MISS"


# 1. False positives: plain human writing, at most 1 of 10 labelled AI
plain = [submit(t).get_json() for t in cal.PLAIN]
fp = sum(1 for r in plain if r["guess"] == "ai")
print(f"1. plain human labelled AI: {fp}/10 (target <= 1)  {verdict(fp <= 1)}")

# 2. Score spread: mean(AI) - mean(human) >= 0.30
ai = [submit(t).get_json()["combined_score"] for t in cal.AI]
hu = [submit(t).get_json()["combined_score"] for t in cal.HUMAN]
gap = sum(ai) / 5 - sum(hu) / 5
print(f"2. spread: {sum(ai)/5:.3f} - {sum(hu)/5:.3f} = {gap:.3f} (target >= 0.30)  {verdict(gap >= 0.30)}")

# 3. Label coverage over 12 varied submissions
twelve = cal.AI[:3] + cal.HUMAN[:3] + cal.PLAIN[:3] + cal.EDITED[:3]
guesses = [submit(t).get_json()["guess"] for t in twelve]
counts = {g: guesses.count(g) for g in ("human", "unsure", "ai")}
ok3 = all(0 < n <= 9 for n in counts.values())
print(f"3. label coverage: {counts} (each 1-9)  {verdict(ok3)}")

# 4. Appeals
ids = [submit(t).get_json()["content_id"] for t in cal.HUMAN * 2]
good = 0
for cid in ids:
    before = len([e for e in audit.entries_for(cid) if e.get("event") == "appeal"])
    r = client.post("/appeal", json={"content_id": cid, "reasoning": "I wrote this myself."})
    after = len([e for e in audit.entries_for(cid) if e.get("event") == "appeal"])
    if r.status_code == 200 and r.get_json()["status"] == "under_review" and after == before + 1:
        good += 1
n_before = len(audit.read_entries())
r = client.post("/appeal", json={"content_id": "no-such-id", "reasoning": "x"})
appeals_after = [e for e in audit.read_entries() if e.get("event") == "appeal" and e["content_id"] == "no-such-id"]
ok4 = good == 10 and r.status_code == 404 and not appeals_after
print(f"4. appeals: {good}/10 ok, unknown id -> {r.status_code}  {verdict(ok4)}")

# 5. Bad input never 5xx
bad = [
    {"creator_id": "x"},
    {"text": "", "creator_id": "x"},
    {"text": "   \n ", "creator_id": "x"},
    {"text": 12345, "creator_id": "x"},
    [1, 2, 3],
    {"text": "word " * 10000, "creator_id": "x"},
]
codes = []
all_json = True
for b in bad:
    r = client.post("/submit", json=b)
    codes.append(r.status_code)
    j = r.get_json()
    all_json &= bool(j and "error" in j)
ping = client.post("/ping", json={"message": "hi"}).status_code
ok5 = all(400 <= c < 500 for c in codes) and all_json and ping == 200
print(f"5. bad input codes: {codes}, /ping after: {ping}  {verdict(ok5)}")
