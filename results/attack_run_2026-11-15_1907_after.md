# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-15 19:07
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `eace836f-ea28-4713-9fad-d3d6027cbb38` | unsure | 0.367 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `69c3e7fe-eb50-4d6e-afc1-e08026bd17fe` | unsure | 0.456 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `8d59ca0b-1c99-48f7-86cc-71b6d608043f` | unsure | 0.569 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `66ff3267-253c-4436-98a0-d9d713d3893a` | unsure | 0.585 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `31815d3e-4cca-4e91-b0a5-631764d739c8` | unsure | 0.363 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `2b8c341a-8df7-499c-beff-95a9744de11e` | unsure | 0.466 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `92ee7f53-e55f-470c-81ca-8e4960e91926` | unsure | 0.585 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `67cc6429-9b4c-46f8-87b5-483d66294ef7` | human | 0.342 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `694c8dd0-b6e7-4d18-b657-4f2f4ef6e755` | unsure | 0.588 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `78fa5ad1-370c-4510-9955-51d34382a769` | ai | 0.858 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `e9a109e0-4a12-4e44-bc93-16a2be77f26b` | unsure | 0.582 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `c20475d9-f8f7-4bc7-bf1a-e69a4432d81b` | unsure | 0.676 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `814dc6ae-f7ff-47fd-ad39-955b4e2a3ceb` | unsure | 0.699 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `8cfaa57f-484f-403f-8aab-1eea8c8734ca` | unsure | 0.676 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `70bd4037-135e-42fd-b4b0-cd8047785ab4` | unsure | 0.714 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `51d57b04-a8c8-49fd-8b4a-a6f9f6aad0c3` | unsure | 0.695 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `bd611cc6-c7eb-4544-b9b9-fb5af47044be` | unsure | 0.692 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `8e00edc4-5542-4722-b028-2474e31a2b14` | human | 0.297 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `1bcae39f-c1d0-4115-a996-ce8f58af26c8` | unsure | 0.428 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `e560d9d9-fae9-49de-87fc-94481ba0a0dc` | human | 0.275 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `8b01cd01-6a3b-49dc-9fc3-873ae8ac02b1` | unsure | 0.558 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `f7573fc2-d75d-4c47-91fb-d8235dae44d6` | unsure | 0.507 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `4ad7bcbc-3754-4e63-bd5e-96ab41a48c1d` | unsure | 0.480 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `06980c46-9fa2-485f-b192-59db149e9fb2` | unsure | 0.554 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `575a29e2-0025-4ed9-8f42-c8e069f80203` | human | 0.333 |  |
| MF04 | malformed | text is only punctuation | 200 | `7b9001c1-1115-40ef-a93b-30bb1f4acc05` | human | 0.256 |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 200 | `99b777e7-88f9-402e-b012-49cd201a4cbb` | unsure | 0.703 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `a9be0f4a-5831-4339-a804-0f7c029d3df2` | ai | 0.889 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `4bc0ac61-370f-4c62-877d-49d56a74f8b9` | unsure | 0.423 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `a1f816a2-b33e-46be-87e2-34ba5ec09c18` | human | 0.247 |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d5640619-8422-4924-ad52-5ed26d0fa353` | human | 0.311 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `65aa86fe-d022-4246-bf20-bba9c81e95f3` | human | 0.311 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `607c4e9d-fa8e-4988-baee-fc2ae877e8b7` | human | 0.311 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ad479f8a-49ab-4ff6-8d94-65064dd76984` | human | 0.311 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `dfc8abea-1c79-4482-af02-5e5d116e671a` | human | 0.311 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `be236b91-9e76-444a-9812-7f967e38a784` | human | 0.311 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d10a0e93-9154-474e-92f1-acdd781ba4d0` | human | 0.311 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cf0231fb-ebca-4117-a3c4-0d363c31b4bb` | human | 0.311 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5b317858-8839-4c80-987d-a0160b8146b7` | human | 0.311 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `914b1e8f-5f33-4d43-a597-61ded9cfdbde` | human | 0.311 |  |
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
  "content_id": "eace836f-ea28-4713-9fad-d3d6027cbb38",
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
  "content_id": "69c3e7fe-eb50-4d6e-afc1-e08026bd17fe",
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
  "content_id": "8d59ca0b-1c99-48f7-86cc-71b6d608043f",
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
  "content_id": "66ff3267-253c-4436-98a0-d9d713d3893a",
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
  "content_id": "31815d3e-4cca-4e91-b0a5-631764d739c8",
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
  "content_id": "2b8c341a-8df7-499c-beff-95a9744de11e",
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
  "content_id": "92ee7f53-e55f-470c-81ca-8e4960e91926",
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
  "content_id": "67cc6429-9b4c-46f8-87b5-483d66294ef7",
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
  "content_id": "694c8dd0-b6e7-4d18-b657-4f2f4ef6e755",
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
  "content_id": "78fa5ad1-370c-4510-9955-51d34382a769",
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
  "content_id": "e9a109e0-4a12-4e44-bc93-16a2be77f26b",
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
  "content_id": "c20475d9-f8f7-4bc7-bf1a-e69a4432d81b",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.675783015325087,
  "model_score": 0.7387,
  "style_score": 0.612866030650174,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
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
  "content_id": "814dc6ae-f7ff-47fd-ad39-955b4e2a3ceb",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6992574760165613,
  "model_score": 0.8051,
  "style_score": 0.5934149520331226,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
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
  "content_id": "8cfaa57f-484f-403f-8aab-1eea8c8734ca",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.676415198237335,
  "model_score": 0.8329,
  "style_score": 0.5199303964746699,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
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
  "content_id": "70bd4037-135e-42fd-b4b0-cd8047785ab4",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.7136258991742646,
  "model_score": 0.8005,
  "style_score": 0.6267517983485292,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
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
  "content_id": "51d57b04-a8c8-49fd-8b4a-a6f9f6aad0c3",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6953185014279366,
  "model_score": 0.8814,
  "style_score": 0.5092370028558734,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
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
  "content_id": "bd611cc6-c7eb-4544-b9b9-fb5af47044be",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6918625631589213,
  "model_score": 0.8816,
  "style_score": 0.5021251263178426,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
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
  "content_id": "8e00edc4-5542-4722-b028-2474e31a2b14",
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
  "content_id": "1bcae39f-c1d0-4115-a996-ce8f58af26c8",
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
  "content_id": "e560d9d9-fae9-49de-87fc-94481ba0a0dc",
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
  "content_id": "8b01cd01-6a3b-49dc-9fc3-873ae8ac02b1",
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
  "content_id": "f7573fc2-d75d-4c47-91fb-d8235dae44d6",
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
  "content_id": "4ad7bcbc-3754-4e63-bd5e-96ab41a48c1d",
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
  "content_id": "06980c46-9fa2-485f-b192-59db149e9fb2",
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
  "content_id": "575a29e2-0025-4ed9-8f42-c8e069f80203",
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
  "content_id": "7b9001c1-1115-40ef-a93b-30bb1f4acc05",
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
  "content_id": "99b777e7-88f9-402e-b012-49cd201a4cbb",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.7032,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We cannot reliably determine whether this text was written by a person or generated by AI. No authorship conclusion should be drawn from this result.",
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
  "content_id": "a9be0f4a-5831-4339-a804-0f7c029d3df2",
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
  "content_id": "4bc0ac61-370f-4c62-877d-49d56a74f8b9",
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
  "content_id": "a1f816a2-b33e-46be-87e2-34ba5ec09c18",
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
  "content_id": "d5640619-8422-4924-ad52-5ed26d0fa353",
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
  "content_id": "65aa86fe-d022-4246-bf20-bba9c81e95f3",
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
  "content_id": "607c4e9d-fa8e-4988-baee-fc2ae877e8b7",
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
  "content_id": "ad479f8a-49ab-4ff6-8d94-65064dd76984",
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
  "content_id": "dfc8abea-1c79-4482-af02-5e5d116e671a",
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
  "content_id": "be236b91-9e76-444a-9812-7f967e38a784",
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
  "content_id": "d10a0e93-9154-474e-92f1-acdd781ba4d0",
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
  "content_id": "cf0231fb-ebca-4117-a3c4-0d363c31b4bb",
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
  "content_id": "5b317858-8839-4c80-987d-a0160b8146b7",
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
  "content_id": "914b1e8f-5f33-4d43-a597-61ded9cfdbde",
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
