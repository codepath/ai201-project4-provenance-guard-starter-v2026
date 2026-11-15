"""Surface statistics: deliberately independent of the language model."""
import re
import statistics
import unicodedata

def sentences(text: str) -> list[str]:
    return [part for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]

def words(text: str) -> list[str]:
    return re.findall(r"[^\W_]+(?:['?][^\W_]+)*", text.lower(), flags=re.UNICODE)

def sentence_length_spread(text: str) -> float:
    lengths = [len(words(s)) for s in sentences(text)]
    if len(lengths) < 2 or not sum(lengths):
        return 0.0
    return statistics.pstdev(lengths) / statistics.mean(lengths)

def type_token_ratio(text: str) -> float:
    tokens = words(text)
    return len(set(tokens)) / len(tokens) if tokens else 0.0

def punctuation_density(text: str) -> float:
    return sum(unicodedata.category(c).startswith("P") for c in text) / len(text) if text else 0.0

def style_signal(text: str) -> float:
    if len(sentences(text)) < 3 or len(words(text)) < 20:
        return 0.5
    regularity = 1 - min(sentence_length_spread(text), 1.0)
    repetition = 1 - type_token_ratio(text)
    sparse_punctuation = 1 - min(punctuation_density(text) / 0.10, 1.0)
    return round(0.5 * regularity + 0.3 * repetition + 0.2 * sparse_punctuation, 4)

if __name__ == "__main__":
    import sys
    text = " ".join(sys.argv[1:]) or "The system works well. It handles most cases correctly and provides good results. Users generally find it easy to use and understand."
    for function in (sentence_length_spread, type_token_ratio, punctuation_density, style_signal):
        print(f"{function.__name__}: {function(text):.4f}")
