# Acceptance criteria check, after the warm-up change

- Produced by: `python check_criteria.py`, run three times in a row
- Run with `AI201_RATE_LIMITS=0`, because the script submits everything as one creator and the limit of 10 a minute would return 429s
- Code state: commit `1f959e4` (`warm_up()` scores one throwaway sentence)
- Output below is copied from the terminal, one block per trial

| Criterion | Target | Trial 1 | Trial 2 | Trial 3 |
|---|---|---|---|---|
| 1. Plain human labelled AI | at most 1 of 10 | 0 | 0 | 0 |
| 2. Score spread (AI mean − human mean) | at least 0.30 | 0.466 | 0.466 | 0.466 |
| 3. Label coverage | each label 1 to 9 times in 12 | 3 / 8 / 1 | 3 / 8 / 1 | 3 / 8 / 1 |
| 4. Appeals | 10/10 recorded, unknown id is 404 | pass | pass | pass |
| 5. Bad input | 400/413, no crash | pass | pass | pass |

All five passed in all three trials.

```
== trial 1
1. plain human labelled AI: 0/10 (target <= 1)  PASS
2. spread: 0.797 - 0.331 = 0.466 (target >= 0.30)  PASS
3. label coverage: {'human': 3, 'unsure': 8, 'ai': 1} (each 1-9)  PASS
4. appeals: 10/10 ok, unknown id -> 404  PASS
5. bad input codes: [400, 400, 400, 400, 400, 413], /ping after: 200  PASS
== trial 2
1. plain human labelled AI: 0/10 (target <= 1)  PASS
2. spread: 0.797 - 0.331 = 0.466 (target >= 0.30)  PASS
3. label coverage: {'human': 3, 'unsure': 8, 'ai': 1} (each 1-9)  PASS
4. appeals: 10/10 ok, unknown id -> 404  PASS
5. bad input codes: [400, 400, 400, 400, 400, 413], /ping after: 200  PASS
== trial 3
1. plain human labelled AI: 0/10 (target <= 1)  PASS
2. spread: 0.797 - 0.331 = 0.466 (target >= 0.30)  PASS
3. label coverage: {'human': 3, 'unsure': 8, 'ai': 1} (each 1-9)  PASS
4. appeals: 10/10 ok, unknown id -> 404  PASS
5. bad input codes: [400, 400, 400, 400, 400, 413], /ping after: 200  PASS
```

Notes:

- The three trials gave identical numbers, so the model signal is effectively deterministic on this machine.
- Criterion 3 is the closest to failing: the `ai` label appeared exactly once, which is the minimum allowed.
