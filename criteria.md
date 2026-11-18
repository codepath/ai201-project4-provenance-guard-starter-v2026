
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
## 1.
Zero false positives among 10 human-written samples in each of three trials.



**Why this target:**
Human writing is creative work, and incorrectly attributing it to AI denies the writer proper credit.


---

## 2.

When I test Provenance Guard using 3 human-written samples and 3 AI-generated samples, I should have a minimum average score difference of 0.50, with AI scoring higher and the target must be met in 3 trials. 



**Why this target:**
I chose this target because human writing naturally contains variations and imperfections while AI writing sound so mechanical 


---

## 3.
At least one submission must produce each of the three labels in every trial, across three trials.



**Why this target:**
I chose this target because in the face of insufficient evidence, it is better to acknowledge uncertainty than present an unreliable conclusion as fact.


---

## 4.

There should be 3 valid appeals per trial. All 3 must be recorded in the audit log and must have the status under_review and the requirement must hold across 3 trials. 



**Why this target:**
I chose this target because every appeal should receive fair consideration based on the merits presented by the writer. 


---

## 5.

There should be test for two invalid submissions: one with empty text and one with the text field missing. Both must return HTTP 400 and must not produce a classification decision and Both tests must pass in each of three trials.



**Why this target:**
I chose this target because there is no information for the system to make any decision.


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


## Unit 9 Capstone Acceptance Criteria

1. Oversized Submission Validation

When a user submits text exceeding 10,000 characters, the system should return HTTP 400 with the error code `submission_too_large`.

**Why this target:** This prevents excessive processing and protects system resources.


2. Unsupported Control Character Validation

When a submission contains an unsupported control character such as `\\x00`, the system should return HTTP 400 with the error code `unsupported_control_character`.

**Why this target:** This prevents malformed inputs from reaching the classification model.


3. Punctuation-Only Submission Validation

When a user submits punctuation-only text such as `!!! ??? ###`, the system should return HTTP 400 with the error code `no_meaningful_words`.

**Why this target:** The submission contains no alphabetic content suitable for meaningful classification.


4. Valid Submission Processing

For each of three trials, a valid submission containing at least three words and no prohibited characters should return HTTP 200 and include a classification result.

**Why this target:** The new validation rules should not prevent legitimate submissions from being classified.


5. Structured Operational Logging

In each of three trials, submit one valid request and one invalid request. Both requests must generate operational log records containing a timestamp, input character count, HTTP status, and execution duration in milliseconds.

**Why this target:** Recording successful and rejected requests helps monitor performance, investigate failures, and provide evidence of system behavior.

