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
The provenance guard takes a piece of text from the writing site and returns four things: a guess about how it was produced, a confidence score for that guess, a plain-English label for readers, and a way for the writer to dispute the result. The path the submission takes is:

1. Arrive. The site sends the text to the service with an ID

2. Prepare. The service cleans and normalizes the text. It also checks that there's enough of it to judge, and very short submissions get an "not enough text" outcome instead of a guess.

3. Analyze. The text goes through the detection checks, and each one produces its own signal.

4. Guess and score. The signals are combined into a single guess and a confidence number. The number reflects how strongly the evidence points one way, so a weak or mixed result gets a low score instead of a forced answer.

5. Choose the label. The guess and confidence are mapped to the wording a reader will see. High confidence gets a direct label, and low confidence gets hedged wording or no label at all.

6. Return and record. The service sends back the guess, the confidence, and the label, and it stores the result so it can be reviewed later.

7. Push back. If the writer disagrees, they file a dispute from the label. The dispute is attached to the stored result and sent for review. If the review overturns the guess, the label is updated or removed.


---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** This signal measures Perplexity. Perplexity indicates how predictable a piece of text is to a LLM. This model reads the text and takes its mean negative log-likelihood per token, then exponentiates it. Low perplexity indicates the model could have guessed the next words. High preplexity indicates the model was surprised.

**Why that might differ between human and AI writing:**
A language model writes by repeatedly picking a likely next word, so its output tends to be text another model finds easy to predict. Human writing wanders more: odd word choices, abrupt turns, and specific details instead of typical ones. That gives human text higher perplexity on average and AI text lower.

**What it can't see:**
Authorship. It only sees predictability, which is not the same thing.
- **Plain human writing looks like AI.** Common words in short, ordinary sentences score as machine-like. That covers people writing in a second language, younger writers, and anyone writing plainly on purpose, who are the least able to argue back.
- **Ornate AI or human text looks human.** Dense prose full of rare words scores as human, because rare words are what a language model fails to predict. Formality alone doesn't decide it.
- **Edited or prompted AI text.** It has no view of the writing process, so AI text that was edited, or prompted to be quirky, can slip past.
- **Topic and length.** The usual perplexity range shifts with both, which is why the raw number isn't what gets scored.
- **Context.** It judges only the text in front of it, so it can't use the author's history, the assignment, or any evidence outside the writing.

### Signal two — the style signal

**What it measures:**

This signal measures shape of the text, not its meaning.

- Sentence-length spread: the standard deviation of sentence lengths divided by the mean, so short and long texts are comparable.
- Type-token ratio: unique words over total words, a measure of vocabulary variety.
- Punctuation density: commas, semicolons, colons, dashes, brackets, quotes, ellipses, "?" and "!" per word. Full stops and apostrophes are not counted.
These are scaled to 0-1, weighted (spread 45%, punctuation 35%, vocabulary 20%) and flipped into one score where higher means more likely AI.


**Why that might differ between human and AI writing:**
Generated prose tends toward even, mid-length sentences and a narrower band of vocabulary, because that is what "most likely next word" produces on average. Human writing is lumpier: a three-word sentence next to a forty-word one, odder word choices, and more varied punctuation such as dashes, parentheses and semicolons. In my test, the clearly human paragraph had a sentence-length spread of 1.5 against 0.2 for the AI paragraph.

**What it can't see:**
- Meaning. It cannot read, so anything that changes the shape without changing the substance moves it. Adding typos, breaking up sentences, or pasting in a quotation is cheap to do on purpose. In my test, a light edit left the AI text at 0.73.
- Plain human writing. Someone writing short, simple sentences with little punctuation gets a score of 0.87, higher than the AI sample, so the people least able to argue back are the ones accused.
- Length. Type-token ratio falls as text gets longer, so texts of different lengths aren't directly comparable.
- Short input. A one-sentence submission has no spread to measure, so it returns 0.0 and reads as machine-like, and fewer than 3 words returns a neutral 0.5.
- Genre and language. Poetry, lists, code, and second-language or very formal writing all have unusual shapes that say nothing about who wrote them.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

**The numbers:**

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

<!-- TODO (Milestone 3): run this locally and paste the real response.
     This sandbox's network policy blocks huggingface.co, so gpt2 can't be
     downloaded here — `python detector.py` and `/submit` both need that
     host. Run `python detector.py` once to download the model, then
     `python app.py`, then the curl below, and paste what comes back. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "creator_id": "..."}'
```

```json

```

**An appeal**

<!-- /appeal isn't built yet (Milestone 5) — fill this in once it is. -->

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json

```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

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
