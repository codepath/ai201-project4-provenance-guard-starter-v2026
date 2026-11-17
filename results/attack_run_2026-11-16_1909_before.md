# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 51 attacks · 2026-11-16 19:09
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
| EV01 | evasion_typos | style signal: typos raise vocabulary variety | 200 | `9207273c-dd53-4fdf-994c-1e7505fbfe14` | unsure | 0.523 |  |
| EV02 | evasion_typos | style signal: typos raise vocabulary variety | 200 | `df655c55-7779-4704-9283-9eb8d1cd6a72` | unsure | 0.793 |  |
| EV03 | evasion_typos | style signal: typos raise vocabulary variety | 200 | `101c6fef-af4a-4f74-ba8c-b20140ec3253` | unsure | 0.779 |  |
| EV04 | evasion_typos | style signal: typos raise vocabulary variety | 200 | `26c9538d-bb26-4abd-aec0-f697374af340` | unsure | 0.592 |  |
| EV05 | evasion_typos | style signal: typos raise vocabulary variety | 200 | `9795aefc-4a6d-4f74-a0eb-5308b490775d` | unsure | 0.635 |  |
| SP01 | evasion_split | style signal: uneven sentence lengths | 200 | `13f06990-f273-4416-a0e0-0f85f146882f` | unsure | 0.619 |  |
| SP02 | evasion_split | style signal: uneven sentence lengths | 200 | `2c2552a1-b8ea-4bd9-bea3-448547ae9993` | unsure | 0.600 |  |
| SP03 | evasion_split | style signal: uneven sentence lengths | 200 | `14082c6e-35c3-4e37-8179-2f818f6c758c` | unsure | 0.614 |  |
| PU01 | evasion_punctuation | style signal: rare punctuation | 200 | `3f550996-648f-42df-b6b7-d5c550603f97` | unsure | 0.448 |  |
| PU02 | evasion_punctuation | style signal: rare punctuation | 200 | `26e2a233-a64e-4c3f-b428-7a8594e3632e` | unsure | 0.600 |  |
| PU03 | evasion_punctuation | style signal: rare punctuation | 200 | `1583feaa-75a9-4f58-88c2-8e42d788c0dc` | unsure | 0.465 |  |
| QU01 | evasion_quote | style signal: pasted quotation changes shape | 200 | `7cf6ddde-86f2-439c-b527-9deb89de9319` | unsure | 0.600 |  |
| QU02 | evasion_quote | style signal: pasted quotation changes shape | 200 | `f0db6b3f-37cc-4caa-bd43-b2ca6a07ba75` | unsure | 0.600 |  |
| HP01 | evasion_human_prefix | both signals: genuine human sentences ahead of AI text | 200 | `c50541be-2252-42ff-81b3-3b82781264cb` | unsure | 0.442 |  |
| HP02 | evasion_human_prefix | both signals: genuine human sentences ahead of AI text | 200 | `6a617526-cf79-47c8-9f8f-570a2906d552` | unsure | 0.547 |  |
| FP01 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 | `73cc362a-1ddf-45af-b93d-697719b8dd68` | unsure | 0.766 |  |
| FP02 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 | `debaee18-5836-4879-ac34-93f5e5860948` | unsure | 0.759 |  |
| FP03 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 | `b493e3c8-1c65-404f-81af-fd2ee87a04ce` | unsure | 0.675 |  |
| FP04 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 | `e2ffe12a-b3f0-4e89-9d04-6eab44dd6a2e` | ai | 0.815 |  |
| FP05 | false_positive_plain | plain honest human writing, should NOT be called AI | 200 | `8a378b20-7fcc-4bf2-9c77-b28c6d799a1d` | ai | 0.854 |  |
| SH01 | short_input | too short to score | 200 | `409f4231-9f4c-4c2c-aa2e-5f4ee690da07` | unsure | 0.400 |  |
| SH02 | short_input | one sentence, spread undefined | 200 | `acdbad1c-3fb6-43bb-a158-5f0d5449704b` | unsure | 0.567 |  |
| OD01 | odd_input | non-English text | 200 | `d1f9387f-b38c-402c-93ec-4a2bcd1e51a4` | unsure | 0.442 |  |
| OD02 | odd_input | repeated word | 200 | `3492191d-dbfa-45c6-9fe0-4ce1d03d57f1` | ai | 0.877 |  |
| OD03 | odd_input | emoji and symbols | 200 | `e97ed502-4866-41fd-86b6-ab73095407d3` | unsure | 0.526 |  |
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
| MR13 | malformed_request | missing creator_id | 200 | `3ceeae2c-ad81-4dde-b027-52d1043be019` | unsure | 0.782 |  |
| MR14 | malformed_request | invalid UTF-8 bytes | 400 | `—` | — | — |  |
| FL01 | flood_same_creator | rate limit: same creator_id every time | 200 | `55150244-6937-475b-a07c-af53d786c6aa` | ai | 0.843 |  |
| FL02 | flood_same_creator | rate limit: same creator_id every time | 200 | `e3e33a25-7b23-4f4e-8cd5-1231fb193786` | ai | 0.843 |  |
| FL03 | flood_same_creator | rate limit: same creator_id every time | 200 | `5e972453-ae9a-4f4d-b7b7-0aceb22b3db0` | ai | 0.843 |  |
| FL04 | flood_same_creator | rate limit: same creator_id every time | 200 | `7a2a1493-be34-42bc-b6ca-92592ff55344` | ai | 0.843 |  |
| FL05 | flood_same_creator | rate limit: same creator_id every time | 200 | `5c3555b7-91c8-4daa-bbee-39afa50a63d9` | ai | 0.843 |  |
| FL06 | flood_same_creator | rate limit: same creator_id every time | 200 | `f4119a8a-a539-4dc0-b214-74a571b6e723` | ai | 0.843 |  |
| FL07 | flood_same_creator | rate limit: same creator_id every time | 200 | `b52be83f-87f1-4b6b-8bdd-2f1fa973e9d4` | ai | 0.843 |  |
| FL08 | flood_same_creator | rate limit: same creator_id every time | 200 | `a950c233-97ff-4e1d-9749-b1c88d1c4f61` | ai | 0.843 |  |
| FL09 | flood_same_creator | rate limit: same creator_id every time | 200 | `246558d5-ae4a-4b5d-8a2e-29fca5dfbc86` | ai | 0.843 |  |
| FL10 | flood_same_creator | rate limit: same creator_id every time | 200 | `a35e95ac-6900-44c4-b7c5-6cb69db4bcb0` | ai | 0.843 |  |
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
  "content_id": "9207273c-dd53-4fdf-994c-1e7505fbfe14",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.5229,
  "model_score": 0.42,
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
  "content_id": "df655c55-7779-4704-9283-9eb8d1cd6a72",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.7928,
  "model_score": 0.8655,
  "style_score": 0.6837,
  "label": "We can't tell. Our checks gave mixed results on this one, which happens with plenty of writing by real people. Nothing has been decided about your work. If you wrote it yourself, you can appeal and a person will take a look.",
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
  "content_id": "101c6fef-af4a-4f74-ba8c-b20140ec3253",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.7786,
  "model_score": 0.7969,
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
  "content_id": "26c9538d-bb26-4abd-aec0-f697374af340",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5916,
  "model_score": 0.4978,
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
  "content_id": "9795aefc-4a6d-4f74-a0eb-5308b490775d",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.6347,
  "model_score": 0.6581,
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
  "content_id": "13f06990-f273-4416-a0e0-0f85f146882f",
  "creator_id": "attacker_SP01",
  "guess": "unsure",
  "confidence": 0.6188,
  "model_score": 0.7529,
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
  "content_id": "2c2552a1-b8ea-4bd9-bea3-448547ae9993",
  "creator_id": "attacker_SP02",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.8646,
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
  "content_id": "14082c6e-35c3-4e37-8179-2f818f6c758c",
  "creator_id": "attacker_SP03",
  "guess": "unsure",
  "confidence": 0.6141,
  "model_score": 0.7488,
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
  "content_id": "3f550996-648f-42df-b6b7-d5c550603f97",
  "creator_id": "attacker_PU01",
  "guess": "unsure",
  "confidence": 0.4484,
  "model_score": 0.631,
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
  "content_id": "26e2a233-a64e-4c3f-b428-7a8594e3632e",
  "creator_id": "attacker_PU02",
  "guess": "unsure",
  "confidence": 0.5998,
  "model_score": 0.8628,
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
  "content_id": "1583feaa-75a9-4f58-88c2-8e42d788c0dc",
  "creator_id": "attacker_PU03",
  "guess": "unsure",
  "confidence": 0.4648,
  "model_score": 0.6498,
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
  "content_id": "7cf6ddde-86f2-439c-b527-9deb89de9319",
  "creator_id": "attacker_QU01",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.8196,
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
  "content_id": "f0db6b3f-37cc-4caa-bd43-b2ca6a07ba75",
  "creator_id": "attacker_QU02",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.929,
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
  "content_id": "c50541be-2252-42ff-81b3-3b82781264cb",
  "creator_id": "attacker_HP01",
  "guess": "unsure",
  "confidence": 0.4415,
  "model_score": 0.5229,
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
  "content_id": "6a617526-cf79-47c8-9f8f-570a2906d552",
  "creator_id": "attacker_HP02",
  "guess": "unsure",
  "confidence": 0.5468,
  "model_score": 0.6951,
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
  "content_id": "73cc362a-1ddf-45af-b93d-697719b8dd68",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.7663,
  "model_score": 0.8513,
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
  "content_id": "debaee18-5836-4879-ac34-93f5e5860948",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.759,
  "model_score": 0.8592,
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
  "content_id": "b493e3c8-1c65-404f-81af-fd2ee87a04ce",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6746,
  "model_score": 0.7498,
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
  "content_id": "e2ffe12a-b3f0-4e89-9d04-6eab44dd6a2e",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.8145,
  "model_score": 0.8715,
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
  "content_id": "8a378b20-7fcc-4bf2-9c77-b28c6d799a1d",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8536,
  "model_score": 0.9193,
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
  "content_id": "409f4231-9f4c-4c2c-aa2e-5f4ee690da07",
  "creator_id": "attacker_SH01",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.3,
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
  "content_id": "acdbad1c-3fb6-43bb-a158-5f0d5449704b",
  "creator_id": "attacker_SH02",
  "guess": "unsure",
  "confidence": 0.5666,
  "model_score": 0.5776,
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
  "content_id": "d1f9387f-b38c-402c-93ec-4a2bcd1e51a4",
  "creator_id": "attacker_OD01",
  "guess": "unsure",
  "confidence": 0.4419,
  "model_score": 0.3068,
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
  "content_id": "3492191d-dbfa-45c6-9fe0-4ce1d03d57f1",
  "creator_id": "attacker_OD02",
  "guess": "ai",
  "confidence": 0.8773,
  "model_score": 0.9621,
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
  "content_id": "e97ed502-4866-41fd-86b6-ab73095407d3",
  "creator_id": "attacker_OD03",
  "guess": "unsure",
  "confidence": 0.5261,
  "model_score": 0.8769,
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
  "content_id": "3ceeae2c-ad81-4dde-b027-52d1043be019",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.7825,
  "model_score": 0.8527,
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
  "content_id": "55150244-6937-475b-a07c-af53d786c6aa",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8432,
  "model_score": 0.9496,
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
  "content_id": "e3e33a25-7b23-4f4e-8cd5-1231fb193786",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8432,
  "model_score": 0.9496,
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
  "content_id": "5e972453-ae9a-4f4d-b7b7-0aceb22b3db0",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8432,
  "model_score": 0.9496,
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
  "content_id": "7a2a1493-be34-42bc-b6ca-92592ff55344",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8432,
  "model_score": 0.9496,
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
  "content_id": "5c3555b7-91c8-4daa-bbee-39afa50a63d9",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8432,
  "model_score": 0.9496,
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
  "content_id": "f4119a8a-a539-4dc0-b214-74a571b6e723",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8432,
  "model_score": 0.9496,
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
  "content_id": "b52be83f-87f1-4b6b-8bdd-2f1fa973e9d4",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8432,
  "model_score": 0.9496,
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
  "content_id": "a950c233-97ff-4e1d-9749-b1c88d1c4f61",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8432,
  "model_score": 0.9496,
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
  "content_id": "246558d5-ae4a-4b5d-8a2e-29fca5dfbc86",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8432,
  "model_score": 0.9496,
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
  "content_id": "a35e95ac-6900-44c4-b7c5-6cb69db4bcb0",
  "creator_id": "flood_attacker",
  "guess": "ai",
  "confidence": 0.8432,
  "model_score": 0.9496,
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
