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

> **Honest note on the attack set.** The staff `attacks.csv` was not in my
> repository and I could not open the unit page that provides it, so I wrote my
> own set in the same two-file format: `attack_set/attacks.csv` (25 text
> attacks) and `attack_set/attacks_malformed_requests.csv` (14 malformed
> requests and 12 flood requests), 51 inputs in all. The run is
> `python run_attacks.py --set attack_set --label before`. To use the staff set,
> run the same command with `--set <staff folder>` and redo the marks.
>
> Marking rule, written down so it can be checked: an **evasion** attack is
> **BROKE** unless it is still labelled `ai`; a **false-positive** attack is
> **BROKE** if a plain human text is labelled `ai`; a **malformed** attack is
> **HELD** if it gets a 4xx JSON answer; a **flood** attack is **HELD** if the
> first 10 pass and later ones get 429. Anything that crashes is BROKE.
> Caveat: two of my five unedited AI texts were already labelled `unsure`
> (combined 0.78 and 0.76), so evasions of those two did not break a detection
> that existed.

Score is the combined score. Results: **evasion 15 of 15 BROKE**,
**false-positive 2 of 5 BROKE**, malformed 0 of 14 BROKE, flood 0 of 12 BROKE,
0 crashes (no 5xx anywhere).

| ID | Family | Targeting | Status / guess / score | Mark |
|---|---|---|---|---|
| EV01 | evasion_typos | style signal: typos raise vocabulary variety | 200 unsure 0.523 | BROKE |
| EV02 | evasion_typos | style signal: typos raise vocabulary variety | 200 unsure 0.793 | BROKE |
| EV03 | evasion_typos | style signal: typos raise vocabulary variety | 200 unsure 0.779 | BROKE |
| EV04 | evasion_typos | style signal: typos raise vocabulary variety | 200 unsure 0.592 | BROKE |
| EV05 | evasion_typos | style signal: typos raise vocabulary variety | 200 unsure 0.635 | BROKE |
| SP01 | evasion_split | style signal: uneven sentence lengths | 200 unsure 0.619 | BROKE |
| SP02 | evasion_split | style signal: uneven sentence lengths | 200 unsure 0.600 | BROKE |
| SP03 | evasion_split | style signal: uneven sentence lengths | 200 unsure 0.614 | BROKE |
| PU01 | evasion_punctuation | style signal: rare punctuation | 200 unsure 0.448 | BROKE |
| PU02 | evasion_punctuation | style signal: rare punctuation | 200 unsure 0.600 | BROKE |
| PU03 | evasion_punctuation | style signal: rare punctuation | 200 unsure 0.465 | BROKE |
| QU01 | evasion_quote | style signal: pasted quotation changes shape | 200 unsure 0.600 | BROKE |
| QU02 | evasion_quote | style signal: pasted quotation changes shape | 200 unsure 0.600 | BROKE |
| HP01 | evasion_human_prefix | both signals: genuine human sentences ahead of AI text | 200 unsure 0.442 | BROKE |
| HP02 | evasion_human_prefix | both signals: genuine human sentences ahead of AI text | 200 unsure 0.547 | BROKE |
| FP01 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 unsure 0.766 | HELD |
| FP02 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 unsure 0.759 | HELD |
| FP03 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 unsure 0.675 | HELD |
| FP04 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 ai 0.815 | BROKE |
| FP05 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 ai 0.854 | BROKE |
| SH01 | short_input | too short to score | 200 unsure 0.400 | HELD |
| SH02 | short_input | one sentence, spread undefined | 200 unsure 0.567 | HELD |
| OD01 | odd_input | non-English text | 200 unsure 0.442 | HELD |
| OD02 | odd_input | repeated word | 200 ai 0.877 | HELD |
| OD03 | odd_input | emoji and symbols | 200 unsure 0.526 | HELD |
| MR01 | malformed_request | missing text | 400 | HELD |
| MR02 | malformed_request | empty text | 400 | HELD |
| MR03 | malformed_request | null text | 400 | HELD |
| MR04 | malformed_request | number as text | 400 | HELD |
| MR05 | malformed_request | list as text | 400 | HELD |
| MR06 | malformed_request | bare list body | 400 | HELD |
| MR07 | malformed_request | bare string body | 400 | HELD |
| MR08 | malformed_request | invalid JSON | 400 | HELD |
| MR09 | malformed_request | empty body | 400 | HELD |
| MR10 | malformed_request | wrong content type | 400 | HELD |
| MR11 | malformed_request | huge text (60k chars) | 413 | HELD |
| MR12 | malformed_request | creator_id is an object | 400 | HELD |
| MR13 | malformed_request | missing creator_id | 200 unsure 0.782 | HELD |
| MR14 | malformed_request | invalid UTF-8 bytes | 400 | HELD |
| FL01 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.843 | HELD |
| FL02 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.843 | HELD |
| FL03 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.843 | HELD |
| FL04 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.843 | HELD |
| FL05 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.843 | HELD |
| FL06 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.843 | HELD |
| FL07 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.843 | HELD |
| FL08 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.843 | HELD |
| FL09 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.843 | HELD |
| FL10 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.843 | HELD |
| FL11 | flood_same_creator | rate limit: same creator_id every time | 429 | HELD |
| FL12 | flood_same_creator | rate limit: same creator_id every time | 429 | HELD |

Full report: `results/attack_run_2026-11-16_1909_before.md`.

**Ten audit log entries from the run**

Chosen to show the interesting failures, not the easiest: the typo attacks (EV01,
EV04) where the *model* score collapsed; the attacks where the *style* score
collapsed (QU02, PU02, SP02); the two accusations of plain human writing (FP04,
FP05); an emoji input that took the style score to 0.0 (OD03); and two
rejections that left a trace (a rate-limit 429 and a missing-`text` refusal).
Pulled from `GET /log` (`results/audit_extract_before.json`).

```json
[
  {
    "combined_score": 0.5229,
    "content_id": "9207273c-dd53-4fdf-994c-1e7505fbfe14",
    "creator_id": "attacker_EV01",
    "guess": "unsure",
    "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
    "model_score": 0.42,
    "status": "decided",
    "style_score": 0.6773,
    "timestamp": "2026-11-17T00:09:36+00:00"
  },
  {
    "combined_score": 0.5916,
    "content_id": "26c9538d-bb26-4abd-aec0-f697374af340",
    "creator_id": "attacker_EV04",
    "guess": "unsure",
    "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
    "model_score": 0.4978,
    "status": "decided",
    "style_score": 0.7324,
    "timestamp": "2026-11-17T00:09:37+00:00"
  },
  {
    "combined_score": 0.6,
    "content_id": "f0db6b3f-37cc-4caa-bd43-b2ca6a07ba75",
    "creator_id": "attacker_QU02",
    "guess": "unsure",
    "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
    "model_score": 0.929,
    "status": "decided",
    "style_score": 0.4531,
    "timestamp": "2026-11-17T00:09:38+00:00"
  },
  {
    "combined_score": 0.5998,
    "content_id": "26e2a233-a64e-4c3f-b428-7a8594e3632e",
    "creator_id": "attacker_PU02",
    "guess": "unsure",
    "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
    "model_score": 0.8628,
    "status": "decided",
    "style_score": 0.2054,
    "timestamp": "2026-11-17T00:09:37+00:00"
  },
  {
    "combined_score": 0.6,
    "content_id": "2c2552a1-b8ea-4bd9-bea3-448547ae9993",
    "creator_id": "attacker_SP02",
    "guess": "unsure",
    "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
    "model_score": 0.8646,
    "status": "decided",
    "style_score": 0.4002,
    "timestamp": "2026-11-17T00:09:37+00:00"
  },
  {
    "combined_score": 0.8536,
    "content_id": "8a378b20-7fcc-4bf2-9c77-b28c6d799a1d",
    "creator_id": "attacker_FP05",
    "guess": "ai",
    "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
    "model_score": 0.9193,
    "status": "decided",
    "style_score": 0.755,
    "timestamp": "2026-11-17T00:09:39+00:00"
  },
  {
    "combined_score": 0.8145,
    "content_id": "e2ffe12a-b3f0-4e89-9d04-6eab44dd6a2e",
    "creator_id": "attacker_FP04",
    "guess": "ai",
    "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
    "model_score": 0.8715,
    "status": "decided",
    "style_score": 0.7289,
    "timestamp": "2026-11-17T00:09:39+00:00"
  },
  {
    "combined_score": 0.5261,
    "content_id": "e97ed502-4866-41fd-86b6-ab73095407d3",
    "creator_id": "attacker_OD03",
    "guess": "unsure",
    "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
    "model_score": 0.8769,
    "status": "decided",
    "style_score": 0.0,
    "timestamp": "2026-11-17T00:09:40+00:00"
  },
  {
    "combined_score": null,
    "content_id": null,
    "creator_id": "flood_attacker",
    "event": "rejected",
    "guess": null,
    "label": null,
    "limit": "10 per 1 minute",
    "model_score": null,
    "reason": "rate_limited",
    "status": "rejected",
    "style_score": null,
    "timestamp": "2026-11-17T00:09:41+00:00"
  },
  {
    "combined_score": null,
    "content_id": null,
    "creator_id": "attacker_MR01",
    "event": "rejected",
    "guess": null,
    "label": null,
    "model_score": null,
    "reason": "missing_text",
    "status": "rejected",
    "style_score": null,
    "timestamp": "2026-11-17T00:09:40+00:00"
  }
]
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it: **FP05**, a plain five-sentence product review
("This product is good. It is easy to use. The price is fair...") that came back
as high-confidence AI with a combined score of 0.854 (model 0.919, style 0.755).
Nothing about it is machine-like except that it is short, plain and correct, and
the writers who naturally write like that are the ones with the least room to
argue. It got the label "This looks like it may have been written with an AI
tool", and the only remedy is an appeal.

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

No criterion was missed, so these diagnose the 15 evasion attacks and the 2
false positives that broke. The service has five stages: the route, signal one,
signal two, the combining rule, and the label mapping.

1. **Typo attacks (EV01, EV04, EV05) — stage: signal one; mechanism:
   typo-broken words inflate mean perplexity.** A misspelled word is split into
   rare sub-word pieces the model never saw together, each with a huge loss, and
   the mean over 400 tokens rises. EV01: model score 0.853 → 0.420 while the style
   score stayed 0.677. EV04: 0.937 → 0.498, style 0.732 → 0.732. EV05: 0.873 →
   0.658, style 0.600 → 0.600. My attack file said these target the style signal
   ("typos raise vocabulary variety"); the data says otherwise, since style did not
   move at all.
2. **Typo attacks that barely moved the model (EV02, EV03) — stage: label
   mapping; mechanism: the 0.80 threshold sits on top of the AI cluster.**
   EV02 model 0.866, style 0.684, combined 0.793; EV03 0.797 / 0.751 / 0.779. The
   unedited versions scored 0.843 and 0.821. A tiny nudge crossed a line I set at
   0.80, and the whole true-AI cluster (0.76 to 0.86) straddles it.
3. **Split, quote, punctuation and human-prefix attacks (SP, QU, PU, HP; 10
   attacks) — stage: signal two, then the combining rule; mechanism: shape
   changes without the substance changing.** Style dropped from about 0.68-0.75
   to 0.40-0.45 for SP and QU, to 0.17-0.21 for PU, and to about 0.32 for HP. In
   QU01 and QU02 the model still said 0.82 and 0.93, but the 0.40 disagreement
   rule clamped the result to exactly 0.600. The rule I built to avoid accusations
   on disagreement is the same rule that lets one signal's evasion pull a
   confident model reading down into "unsure".
4. **Emoji input (OD03) — stage: signal two feeding the combining rule;
   mechanism:** `!`, `#` and quotation marks put punctuation density far over its
   cap, so style went to 0.0 while the model said 0.877, and the clamp returned
   0.526. Not an accusation, just more proof that style is trivially gamed.
5. **False positives FP04 and FP05 — stages: signal one and signal two
   together; mechanism: plain, short, common-word, evenly-sized sentences look the
   same as AI to both signals.** FP04 model 0.872 style 0.729; FP05 0.919 / 0.755.
   Because both signals share the blind spot, they *agree*, so the combining rule
   has nothing to disagree about and nothing to soften.

**The pattern:** two mechanisms account for nearly everything. Signal two is
cheap to move (10 attacks, one mechanism), and both signals misread plain human
writing the same way (2 broken, 3 more within 0.15 of the line). The typo
failures are a third, separate problem in signal one.

---

## The Improvement

**What I changed:** Signal one now averages over the 90% of tokens with the
*lowest* loss (a trimmed mean) instead of all of them:
`detector.py::robust_perplexity`. Trimming roughly halves every perplexity, so I
moved the logistic midpoint from 45 to 22 (`detector.py::model_signal`) so
ordinary text scores where it did. Thresholds and the combining rule are
untouched.

**Which diagnosis pointed at it:** Diagnosis 1. The typo attacks lowered the model
score by inflating a few outlier tokens, and a trimmed mean ignores outliers.

### Attack Run — After

`python run_attacks.py --set attack_set --label after`
(`results/attack_run_2026-11-16_1911_after.md`). Same marking rule. Results:
**evasion 14 of 15 BROKE** (was 15), **false-positive 2 of 5 BROKE** (was 2),
malformed 0 of 14, flood 0 of 12, 0 crashes.

| ID | Family | Targeting | Status / guess / score | Mark |
|---|---|---|---|---|
| EV01 | evasion_typos | style signal: typos raise vocabulary variety | 200 unsure 0.643 | BROKE |
| EV02 | evasion_typos | style signal: typos raise vocabulary variety | 200 ai 0.806 | HELD |
| EV03 | evasion_typos | style signal: typos raise vocabulary variety | 200 unsure 0.784 | BROKE |
| EV04 | evasion_typos | style signal: typos raise vocabulary variety | 200 unsure 0.685 | BROKE |
| EV05 | evasion_typos | style signal: typos raise vocabulary variety | 200 unsure 0.676 | BROKE |
| SP01 | evasion_split | style signal: uneven sentence lengths | 200 unsure 0.640 | BROKE |
| SP02 | evasion_split | style signal: uneven sentence lengths | 200 unsure 0.600 | BROKE |
| SP03 | evasion_split | style signal: uneven sentence lengths | 200 unsure 0.613 | BROKE |
| PU01 | evasion_punctuation | style signal: rare punctuation | 200 unsure 0.436 | BROKE |
| PU02 | evasion_punctuation | style signal: rare punctuation | 200 unsure 0.587 | BROKE |
| PU03 | evasion_punctuation | style signal: rare punctuation | 200 unsure 0.444 | BROKE |
| QU01 | evasion_quote | style signal: pasted quotation changes shape | 200 unsure 0.600 | BROKE |
| QU02 | evasion_quote | style signal: pasted quotation changes shape | 200 unsure 0.600 | BROKE |
| HP01 | evasion_human_prefix | both signals: genuine human sentences ahead of AI text | 200 unsure 0.441 | BROKE |
| HP02 | evasion_human_prefix | both signals: genuine human sentences ahead of AI text | 200 unsure 0.541 | BROKE |
| FP01 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 unsure 0.733 | HELD |
| FP02 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 unsure 0.744 | HELD |
| FP03 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 unsure 0.662 | HELD |
| FP04 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 ai 0.807 | BROKE |
| FP05 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 ai 0.843 | BROKE |
| SH01 | short_input | too short to score | 200 unsure 0.729 | HELD |
| SH02 | short_input | one sentence, spread undefined | 200 unsure 0.534 | HELD |
| OD01 | odd_input | non-English text | 200 unsure 0.414 | HELD |
| OD02 | odd_input | repeated word | 200 ai 0.878 | HELD |
| OD03 | odd_input | emoji and symbols | 200 unsure 0.525 | HELD |
| MR01 | malformed_request | missing text | 400 | HELD |
| MR02 | malformed_request | empty text | 400 | HELD |
| MR03 | malformed_request | null text | 400 | HELD |
| MR04 | malformed_request | number as text | 400 | HELD |
| MR05 | malformed_request | list as text | 400 | HELD |
| MR06 | malformed_request | bare list body | 400 | HELD |
| MR07 | malformed_request | bare string body | 400 | HELD |
| MR08 | malformed_request | invalid JSON | 400 | HELD |
| MR09 | malformed_request | empty body | 400 | HELD |
| MR10 | malformed_request | wrong content type | 400 | HELD |
| MR11 | malformed_request | huge text (60k chars) | 413 | HELD |
| MR12 | malformed_request | creator_id is an object | 400 | HELD |
| MR13 | malformed_request | missing creator_id | 200 unsure 0.777 | HELD |
| MR14 | malformed_request | invalid UTF-8 bytes | 400 | HELD |
| FL01 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.828 | HELD |
| FL02 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.828 | HELD |
| FL03 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.828 | HELD |
| FL04 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.828 | HELD |
| FL05 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.828 | HELD |
| FL06 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.828 | HELD |
| FL07 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.828 | HELD |
| FL08 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.828 | HELD |
| FL09 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.828 | HELD |
| FL10 | flood_same_creator | rate limit: same creator_id every time | 200 ai 0.828 | HELD |
| FL11 | flood_same_creator | rate limit: same creator_id every time | 429 | HELD |
| FL12 | flood_same_creator | rate limit: same creator_id every time | 429 | HELD |

**Did it help, and how do I know:** A little, and it cost something. The typo
scores moved the right way: combined EV01 0.523 → 0.64, EV04 0.592 → 0.69, EV05
0.635 → 0.68, and EV02 went from 0.793 to 0.81, which crossed the line and is the
one extra evasion now caught. None of the other three crossed it. The false
positives did not improve at all (FP04 0.81 → 0.81, FP05 0.85 → 0.84), which is
what the diagnosis predicted, since they are a different mechanism.

The trade, from `run_eval.py --label after`
(`results/run_2026-11-16_1914_after.md`, three identical trials): the clearly-AI
set now gets the `ai` label on 2 of 5 texts instead of 3, and the 12-text
coverage set has 1 `ai` instead of 2, so that label is reachable but barely.
Spread is 0.797 − 0.331 = 0.466 (was 0.473), still met. Criterion 1 is still 0 of
10. Net: one more attack caught, one more real AI text missed. Trimming helps
against typos but also removes some signal from genuinely predictable machine
text. I'd call this a wash, not a fix, and the honest takeaway is that the
threshold, not the signal, is where the real leverage is.

---

## What's Still Broken

- **14 of 15 evasion attacks still get through.** Fix: make the style signal
  harder to move (median-based sentence lengths, ignoring quoted text) and add a
  third signal that is neither shape nor predictability. I stopped because a
  signal this cheap to fool can't carry weight, and I'd want data before
  choosing a replacement.
- **FP04 and FP05 are still accused**, and criterion 1 only passes because my
  ten test texts happen to score under 0.80. Fix: the unsure band would have to
  reach about 0.87, which would leave almost no true AI text labelled `ai`. I
  stopped because there is no setting that avoids the trade, and I did not want to
  tune the threshold on the attack set's own false positives.
- **Rotating `creator_id` defeats the rate limit.** Fix: also count by address
  with a looser limit. I stopped because it would have blocked my own attack run.
- **Criterion 1 is tested on drafted texts, not my own writing** (see above), and
  my attack set is a stand-in for the staff set.

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
