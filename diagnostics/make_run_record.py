"""Produce the committed run record: one real session against gunicorn, logs in a temp dir."""
import json, os, subprocess, sys, tempfile, shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import run_capstone_criteria as rc

tmp = Path(tempfile.mkdtemp())
s = rc.Server(rc.ROOT, tmp / "logs"); s.wait_ready()
texts = [rc.TEXT,
         "I woke up late, burnt the toast, and missed the bus. It was not my best morning, but the coffee helped a little.",
         "The committee reviewed the proposal in detail and concluded that further analysis of the budget was required before any decision could be reached.",
         "Honestly the film was fine. Long, a bit slow in the middle, but the ending made up for it and I left the cinema in a good mood.",
         "Our quarterly results demonstrate a significant improvement across all key performance indicators, reflecting the effectiveness of our strategic initiatives and the dedication of our team.",
         "We drove north for three hours with no radio. My brother slept. I counted the farms and lost count somewhere around forty.",
         "In conclusion, it is important to note that there are many factors to consider, and each of these factors plays a crucial role in the overall outcome of the process.",
         "The dog barked at the mailman again today. He has done this every day for six years and the mailman still flinches.",
         "Photosynthesis is the process by which plants convert light energy into chemical energy, storing it in the bonds of glucose molecules for later use.",
         "My grandmother kept her recipes on index cards, stained with butter and sometimes with tears, and I still cannot cook without hearing her voice."]
for i, t in enumerate(texts):
    rc.post({"text": t, "creator_id": f"writer-{i+1}"})
rc.post({"creator_id": "writer-11"})                       # missing text
rc.post({"text": "   ", "creator_id": "writer-12"})        # empty text
rc.post("not json at all", raw=True)                       # invalid body
rc.post({"text": "x" * 60000, "creator_id": "writer-14"})  # too long
rc.post({"text": "word " * 5, "creator_id": "writer-15"})  # too short to score
for _ in range(12):                                        # same creator, 11th and 12th are limited
    rc.post({"text": texts[0], "creator_id": "flooder"})
s.stop()
rows = [l for l in (tmp / "logs" / "requests.jsonl").read_text().splitlines() if '"/submit"' in l]
out = rc.ROOT / "results" / "run_record.jsonl"
out.write_text("\n".join(rows) + "\n")
print(len(rows), "lines ->", out)
