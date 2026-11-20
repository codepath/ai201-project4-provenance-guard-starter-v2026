# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-19 19:02
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `b229bc7c-5781-4a9c-acfe-7b6968b61cd6` | unsure | 0.400 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `d1484971-e635-41a9-922b-2a89cc94591b` | unsure | 0.400 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `259f1c41-5ab1-4299-98bb-4daf1176f9b4` | unsure | 0.473 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `45ff557e-4633-417e-bc6f-a4c0995dcd03` | unsure | 0.649 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `12d75a53-5606-4229-976a-93e6c2c50630` | human | 0.272 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `3e40dfa9-9a62-47c2-a015-5b460aec07b5` | unsure | 0.454 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `914aacd1-f47b-4e4a-8960-bff5ca2fdb20` | unsure | 0.474 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `aa5c41e4-13bf-4c0a-ad54-cae6f12bde2a` | unsure | 0.401 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `90e678bc-dec6-48ee-b11d-28b6f21aa9d2` | unsure | 0.594 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `72f8f0ae-22aa-43e2-94b5-aaff0a502deb` | ai | 0.875 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `50f61846-c375-4a59-85cb-468ba50051b8` | unsure | 0.545 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `a909b5ad-e8b4-4147-8e09-5d0cc71760c9` | unsure | 0.695 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `6a563f5f-0f08-491e-a741-b6767cd0a7f7` | unsure | 0.666 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `17396db3-dd36-44cb-a4e5-9ce982315fea` | unsure | 0.700 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `529e1def-aa83-41b5-9acc-fcb05e5c4ed3` | unsure | 0.763 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `54121a06-d41c-4596-b0cc-217ca255afdc` | unsure | 0.734 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `05f246d5-2683-4c74-9a30-d2f78903098a` | unsure | 0.724 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `c69e991b-0cff-450c-acb9-a01c93bc89e9` | unsure | 0.460 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `4306976f-59e7-4de9-85f0-8596cf48c5a2` | unsure | 0.397 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c67484c5-9022-475f-8743-c9725bfca5bc` | human | 0.248 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `dcf1b014-f59c-419c-a351-04aaec8fd923` | unsure | 0.476 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `a8f693dc-33e6-469c-a589-42e8245f50f2` | unsure | 0.462 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `4d67506f-a6b6-4dd3-9f07-d8f1342b1b91` | unsure | 0.477 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `7887536d-b25b-4e31-98fe-dcd510c6a248` | unsure | 0.528 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 422 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `935e7036-0c78-405b-9ac1-1d8a240536bf` | unsure | 0.400 |  |
| MF04 | malformed | text is only punctuation | 200 | `80698461-1f61-4cc6-b9ba-9a419272888a` | unsure | 0.400 |  |
| MF05 | malformed | text is a very long single word | 200 | `2566c801-0ee4-4f5c-acfd-1111896e4216` | unsure | 0.600 |  |
| MF06 | malformed | text is emoji only | 200 | `5453f84c-0267-43e0-ac91-7aba5bd75cd7` | unsure | 0.600 |  |
| MF07 | malformed | text is right-to-left script | 200 | `261431e4-7bac-40b5-aae0-d2beeb2a25d1` | unsure | 0.695 |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `3a786e40-334d-4d55-a055-78756a81ebfa` | unsure | 0.482 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `71faf2a1-b09a-4474-afee-96ad4f49e95a` | unsure | 0.400 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `50ee8a84-f56a-4691-a243-9bad959a71af` | unsure | 0.400 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fbd42916-1a78-4b7a-900e-102165adc5eb` | unsure | 0.400 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3f5dacf9-0f44-47dd-bf74-c8ca3bcb7f64` | unsure | 0.400 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `131488d1-eef9-4672-8e13-13aa815eb889` | unsure | 0.400 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d7a51771-b0f5-4ad8-8623-bee8c8380440` | unsure | 0.400 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8b885af7-74a7-48c7-a8e6-9d84a33f6d60` | unsure | 0.400 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `44b9ca05-72e6-45e2-a36c-180eb1c60d6e` | unsure | 0.400 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `130f5259-7303-49ba-8792-dcdefef2179b` | unsure | 0.400 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1c2d715c-c24d-432f-b960-d56752782148` | unsure | 0.400 |  |
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
  "content_id": "b229bc7c-5781-4a9c-acfe-7b6968b61cd6",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.1797,
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
  "content_id": "d1484971-e635-41a9-922b-2a89cc94591b",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.5757,
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
  "content_id": "259f1c41-5ab1-4299-98bb-4daf1176f9b4",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.4732,
  "model_score": 0.6422,
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
  "content_id": "45ff557e-4633-417e-bc6f-a4c0995dcd03",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6486,
  "model_score": 0.6306,
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
  "content_id": "12d75a53-5606-4229-976a-93e6c2c50630",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2724,
  "model_score": 0.2996,
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
  "content_id": "3e40dfa9-9a62-47c2-a015-5b460aec07b5",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4535,
  "model_score": 0.5552,
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
  "content_id": "914aacd1-f47b-4e4a-8960-bff5ca2fdb20",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4741,
  "model_score": 0.6211,
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
  "content_id": "aa5c41e4-13bf-4c0a-ad54-cae6f12bde2a",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.4009,
  "model_score": 0.2695,
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
  "content_id": "90e678bc-dec6-48ee-b11d-28b6f21aa9d2",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5935,
  "model_score": 0.6785,
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
  "content_id": "72f8f0ae-22aa-43e2-94b5-aaff0a502deb",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8747,
  "model_score": 0.9787,
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
  "content_id": "50f61846-c375-4a59-85cb-468ba50051b8",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5451,
  "model_score": 0.5697,
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
  "content_id": "a909b5ad-e8b4-4147-8e09-5d0cc71760c9",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6947,
  "model_score": 0.696,
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
  "content_id": "6a563f5f-0f08-491e-a741-b6767cd0a7f7",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6665,
  "model_score": 0.7175,
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
  "content_id": "17396db3-dd36-44cb-a4e5-9ce982315fea",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.7,
  "model_score": 0.7926,
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
  "content_id": "529e1def-aa83-41b5-9acc-fcb05e5c4ed3",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.7635,
  "model_score": 0.7514,
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
  "content_id": "54121a06-d41c-4596-b0cc-217ca255afdc",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.7344,
  "model_score": 0.8878,
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
  "content_id": "05f246d5-2683-4c74-9a30-d2f78903098a",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.7243,
  "model_score": 0.8738,
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
  "content_id": "c69e991b-0cff-450c-acb9-a01c93bc89e9",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.4599,
  "model_score": 0.4394,
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
  "content_id": "4306976f-59e7-4de9-85f0-8596cf48c5a2",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.3974,
  "model_score": 0.4446,
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
  "content_id": "c67484c5-9022-475f-8743-c9725bfca5bc",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2482,
  "model_score": 0.2814,
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
  "content_id": "dcf1b014-f59c-419c-a351-04aaec8fd923",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4758,
  "model_score": 0.5776,
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
  "content_id": "a8f693dc-33e6-469c-a589-42e8245f50f2",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4619,
  "model_score": 0.5075,
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
  "content_id": "4d67506f-a6b6-4dd3-9f07-d8f1342b1b91",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.477,
  "model_score": 0.6862,
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
  "content_id": "7887536d-b25b-4e31-98fe-dcd510c6a248",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5278,
  "model_score": 0.5384,
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
  "content_id": "935e7036-0c78-405b-9ac1-1d8a240536bf",
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
  "content_id": "80698461-1f61-4cc6-b9ba-9a419272888a",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0068,
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
  "content_id": "2566c801-0ee4-4f5c-acfd-1111896e4216",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.9929,
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
  "content_id": "5453f84c-0267-43e0-ac91-7aba5bd75cd7",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.9929,
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
  "content_id": "261431e4-7bac-40b5-aae0-d2beeb2a25d1",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.6949,
  "model_score": 0.8248,
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
  "content_id": "3a786e40-334d-4d55-a055-78756a81ebfa",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.4817,
  "model_score": 0.4362,
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
  "content_id": "71faf2a1-b09a-4474-afee-96ad4f49e95a",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0194,
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
  "content_id": "50ee8a84-f56a-4691-a243-9bad959a71af",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0194,
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
  "content_id": "fbd42916-1a78-4b7a-900e-102165adc5eb",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0194,
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
  "content_id": "3f5dacf9-0f44-47dd-bf74-c8ca3bcb7f64",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0194,
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
  "content_id": "131488d1-eef9-4672-8e13-13aa815eb889",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0194,
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
  "content_id": "d7a51771-b0f5-4ad8-8623-bee8c8380440",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0194,
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
  "content_id": "8b885af7-74a7-48c7-a8e6-9d84a33f6d60",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0194,
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
  "content_id": "44b9ca05-72e6-45e2-a36c-180eb1c60d6e",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0194,
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
  "content_id": "130f5259-7303-49ba-8792-dcdefef2179b",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0194,
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
  "content_id": "1c2d715c-c24d-432f-b960-d56752782148",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.0194,
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
