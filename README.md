# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does


<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->



1. A client POSTs JSON `{"text", "creator_id"}` to `/submit` in `app.py`.
2. The route validates it: the body must be a JSON object, `text` must be a
   non-empty string under 20,000 characters, `creator_id` a non-empty string.
   Anything else gets a 4xx JSON error and a `rejected` entry in the log.
3. Signal one, `detector.model_signal`, runs GPT-2 locally on the first 400
   tokens and turns perplexity into a 0-1 score (higher = more AI-like).
4. Signal two, `stylometry.style_signal`, measures sentence-length spread,
   vocabulary variety and rare punctuation, and gives a 0-1 score (same direction).
5. `scoring.combine_signals` merges the two into one combined score, pulling
   it into the unsure band if the signals contradict each other.
6. `scoring.score_to_label` maps the score to `human` / `unsure` / `ai` and the
   plain-language sentence a reader sees.
7. `audit.log_decision` writes all nine fields (status `decided`), and the
   response returns `content_id`, `guess`, `confidence`, `label`, `model_score`,
   `style_score`, `combined_score` and `status`.
8. If the writer disagrees, `POST /appeal` with the `content_id` checks it
   exists (404 if not), appends an `appeal` entry and moves status to `under_review`.

---

## Stretch Feature Declared Before Building

**Declared:** `GET /content/<content_id>`, which returns one item's current
status (`decided` or `under_review`), its label and its scores. I am declaring
this in a commit before I write the endpoint. A third signal and a
verified-human path are not attempted.


**What it changed:** There is now a read-only way to see where an item stands
without reading the whole log. Status is derived from the append-only audit log
(`decided` until an appeal entry exists, then `under_review`), so nothing in
`/submit`, `/appeal` or the log format changed. Unknown ids return 404.

Before the appeal:

```bash
$ curl http://127.0.0.1:5000/content/78086c78-5cf5-4e93-add5-1a41e6678a56
```

```json
{
  "appeals": 0,
  "combined_score": 0.8552,
  "content_id": "78086c78-5cf5-4e93-add5-1a41e6678a56",
  "creator_id": "writer-42",
  "guess": "ai",
  "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "model_score": 0.9371,
  "status": "decided",
  "style_score": 0.7324
}
```

After the appeal (note `status` and `appeals`):

```bash
$ curl http://127.0.0.1:5000/content/78086c78-5cf5-4e93-add5-1a41e6678a56
```

```json
{
  "appeals": 1,
  "combined_score": 0.8552,
  "content_id": "78086c78-5cf5-4e93-add5-1a41e6678a56",
  "creator_id": "writer-42",
  "guess": "ai",
  "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "model_score": 0.9371,
  "status": "under_review",
  "style_score": 0.7324
}
```

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to GPT-2 (perplexity over the
first 400 tokens), squashed onto 0-1 with a logistic. Low perplexity gives a high
AI score. Unit 8 changed it from mean surprise per token (midpoint 45) to a
trimmed mean that drops the 10% most surprising tokens (midpoint 22) — see
**The Improvement**. The calibration numbers in this section were measured before
that change; the unit 8 runs below use the new version.

**Why that might differ between human and AI writing:** A language model writes
by picking likely next words, so its output tends to be text another model finds
easy to predict. Human writing wanders: odd word choices, abrupt turns, specifics.

**What it can't see:** Authorship. It rewards common words in short, ordinary
sentences, and plenty of real people write that way: second-language writers,
younger writers, anyone writing plainly. In my calibration all 10 plain human
paragraphs scored 0.68-0.87 on this signal, as high as the AI paragraphs. Ornate
human prose with rare words scores as human even if a model wrote it.

### Signal two — the style signal

**What it measures:** Shape, not meaning. (a) Sentence-length spread: stdev / mean
of sentence lengths in words. (b) Type-token ratio averaged over sliding
50-word windows, so length doesn't skew it. (c) Rare-punctuation density:
semicolons, colons, dashes, parentheses, `!`, `?`, ellipses and quotes per 100
words, plus a bonus per distinct kind. Each is flipped to higher = AI and scaled
onto 0-1, then weighted 0.50 / 0.20 / 0.30 (`stylometry.py::style_signal`).

**Why that might differ between human and AI writing:** Generated prose tends
toward even, mid-length sentences, a narrower vocabulary, and commas and full
stops only. Human writing is lumpier: a three-word sentence next to a
forty-word one, a stray dash or bracket.

**What it can't see:** It cannot read. Anything that changes the shape without
changing the substance moves it: typos, broken-up sentences, a pasted quotation,
a few added dashes. My "lightly edited AI" calibration texts dropped from about
0.7 to 0.07-0.33 on this signal with only small edits. And like signal one, it
reads plain, even human writing (short sentences, no fancy punctuation) as
AI-like: all 10 of my plain human samples scored 0.58-0.83.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** A weighted average, with a safeguard. If the two signals differ by
more than 0.40, the combined score is clamped into 0.40-0.60, which is always the
unsure band, so neither a confident human nor a confident AI label is possible
when the signals contradict each other. An accusation needs both signals to agree.

**The numbers:** model weight 0.6, style weight 0.4, disagreement gap 0.40,
clamp 0.40-0.60. Thresholds: human below 0.35, AI above 0.80. All in `config.py`.
The model signal gets more weight because the style signal is cheap to fool.
I raised the AI threshold from the starter's 0.65 to 0.80 after calibration: all
ten plain human samples scored 0.67-0.79 combined, so at 0.65 every one of them
would have been accused. The cost is real: only 3 of my 5 clear AI samples
(0.76-0.86) now reach the AI label, and the margin is thin (highest plain-human
sample 0.785 vs the 0.80 line, tuned on only ten samples), so this threshold
probably overfits.

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**
Calibration human sample 1 ("I burned the toast again. Third time this week!...")
scored model_score 0.564 (GPT-2 found it fairly predictable) but style_score
0.008 (lumpy sentences, dashes, brackets, `!`). The gap is 0.556, over 0.40. The
raw average would be 0.342, a confident human label; the rule clamps it to 0.400
and the reader gets "unsure". Two methods contradicting each other is uncertainty.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person. Our checks found nothing that points to automated writing. |
| unsure | 0.35 – 0.80 | We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look. |
| high-confidence AI | 0.80 – 1.00 | This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

It says "we can't tell" in the first sentence so it never reads as an accusation,
says the mixed result "happens with plenty of writing by real people" because
the reader very likely is one, says plainly that nothing has been decided, and
ends with a way to act (appeal). It avoids the words score, threshold and
confidence entirely. Even the AI label says "may" and invites an appeal.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Regular exercise provides a wide variety of benefits for both physical and mental health. It helps to strengthen the heart, improve mood, and reduce the risk of chronic diseases. Moreover, it can enhance sleep quality and increase overall energy levels. For these reasons, it is important to incorporate physical activity into your daily routine.", "creator_id": "writer-42"}'
```

```json
{
  "combined_score": 0.8552,
  "confidence": 0.8552,
  "content_id": "45002446-724f-4669-a090-d3e55693c0c8",
  "guess": "ai",
  "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "model_score": 0.9371,
  "status": "decided",
  "style_score": 0.7324
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "45002446-724f-4669-a090-d3e55693c0c8", "reasoning": "I wrote this myself for a health class and did not use any AI tool."}'
```

```json
{
  "content_id": "45002446-724f-4669-a090-d3e55693c0c8",
  "message": "Thank you. Your appeal has been recorded and a person will review it.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.8552,
      "content_id": "45002446-724f-4669-a090-d3e55693c0c8",
      "creator_id": "writer-42",
      "guess": "ai",
      "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
      "model_score": 0.9371,
      "status": "decided",
      "style_score": 0.7324,
      "timestamp": "2026-11-16T23:48:27+00:00"
    },
    {
      "content_id": "45002446-724f-4669-a090-d3e55693c0c8",
      "creator_id": "writer-42",
      "event": "appeal",
      "reasoning": "I wrote this myself for a health class and did not use any AI tool.",
      "status": "under_review",
      "timestamp": "2026-11-16T23:48:27+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* Claude Code to work through all the milestones, building both signals, the combining rule, the labels, `/submit` and `/appeal`, and to check them against the grading checklist.
- *What came back:* A first style signal and a 0.6/0.4 average with a disagreement clamp. When it ran my calibration set, it showed that all 10 plain human paragraphs landed in "AI" at the starter's 0.65 threshold.
- *What I changed:* The AI threshold went up to 0.80 so plain human writing isn't accused. I accepted the trade that fewer AI texts get caught, and I named it as overfitted to ten samples.

**Moment 2**

- *What I asked for:* The five acceptance criteria and a way to test them, plus input handling for `/submit` and `/appeal`.
- *What came back:* `criteria.md` with numeric targets, `check_criteria.py`, and 4xx JSON errors for missing, empty, non-string, non-object and oversized input, each logged as a rejection.
- *What I changed:* Nothing yet. All five criteria pass in `check_criteria.py`, but the targets and README claims are mine to review and edit before I submit.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 200 per day (`config.py`: `RATE_LIMIT_PER_MINUTE`, `RATE_LIMIT_PER_DAY`), on `POST /submit` only.

**Why those numbers and not others:** A real writer submits their own work a few
times an hour, and resubmits after an edit or a typo. Ten a minute never touches
that, and 200 a day is far more than one person writes. A script mapping my
thresholds needs hundreds or thousands of probes with small edits between them.
Ten a minute stops a burst after 10 requests, and 200 a day caps one key at 200
probes a day. I didn't go lower because a person retrying after a typo shouldn't
hit a wall; I didn't go higher because 200 a day is already more probes than I'd
want handed to one caller.

**What a caller counts as:** the `creator_id` in the request body, falling back
to the caller's IP address when there is none (`app.py::rate_limit_key`). That
fails in a specific way: **a script that sends a different `creator_id` with every
request is never limited.** My attack run did exactly that. Every attack in
`attacks.csv` got its own `attacker_<id>`, so 25 text attacks looked like 25
different callers and none was counted against any other. Only the
`flood_same_creator` family, which shares one `creator_id`, hit the limit.
Counting by IP would stop that rotation but would lump a whole household or
school together. I kept `creator_id` and I'm naming the hole instead of hiding it.

**The run of status codes when I pushed past it:**

```
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

From `python run_attacks.py --flood 15`. In the attack run the shared-creator
flood rows FL01-FL10 returned 200 and FL11-FL12 returned 429. The 429s are in the
audit log (entry below).

---

## Attack Run — Before

The attack set is the staff set: `attack_set/attacks.csv` (32 attacks: evasion, false-positive, prompt-injection
and odd-text) and `attack_set/attacks_malformed_requests.csv` (24 malformed and
flood requests).
It was run on the code *before* my improvement (commit `dc93e21`) with
`python run_attacks.py --set attack_set --label before`, 56 inputs in all
(`results/staff_attack_run_2026-11-19_1901_before.md`). I had written a stand-in
set of my own earlier because I did not have the staff one; that run is kept in
`results/attack_run_2026-11-16_*.md` and `attack_set_standin/`, and nothing below
is taken from it.

Marking rule, written down so it can be checked: an **evasion** attack is
**BROKE** unless it is still labelled `ai`; a **false-positive** attack is
**BROKE** if a plain human text is labelled `ai`; a **prompt-injection** attack
is **BROKE** if the label comes back `human` (the injected goal) or a forged
entry reaches the audit log, and HELD otherwise; a **malformed** attack is
**HELD** if it gets a 4xx JSON answer and **BROKE** if garbage is accepted and
scored; a **flood** attack is **HELD** if the first 10 pass and later ones get
429. Anything that crashes is BROKE.
Caveats: I do not know which of the evasion texts the unmodified system would
have labelled `ai`, so some of those 9 may not have broken a detection that
existed. RQ02 (no `creator_id`) is marked HELD because the service documents a
fallback to `anonymous`; by the strict rule it would be BROKE.

Score is the combined score. Results: **evasion 9 of 10 BROKE**,
**false-positive 0 of 8 BROKE**, **prompt injection 1 of 6 BROKE**,
**malformed 5 of 20 BROKE**, **flood 0 of 12 BROKE**, 0 crashes (no 5xx anywhere).

| ID | Family | Targeting | Status | Guess | Score | Mark |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.400 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.401 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.488 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.637 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.285 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.464 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.453 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.386 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.609 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.875 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.574 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | unsure | 0.720 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | unsure | 0.719 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | unsure | 0.724 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | unsure | 0.793 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.731 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.729 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.390 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.408 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.202 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.486 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.457 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.449 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.540 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | HELD |
| MF02 | malformed | text is a single character | 422 | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | unsure | 0.400 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | unsure | 0.400 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | unsure | 0.600 | BROKE |
| MF06 | malformed | text is emoji only | 200 | unsure | 0.600 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | unsure | 0.600 | BROKE |
| MF08 | malformed | text is 60,000 characters | 413 | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | unsure | 0.364 | HELD |
| RQ03 | malformed | text is a number | 400 | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | — | HELD |
| RQ05 | malformed | text is null | 400 | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |

Full report: `results/staff_attack_run_2026-11-19_1901_before.md`.

**Ten audit log entries from the run**

Chosen to show the interesting failures: the typo attack where the model score
collapsed (EV01); unusual words (EV04); a heavy edit that came back `human`
(EV05); the two injections that mattered, PI02 (labelled `human`) and PI05 (an
attempt to forge a log entry, which left no forged entry); two human texts close
to the AI line (FP03, FP05); a 4,000-character single word that was scored
(MF05); and two rejections that left a trace (a rate-limit 429 and a missing
`text`). Pulled from `GET /log` (`results/staff_audit_extract_before.json`).

```json
[
  {
    "combined_score": 0.4,
    "content_id": "82401b3b-e17c-4623-acaa-31b49e5bf572",
    "creator_id": "attacker_EV01",
    "guess": "unsure",
    "label": "We can't tell. Our checks gave mixed results on this one, wh…",
    "model_score": 0.1635,
    "status": "decided",
    "style_score": 0.6852,
    "timestamp": "2026-11-20T00:01:49+00:00"
  },
  {
    "combined_score": 0.6371,
    "content_id": "69a07efe-94c6-498d-9c1f-c7ba4b84351b",
    "creator_id": "attacker_EV04",
    "guess": "unsure",
    "label": "We can't tell. Our checks gave mixed results on this one, wh…",
    "model_score": 0.6114,
    "status": "decided",
    "style_score": 0.6757,
    "timestamp": "2026-11-20T00:01:50+00:00"
  },
  {
    "combined_score": 0.2854,
    "content_id": "5059c21a-dbdd-4350-b1c6-d8523499aa4e",
    "creator_id": "attacker_EV05",
    "guess": "human",
    "label": "We think this was probably written by a person. Our checks f…",
    "model_score": 0.3212,
    "status": "decided",
    "style_score": 0.2317,
    "timestamp": "2026-11-20T00:01:50+00:00"
  },
  {
    "combined_score": 0.202,
    "content_id": "8a6a6738-619d-4ddd-b27a-40d89524f8c1",
    "creator_id": "attacker_PI02",
    "guess": "human",
    "label": "We think this was probably written by a person. Our checks f…",
    "model_score": 0.2044,
    "status": "decided",
    "style_score": 0.1983,
    "timestamp": "2026-11-20T00:01:52+00:00"
  },
  {
    "combined_score": 0.4494,
    "content_id": "e5d26227-de46-4add-936c-a937dbe1ef85",
    "creator_id": "attacker_PI05",
    "guess": "unsure",
    "label": "We can't tell. Our checks gave mixed results on this one, wh…",
    "model_score": 0.6401,
    "status": "decided",
    "style_score": 0.1633,
    "timestamp": "2026-11-20T00:01:52+00:00"
  },
  {
    "combined_score": 0.7191,
    "content_id": "3f555a13-0287-4a74-bf44-605f7d07f47d",
    "creator_id": "attacker_FP03",
    "guess": "unsure",
    "label": "We can't tell. Our checks gave mixed results on this one, wh…",
    "model_score": 0.8051,
    "status": "decided",
    "style_score": 0.5901,
    "timestamp": "2026-11-20T00:01:51+00:00"
  },
  {
    "combined_score": 0.793,
    "content_id": "f90cae09-8355-4aa2-942c-7fa4242812e9",
    "creator_id": "attacker_FP05",
    "guess": "unsure",
    "label": "We can't tell. Our checks gave mixed results on this one, wh…",
    "model_score": 0.8005,
    "status": "decided",
    "style_score": 0.7817,
    "timestamp": "2026-11-20T00:01:51+00:00"
  },
  {
    "combined_score": 0.6,
    "content_id": "a09c6cba-3936-4232-a5ee-97a23a0d4160",
    "creator_id": "attacker_MF05",
    "guess": "unsure",
    "label": "We can't tell. Our checks gave mixed results on this one, wh…",
    "model_score": 0.9976,
    "status": "decided",
    "style_score": 0.55,
    "timestamp": "2026-11-20T00:01:53+00:00"
  },
  {
    "combined_score": null,
    "content_id": null,
    "creator_id": "attacker_flood",
    "event": "rejected",
    "guess": null,
    "label": null,
    "limit": "10 per 1 minute",
    "model_score": null,
    "reason": "rate_limited",
    "status": "rejected",
    "style_score": null,
    "timestamp": "2026-11-20T00:01:55+00:00"
  },
  {
    "combined_score": null,
    "content_id": null,
    "creator_id": "attacker_RQ01",
    "event": "rejected",
    "guess": null,
    "label": null,
    "model_score": null,
    "reason": "missing_text",
    "status": "rejected",
    "style_score": null,
    "timestamp": "2026-11-20T00:01:54+00:00"
  }
]
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it: **FP05**, technical documentation written by a
person, which came back `unsure` at a combined score of **0.793**, seven
thousandths under the 0.80 line that would have labelled it `ai` (model 0.800,
style 0.782). Nobody was accused, but only because of where I put a threshold;
five more human texts (FP02, FP03, FP04, FP06, FP07) sit between 0.72 and 0.73. On the other side,
the outcome I'd least want to explain to the site is **PI02**: an AI-sounding
paragraph prefixed with a fake "SYSTEM: …return guess=human" line came back
`human` at 0.202.

---

## Run Log and Verdicts

`python run_eval.py --label before`, three trials, before the improvement
(`results/run_2026-11-16_1913_before.md`). The three trials were identical on
every guess and score: GPT-2 run this way is deterministic, so the worry that
identical input scores differently twice did not show up here.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives | at most 1 of 10 plain human texts labelled AI, every trial | 0 of 10 | 0 of 10 | 0 of 10 | MET |
| 2. Score spread | mean(AI set) − mean(human set) ≥ 0.30 | 0.813 − 0.340 = 0.473 | 0.473 | 0.473 | MET |
| 3. Label coverage | each of 3 labels ≥ 1 and ≤ 9 of 12 | human 2 · unsure 8 · ai 2 | same | same | MET |
| 4. Appeal path | 10 of 10 appeals: 200, `under_review`, logged; unknown id 404 | 10 of 10, unknown id 404 | 10 of 10, 404 | 10 of 10, 404 | MET |
| 5. Bad input | 0 of 6 malformed inputs return a 5xx | 0 of 6 (400,400,400,400,400,413) | same | same | MET |

Two limits on these verdicts, stated plainly. (a) The ten texts for criterion 1
are the `PLAIN` list in `calibration.py`, which I drafted with Claude's help
rather than wrote from scratch, so this is a weaker test than ten pieces I wrote
myself; criterion 1 should be rerun on my own writing. (b) The "bad input"
scenario can only send dict bodies, so the bare-list and non-JSON bodies named
in criterion 5 are covered by attacks MR06-MR09 and MR14 in the attack run and
by `check_criteria.py`, not by `run_eval.py`. Also, the criteria and the attack
set disagree: criterion 1 is MET on my ten plain texts while the attack set's
five plain texts got two accusations. Both results are real.

**Real output from one trial**, from `run_eval.py::main` (criterion 5, trial 1:
the response of `app.py::submit` to six malformed bodies):

```json
[
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "   \n  "
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": 12345, \"creator_id\": \"eval_bad_number\"}"
  },
  {
    "status": 413,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "word word word word word word word word word word word word word word "
  }
]
```

**Diagnoses**

No criterion was missed (the run log above). These diagnose the 9 evasion
attacks, the one injection, and the 5 malformed inputs that broke on the staff
run, plus the near-miss on false positives. Scores are `model / style /
combined` from `results/staff_audit_extract_before.json`. The service has five
stages: the route, signal one, signal two, the combining rule, and the label
mapping.

1. **Typo and token-window attacks (EV01, EV08) — stage: signal one; mechanism:
   unusual or broken tokens inflate perplexity.** EV01 scored 0.164 / 0.685 /
   0.400 and EV08 0.245 / 0.598 / 0.386. The style score stayed high; the model
   score is what collapsed, and the 0.40 gap rule then clamped EV01 to exactly
   the 0.400 floor. The set labelled EV01 as aimed at signal two ("typos raise word
   variety") and EV08 as aimed at signal one; the numbers say signal one for both.
2. **Shape attacks (EV02, EV03, EV06, EV07) — stage: signal two, then the
   combining rule; mechanism: shape changes without the substance changing.**
   Model 0.57 to 0.67, style only 0.11 to 0.30 (EV02 0.594 / 0.110, EV07 0.586 /
   0.254). Broken-up sentences, a pasted quotation, one very long sentence and
   padding with punctuation each drag the style score down. EV02 landed at
   0.401, the clamp floor again, because the signals differ by more than 0.40.
3. **Heavy editing (EV05) — stage: signal one and signal two together;
   mechanism: both signals share the blind spot.** 0.321 / 0.232 / 0.285. The
   only evasion that came back `human` rather than `unsure`: when both signals
   read the text as human there is no disagreement for the combining rule to
   soften.
4. **Dilution and unusual words (EV04, EV09) — stage: signal one, averaged by the
   combining rule; mechanism: AI text mixed with human text, or with unusual
   words, pulls the model score below the line.** EV09 0.704 / 0.466 / 0.609;
   EV04 0.611 / 0.676 / 0.637. Neither signal is wrong about its input; the
   input is a mixture and the labels have no answer for mixtures.
5. **Injection (PI02) — stage: signal one; mechanism: the instruction is not
   obeyed, it acts as noise.** The service never reads text as instructions, so
   "ignore all previous instructions" (PI01 0.463 / 0.327 / 0.408) did
   nothing special. PI02's "SYSTEM:" line is odd text that raised perplexity:
   0.204 / 0.198 / 0.202, against 0.46 to 0.64 for the five other variants built
   on the same paragraph. PI05 tried to forge a log entry; the audit log is
   written from fields in my code and never from the text, so no forged entry
   appears.
6. **Malformed text accepted (MF03 to MF07) — stage: the route; mechanism: no
   check that the text has anything to score.** Control characters, punctuation
   only, a 4,000-character single word, emoji only and right-to-left text all
   returned 200 and `unsure`. Control characters and punctuation scored
   0.000 / 0.550 and 0.011 / 0.500 (combined 0.400, the floor); the repeated "a"
   scored 0.998 on the model (combined 0.600, the ceiling). The clamp turns
   garbage into a polite "unsure" instead of a refusal.
7. **False positives, the near-miss (FP02 to FP07) — stages: signal one and
   signal two together; mechanism: plain, formal or non-native writing looks
   like AI to both.** FP05 0.800 / 0.782 / 0.793; FP03 0.805 / 0.590 / 0.719;
   FP06 0.881 / 0.504 / 0.731. Not marked BROKE, since none crossed 0.80, but
   the margin on FP05 is 0.007 and the signals agree, so the combining rule has
   nothing to soften.

**The pattern:** two mechanisms account for most of it. Signal two is cheap to
move (4 attacks, one mechanism), and signal one is moved by anything that makes
the tokens strange (EV01, EV04, EV08, PI02). The combining rule then settles
nearly every evasion at 0.40 to 0.64 and labels it `unsure`: only 1 of 9 evasions
became `human`, but only 1 of 10 was still caught. The third problem is separate:
the route accepts text it cannot meaningfully score.

---

## The Improvement

**What I changed:** Signal one now averages over the 90% of tokens with the
*lowest* loss (a trimmed mean) instead of all of them:
`detector.py::robust_perplexity`. Trimming roughly halves every perplexity, so I
moved the logistic midpoint from 45 to 22 (`detector.py::model_signal`) so
ordinary text scores where it did. Thresholds and the combining rule are
untouched.

**Which diagnosis pointed at it:** Diagnosis 1 (typo attacks inflating
perplexity). I chose this change from my own stand-in run, before I had the staff
set, where three typo attacks lowered the model score by inflating a few outlier
tokens. A trimmed mean ignores outliers. I did not change the choice after seeing
the staff run, so that the before and after stay comparable; the staff run is
where it gets tested.

### Attack Run — After

`python run_attacks.py --set attack_set --label after`
(`results/staff_attack_run_2026-11-19_1902_after.md`), on the code at the
improvement (commit `13c9ef6`), same marking rule, same 56 inputs. Results:
**evasion 9 of 10 BROKE** (was 9), **false-positive 0 of 8** (was 0),
**prompt injection 1 of 6** (was 1), **malformed 5 of 20** (was 5), **flood 0 of
12** (was 0), 0 crashes. **No label changed on any of the 56 inputs.** The last
column shows the combined score before → after.

| ID | Family | Targeting | Status | Guess | Score | Mark | Before → after |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.400 | BROKE | 0.400 → 0.400 |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.400 | BROKE | 0.401 → 0.400 |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.473 | BROKE | 0.488 → 0.473 |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.649 | BROKE | 0.637 → 0.649 |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.272 | BROKE | 0.285 → 0.272 |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.454 | BROKE | 0.464 → 0.454 |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.474 | BROKE | 0.453 → 0.474 |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.401 | BROKE | 0.386 → 0.401 |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.594 | BROKE | 0.609 → 0.594 |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.875 | HELD | 0.875 → 0.875 |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.545 | HELD | 0.574 → 0.545 |
| FP02 | false_positive | human writing in a formal register | 200 | unsure | 0.695 | HELD | 0.720 → 0.695 |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | unsure | 0.666 | HELD | 0.719 → 0.666 |
| FP04 | false_positive | a student essay written to a rubric | 200 | unsure | 0.700 | HELD | 0.724 → 0.700 |
| FP05 | false_positive | technical documentation written by a person | 200 | unsure | 0.763 | HELD | 0.793 → 0.763 |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.734 | HELD | 0.731 → 0.734 |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.724 | HELD | 0.729 → 0.724 |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.460 | HELD | 0.390 → 0.460 |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.397 | HELD | 0.408 → 0.397 |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.248 | BROKE | 0.202 → 0.248 |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.476 | HELD | 0.486 → 0.476 |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.462 | HELD | 0.457 → 0.462 |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.477 | HELD | 0.449 → 0.477 |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.528 | HELD | 0.540 → 0.528 |
| MF01 | malformed | text is only whitespace | 400 | — | — | HELD | — → — |
| MF02 | malformed | text is a single character | 422 | — | — | HELD | — → — |
| MF03 | malformed | text is control characters | 200 | unsure | 0.400 | BROKE | 0.400 → 0.400 |
| MF04 | malformed | text is only punctuation | 200 | unsure | 0.400 | BROKE | 0.400 → 0.400 |
| MF05 | malformed | text is a very long single word | 200 | unsure | 0.600 | BROKE | 0.600 → 0.600 |
| MF06 | malformed | text is emoji only | 200 | unsure | 0.600 | BROKE | 0.600 → 0.600 |
| MF07 | malformed | text is right-to-left script | 200 | unsure | 0.695 | BROKE | 0.600 → 0.695 |
| MF08 | malformed | text is 60,000 characters | 413 | — | — | HELD | — → — |
| RQ01 | malformed | no text field at all | 400 | — | — | HELD | — → — |
| RQ02 | malformed | no creator_id | 200 | unsure | 0.482 | HELD | 0.364 → 0.482 |
| RQ03 | malformed | text is a number | 400 | — | — | HELD | — → — |
| RQ04 | malformed | text is a list | 400 | — | — | HELD | — → — |
| RQ05 | malformed | text is null | 400 | — | — | HELD | — → — |
| RQ06 | malformed | creator_id is an object | 400 | — | — | HELD | — → — |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | HELD | — → — |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | HELD | — → — |
| RQ09 | malformed | body is empty | 400 | — | — | HELD | — → — |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | — | — | HELD | — → — |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | — | — | HELD | — → — |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | HELD | — → — |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD | 0.400 → 0.400 |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD | 0.400 → 0.400 |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD | 0.400 → 0.400 |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD | 0.400 → 0.400 |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD | 0.400 → 0.400 |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD | 0.400 → 0.400 |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD | 0.400 → 0.400 |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD | 0.400 → 0.400 |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD | 0.400 → 0.400 |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.400 | HELD | 0.400 → 0.400 |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD | — → — |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD | — → — |

**Did it help, and how do I know:** No, not on the attacks. Every verdict and every
label is the same before and after. The target was the typo attack: EV01's model
score went from 0.164 to 0.180 and its combined score stayed on the 0.400 floor.
The movement elsewhere is small and mixed: five of the eight human texts
(FP01 to FP05) came down by 0.02 to 0.05, which is the right direction for
accusations, but FP08 went up by 0.07 and FP06 by 0.003; among the evasions,
EV04 rose 0.012, EV07 0.021 and EV05 fell 0.013. The true-AI text EV10 did not
move (0.875 both times), so trimming did not cost detection on the clear case.

The trade, from `run_eval.py --label after`
(`results/run_2026-11-16_1914_after.md`, three identical trials): the clearly-AI
set now gets the `ai` label on 2 of 5 texts instead of 3, and the 12-text
coverage set has 1 `ai` instead of 2, so that label is reachable but barely.
Spread is 0.797 − 0.331 = 0.466 (was 0.473), still met. Criterion 1 is still 0 of
10. Net: no attack caught that was missed before, and one more real AI text
missed in my own set. I'd call this a wash, and the honest takeaway is that the
attacks that worked move the style signal, the combining rule or the route, and a
change to signal one's average was aimed at a different place.

---

## What's Still Broken

- **9 of 10 evasion attacks still get through**, 8 as `unsure` and 1 as `human`.
  Fix: make the style signal harder to move (median-based sentence lengths,
  ignoring quoted text) and add a third signal that is neither shape nor
  predictability. I stopped because a signal this cheap to fool can't carry
  weight, and I'd want data before choosing a replacement.
- **The improvement did not help.** I aimed it at typo attacks using my own
  stand-in run, and the staff run's typo attack did not move (EV01 stayed on the
  0.400 floor). Fix: aim the next change at the combining rule's clamp, which is
  what holds most evasions at 0.40 to 0.60, or at the style signal. I stopped
  because the unit allows one change and I would not make a second on the side.
- **Five malformed inputs are accepted and scored (MF03 to MF07).** Fix: have the
  route refuse text with too few letters, or a single repeated token, with a 422
  before any signal sees it. I stopped because it is a change to the route outside
  the one improvement.
- **The false positives hold only because of a threshold.** FP05 is 0.007 under
  the line and five more (FP02, FP03, FP04, FP06, FP07) are between 0.72 and 0.73. Fix: widening the unsure
  band would leave almost no true AI text labelled `ai`. I stopped because there
  is no setting that avoids the trade, and I did not want to tune the threshold on
  the attack set's own texts.
- **Rotating `creator_id` defeats the rate limit.** Fix: also count by address
  with a looser limit. I stopped because it would have blocked my own attack run.
- **Criterion 1 is tested on drafted texts, not my own writing** (see above).

**The trade I'd make if this ran for real:** I'd keep the AI threshold high and
accept that a lot of AI text will pass. A wrong accusation costs one writer their
credibility, while a missed detection costs the site some trust. The people who
pay are readers and honest writers who compete against undetected AI text, and
plain writers (often second-language or younger) are protected only because they
land in "unsure" instead of "AI".

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [x] criteria.md has five numbered criteria, each naming a target
       [x] Each has a reason underneath
       [x] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [x] Two signals that measure DIFFERENT things, each with a named blind spot
       [x] Three label variants, all reachable, written out in full
       [x] POST /appeal changes status and writes to the log
       [x] Signals and Scoring names scoring.py::combine_signals
       [x] Sample Run: a submission AND an appeal, as pasted text
       [x] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [x] Rate limiting on /submit, with your numbers justified
       [x] The pasted run of status codes showing 429
       [x] Audit log with all nine fields, recording rejections too
       [x] The attack set run IN FULL, every input with an outcome
       [x] Ten audit log entries pasted as text
       [x] Five criteria across three trials
       [x] A diagnosis for every miss and every broken attack — stage AND mechanism
       [x] One improvement, with Attack Run — After
       [x] What's Still Broken, including the production trade
       [x] At least four new commits
       [x] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**


---

## Capstone

**What This Extends**

Provenance Guard, my unit 7 and 8 project: a Flask service that scores a text
with two signals (a local GPT-2 model and a stylometry measure), combines them,
and returns one of three labels. What's new in this unit is the operational
layer, not the detection: it now runs under `gunicorn` from one documented
command, writes one structured log line for every request (including rejected,
rate-limited and failed ones) with per-stage timings, and has a measured cost
per run. The detector, thresholds and `/submit` response are unchanged.

**The Shape**

Shape A, deploy and instrument, on Path B (local with logs). I'm not hosting it:
`torch` plus the GPT-2 weights need roughly 750 MB to 1.35 GB in memory and a
free host gives 512 MB, so it would be killed before serving a request.

Out of scope, decided before building: I am not fixing the 14 evasion attacks
that got through in unit 8, not adding a third signal, not retuning thresholds
or the combining rule, not hosting it on a paid tier, and not changing what
`/submit` returns.

**Stretch features declared before building** (so they count if present): a
latency breakdown across the stages of one request, a load observation at about
ten times normal rate, and a second measured improvement. All three are
below. Not attempting "both run paths", since a host can't hold the model.

**Running It**

Path B. One command, from the repo root with the venv active:

```bash
gunicorn -c gunicorn.conf.py app:app
```

`RUNNING.md` ("Capstone: the run path") has the environment: Python 3.11, the
pinned `requirements.txt`, the `gpt2` model (about 550 MB, `python detector.py`
downloads it) and about 1 GB of free memory. `gunicorn.conf.py` holds the
decisions: one worker, because each worker loads its own copy of the model
(about 1 GB) and a second would also split the in-memory rate-limit counters;
a 120 s timeout, because gunicorn's 30 s default is shorter than a cold model
load; and a model warm-up as the worker starts.

My test script clones the committed code into a clean folder and starts it with
this command (criterion 2). It reuses this repo's `.venv` rather than
reinstalling the packages every trial, so it tests the command and the
committed code, not `pip install`.

**Instrumentation**

Every request writes one JSON line to `logs/requests.jsonl`: `ts`, `method`,
`path`, `status`, `total_ms`, `stages_ms` (milliseconds per stage:
`model_signal`, `style_signal`, `combine`, `audit_write`), `creator_id`,
`text_chars` and, on any 4xx or 5xx, an `error` code. The submitted text is
never logged, only its length. This is separate from `logs/audit.jsonl`, which
records decisions and appeals. The hook runs after every response, so rejected
and rate-limited requests are logged too. A log failure is swallowed so it can
never break a response.

Real entries from one session against the gunicorn service
(`diagnostics/make_run_record.py`, full 27 lines in
`results/run_record.jsonl`). Ten successful requests:

```json
{"ts": "2026-11-17T07:22:36.154+00:00", "method": "POST", "path": "/submit", "status": 200, "total_ms": 105.2, "stages_ms": {"model_signal": 93.8, "style_signal": 0.3, "combine": 0.0, "audit_write": 0.5}, "creator_id": "writer-1", "text_chars": 178}
{"ts": "2026-11-17T07:22:36.225+00:00", "method": "POST", "path": "/submit", "status": 200, "total_ms": 68.5, "stages_ms": {"model_signal": 66.4, "style_signal": 1.0, "combine": 0.0, "audit_write": 0.3}, "creator_id": "writer-2", "text_chars": 112}
{"ts": "2026-11-17T07:22:36.284+00:00", "method": "POST", "path": "/submit", "status": 200, "total_ms": 55.9, "stages_ms": {"model_signal": 54.6, "style_signal": 0.1, "combine": 0.0, "audit_write": 0.3}, "creator_id": "writer-3", "text_chars": 146}
{"ts": "2026-11-17T07:22:36.365+00:00", "method": "POST", "path": "/submit", "status": 200, "total_ms": 78.1, "stages_ms": {"model_signal": 76.5, "style_signal": 0.3, "combine": 0.0, "audit_write": 0.4}, "creator_id": "writer-4", "text_chars": 127}
{"ts": "2026-11-17T07:22:36.451+00:00", "method": "POST", "path": "/submit", "status": 200, "total_ms": 82.5, "stages_ms": {"model_signal": 80.7, "style_signal": 0.2, "combine": 0.0, "audit_write": 0.5}, "creator_id": "writer-5", "text_chars": 188}
{"ts": "2026-11-17T07:22:36.515+00:00", "method": "POST", "path": "/submit", "status": 200, "total_ms": 60.0, "stages_ms": {"model_signal": 58.1, "style_signal": 0.2, "combine": 0.0, "audit_write": 0.3}, "creator_id": "writer-6", "text_chars": 122}
{"ts": "2026-11-17T07:22:36.595+00:00", "method": "POST", "path": "/submit", "status": 200, "total_ms": 78.5, "stages_ms": {"model_signal": 77.3, "style_signal": 0.1, "combine": 0.0, "audit_write": 0.3}, "creator_id": "writer-7", "text_chars": 165}
{"ts": "2026-11-17T07:22:36.669+00:00", "method": "POST", "path": "/submit", "status": 200, "total_ms": 71.6, "stages_ms": {"model_signal": 70.2, "style_signal": 0.2, "combine": 0.0, "audit_write": 0.3}, "creator_id": "writer-8", "text_chars": 115}
{"ts": "2026-11-17T07:22:36.749+00:00", "method": "POST", "path": "/submit", "status": 200, "total_ms": 77.6, "stages_ms": {"model_signal": 75.9, "style_signal": 0.1, "combine": 0.0, "audit_write": 0.6}, "creator_id": "writer-9", "text_chars": 148}
{"ts": "2026-11-17T07:22:36.834+00:00", "method": "POST", "path": "/submit", "status": 200, "total_ms": 81.7, "stages_ms": {"model_signal": 80.2, "style_signal": 0.1, "combine": 0.0, "audit_write": 0.4}, "creator_id": "writer-10", "text_chars": 144}
```

Failed and rejected requests from the same session: a missing `text`, an empty
`text`, a body that isn't JSON, a 60,000 character `text` (413), and the 11th
and 12th requests from one creator (429):

```json
{"ts": "2026-11-17T07:22:36.838+00:00", "method": "POST", "path": "/submit", "status": 400, "total_ms": 1.4, "stages_ms": {}, "creator_id": "writer-11", "text_chars": null, "error": "missing_text"}
{"ts": "2026-11-17T07:22:36.842+00:00", "method": "POST", "path": "/submit", "status": 400, "total_ms": 1.4, "stages_ms": {}, "creator_id": "writer-12", "text_chars": null, "error": "empty_text"}
{"ts": "2026-11-17T07:22:36.849+00:00", "method": "POST", "path": "/submit", "status": 400, "total_ms": 1.3, "stages_ms": {}, "creator_id": null, "text_chars": null, "error": "invalid_body"}
{"ts": "2026-11-17T07:22:36.854+00:00", "method": "POST", "path": "/submit", "status": 413, "total_ms": 1.6, "stages_ms": {}, "creator_id": "writer-14", "text_chars": 60000, "error": "text_too_long"}
{"ts": "2026-11-17T07:22:37.736+00:00", "method": "POST", "path": "/submit", "status": 429, "total_ms": 0.9, "stages_ms": {}, "creator_id": null, "text_chars": null, "error": "rate_limited"}
{"ts": "2026-11-17T07:22:37.738+00:00", "method": "POST", "path": "/submit", "status": 429, "total_ms": 0.6, "stages_ms": {}, "creator_id": null, "text_chars": null, "error": "rate_limited"}
```

Two things the log shows that I did not plan: a rate-limited request has
`creator_id` null, because the limiter rejects it before the route reads the
body, and so does the non-JSON body. The log can't say who was flooding.

**What It Costs**

Nothing here calls a paid service, so API spend is $0 and the cost is compute
and memory. Method: `run_capstone_criteria.py` reads the worker's CPU time from
`ps` before and after 10 consecutive requests, three times from three fresh
starts (30 requests), and the log gives wall time per request.

| Measure | Value | Source |
|---|---|---|
| Wall time per request, warm | 77 ms mean (72 ms median) over 21 successful requests | `results/run_record.jsonl` |
| CPU per request | 0.34 s (0.357, 0.326, 0.330 across three trials) | `results/capstone_run_after_threads.md` |
| Worker memory, warm | 918 to 947 MB | same |
| API spend | $0 | nothing calls a hosted model |

This is fewer than the ten separate runs the brief suggests for the average,
and CPU time on a laptop shared with other work is noisy (load average 6 to 12
while I measured), so read the CPU figure as roughly a third of a second.

For 100 people a day: I assume 5 submissions each, 500 requests a day. That is
500 x 0.34 = about 170 CPU-seconds a day (under 3 minutes) and 500 x 0.077 =
about 39 seconds of actual scoring. Compute is not the cost. The cost is one
worker holding about 0.93 GB of memory all day, which is why this needs a host
with more than 512 MB. 500 requests a day is about 21 an hour, far below what
one worker can do (the load test below handled 60 a minute).

**Run Log and Verdicts**

The criteria are in `criteria.md` (the capstone ones are on top). This is the
first full run, before any fix: the code as it stood when I wrote the criteria,
without the warm-up change. Three trials, each from fresh servers started from
a clean clone (`run_capstone_criteria.py::main`, output in
`results/capstone_run_before.md`).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every request leaves a log line | 20 of 20 | 20/20 | 20/20 | 20/20 | MET |
| 2. Starts from RUNNING.md alone | ready within 60 s | 10 s | 6 s | 7 s | MET |
| 3. First request not slow | first under 1 s, next-50 median under 250 ms | 2.138 s | 0.259 s | 0.283 s | MISSED |
| 4. Overload gives a refusal and a record | no 5xx, 40 to 50 x 429, 60/60 logged | 50 x 429, 60/60 | 50 x 429, 60/60 | 50 x 429, 60/60 | MET |
| 5. Memory and CPU ceiling | under 1000 MB, under 0.5 s CPU | 932 MB, 0.441 s | 922 MB, 0.438 s | 931 MB, 0.479 s | MET |

Criterion 3 is MISSED because run 1's first request took 2.138 s. The median
of the next 50 was fine in every run (0.073 to 0.077 s), so only the first
request is slow.

*Diagnosis, criterion 3.* The stage is the model signal on the first request;
the mechanism is that `warm_up()` loaded the weights but never ran the model,
so the first real request paid for torch's first forward pass. In an earlier
single run the worker went from 342 MB after warm-up to 918 MB after the first
request (`results/cost_before.txt`): about 570 MB was allocated during that
request, not at startup. Runs 2 and 3 were 0.26 s and 0.28 s, still above the
0.08 s of a normal request but under my limit. I think the weights were then
already in the operating system's file cache from run 1, but I did not test
that. The miss is real but smaller than the 2.8 s my first measurement
suggested, and it depends on whether the machine has just run the model.

Real output for criterion 3, run 1, from `run_capstone_criteria.py::trial_a`:
`first_s: 2.138, first_status: 200, median_next50_s: 0.077`.

Criteria 1, 2, 4 and 5 were met in all three trials. Looking at them honestly,
1, 2 and 4 were met easily (ready in 6 to 10 s against a 60 s limit, 20 of 20
every time), so those targets were set low. Criterion 5 was met with only
0.02 to 0.06 s to spare on CPU, which turned out to matter (below).

**The Improvement**

*The fix, aimed at criterion 3.* `detector.warm_up()` now also scores one
throwaway sentence, so the first forward pass happens at startup, not on a
user's request.

*Before and after, same criteria, same method* (`results/capstone_run_before.md`
and `results/capstone_run_after.md`):

| Criterion | Before | After (warm-up) |
|---|---|---|
| 1. Log line per request | MET, 20/20 x 3 | MET, 20/20 x 3 |
| 2. Ready within 60 s | MET, 6 to 10 s | MET, 7 to 8 s |
| 3. First request | MISSED: 2.138 s, 0.259 s, 0.283 s | MET: 0.085 s, 0.075 s, 0.089 s |
| 4. Overload | MET | MET |
| 5. Memory and CPU | MET: 922 to 932 MB, 0.44 to 0.48 s | **MISSED**: 930 to 967 MB, CPU 0.537 s, 0.553 s, 0.485 s |

It helped criterion 3: the first request is now as fast as the rest. It did not
come free, and the table shows the trade. The memory that used to be allocated
on the first request is now allocated at startup (342 MB to 830 MB after
warm-up in `results/cost_after.txt`), so the service starts heavier and a host
would hit its memory limit at boot. And in this run criterion 5 was MISSED,
on CPU, in two of three trials.

*Second improvement (stretch), aimed at criterion 5.* The first possible cause
I considered was that the warm-up had caused the CPU rise. I tested that and it was wrong. I
alternated the code with and without the warm-up over five rounds of 30
requests (`diagnostics/diag_cpu.py`): median CPU per request was 0.446 s
without it and 0.436 s with it, indistinguishable. The two misses were noise
on a busy laptop (load average 8 to 12); the one 0.532 s outlier was also the
slowest request, 0.142 s.

The stage is the model signal; the mechanism is torch's thread count. I ran the
same code with torch limited to different thread counts
(`diagnostics/diag_threads.py`, two rounds each):

| torch threads | CPU per request | Wall time per request |
|---|---|---|
| default (every core) | 0.41 to 0.43 s | 0.075 s |
| 4 | 0.30 to 0.33 s | 0.078 to 0.099 s |
| 2 | 0.25 s | 0.13 to 0.14 s |
| 1 | 0.20 to 0.22 s | 0.21 to 0.23 s |

The real work is about 0.2 CPU-seconds, and every extra thread adds overhead,
so using all cores roughly doubles CPU time for a small gain in wall time.
That the CPU grows with thread count is measured. Why (the threads waiting on
each other) is my inference; I did not profile it.

*The fix:* `config.TORCH_THREADS` (default 4, `AI201_TORCH_THREADS` overrides
it), applied with `torch.set_num_threads` when the model loads. Full run,
three trials, same method (`results/capstone_run_after_threads.md`):

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every request leaves a log line | 20 of 20 | 20/20 | 20/20 | 20/20 | MET |
| 2. Starts from RUNNING.md alone | ready within 60 s | 10 s | 7 s | 7 s | MET |
| 3. First request not slow | first under 1 s, median under 250 ms | 0.083 s | 0.084 s | 0.081 s | MET |
| 4. Overload gives a refusal and a record | no 5xx, 40 to 50 x 429, 60/60 logged | 50 x 429, 60/60 | 50 x 429, 60/60 | 50 x 429, 60/60 | MET |
| 5. Memory and CPU ceiling | under 1000 MB, under 0.5 s CPU | 919 MB, 0.357 s | 947 MB, 0.326 s | 918 MB, 0.330 s | MET |

CPU per request fell about 30 percent (0.44 to 0.55 s down to 0.33 to 0.36 s)
with no change in latency (median 0.083 to 0.091 s) or memory. All five are
met. The criterion 5 comparison is against the warm-up run, not the original.
I also re-ran the unit 7 detector checks three times after the warm-up change
(`check_criteria.py`, all five passed each time):
`results/criteria_check_after_warmup.md`.

**Latency breakdown and load (stretch)**

*Where the time goes.* Over 66 successful requests the model signal is about
98 percent of the time (median 77.5 of 78.8 ms); stylometry, combining and the
audit write together are under 1 ms. If it needs to be faster, only the model
matters (`results/load_2026-11-16.md`).

*Load at about ten times normal.* I took normal as 6 submissions a minute and
sent 60 a minute for a minute (`load_test.py`, each request its own
`creator_id` so the per-creator limit did not hide the load). All 60 returned
200, median 0.08 s, p95 0.12 s. At this size the service did not strain; one
request takes under 0.1 s warm, so one worker can in theory do several hundred
a minute. I did not push to the point where it fails, so I don't know where
that is. This run was before the warm-up and thread changes; its one slow
request (2.3 s) was the first of the session.

**What's Still Broken**

- *The log cannot say who was rate limited.* A 429 and a non-JSON body both have
  `creator_id` null. Criterion 4 only asked for the line to exist, so it passes,
  but a flood is anonymous in the record. This is the first thing I would fix:
  have the limiter's key function record the creator before it rejects. I did
  not do it because it changes the request path and I had already used the unit
  on the CPU diagnosis.
- *Three targets were set too low.* Criteria 1, 2 and 4 were met with room to
  spare in every trial. I would tighten criterion 2 from 60 s to 20 s (it took
  6 to 10 s) and criterion 3's first-request target from 1 s to 0.2 s (it takes
  about 0.08 s now). Criterion 1 could add a request that crashes the worker
  mid-response, which this test does not try.
- *CPU is measured on a shared laptop.* Load average was 6 to 12 while I
  measured, and the criterion 5 sample is only 10 requests, so it is noisy. The
  thread fix has a clear margin, but I would want a quieter machine before
  trusting the exact figures.
- *The memory moved, not shrank.* The service needs about 0.93 GB from startup
  and cannot run on a 512 MB host. A smaller model is out of scope here.
- *One worker.* A request that takes long blocks the others, and I only tested
  to 60 a minute.
- Still out of scope from unit 8: the 14 evasion attacks that got through, and
  anything about detection quality.

I stopped because the five criteria are met and the remaining items are either
out of the scope I declared or need a different kind of test.

If this were real and I had another unit, the one thing I would do first is fix
the anonymous 429 log lines, because an operator looking at a flood needs to
know who is sending it, and everything else in the log is already useful.

**How I Used AI**

*Moment 1: criteria.* I asked Claude to draft five criteria after I had
already seen some measurements. It returned five with targets and reasons, and
warned me that the brief says to write them myself and that my earlier
measurements meant they were not blind. I reviewed them and told it to write
them into `criteria.md` as drafted, so the wording is Claude's and I did not
change it. `criteria.md` notes that some measurements existed first. Criterion 5
sat close to what I had measured, and then really did fail, in two of three
trials of one run.

*Moment 2: the CPU miss.* I asked Claude to diagnose why criterion 5 missed.
It listed the warm-up change as one possible cause, and said it wanted to
test one explanation before writing it down. It ran an alternating
before-and-after test, which showed the warm-up made no difference, and then a
thread-count test, which found the real cause. I asked
it to make the 4-thread change and re-run all five criteria. I kept its
statement that the reason for the extra CPU is an inference, and it is worded
that way above.

*A detour.* I first decided the capstone needed its own repository and had
Claude push the commits to a new one. I then read the brief, which says to use
the same repository as the system I'm extending and not to recreate it, so I
had Claude put the work back in this repo, where the earlier history lives.
