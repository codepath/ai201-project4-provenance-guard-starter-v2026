# Implementation plan (recorded before scoring results)

Submission path: validate JSON -> assign content ID -> local GPT-2 predictability signal -> style measurements -> weighted score -> reader label -> append audit decision and return JSON. Appeals append an under_review event without replacing the decision.

POST /submit accepts text (nonblank string, at most 20,000 characters) and creator_id (nonblank string, at most 200 characters). Returns content_id, guess (ai/human/unsure), confidence (AI-likelihood index, 0 to 1), label, model_score, style_score, status. Invalid input: JSON error, HTTP 400; excessive text: HTTP 413; unavailable detector: HTTP 503.

POST /appeal accepts content_id and reasoning (nonblank string, at most 5,000 characters). Unknown ID: 404; invalid input: 400. Success returns content_id, status under_review, and confirmation.

Signal one: GPT-2 token predictability, not verification of meaning or authorship. Familiar human prose may look AI-like; unusual AI prose may look human. Only the first 400 tokens are analyzed.
Signal two: sentence-length coefficient of variation, unique-word ratio, punctuation density. It cannot understand content; editing shape can fool it. Short texts and non-English writing are unreliable.

Proposed combining rule: 0.7 model + 0.3 style. If the signals differ by at least 0.5, clamp the result to [0.35, 0.65] to express uncertainty. Human label at scores <= 0.20, AI label at >= 0.80, unsure otherwise. These conservative bands prioritize reducing false accusations. Scores are heuristic indices, not calibrated probabilities.

Style rule: 0.5 * (1 - min(sentence spread, 1)) + 0.3 * (1 - unique-word ratio) + 0.2 * (1 - min(punctuation density / 0.10, 1)). Fewer than three sentences or twenty words returns neutral 0.5.

False-positive trace: a human could score 0.85 and receive the AI label. The label must acknowledge error and direct them to appeal. An appeal preserves the original score and appends status under_review; it does not rerun the detector.

No stretch features are planned. Acceptance criteria must be supplied by the student before results are generated.
