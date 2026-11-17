# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 51 attacks · 2026-11-16 19:11
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **51**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion_typos | style signal: typos raise vocabulary variety | 200 | `65f4d0fa-50b3-4387-a46e-5572f90b4b27` | unsure | 0.643 |  |
| EV02 | evasion_typos | style signal: typos raise vocabulary variety | 200 | `548161f4-5fa6-4aaa-b78e-21b1b1f9d413` | ai | 0.806 |  |
| EV03 | evasion_typos | style signal: typos raise vocabulary variety | 200 | `9604a56a-417b-4cf1-9102-017f6462d2a8` | unsure | 0.784 |  |
| EV04 | evasion_typos | style signal: typos raise vocabulary variety | 200 | `8848de48-5a5c-49ea-b77c-1129dd6ea732` | unsure | 0.685 |  |
| EV05 | evasion_typos | style signal: typos raise vocabulary variety | 200 | `534c117b-c36f-4298-8e42-5e847ad0dac1` | unsure | 0.676 |  |
| SP01 | evasion_split | style signal: uneven sentence lengths | 200 | `cce77f91-2f5a-4e3a-92a4-ffc53fd66991` | unsure | 0.640 |  |
| SP02 | evasion_split | style signal: uneven sentence lengths | 200 | `1d81d029-9eec-4f0b-9ce4-d784307e9ce0` | unsure | 0.600 |  |
| SP03 | evasion_split | style signal: uneven sentence lengths | 200 | `7e786c22-5f7a-46ff-aa7c-8c9574f66ea1` | unsure | 0.613 |  |
| PU01 | evasion_punctuation | style signal: rare punctuation | 200 | `12d85637-bc76-4a2a-9283-aa0b161e5db3` | unsure | 0.436 |  |
| PU02 | evasion_punctuation | style signal: rare punctuation | 200 | `d000eafa-8a9b-41de-80eb-ab70d68d1b69` | unsure | 0.587 |  |
| PU03 | evasion_punctuation | style signal: rare punctuation | 200 | `c372c72a-e3e6-40e8-9389-e75f44972989` | unsure | 0.444 |  |
| QU01 | evasion_quote | style signal: pasted quotation changes shape | 200 | `8bd32438-c178-4228-b161-3dc6a1978fe4` | unsure | 0.600 |  |
| QU02 | evasion_quote | style signal: pasted quotation changes shape | 200 | `195e68c2-dbae-445c-856d-80ca08eaa25c` | unsure | 0.600 |  |
| HP01 | evasion_human_prefix | both signals: genuine human sentences ahead of AI text | 200 | `7d50e9cc-d2ca-41a1-8662-edf515cf6624` | unsure | 0.441 |  |
| HP02 | evasion_human_prefix | both signals: genuine human sentences ahead of AI text | 200 | `30381552-e5e3-43e1-adad-ad86ce4a7f48` | unsure | 0.541 |  |
| FP01 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 | `461c348f-ba45-4060-a414-c90464bdbee8` | unsure | 0.733 |  |
| FP02 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 | `211bec4d-a1d5-4eed-8aa4-20d9726d4787` | unsure | 0.744 |  |
| FP03 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 | `3a96a30f-0a71-4465-88dc-3b4879a389fe` | unsure | 0.662 |  |
| FP04 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 | `df8168c7-131a-4c3b-bfa5-114adaa5e982` | ai | 0.807 |  |
| FP05 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 | `e85b0850-ed66-4cc6-af8b-751c56e55453` | ai | 0.843 |  |
| SH01 | short_input | too short to score | 200 | `f5662dcb-673a-496d-8a7d-67b739b0c872` | unsure | 0.729 |  |
| SH02 | short_input | one sentence, spread undefined | 200 | `6150b63a-3313-4eb6-a042-29bcfdeb5645` | unsure | 0.534 |  |
| OD01 | odd_input | non-English text | 200 | `7ede7686-fc79-4b4d-9ae9-192fca17893c` | unsure | 0.414 |  |
| OD02 | odd_input | repeated word | 200 | `bff5d5bb-b1f2-41b1-8e0d-0bdffd4783fe` | ai | 0.878 |  |
| OD03 | odd_input | emoji and symbols | 200 | `1eedd885-41db-47b7-8dd0-6b99aaa9eb73` | unsure | 0.525 |  |
| MR01 | malformed_request | missing text | 400 | `—` | — | — |  |
| MR02 | malformed_request | empty text | 400 | `—` | — | — |  |
| MR03 | malformed_request | null text | 400 | `—` | — | — |  |
| MR04 | malformed_request | number as text | 400 | `—` | — | — |  |
| MR05 | malformed_request | list as text | 400 | `—` | — | — |  |
| MR06 | malformed_request | bare list body | 400 | `—` | — | — |  |
| MR07 | malformed_request | bare string body | 400 | `—` | — | — |  |
| MR08 | malformed_request | invalid JSON | 400 | `—` | — | — |  |
| MR09 | malformed_request | empty body | 400 | `—` | — | — |  |
| MR10 | malformed_request | wrong content type | 400 | `—` | — | — |  |
| MR11 | malformed_request | huge text (60k chars) | 413 | `—` | — | — |  |
| MR12 | malformed_request | creator_id is an object | 400 | `—` | — | — |  |
| MR13 | malformed_request | missing creator_id | 200 | `b5bcf17f-a3b7-4e85-bfcd-a0f19d67a361` | unsure | 0.777 |  |
| MR14 | malformed_request | invalid UTF-8 bytes | 400 | `—` | — | — |  |
| FL01 | flood_same_creator | rate limit: same creator_id every time | 200 | `edc62bc0-5eda-443c-aa36-5ca095ec021c` | ai | 0.828 |  |
| FL02 | flood_same_creator | rate limit: same creator_id every time | 200 | `982cb123-60ec-4346-9ba0-994882225ea4` | ai | 0.828 |  |
| FL03 | flood_same_creator | rate limit: same creator_id every time | 200 | `12c78487-3760-43c2-bb42-fb4a9a616e87` | ai | 0.828 |  |
| FL04 | flood_same_creator | rate limit: same creator_id every time | 200 | `8f2195db-c856-4f60-bf9d-5619bc3f0e1f` | ai | 0.828 |  |
| FL05 | flood_same_creator | rate limit: same creator_id every time | 200 | `51af43ab-7a37-4a58-9261-f5db0f88b047` | ai | 0.828 |  |
| FL06 | flood_same_creator | rate limit: same creator_id every time | 200 | `c668ad5e-7d32-408f-8353-16186f9c46d5` | ai | 0.828 |  |
| FL07 | flood_same_creator | rate limit: same creator_id every time | 200 | `227cd2fa-ec0e-4890-baee-1a1c50ca938e` | ai | 0.828 |  |
| FL08 | flood_same_creator | rate limit: same creator_id every time | 200 | `a6b20270-8631-4f27-9b08-d2c325778c8a` | ai | 0.828 |  |
| FL09 | flood_same_creator | rate limit: same creator_id every time | 200 | `e84e0b4e-7212-441a-beb3-dab46761097f` | ai | 0.828 |  |
| FL10 | flood_same_creator | rate limit: same creator_id every time | 200 | `ff7e67a4-02ea-40da-962c-37ca69d06f57` | ai | 0.828 |  |
| FL11 | flood_same_creator | rate limit: same creator_id every time | 429 | `—` | — | — |  |
| FL12 | flood_same_creator | rate limit: same creator_id every time | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion_human_prefix` | 2 | 0 | 2 |
| `evasion_punctuation` | 3 | 0 | 3 |
| `evasion_quote` | 2 | 0 | 2 |
| `evasion_split` | 3 | 0 | 3 |
| `evasion_typos` | 5 | 0 | 5 |
| `false_positive_plain` | 5 | 0 | 5 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed_request` | 14 | 0 | 14 |
| `odd_input` | 3 | 0 | 3 |
| `short_input` | 2 | 0 | 2 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion_typos`

*Targeting:* style signal: typos raise vocabulary variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "65f4d0fa-50b3-4387-a46e-5572f90b4b27",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.6426,
  "model_score": 0.6195,
  "style_score": 0.6773,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion_typos`

*Targeting:* style signal: typos raise vocabulary variety

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "548161f4-5fa6-4aaa-b78e-21b1b1f9d413",
  "creator_id": "attacker_EV02",
  "guess": "ai",
  "confidence": 0.8064,
  "model_score": 0.8882,
  "style_score": 0.6837,
  "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion_typos`

*Targeting:* style signal: typos raise vocabulary variety

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "9604a56a-417b-4cf1-9102-017f6462d2a8",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.7837,
  "model_score": 0.8055,
  "style_score": 0.7511,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion_typos`

*Targeting:* style signal: typos raise vocabulary variety

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "8848de48-5a5c-49ea-b77c-1129dd6ea732",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6855,
  "model_score": 0.6543,
  "style_score": 0.7324,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion_typos`

*Targeting:* style signal: typos raise vocabulary variety

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "534c117b-c36f-4298-8e42-5e847ad0dac1",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.6762,
  "model_score": 0.7272,
  "style_score": 0.5996,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### SP01 — `evasion_split`

*Targeting:* style signal: uneven sentence lengths

```json
{
  "id": "SP01",
  "status": 200,
  "content_id": "cce77f91-2f5a-4e3a-92a4-ffc53fd66991",
  "creator_id": "attacker_SP01",
  "guess": "unsure",
  "confidence": 0.6404,
  "model_score": 0.7888,
  "style_score": 0.4177,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### SP02 — `evasion_split`

*Targeting:* style signal: uneven sentence lengths

```json
{
  "id": "SP02",
  "status": 200,
  "content_id": "1d81d029-9eec-4f0b-9ce4-d784307e9ce0",
  "creator_id": "attacker_SP02",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.8576,
  "style_score": 0.4002,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### SP03 — `evasion_split`

*Targeting:* style signal: uneven sentence lengths

```json
{
  "id": "SP03",
  "status": 200,
  "content_id": "7e786c22-5f7a-46ff-aa7c-8c9574f66ea1",
  "creator_id": "attacker_SP03",
  "guess": "unsure",
  "confidence": 0.6132,
  "model_score": 0.7472,
  "style_score": 0.4121,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### PU01 — `evasion_punctuation`

*Targeting:* style signal: rare punctuation

```json
{
  "id": "PU01",
  "status": 200,
  "content_id": "12d85637-bc76-4a2a-9283-aa0b161e5db3",
  "creator_id": "attacker_PU01",
  "guess": "unsure",
  "confidence": 0.4362,
  "model_score": 0.6108,
  "style_score": 0.1744,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### PU02 — `evasion_punctuation`

*Targeting:* style signal: rare punctuation

```json
{
  "id": "PU02",
  "status": 200,
  "content_id": "d000eafa-8a9b-41de-80eb-ab70d68d1b69",
  "creator_id": "attacker_PU02",
  "guess": "unsure",
  "confidence": 0.5866,
  "model_score": 0.8407,
  "style_score": 0.2054,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### PU03 — `evasion_punctuation`

*Targeting:* style signal: rare punctuation

```json
{
  "id": "PU03",
  "status": 200,
  "content_id": "c372c72a-e3e6-40e8-9389-e75f44972989",
  "creator_id": "attacker_PU03",
  "guess": "unsure",
  "confidence": 0.4437,
  "model_score": 0.6147,
  "style_score": 0.1873,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### QU01 — `evasion_quote`

*Targeting:* style signal: pasted quotation changes shape

```json
{
  "id": "QU01",
  "status": 200,
  "content_id": "8bd32438-c178-4228-b161-3dc6a1978fe4",
  "creator_id": "attacker_QU01",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.811,
  "style_score": 0.4017,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### QU02 — `evasion_quote`

*Targeting:* style signal: pasted quotation changes shape

```json
{
  "id": "QU02",
  "status": 200,
  "content_id": "195e68c2-dbae-445c-856d-80ca08eaa25c",
  "creator_id": "attacker_QU02",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.9016,
  "style_score": 0.4531,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### HP01 — `evasion_human_prefix`

*Targeting:* both signals: genuine human sentences ahead of AI text

```json
{
  "id": "HP01",
  "status": 200,
  "content_id": "7d50e9cc-d2ca-41a1-8662-edf515cf6624",
  "creator_id": "attacker_HP01",
  "guess": "unsure",
  "confidence": 0.4412,
  "model_score": 0.5224,
  "style_score": 0.3195,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### HP02 — `evasion_human_prefix`

*Targeting:* both signals: genuine human sentences ahead of AI text

```json
{
  "id": "HP02",
  "status": 200,
  "content_id": "30381552-e5e3-43e1-adad-ad86ce4a7f48",
  "creator_id": "attacker_HP02",
  "guess": "unsure",
  "confidence": 0.5409,
  "model_score": 0.6853,
  "style_score": 0.3243,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive_plain`

*Targeting:* plain honest human writing, should NOT be called AI

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "461c348f-ba45-4060-a414-c90464bdbee8",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.7326,
  "model_score": 0.7951,
  "style_score": 0.6389,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive_plain`

*Targeting:* plain honest human writing, should NOT be called AI

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "211bec4d-a1d5-4eed-8aa4-20d9726d4787",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.7444,
  "model_score": 0.835,
  "style_score": 0.6086,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive_plain`

*Targeting:* plain honest human writing, should NOT be called AI

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "3a96a30f-0a71-4465-88dc-3b4879a389fe",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6616,
  "model_score": 0.7281,
  "style_score": 0.5619,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive_plain`

*Targeting:* plain honest human writing, should NOT be called AI

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "df8168c7-131a-4c3b-bfa5-114adaa5e982",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.8073,
  "model_score": 0.8595,
  "style_score": 0.7289,
  "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive_plain`

*Targeting:* plain honest human writing, should NOT be called AI

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "e85b0850-ed66-4cc6-af8b-751c56e55453",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8425,
  "model_score": 0.9009,
  "style_score": 0.755,
  "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### SH01 — `short_input`

*Targeting:* too short to score

```json
{
  "id": "SH01",
  "status": 200,
  "content_id": "f5662dcb-673a-496d-8a7d-67b739b0c872",
  "creator_id": "attacker_SH01",
  "guess": "unsure",
  "confidence": 0.7285,
  "model_score": 0.8475,
  "style_score": 0.55,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### SH02 — `short_input`

*Targeting:* one sentence, spread undefined

```json
{
  "id": "SH02",
  "status": 200,
  "content_id": "6150b63a-3313-4eb6-a042-29bcfdeb5645",
  "creator_id": "attacker_SH02",
  "guess": "unsure",
  "confidence": 0.5343,
  "model_score": 0.5238,
  "style_score": 0.55,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### OD01 — `odd_input`

*Targeting:* non-English text

```json
{
  "id": "OD01",
  "status": 200,
  "content_id": "7ede7686-fc79-4b4d-9ae9-192fca17893c",
  "creator_id": "attacker_OD01",
  "guess": "unsure",
  "confidence": 0.4137,
  "model_score": 0.2597,
  "style_score": 0.6446,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### OD02 — `odd_input`

*Targeting:* repeated word

```json
{
  "id": "OD02",
  "status": 200,
  "content_id": "bff5d5bb-b1f2-41b1-8e0d-0bdffd4783fe",
  "creator_id": "attacker_OD02",
  "guess": "ai",
  "confidence": 0.878,
  "model_score": 0.9634,
  "style_score": 0.75,
  "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### OD03 — `odd_input`

*Targeting:* emoji and symbols

```json
{
  "id": "OD03",
  "status": 200,
  "content_id": "1eedd885-41db-47b7-8dd0-6b99aaa9eb73",
  "creator_id": "attacker_OD03",
  "guess": "unsure",
  "confidence": 0.5255,
  "model_score": 0.8759,
  "style_score": 0.0,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MR01 — `malformed_request`

*Targeting:* missing text

```json
{
  "id": "MR01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MR01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR02 — `malformed_request`

*Targeting:* empty text

```json
{
  "id": "MR02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MR02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR03 — `malformed_request`

*Targeting:* null text

```json
{
  "id": "MR03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MR03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR04 — `malformed_request`

*Targeting:* number as text

```json
{
  "id": "MR04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MR04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR05 — `malformed_request`

*Targeting:* list as text

```json
{
  "id": "MR05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MR05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR06 — `malformed_request`

*Targeting:* bare list body

```json
{
  "id": "MR06",
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

### MR07 — `malformed_request`

*Targeting:* bare string body

```json
{
  "id": "MR07",
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

### MR08 — `malformed_request`

*Targeting:* invalid JSON

```json
{
  "id": "MR08",
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

### MR09 — `malformed_request`

*Targeting:* empty body

```json
{
  "id": "MR09",
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

### MR10 — `malformed_request`

*Targeting:* wrong content type

```json
{
  "id": "MR10",
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

### MR11 — `malformed_request`

*Targeting:* huge text (60k chars)

```json
{
  "id": "MR11",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MR11",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR12 — `malformed_request`

*Targeting:* creator_id is an object

```json
{
  "id": "MR12",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "a": 1
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

### MR13 — `malformed_request`

*Targeting:* missing creator_id

```json
{
  "id": "MR13",
  "status": 200,
  "content_id": "b5bcf17f-a3b7-4e85-bfcd-a0f19d67a361",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.7771,
  "model_score": 0.8437,
  "style_score": 0.6773,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MR14 — `malformed_request`

*Targeting:* invalid UTF-8 bytes

```json
{
  "id": "MR14",
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

### FL01 — `flood_same_creator`

*Targeting:* rate limit: same creator_id every time

```json
{
  "id": "FL01",
  "status": 200,
  "content_id": "edc62bc0-5eda-443c-aa36-5ca095ec021c",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8281,
  "model_score": 0.9244,
  "style_score": 0.6837,
  "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL02 — `flood_same_creator`

*Targeting:* rate limit: same creator_id every time

```json
{
  "id": "FL02",
  "status": 200,
  "content_id": "982cb123-60ec-4346-9ba0-994882225ea4",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8281,
  "model_score": 0.9244,
  "style_score": 0.6837,
  "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL03 — `flood_same_creator`

*Targeting:* rate limit: same creator_id every time

```json
{
  "id": "FL03",
  "status": 200,
  "content_id": "12c78487-3760-43c2-bb42-fb4a9a616e87",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8281,
  "model_score": 0.9244,
  "style_score": 0.6837,
  "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL04 — `flood_same_creator`

*Targeting:* rate limit: same creator_id every time

```json
{
  "id": "FL04",
  "status": 200,
  "content_id": "8f2195db-c856-4f60-bf9d-5619bc3f0e1f",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8281,
  "model_score": 0.9244,
  "style_score": 0.6837,
  "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL05 — `flood_same_creator`

*Targeting:* rate limit: same creator_id every time

```json
{
  "id": "FL05",
  "status": 200,
  "content_id": "51af43ab-7a37-4a58-9261-f5db0f88b047",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8281,
  "model_score": 0.9244,
  "style_score": 0.6837,
  "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL06 — `flood_same_creator`

*Targeting:* rate limit: same creator_id every time

```json
{
  "id": "FL06",
  "status": 200,
  "content_id": "c668ad5e-7d32-408f-8353-16186f9c46d5",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8281,
  "model_score": 0.9244,
  "style_score": 0.6837,
  "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL07 — `flood_same_creator`

*Targeting:* rate limit: same creator_id every time

```json
{
  "id": "FL07",
  "status": 200,
  "content_id": "227cd2fa-ec0e-4890-baee-1a1c50ca938e",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8281,
  "model_score": 0.9244,
  "style_score": 0.6837,
  "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL08 — `flood_same_creator`

*Targeting:* rate limit: same creator_id every time

```json
{
  "id": "FL08",
  "status": 200,
  "content_id": "a6b20270-8631-4f27-9b08-d2c325778c8a",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8281,
  "model_score": 0.9244,
  "style_score": 0.6837,
  "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL09 — `flood_same_creator`

*Targeting:* rate limit: same creator_id every time

```json
{
  "id": "FL09",
  "status": 200,
  "content_id": "e84e0b4e-7212-441a-beb3-dab46761097f",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8281,
  "model_score": 0.9244,
  "style_score": 0.6837,
  "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL10 — `flood_same_creator`

*Targeting:* rate limit: same creator_id every time

```json
{
  "id": "FL10",
  "status": 200,
  "content_id": "ff7e67a4-02ea-40da-962c-37ca69d06f57",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8281,
  "model_score": 0.9244,
  "style_score": 0.6837,
  "label": "This looks like it may have been written with an AI tool. Our checks are not perfect, and we can be wrong. If you wrote this yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL11 — `flood_same_creator`

*Targeting:* rate limit: same creator_id every time

```json
{
  "id": "FL11",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_attacker",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL12 — `flood_same_creator`

*Targeting:* rate limit: same creator_id every time

```json
{
  "id": "FL12",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_attacker",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
