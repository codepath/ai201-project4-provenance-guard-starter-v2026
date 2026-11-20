# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-19 19:01
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `82401b3b-e17c-4623-acaa-31b49e5bf572` | unsure | 0.400 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `0be133a4-d339-475a-b99d-0858ae829a7d` | unsure | 0.401 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `89eebd80-08f8-4b49-8b16-3d25f0a3e3fe` | unsure | 0.488 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `69a07efe-94c6-498d-9c1f-c7ba4b84351b` | unsure | 0.637 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `5059c21a-dbdd-4350-b1c6-d8523499aa4e` | human | 0.285 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `6c9739f6-8ce1-4ce1-ba94-5ae39ac90489` | unsure | 0.464 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `8003e7a1-5a4f-445d-8778-a700d0b6e516` | unsure | 0.453 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `b6552f2d-d0ea-446f-a6d5-aa96997aacaa` | unsure | 0.386 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `089bd790-1c33-4157-8691-88c30c79575c` | unsure | 0.609 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `6af325f5-5515-40ab-9841-042faa892029` | ai | 0.875 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `3aaea835-bdef-4511-b5b4-ab540ed2270b` | unsure | 0.574 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `f74bacd3-0489-4857-9d13-23cd95d159b3` | unsure | 0.720 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `3f555a13-0287-4a74-bf44-605f7d07f47d` | unsure | 0.719 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `500df902-5b96-45f8-8e60-7781cc79be19` | unsure | 0.724 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `f90cae09-8355-4aa2-942c-7fa4242812e9` | unsure | 0.793 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `bdc7edf5-aae8-48bf-895f-0779038198a0` | unsure | 0.731 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `9b9803c2-7942-42bd-b4c1-88bda35f53ae` | unsure | 0.729 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `798c1353-b659-49e1-8502-29a44acc92a5` | unsure | 0.390 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `52f2222f-ecf4-4123-a538-47cc743aef5c` | unsure | 0.408 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `8a6a6738-619d-4ddd-b27a-40d89524f8c1` | human | 0.202 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `ddda83d5-be99-4889-bbcd-94a8f184abfd` | unsure | 0.486 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `6dd715b0-3085-4ce6-a4b2-0085d84d3836` | unsure | 0.457 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `e5d26227-de46-4add-936c-a937dbe1ef85` | unsure | 0.449 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `a83b8b41-9c5e-4140-92f2-2fd5affa93c9` | unsure | 0.540 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 422 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `3e9c840f-dc85-4c4e-a571-ff6840deec1e` | unsure | 0.400 |  |
| MF04 | malformed | text is only punctuation | 200 | `50beeb72-8a32-4051-aef3-c7b430729422` | unsure | 0.400 |  |
| MF05 | malformed | text is a very long single word | 200 | `a09c6cba-3936-4232-a5ee-97a23a0d4160` | unsure | 0.600 |  |
| MF06 | malformed | text is emoji only | 200 | `8c789257-fa8c-470c-aa81-3914e450d443` | unsure | 0.600 |  |
| MF07 | malformed | text is right-to-left script | 200 | `0195ea56-cfcc-4e93-b8eb-c6abbef36315` | unsure | 0.600 |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `a4917c92-a86b-444d-b4fc-598d2081c481` | unsure | 0.364 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `09274bdf-6aa4-47b6-a8e8-0bd9a921ac0a` | unsure | 0.400 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1048fbf2-899a-4cc1-bc05-4db685816ee6` | unsure | 0.400 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `30fa68b3-a73b-4ab3-b4b5-2c6754c5c4d7` | unsure | 0.400 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `74da3ffb-1f89-4413-b735-12264be9ccc2` | unsure | 0.400 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `57f55ab5-21a2-482e-946f-e19374dca70c` | unsure | 0.400 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4f2727bb-e747-4cc3-8a16-d4f253990ea9` | unsure | 0.400 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5bc4b417-cc8f-49a8-99d8-515ccbfed279` | unsure | 0.400 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `aa26abdc-116b-45c6-be10-360bb7fae4d6` | unsure | 0.400 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e03f77d3-afb3-4187-a9f8-f7c23fff196e` | unsure | 0.400 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f696ad56-3cc8-45ec-94af-2f38d03132a6` | unsure | 0.400 |  |
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
  "content_id": "82401b3b-e17c-4623-acaa-31b49e5bf572",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.1635,
  "style_score": 0.6852,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "0be133a4-d339-475a-b99d-0858ae829a7d",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4007,
  "model_score": 0.5943,
  "style_score": 0.1102,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "89eebd80-08f8-4b49-8b16-3d25f0a3e3fe",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.4876,
  "model_score": 0.6662,
  "style_score": 0.2196,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "69a07efe-94c6-498d-9c1f-c7ba4b84351b",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6371,
  "model_score": 0.6114,
  "style_score": 0.6757,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "5059c21a-dbdd-4350-b1c6-d8523499aa4e",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2854,
  "model_score": 0.3212,
  "style_score": 0.2317,
  "label": "We think this was probably written by a person. Our checks found nothing that points to automated writing.",
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
  "content_id": "6c9739f6-8ce1-4ce1-ba94-5ae39ac90489",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.464,
  "model_score": 0.5727,
  "style_score": 0.301,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "8003e7a1-5a4f-445d-8778-a700d0b6e516",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4532,
  "model_score": 0.5862,
  "style_score": 0.2537,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "b6552f2d-d0ea-446f-a6d5-aa96997aacaa",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.3863,
  "model_score": 0.2452,
  "style_score": 0.598,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "089bd790-1c33-4157-8691-88c30c79575c",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.609,
  "model_score": 0.7042,
  "style_score": 0.4661,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "6af325f5-5515-40ab-9841-042faa892029",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.875,
  "model_score": 0.9792,
  "style_score": 0.7186,
  "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
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
  "content_id": "3aaea835-bdef-4511-b5b4-ab540ed2270b",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5738,
  "model_score": 0.6175,
  "style_score": 0.5082,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "f74bacd3-0489-4857-9d13-23cd95d159b3",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.7203,
  "model_score": 0.7387,
  "style_score": 0.6927,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "3f555a13-0287-4a74-bf44-605f7d07f47d",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.7191,
  "model_score": 0.8051,
  "style_score": 0.5901,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "500df902-5b96-45f8-8e60-7781cc79be19",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.7242,
  "model_score": 0.8329,
  "style_score": 0.5612,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "f90cae09-8355-4aa2-942c-7fa4242812e9",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.793,
  "model_score": 0.8005,
  "style_score": 0.7817,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "bdc7edf5-aae8-48bf-895f-0779038198a0",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.7306,
  "model_score": 0.8814,
  "style_score": 0.5043,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "9b9803c2-7942-42bd-b4c1-88bda35f53ae",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.729,
  "model_score": 0.8816,
  "style_score": 0.5,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "798c1353-b659-49e1-8502-29a44acc92a5",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.3897,
  "model_score": 0.3223,
  "style_score": 0.4907,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "52f2222f-ecf4-4123-a538-47cc743aef5c",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4081,
  "model_score": 0.4625,
  "style_score": 0.3266,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "8a6a6738-619d-4ddd-b27a-40d89524f8c1",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.202,
  "model_score": 0.2044,
  "style_score": 0.1983,
  "label": "We think this was probably written by a person. Our checks found nothing that points to automated writing.",
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
  "content_id": "ddda83d5-be99-4889-bbcd-94a8f184abfd",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4858,
  "model_score": 0.5943,
  "style_score": 0.3231,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "6dd715b0-3085-4ce6-a4b2-0085d84d3836",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4573,
  "model_score": 0.4998,
  "style_score": 0.3936,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "e5d26227-de46-4add-936c-a937dbe1ef85",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4494,
  "model_score": 0.6401,
  "style_score": 0.1633,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "a83b8b41-9c5e-4140-92f2-2fd5affa93c9",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5397,
  "model_score": 0.5583,
  "style_score": 0.5119,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "status": 422,
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
  "content_id": "3e9c840f-dc85-4c4e-a571-ff6840deec1e",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0,
  "style_score": 0.55,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "50beeb72-8a32-4051-aef3-c7b430729422",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "a09c6cba-3936-4232-a5ee-97a23a0d4160",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.9976,
  "style_score": 0.55,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "8c789257-fa8c-470c-aa81-3914e450d443",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "0195ea56-cfcc-4e93-b8eb-c6abbef36315",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
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
  "content_id": "a4917c92-a86b-444d-b4fc-598d2081c481",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.3637,
  "model_score": 0.2395,
  "style_score": 0.55,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
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
  "content_id": "09274bdf-6aa4-47b6-a8e8-0bd9a921ac0a",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "1048fbf2-899a-4cc1-bc05-4db685816ee6",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "30fa68b3-a73b-4ab3-b4b5-2c6754c5c4d7",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "74da3ffb-1f89-4413-b735-12264be9ccc2",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "57f55ab5-21a2-482e-946f-e19374dca70c",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "4f2727bb-e747-4cc3-8a16-d4f253990ea9",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "5bc4b417-cc8f-49a8-99d8-515ccbfed279",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "aa26abdc-116b-45c6-be10-360bb7fae4d6",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "e03f77d3-afb3-4187-a9f8-f7c23fff196e",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "f696ad56-3cc8-45ec-94af-2f38d03132a6",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
