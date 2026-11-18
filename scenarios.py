"""
Unit 8 — Provenance Guard acceptance test scenarios.

Criteria:
1. Zero false positives among ten human-written samples.
2. Mean AI score >= mean human score + 0.50.
3. All three labels must appear.
4. Appeals are tested separately against /appeal and /log.
5. Empty and missing text must return HTTP 400.

Source files:
- human_samples.txt: ten genuinely human-written paragraphs
- ai_samples.txt: three identified AI-generated paragraphs

Separate paragraphs in each file with a blank line.
"""

from pathlib import Path


def load_paragraphs(filename):
    path = Path(__file__).resolve().parent / filename

    if not path.exists():
        return []

    return [
        paragraph.strip()
        for paragraph in path.read_text(encoding="utf-8").split("\n\n")
        if paragraph.strip()
    ]


HUMAN_SAMPLES = load_paragraphs("human_samples.txt")
AI_SAMPLES = load_paragraphs("ai_samples.txt")


SCENARIOS = [
    {
        "name": "human_false_positives",
        "criterion": 1,
        "texts": HUMAN_SAMPLES[:10],
    },
    {
        "name": "human_score_separation",
        "criterion": 2,
        "texts": HUMAN_SAMPLES[:3],
    },
    {
        "name": "ai_score_separation",
        "criterion": 2,
        "texts": AI_SAMPLES[:3],
    },
    {
        "name": "label_coverage",
        "criterion": 3,
        "texts": (
            HUMAN_SAMPLES[:2]
            + AI_SAMPLES[:2]
            + HUMAN_SAMPLES[2:3]
        ),
    },
    {
        "name": "invalid_submissions",
        "criterion": 5,
        "bodies": [
            {"text": "", "creator_id": "eval_empty"},
            {"creator_id": "eval_missing"},
        ],
    },
]


def validate():
    problems = []

    if len(HUMAN_SAMPLES) < 10:
        problems.append(
            "human_samples.txt must contain at least 10 "
            "genuinely human-written paragraphs."
        )

    if len(AI_SAMPLES) < 3:
        problems.append(
            "ai_samples.txt must contain at least 3 "
            "identified AI-generated paragraphs."
        )

    for scenario in SCENARIOS:
        if not scenario.get("texts") and not scenario.get("bodies"):
            problems.append(
                f"Scenario {scenario['name']} has no inputs."
            )

    return problems
