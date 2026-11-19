# Capstone acceptance criteria — Provenance Guard

Five criteria for the capstone (unit 9, shape A: deploy and instrument, path B:
local with logs). Four are about the extension, which is the operational layer:
the request log, the run path, the warm-up, and the failure and cost behaviour.

Some measurements (first-request latency, a 10x load run, memory and CPU per
request) existed before these were written, so the targets are not blind. I set
them where they could really fail, not at the numbers I saw.

The unit 7 criteria for the detector itself are kept unchanged below the line.

---

## 1. Every request leaves a log line

On a freshly started service I send 20 mixed requests: 10 valid, 5 malformed and
5 over the rate limit. Each one produces exactly one line in
`logs/requests.jsonl` with `ts`, `path`, `status`, `total_ms`, and an `error`
code on every failure. **20 of 20 in each of three trials.**

**Why this target:** A failure that leaves no record is one I would never find.
The logging hook swallows its own errors so it can't break a response, which
means it could also fail silently. Anything under 20 of 20 means some requests
are invisible.

## 2. It starts from RUNNING.md alone

I clone the repo into a clean folder and follow only `RUNNING.md`. `/health`
reports the model loaded within 60 seconds. **3 of 3 clean starts.**

**Why this target:** A run path that only works on my machine isn't a run path.
60 seconds is tighter than gunicorn's 120 second timeout, so a slow cold load
counts as a miss even though the service would technically still start.

## 3. The first request after startup isn't slow

Over three cold starts, the first `POST /submit` takes **under 1 second**, and
the median of the next 50 requests is **under 250 ms**.

**Why this target:** The warm-up exists to fix this. Before it, the first
request took 2.8 seconds, and the first user is the one who sees the hang. One
second leaves room for laptop variance without letting the old behaviour pass.

## 4. Overload turns into a clear refusal and a record

One creator sends 60 requests in a minute against a limit of 10 a minute.
**No 5xx responses, between 40 and 50 are 429, and all 60 appear in the request
log.**

**Why this target:** This is the bad path. Overload must become a refusal with
a trace, not a crash or silent drops. The window is 40 to 50 because a counter
reset at a minute boundary can let a few extra requests through.

## 5. The memory and CPU ceiling holds

Over 10 runs, the worker's resident memory after warm-up and 50 requests stays
**under 1,000 MB**, and the average CPU time per request stays **under 500 ms**.

**Why this target:** Memory is the real cost of this service, and it is why it
cannot run on a 512 MB free host. Both ceilings sit close to what I measured
earlier, so a longer text or a library change could genuinely break them.

---

# Unit 7 criteria (earlier project, unchanged)

The numbering restarts here. These are the criteria for the detector itself.

# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False positives: plain human writing is rarely called AI

Of 10 plainly-written pieces I wrote myself (short sentences, common words, the
kind of writing signal one is most likely to over-read), **at most 1 gets the
high-confidence AI label** — and that has to hold in each of three trials, not
on average.

**How to check:** Run `python check_criteria.py`. It submits the 10 plain paragraphs in `calibration.py` (the `PLAIN` list) to `POST /submit` and counts responses where `guess` is `"ai"`. Run it three times; every run must print 1 or fewer.

**Why this target:** On a writing site, a wrong accusation costs a real person
their credibility, while a missed detection costs the site a little. So I
tolerate one wrong accusation in ten at the very most. I picked plain writing
as the test set on purpose, because that is the writing this detector is most
likely to get wrong; testing on easy human text would make the target
meaningless.

---

## 2. Score spread: clearly-AI and clearly-human text score far apart

Across 5 clearly-AI and 5 clearly-human samples, the **mean combined score of
the AI set is at least 0.30 higher than the mean of the human set.**

**How to check:** Submit the 5 texts in `calibration.py::AI` and the 5 in `calibration.py::HUMAN` to `POST /submit`, average each group's `combined_score`, and subtract. `check_criteria.py` prints it as check 2.

**Why this target:** If the two groups sit within 0.30 of each other, the
thresholds are splitting hairs and the labels are close to coin flips. 0.30 is
roughly one full label band (the unsure band is 0.30 wide), so a gap that size
means clearly-AI and clearly-human text usually land in different labels.

---

## 3. Label coverage: all three labels are reachable

In a set of 12 varied submissions, **each of the three labels (human, unsure,
AI) is produced at least once** — and none of them is produced by more than 9
of the 12.

**How to check:** Submit the first three texts of each of `AI`, `HUMAN`, `PLAIN` and `EDITED` in `calibration.py` (12 total) to `POST /submit`, then count the `guess` values (`human`, `unsure`, `ai`). Each must appear at least once and none more than 9 times. `check_criteria.py` prints it as check 3.

**Why this target:** A label nothing can produce is dead code, and a service
that answers "unsure" to nearly everything is not making decisions. With the unsure band at 0.35-0.80 it would be easy to land everything there and
never use the human or AI label. The upper cap of 9 of 12 stops me from "passing" with one label that swallows
everything.

---

## 4. The appeal path always changes status and always gets recorded

For **10 of 10 appeals** on a real content_id: the response is HTTP 200, the
status is `under_review`, and the audit log gains exactly one `appeal` entry for
that content_id. For an unknown content_id: HTTP 404 and **0** new log
entries claiming an appeal happened.

**How to check:** Submit 10 texts, then `POST /appeal` with each returned `content_id` and a reasoning string. Check the HTTP code, the `status` field, and count `event: "appeal"` entries for that id in `GET /log`. Then appeal with `content_id: "no-such-id"` and confirm a 404 and no new appeal entry. `check_criteria.py` prints it as check 4.

**Why this target:** The appeal is the only thing between a wrong accusation
and nothing at all, so it has to be 100%, not "usually". A silent failure here
is the worst bug in the service, because the writer believes they were heard.

---

## 5. Bad input never crashes the service

For 6 malformed inputs (missing `text`, empty `text`, whitespace-only `text`,
non-string `text`, a body that isn't a JSON object, and 50,000 characters of
text), **0 return a 5xx**, and every one returns a JSON body with an `error`
field and a 4xx status. `/ping` still answers afterwards.

**How to check:** `POST /submit` with each of the six bodies listed above and record each status code and whether the JSON has an `error` field; then `POST /ping` and confirm 200. `check_criteria.py` prints it as check 5.

**Why this target:** A crash on malformed input is one of the most common real
failures, and an attacker finds it first. Rejecting with a clear 4xx is the
whole job; the number is zero because even one 500 means a request can take the
handler down.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
