# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-15 17:44
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `0426697f-6a99-49e9-aa88-e366c03154db` | unsure | 0.367 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `4795ba0e-8497-4e8a-af6a-34feefdf8dd4` | unsure | 0.456 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `d6bc683a-7df8-4713-a98e-03bd965c6588` | unsure | 0.569 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c9cf9f81-bf5d-4dea-815a-eddad3f6ddd9` | unsure | 0.585 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `85e25cc4-7495-46e1-b325-d706dfe88e50` | unsure | 0.363 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `58ea8125-e22c-416a-b844-fe037f0b4aa1` | unsure | 0.466 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `36d0edc5-a590-4d91-b4eb-374f1f18a24b` | unsure | 0.585 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `f128b8f2-5a55-4787-9db1-685e03bf3de7` | human | 0.342 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `eb7d26fb-0fa0-4cf9-b3be-ceba24bdb81a` | unsure | 0.588 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `6cdaaf5f-d1b8-4fcc-8d41-b7b2e35abb3b` | ai | 0.858 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `89893298-f870-4028-9e8d-3da251cc5d1c` | unsure | 0.582 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `56d3a778-4875-401f-b5f5-4f8218489e8e` | ai | 0.676 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `9626affc-55b3-4e2f-b371-85b22b955ceb` | ai | 0.699 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `ca92d8c9-eb3a-4a46-950d-eb80d2dc3b22` | ai | 0.676 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `5e0757a5-7444-4783-9066-20c225b649c4` | ai | 0.714 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `c780f8e2-7a92-46c1-af44-b18aad3860af` | ai | 0.695 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `12a95d14-d063-44f9-a723-470e1d12fe69` | ai | 0.692 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `06aad5da-ba91-4ee7-95f8-8a4dd635b6fc` | human | 0.297 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `44f2e6a0-b970-4022-b19a-d13842085694` | unsure | 0.428 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `d2c3cb5c-c612-4ef3-b63b-92996cbde6cf` | human | 0.275 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `81382d86-7840-4229-97c8-592edc404659` | unsure | 0.558 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `2733dbfe-ad58-41a0-914a-f33191b81e59` | unsure | 0.507 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `2e363450-475a-4076-9a93-4764ba3b8ea2` | unsure | 0.480 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `ca1659f9-5e17-4d45-81c2-143b6b9c0a50` | unsure | 0.554 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `b8201191-5de3-4595-b946-9dbd63e428ad` | human | 0.333 |  |
| MF04 | malformed | text is only punctuation | 200 | `6ff20b73-1b09-4a49-9c1a-c265c1c626af` | human | 0.256 |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 200 | `6d6624f5-258e-482e-8f0d-ed3b6e96bf64` | ai | 0.703 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `5018f5f2-5d37-497b-be6a-192b356c8ba7` | ai | 0.889 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `cac1e239-a0a1-4d77-adad-0550661394a1` | unsure | 0.423 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `55ae623f-56f9-46a6-beb4-6da521528cc3` | human | 0.247 |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a9a52338-3141-4db3-9923-fee25c9c0848` | human | 0.311 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9d161c55-c6dd-45e5-ba6a-138d679be7ea` | human | 0.311 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a5ffafb6-61d1-4ded-93b6-f454b4456053` | human | 0.311 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a0366389-f11c-48a2-b612-6bc5d5f8727b` | human | 0.311 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `24f8f01d-f347-4873-8701-e9a3196f373c` | human | 0.311 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `955344c7-1368-4f69-ae43-7f9bb97caa7d` | human | 0.311 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a80811cd-e8c1-4c11-bbab-1aae86c9b6d3` | human | 0.311 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0ec5952d-f1b7-4052-a2b4-e132ef42a8d8` | human | 0.311 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1b966f06-b885-4066-af36-be249850ded9` | human | 0.311 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `52e6a770-d88a-45b6-92e1-d78e90394cc6` | human | 0.311 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "0426697f-6a99-49e9-aa88-e366c03154db",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.3667252921151383,
  "model_score": 0.1635,
  "style_score": 0.5699505842302767,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "4795ba0e-8497-4e8a-af6a-34feefdf8dd4",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.45598809004783203,
  "model_score": 0.5943,
  "style_score": 0.31767618009566406,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "d6bc683a-7df8-4713-a98e-03bd965c6588",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5689524020561879,
  "model_score": 0.6662,
  "style_score": 0.47170480411237586,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "c9cf9f81-bf5d-4dea-815a-eddad3f6ddd9",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5848344388622175,
  "model_score": 0.6114,
  "style_score": 0.558268877724435,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "85e25cc4-7495-46e1-b325-d706dfe88e50",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.3630970065048201,
  "model_score": 0.3212,
  "style_score": 0.40499401300964016,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "58ea8125-e22c-416a-b844-fe037f0b4aa1",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.46569782608695653,
  "model_score": 0.5727,
  "style_score": 0.3586956521739131,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "36d0edc5-a590-4d91-b4eb-374f1f18a24b",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5851962199312715,
  "model_score": 0.5862,
  "style_score": 0.584192439862543,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "f128b8f2-5a55-4787-9db1-685e03bf3de7",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3421262145875635,
  "model_score": 0.2452,
  "style_score": 0.439052429175127,
  "label": "This text shows patterns consistent with human writing, although the system cannot verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "eb7d26fb-0fa0-4cf9-b3be-ceba24bdb81a",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5879910935795517,
  "model_score": 0.7042,
  "style_score": 0.4717821871591033,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "6cdaaf5f-d1b8-4fcc-8d41-b7b2e35abb3b",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8577098654028323,
  "model_score": 0.9792,
  "style_score": 0.7362197308056647,
  "label": "This text shows patterns associated with AI-generated writing, but this result does not prove AI authorship.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "89893298-f870-4028-9e8d-3da251cc5d1c",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5820138519168392,
  "model_score": 0.6175,
  "style_score": 0.5465277038336782,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "56d3a778-4875-401f-b5f5-4f8218489e8e",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.675783015325087,
  "model_score": 0.7387,
  "style_score": 0.612866030650174,
  "label": "This text shows patterns associated with AI-generated writing, but this result does not prove AI authorship.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "9626affc-55b3-4e2f-b371-85b22b955ceb",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.6992574760165613,
  "model_score": 0.8051,
  "style_score": 0.5934149520331226,
  "label": "This text shows patterns associated with AI-generated writing, but this result does not prove AI authorship.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "ca92d8c9-eb3a-4a46-950d-eb80d2dc3b22",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.676415198237335,
  "model_score": 0.8329,
  "style_score": 0.5199303964746699,
  "label": "This text shows patterns associated with AI-generated writing, but this result does not prove AI authorship.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "5e0757a5-7444-4783-9066-20c225b649c4",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7136258991742646,
  "model_score": 0.8005,
  "style_score": 0.6267517983485292,
  "label": "This text shows patterns associated with AI-generated writing, but this result does not prove AI authorship.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "c780f8e2-7a92-46c1-af44-b18aad3860af",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.6953185014279366,
  "model_score": 0.8814,
  "style_score": 0.5092370028558734,
  "label": "This text shows patterns associated with AI-generated writing, but this result does not prove AI authorship.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "12a95d14-d063-44f9-a723-470e1d12fe69",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.6918625631589213,
  "model_score": 0.8816,
  "style_score": 0.5021251263178426,
  "label": "This text shows patterns associated with AI-generated writing, but this result does not prove AI authorship.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "06aad5da-ba91-4ee7-95f8-8a4dd635b6fc",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.2973145496846301,
  "model_score": 0.3223,
  "style_score": 0.27232909936926025,
  "label": "This text shows patterns consistent with human writing, although the system cannot verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "44f2e6a0-b970-4022-b19a-d13842085694",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.42821497505372585,
  "model_score": 0.4625,
  "style_score": 0.39392995010745163,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "d2c3cb5c-c612-4ef3-b63b-92996cbde6cf",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.27504231204521196,
  "model_score": 0.2044,
  "style_score": 0.34568462409042394,
  "label": "This text shows patterns consistent with human writing, although the system cannot verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "81382d86-7840-4229-97c8-592edc404659",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5581561749572328,
  "model_score": 0.5943,
  "style_score": 0.5220123499144654,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "2733dbfe-ad58-41a0-914a-f33191b81e59",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5073118043333615,
  "model_score": 0.4998,
  "style_score": 0.5148236086667232,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "2e363450-475a-4076-9a93-4764ba3b8ea2",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4803714687570503,
  "model_score": 0.6401,
  "style_score": 0.32064293751410056,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "ca1659f9-5e17-4d45-81c2-143b6b9c0a50",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5544687533824668,
  "model_score": 0.5583,
  "style_score": 0.5506375067649335,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "b8201191-5de3-4595-b946-9dbd63e428ad",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.3333333333333333,
  "model_score": 0.0,
  "style_score": 0.6666666666666666,
  "label": "This text shows patterns consistent with human writing, although the system cannot verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "6ff20b73-1b09-4a49-9c1a-c265c1c626af",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.2556,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "This text shows patterns consistent with human writing, although the system cannot verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "6d6624f5-258e-482e-8f0d-ed3b6e96bf64",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.7032,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "This text shows patterns associated with AI-generated writing, but this result does not prove AI authorship.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "5018f5f2-5d37-497b-be6a-192b356c8ba7",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.8889971252981523,
  "model_score": 0.9876,
  "style_score": 0.7903942505963047,
  "label": "This text shows patterns associated with AI-generated writing, but this result does not prove AI authorship.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "cac1e239-a0a1-4d77-adad-0550661394a1",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.422780303030303,
  "model_score": 0.2395,
  "style_score": 0.6060606060606061,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "55ae623f-56f9-46a6-beb4-6da521528cc3",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.24682222222222225,
  "model_score": 0.0492,
  "style_score": 0.4444444444444445,
  "label": "This text shows patterns consistent with human writing, although the system cannot verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "a9a52338-3141-4db3-9923-fee25c9c0848",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.31064629629629625,
  "model_score": 0.0287,
  "style_score": 0.5925925925925926,
  "label": "This text shows patterns consistent with human writing, although the system cannot verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "9d161c55-c6dd-45e5-ba6a-138d679be7ea",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.31064629629629625,
  "model_score": 0.0287,
  "style_score": 0.5925925925925926,
  "label": "This text shows patterns consistent with human writing, although the system cannot verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "a5ffafb6-61d1-4ded-93b6-f454b4456053",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.31064629629629625,
  "model_score": 0.0287,
  "style_score": 0.5925925925925926,
  "label": "This text shows patterns consistent with human writing, although the system cannot verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "a0366389-f11c-48a2-b612-6bc5d5f8727b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.31064629629629625,
  "model_score": 0.0287,
  "style_score": 0.5925925925925926,
  "label": "This text shows patterns consistent with human writing, although the system cannot verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "24f8f01d-f347-4873-8701-e9a3196f373c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.31064629629629625,
  "model_score": 0.0287,
  "style_score": 0.5925925925925926,
  "label": "This text shows patterns consistent with human writing, although the system cannot verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "955344c7-1368-4f69-ae43-7f9bb97caa7d",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.31064629629629625,
  "model_score": 0.0287,
  "style_score": 0.5925925925925926,
  "label": "This text shows patterns consistent with human writing, although the system cannot verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "a80811cd-e8c1-4c11-bbab-1aae86c9b6d3",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.31064629629629625,
  "model_score": 0.0287,
  "style_score": 0.5925925925925926,
  "label": "This text shows patterns consistent with human writing, although the system cannot verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "0ec5952d-f1b7-4052-a2b4-e132ef42a8d8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.31064629629629625,
  "model_score": 0.0287,
  "style_score": 0.5925925925925926,
  "label": "This text shows patterns consistent with human writing, although the system cannot verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "1b966f06-b885-4066-af36-be249850ded9",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.31064629629629625,
  "model_score": 0.0287,
  "style_score": 0.5925925925925926,
  "label": "This text shows patterns consistent with human writing, although the system cannot verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "52e6a770-d88a-45b6-92e1-d78e90394cc6",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.31064629629629625,
  "model_score": 0.0287,
  "style_score": 0.5925925925925926,
  "label": "This text shows patterns consistent with human writing, although the system cannot verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
