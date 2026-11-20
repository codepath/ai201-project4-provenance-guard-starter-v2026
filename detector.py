"""
Signal one: the model signal.

This is the signal that "reads the text for meaning". It runs a language model
on your own machine and asks one question: **how predictable is this text?**

The idea is the one every AI-detection product is built on. A language model
writes by repeatedly picking a likely next word, so text a model produced tends
to be text a model finds easy to predict. Human writing wanders more — odd word
choices, abrupt turns, the specific rather than the typical.

The measure is called **perplexity**. Low perplexity means "I could have
guessed this"; high perplexity means "that surprised me". This module turns
that into a 0–1 score where **higher means more likely AI**.

    from detector import model_signal
    score = model_signal("some text")     # 0.0 human-ish … 1.0 AI-ish

Everything runs locally. No account, no key, no card.

⚠️ **The blind spot, which you have to name in Milestone 1.**

Predictability is not the same thing as authorship. What this signal actually
rewards is **common words in short, ordinary sentences** — and plenty of real
people write that way.

Someone writing in a second language, sticking to vocabulary they're sure of.
A younger writer. Anyone writing plainly on purpose. Measured against gpt2,
writing like that scores about as machine-like as machine writing does.

The reverse trips people up too: dense, ornate prose full of rare words often
scores as *human* on this signal, because rare words are exactly what a
language model fails to predict. Formality on its own doesn't decide it.

So the writers this signal is most likely to accuse are the ones with the
least room to argue back. That is structural rather than a bug you can fix,
and it is the person Milestone 1 asks you to follow through your service.

Don't take that on trust — it's a claim you can check. Milestone 4 has you run
four calibration inputs. Add a plainly-written human paragraph to them and see
for yourself where it lands.
"""

import math

import config

_model = None
_tokenizer = None


class DetectorUnavailable(RuntimeError):
    """The model couldn't be loaded — no download yet, or no disk."""


def _load():
    """Load the model once and keep it. First call downloads ~550 MB."""
    global _model, _tokenizer
    if _model is not None:
        return _model, _tokenizer

    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:
        raise DetectorUnavailable(
            f"transformers or torch isn't installed ({exc}).\n"
            f"Run: pip install -r requirements.txt"
        ) from exc

    if config.TORCH_THREADS > 0:
        torch.set_num_threads(config.TORCH_THREADS)

    try:
        _tokenizer = AutoTokenizer.from_pretrained(config.DETECTOR_MODEL)
        _model = AutoModelForCausalLM.from_pretrained(config.DETECTOR_MODEL)
        _model.eval()
    except Exception as exc:  # noqa: BLE001
        raise DetectorUnavailable(
            f"Couldn't load '{config.DETECTOR_MODEL}': {exc}\n"
            f"The first run downloads about 550 MB — check your connection and "
            f"that you have disk space free."
        ) from exc

    return _model, _tokenizer


def perplexity(text: str) -> float:
    """
    How surprised the model is by this text. Lower means more predictable.

    Returns a positive number. Typical values land roughly between 10 and 200,
    but that range shifts with topic and length, which is one reason the raw
    number isn't what you score on.
    """
    import torch

    model, tokenizer = _load()

    encoded = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=config.DETECTOR_MAX_TOKENS,
    )
    input_ids = encoded["input_ids"]

    # Two tokens is not enough to be surprised by anything.
    if input_ids.shape[1] < 3:
        raise ValueError("Text is too short to score — a few sentences at least.")

    with torch.no_grad():
        output = model(input_ids, labels=input_ids)

    # The model's loss here IS mean negative log-likelihood per token.
    return float(math.exp(output.loss.item()))


TRIM_FRACTION = 0.10   # drop this share of the highest-loss tokens before averaging


def robust_perplexity(text: str) -> float:
    """
    Perplexity with the most surprising 10% of tokens thrown away.

    Plain perplexity is the mean surprise per token, so a few typo-broken
    words (each shattered into rare sub-word pieces the model has never seen
    together) drag the whole mean up and make machine text look human. A
    trimmed mean ignores those few outliers. Added in unit 8 after the typo
    attacks (EV01, EV04) took a 0.85 model score down to 0.42.
    """
    import torch

    model, tokenizer = _load()
    ids = tokenizer(text, return_tensors="pt", truncation=True,
                    max_length=config.DETECTOR_MAX_TOKENS)["input_ids"]
    if ids.shape[1] < 3:
        raise ValueError("Text is too short to score — a few sentences at least.")

    with torch.no_grad():
        logits = model(ids).logits
    losses = torch.nn.functional.cross_entropy(
        logits[0, :-1], ids[0, 1:], reduction="none").tolist()
    losses.sort()
    keep = max(int(len(losses) * (1 - TRIM_FRACTION)), 1)
    return float(math.exp(sum(losses[:keep]) / keep))


def model_signal(text: str) -> float:
    """
    The signal, as a 0–1 score. **Higher means more likely AI.**

    Trimmed perplexity is squashed onto 0–1 with a logistic. The midpoint is the
    trimmed perplexity that maps to 0.5. Trimming lowers every perplexity by
    roughly half, so the midpoint moved from 45 (plain perplexity) to 22 to keep
    ordinary text scoring about where it did before.
    """
    ppl = robust_perplexity(text)

    midpoint = 22.0    # trimmed perplexity that scores 0.5
    steepness = 1.6    # how sharply the score moves either side of it

    # Logistic on log-perplexity. Low perplexity -> high AI score.
    score = 1.0 / (1.0 + (ppl / midpoint) ** steepness)
    return round(min(max(score, 0.0), 1.0), 4)


def warm_up() -> str:
    """Load the model and run one throwaway score, so the first real request
    doesn't pay for the model's first forward pass (about 2.5 s and ~570 MB)."""
    _load()
    try:
        model_signal("The quick brown fox jumps over the lazy dog near the old river bank today.")
    except Exception:
        pass  # warming up must never stop the service starting
    return f"{config.DETECTOR_MODEL} loaded and ready."


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = (
            "The implementation of the proposed framework requires careful "
            "consideration of several key factors. First, it is important to "
            "note that the system must be able to handle a wide variety of "
            "different inputs. Additionally, the overall performance of the "
            "solution depends on a number of important variables."
        )
        print("(no text given — scoring a sample)\n")

    print(f"Loading {config.DETECTOR_MODEL} (first run downloads ~550 MB)…")
    print(f"perplexity     {perplexity(text):.1f}")
    print(f"model_signal   {model_signal(text):.4f}   (higher = more likely AI)")
