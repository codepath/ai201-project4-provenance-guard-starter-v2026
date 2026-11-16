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

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to GPT-2 (perplexity: mean
surprise per token over the first 400 tokens), squashed onto 0-1 with a
logistic centred on perplexity 45. Low perplexity gives a high AI score.

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

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
