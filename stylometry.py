"""
Signal two: the style signal.

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures ───────────────────────────────────────────────────────

def _clip01(x: float) -> float:
    return min(max(x, 0.0), 1.0)


def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies: standard deviation of sentence lengths (in
    words) divided by their mean — the coefficient of variation.

    Scale: 0.0 and up. **Higher means more human** (lumpy). Even, marching
    sentences give about 0.1-0.3; human writing with a short sentence beside a
    long one gives 0.5 or more.

    Edge case: fewer than two sentences has no spread to measure, so this
    returns 0.0 and `style_signal` treats that as "no evidence" (neutral), not
    as "very AI". A one-sentence submission must not be accused for being one
    sentence.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    if mean == 0:
        return 0.0
    return round(statistics.stdev(lengths) / mean, 4)


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words, 0-1. **Higher means more varied vocabulary.**

    A raw ratio falls as text gets longer, so this averages the ratio over
    sliding 50-word windows (a moving-average TTR). Texts of different lengths
    are then comparable. Under 50 words it is just the plain ratio.
    """
    ws = words(text)
    if not ws:
        return 0.0
    window = 50
    if len(ws) <= window:
        return round(len(set(ws)) / len(ws), 4)
    ratios = [
        len(set(ws[i:i + window])) / window
        for i in range(0, len(ws) - window + 1)
    ]
    return round(sum(ratios) / len(ratios), 4)


# Punctuation that varies between writers, unlike the full stop. Commas are
# counted separately because nearly everyone uses them.
_RARE_MARKS = [";", ":", "—", "–", " - ", "(", "!", "?", "…", '"', "“"]


def punctuation_density(text: str) -> float:
    """
    How varied and frequent the *uncommon* punctuation is.

    Counts semicolons, colons, dashes, parentheses, exclamation and question
    marks, ellipses and quotes — not full stops or commas — as a rate per 100
    words, plus a bonus for how many different kinds appear.

    Scale: 0.0 and up. **Higher means more human.** Plain generated prose
    leans on commas and full stops only, so it scores near 0.
    """
    n = len(words(text))
    if n == 0:
        return 0.0
    counts = [text.count(m) for m in _RARE_MARKS]
    rate = 100.0 * sum(counts) / n
    kinds = sum(1 for c in counts if c > 0)
    return round(rate + 0.5 * kinds, 4)


# ── Combining them ───────────────────────────────────────────────────────────
# Each measure is flipped to "higher = more AI" and mapped onto 0-1 with the
# anchors below, then the three are averaged with these weights. Spread gets
# the most weight because it is the least dependent on topic; vocabulary
# variety the least because it is so length- and topic-sensitive.

W_SPREAD, W_TTR, W_PUNCT = 0.50, 0.20, 0.30

SPREAD_HUMAN_AT = 0.70   # spread at or above this reads fully human (AI score 0)
TTR_AI_AT, TTR_HUMAN_AT = 0.60, 0.85
PUNCT_HUMAN_AT = 6.0     # density at or above this reads fully human


def style_signal(text: str) -> float:
    """
    The style signal as a 0-1 score. **Higher means more likely AI.**

    Directions: low sentence spread -> AI (flipped); low type-token ratio ->
    AI (flipped); low rare-punctuation density -> AI (flipped). Each measure is
    rescaled onto 0-1 against fixed anchors first, so none wins just by having
    bigger raw numbers.

    Text with fewer than two sentences gives the spread measure nothing to
    work with; its share is replaced by a neutral 0.5 rather than guessed.
    """
    if not words(text):
        return 0.5

    if len(sentences(text)) < 2:
        spread_ai = 0.5
    else:
        spread_ai = 1.0 - _clip01(sentence_length_spread(text) / SPREAD_HUMAN_AT)

    ttr = type_token_ratio(text)
    ttr_ai = 1.0 - _clip01((ttr - TTR_AI_AT) / (TTR_HUMAN_AT - TTR_AI_AT))

    punct_ai = 1.0 - _clip01(punctuation_density(text) / PUNCT_HUMAN_AT)

    score = W_SPREAD * spread_ai + W_TTR * ttr_ai + W_PUNCT * punct_ai
    return round(_clip01(score), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
