"""
Turning two numbers into one, and one number into something a person can read.


Two functions live here.

`combine_signals` is where your false-positive decision from Milestone 1
actually gets made. Everything above it — the labels, the appeal path — is
downstream of a number this function produced.

`score_to_label` is where you stop writing for a machine and start writing for
a person. A score of 0.62 means nothing to a writer.

⚠️ Your README's **Signals and Scoring** section has to name the file and
function holding your combining rule. The grader checks your code against what
you claim, so that line should read `scoring.py::combine_signals`.
"""

import config


# What a reader sees. Written for someone who has never heard of a threshold,
# and who may well have written every word themselves.
LABEL_HUMAN = (
    "We think this was probably written by a person. Our checks found nothing "
    "that points to automated writing."
)
LABEL_UNSURE = (
    "We can't tell. Our checks gave mixed results on this one, which happens "
    "with plenty of writing by real people. Nothing has been decided about "
    "your work. If you wrote it yourself, you can appeal and a person will "
    "take a look."
)
LABEL_AI = (
    "This looks like it may have been written with an AI tool. Our checks are "
    "not perfect, and we can be wrong. If you wrote this yourself, please "
    "appeal and a person will review it."
)


def combine_signals(model_score: float, style_score: float) -> float:
    """
    Combine two 0-1 signals (higher = more likely AI) into one 0-1 score.

    The rule, in words: a weighted average, with one safeguard. If the two
    signals disagree by more than DISAGREEMENT_GAP, the answer is pulled into
    the unsure band — it can no longer be a confident human OR a confident AI
    label. Two methods that contradict each other are, by definition,
    uncertainty, and the expensive mistake is an accusation, so an accusation
    needs BOTH signals to agree.

    The numbers (all in config.py): model 0.6, style 0.4, gap 0.40, clamp to
    0.40-0.60. The model signal gets more weight because it reads the text's
    content-level predictability; the style signal is cheap to fool with typos
    and edits, so it should not be able to drive a result by itself.
    """
    avg = (
        config.WEIGHT_MODEL_SIGNAL * model_score
        + config.WEIGHT_STYLE_SIGNAL * style_score
    )
    if abs(model_score - style_score) > config.DISAGREEMENT_GAP:
        avg = min(max(avg, config.DISAGREEMENT_FLOOR), config.DISAGREEMENT_CEILING)
    return round(min(max(avg, 0.0), 1.0), 4)


def score_to_label(score: float) -> tuple[str, str]:
    """
    Turn a score into (guess, label_text). `guess` is "human" / "unsure" /
    "ai"; `label_text` is the sentence a person reads. Thresholds are in
    config.py.
    """
    if score > config.AI_THRESHOLD:
        return "ai", LABEL_AI
    if score < config.HUMAN_THRESHOLD:
        return "human", LABEL_HUMAN
    return "unsure", LABEL_UNSURE


def label_ranges() -> list[tuple[str, str]]:
    """
    The score range each label covers. Your README needs these beside the
    label text — given to you so the numbers can't drift apart from config.py.
    """
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} – {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]
