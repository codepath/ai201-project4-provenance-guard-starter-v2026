# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-15 17:46
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `fa661518-9b37-4ba7-b336-438beffac238` | unsure | 0.367 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `b4278312-4c76-4ce0-b740-3aef49d903ff` | unsure | 0.456 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `4495d555-cced-409e-9dae-2801eab00921` | unsure | 0.569 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c6508c62-dc83-4b43-93fe-4d87abfdfe6c` | unsure | 0.585 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `dac98fb1-cd5a-4fdf-8bff-7a4541c899ef` | unsure | 0.363 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `bdf611ba-9d73-463b-a721-7bd1a293af7e` | unsure | 0.466 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `4ec81e0a-f68c-478e-87fc-f4a8b2cc7206` | unsure | 0.585 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `77acda4f-3279-4f40-9b16-8d51b112cbc5` | human | 0.342 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `5920fabd-cb11-4e9e-8a00-4cae1b8104c2` | unsure | 0.588 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `559cbf9c-4876-495d-a9e6-485372ef1db1` | ai | 0.858 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `6aba6183-dbc9-4d30-b664-fd4e22ce53ec` | unsure | 0.582 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `8124dec3-8397-4866-99a9-7a57aefbb01c` | ai | 0.676 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `63f6e579-9a9d-4ccc-ab7e-2f1e8c3c23f3` | ai | 0.699 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `d11934ed-5da3-4f01-8183-66aaf8f0db3d` | ai | 0.676 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `6a3875c9-32aa-4c8b-8a75-6f09ade1fda3` | ai | 0.714 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `237d7ea2-4720-4274-9a01-ad891b0ea111` | ai | 0.695 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c17347b3-21ec-4ec1-9ff5-73f778d7e347` | ai | 0.692 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `9d28a049-9347-4b6e-9eba-1b1f6cbc5b93` | human | 0.297 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `e75d557d-3305-4907-8df4-4e301ac4276e` | unsure | 0.428 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `a8de1bb7-b217-4dfe-9567-69f94a50ddfa` | human | 0.275 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `00582958-4eeb-402e-9a87-752cd64b72d9` | unsure | 0.558 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `ddcfb530-5013-44f8-90bf-f29c2a901ac7` | unsure | 0.507 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `9febc443-37de-433a-b054-c3dcdcd895a2` | unsure | 0.480 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `68f8015d-7766-415c-ab4e-fbc543138ef1` | unsure | 0.554 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `61c38b6a-30e7-4081-9727-3a468ed82c96` | human | 0.333 |  |
| MF04 | malformed | text is only punctuation | 200 | `fd121b58-41a9-4402-8239-6af810f066c0` | human | 0.256 |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 200 | `a5819851-2da2-424f-923d-ba14e55384f4` | ai | 0.703 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `4178a9cc-59e0-4579-8c6d-ecf96df342d0` | ai | 0.889 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `bda24eda-e818-40bc-b569-2f0c63bf6d9d` | unsure | 0.423 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `0abc3ffd-1ea8-4e31-85de-9a07ee5afae5` | human | 0.247 |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a07d97a7-9985-440f-8ca6-c9fd65827213` | human | 0.311 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `200a5682-866a-47f2-9782-7ba2bcb1e6ca` | human | 0.311 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `23d266c2-5795-4072-a036-5ae7a2ee952b` | human | 0.311 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c3b1a385-0ef8-43f0-b70b-6f832588ffd8` | human | 0.311 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7793c057-561e-430a-b491-d26478c11191` | human | 0.311 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6e9bda6f-38ec-4626-b733-8b1746bad307` | human | 0.311 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `19c80a50-58fc-4120-a8bd-7adfea32ed50` | human | 0.311 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8e526e5c-2b51-4748-ac72-a7a95525fb66` | human | 0.311 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8f8ae476-55b9-4224-a91f-76c312ea80d5` | human | 0.311 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b5ce5b53-1c7a-4f0b-a424-e93be7ebfc3f` | human | 0.311 |  |
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
  "content_id": "fa661518-9b37-4ba7-b336-438beffac238",
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
  "content_id": "b4278312-4c76-4ce0-b740-3aef49d903ff",
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
  "content_id": "4495d555-cced-409e-9dae-2801eab00921",
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
  "content_id": "c6508c62-dc83-4b43-93fe-4d87abfdfe6c",
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
  "content_id": "dac98fb1-cd5a-4fdf-8bff-7a4541c899ef",
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
  "content_id": "bdf611ba-9d73-463b-a721-7bd1a293af7e",
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
  "content_id": "4ec81e0a-f68c-478e-87fc-f4a8b2cc7206",
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
  "content_id": "77acda4f-3279-4f40-9b16-8d51b112cbc5",
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
  "content_id": "5920fabd-cb11-4e9e-8a00-4cae1b8104c2",
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
  "content_id": "559cbf9c-4876-495d-a9e6-485372ef1db1",
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
  "content_id": "6aba6183-dbc9-4d30-b664-fd4e22ce53ec",
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
  "content_id": "8124dec3-8397-4866-99a9-7a57aefbb01c",
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
  "content_id": "63f6e579-9a9d-4ccc-ab7e-2f1e8c3c23f3",
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
  "content_id": "d11934ed-5da3-4f01-8183-66aaf8f0db3d",
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
  "content_id": "6a3875c9-32aa-4c8b-8a75-6f09ade1fda3",
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
  "content_id": "237d7ea2-4720-4274-9a01-ad891b0ea111",
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
  "content_id": "c17347b3-21ec-4ec1-9ff5-73f778d7e347",
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
  "content_id": "9d28a049-9347-4b6e-9eba-1b1f6cbc5b93",
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
  "content_id": "e75d557d-3305-4907-8df4-4e301ac4276e",
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
  "content_id": "a8de1bb7-b217-4dfe-9567-69f94a50ddfa",
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
  "content_id": "00582958-4eeb-402e-9a87-752cd64b72d9",
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
  "content_id": "ddcfb530-5013-44f8-90bf-f29c2a901ac7",
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
  "content_id": "9febc443-37de-433a-b054-c3dcdcd895a2",
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
  "content_id": "68f8015d-7766-415c-ab4e-fbc543138ef1",
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
  "content_id": "61c38b6a-30e7-4081-9727-3a468ed82c96",
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
  "content_id": "fd121b58-41a9-4402-8239-6af810f066c0",
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
  "content_id": "a5819851-2da2-424f-923d-ba14e55384f4",
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
  "content_id": "4178a9cc-59e0-4579-8c6d-ecf96df342d0",
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
  "content_id": "bda24eda-e818-40bc-b569-2f0c63bf6d9d",
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
  "content_id": "0abc3ffd-1ea8-4e31-85de-9a07ee5afae5",
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
  "content_id": "a07d97a7-9985-440f-8ca6-c9fd65827213",
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
  "content_id": "200a5682-866a-47f2-9782-7ba2bcb1e6ca",
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
  "content_id": "23d266c2-5795-4072-a036-5ae7a2ee952b",
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
  "content_id": "c3b1a385-0ef8-43f0-b70b-6f832588ffd8",
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
  "content_id": "7793c057-561e-430a-b491-d26478c11191",
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
  "content_id": "6e9bda6f-38ec-4626-b733-8b1746bad307",
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
  "content_id": "19c80a50-58fc-4120-a8bd-7adfea32ed50",
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
  "content_id": "8e526e5c-2b51-4748-ac72-a7a95525fb66",
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
  "content_id": "8f8ae476-55b9-4224-a91f-76c312ea80d5",
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
  "content_id": "b5ce5b53-1c7a-4f0b-a424-e93be7ebfc3f",
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
