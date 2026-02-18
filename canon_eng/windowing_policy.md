# edcmbone — Windowing Policy v1
GPT generated; context, prompt Erin Spencer

## Frozen defaults (v1)

### Units
- Operator is **Turn-native**
- Behavioral is **Round-native**
- Bridge aligns **per closed Round**

### Window sizes
- Operator window: **W_turn(k=8)**
- Behavioral window: **W_round(m=4)**

### Stride (the missing freeze)
- Default stride is **rolling by 1**:
  - Operator windows advance by 1 Turn
  - Behavioral windows advance by 1 Round

Rationale: preserves temporal resolution and supports correlation without aliasing.

## Alignment rules

### Closed-round rule (frozen)
- Behavioral metrics computed on **CLOSED** rounds only.
- Open rounds:
  - retain in storage with `status="open"`
  - excluded from Behavioral computation by default
  - excluded from Bridge correlation inputs by default

### Operator-to-round alignment (frozen)
To attach an Operator vector to a Round:
1) compute bone counts for each Turn in the Round
2) sum counts across turns
3) renormalize:
   O_round = (Σ bone_counts_f) / (Σ bone_counts_total)

Mean averaging of turn vectors is not permitted.

## Edge cases

### Beginning of transcript
- If fewer than k=8 Turns exist:
  - compute with available Turns (min-fill)
  - emit `window_is_partial=true` in metadata

### Sparse rounds
- If fewer than m=4 closed Rounds exist:
  - compute with available closed Rounds (min-fill)
  - emit `window_is_partial=true`

### SYS/TOOL/UNK
- SYS/TOOL excluded from Rounds by default.
- Operator excludes SYS/TOOL by default.
- UNK is treated as its own actor and never merged.

hmm: Optional future modes (not v1)
- Fixed bone-count windows (e.g., 100 bones) for verbosity-normalized cadence
- Non-overlapping stride (stride = k or m)
- Per-actor operator windows (actor-local cadence) with global reconciliation
