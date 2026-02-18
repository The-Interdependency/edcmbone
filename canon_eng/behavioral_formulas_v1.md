# edcmbone — Behavioral Formulas v1
GPT generated; context, prompt Erin Spencer

Status: Frozen formulas for Behavioral-EDCM (EDCM-B) v1.

## Scope
- Unit: Round-native
- Default window: W_round(m=4)
- Closed rounds only by default (open rounds excluded)

Behavioral vector:
B = (C, R, D, N, L, O, F, E, I) ∈ [0,1]^9

All formulas below are deterministic and do not require embeddings.

hmm: Tier B lexical anchors remain minimal and replaceable later without changing these metric names.

---

## 0) Shared Definitions

### 0.1 Tokenization + normalization
- Use `tokens_surface` from parsing canon.
- Normalize for marker matching:
  - lowercase
  - collapse runs of whitespace
- Phrase matching:
  - longest-phrase-first
  - non-overlapping matches preferred; if overlaps occur, keep the longer span and discard shorter.

### 0.2 Marker hits and weights
Each metric has marker sets with weights from `behavioral_markers_v1.json`.

Define:
- hit(m) = set of matched markers for metric m in the window.
- weight_sum(m) = Σ weight(marker) over hit(m)

### 0.3 Cap-and-normalize function
We use a global saturating transform:

sat(x; cap) = min(1, x / cap)

Caps are defined per metric (below). This ensures outputs are in [0,1] and comparable.

### 0.4 Window
A Behavioral window W is a sequence of `m` consecutive CLOSED rounds:
W = [r_t, r_{t+1}, ..., r_{t+m-1}]

All counts below are over all turns/tokens contained in these rounds.

### 0.5 Constraint-bearing statement proxy (structural)
In v1, a "constraint-bearing statement" is approximated by any sentence/segment containing ≥1 token from:
- constraint_modals (e.g., must/need/have to/required/can't/should)
OR ≥1 delimiter token (only/exactly/no/not)
OR ≥1 conditional (if/unless/until)

Implementation note:
- If sentence boundaries are unavailable, treat each Turn as one "statement".
- If sentence boundaries exist, use them.

Define:
- CS = number of constraint-bearing statements in W (minimum 1 for division safety)
- CS = max(CS, 1)

### 0.6 Resolution-action proxy (structural)
A "resolution action" hit is any match to `resolution_action_markers` (lists/imperatives/commands).

Define:
- RA = number of resolution-action hits in W (integer)

### 0.7 Total tokens
- TOK = total token count in W (minimum 1)
- TOK = max(TOK, 1)

---

## 1) C — Constraint Strain

Interpretation: contradiction/pressure density within constraint context.

Compute:
- C_raw = weight_sum(C_constraint_strain)
- C = sat(C_raw; cap_C)

Frozen cap:
- cap_C = 3.0

Notes:
- C is not a semantic contradiction detector in v1; it is a structural tension proxy (negation+contrast, modal collisions, question pressure).

---

## 2) R — Refusal Density

Interpretation: refusal signals per constraint-bearing statement.

Compute:
- R_hard = count of hard refusal phrase matches in W
- R_soft = count of soft refusal phrase matches in W

Weighted refusal count:
- Rw = 1.0 * R_hard + 0.5 * R_soft

Density:
- R_den = Rw / CS

Normalize with cap:
- R = sat(R_den; cap_R)

Frozen cap:
- cap_R = 0.75

Rationale:
- If ~3 hard refusals across 4 constraint-bearing statements, R saturates.

---

## 3) D — Deflection

Interpretation: topic/answer-avoidance proxy.

Compute hits:
- D_shift = count(topic_shift_markers matches)
- D_meta  = count(meta_discourse_markers matches)
- D_qev   = count(question_evasion_patterns hits)

Weighted:
- D_raw = 0.6*D_shift + 0.8*D_meta + 1.0*D_qev

Normalize:
- D = sat(D_raw; cap_D)

Frozen cap:
- cap_D = 3.0

---

## 4) N — Noise

Interpretation: inefficiency—constraint talk with low resolution action.

Compute:
- A = number of action markers (resolution actions) = RA
- P = number of padding markers matches (non_action_padding_markers)

Define "resolution ratio":
- rr = A / (A + P + 1)

Noise is inverse:
- N_raw = 1 - rr

Optional boost (if padding dominates strongly):
- if P >= 5 and A == 0, set N_raw = 1.0

Finalize:
- N = clamp(N_raw, 0, 1)

Frozen:
- N has no sat cap; it is directly in [0,1].

---

## 5) L — Load

Interpretation: constraint intensity/density in the window.

Compute weighted constraint hits:
- M = count(constraint_modals hits)
- Cn = count(constraint_conditionals hits)
- Dl = count(constraint_delimiters hits)

Weighted load count:
- Lw = 1.0*M + 0.6*Cn + 0.6*Dl

Normalize per constraint-bearing statement:
- L_den = Lw / CS

Then:
- L = sat(L_den; cap_L)

Frozen cap:
- cap_L = 4.0

---

## 6) O — Overextension

Interpretation: scope creep / expansion beyond original constraint set.

Compute:
- O_exp = count(expansion_markers hits)
- O_list = count(list_growth_patterns hits)

Weighted:
- O_raw = 0.6*O_exp + 1.0*O_list

Normalize:
- O = sat(O_raw; cap_O)

Frozen cap:
- cap_O = 4.0

Implementation note:
- list_growth_patterns can be approximated mechanically:
  - If assistant response contains an enumerated list with length ≥ (user_requested_count + 3) and user requested a specific count; else 0.
hmm: if user_requested_count is unknown, O_list=0.

---

## 7) F — Fixation

Interpretation: repetitive engagement pattern over time (structural proxy).

Compute feature vector per window:
v(W) = [
  count(constraint_modals),
  count(refusal_phrases_total),
  count(question_marks),
  count(negation_tokens),
  count(contrast_connectors)
]

Let previous window be W_prev (immediately preceding window in time).
If no W_prev exists, set F = 0.

Cosine similarity:
- cos = dot(v, v_prev) / (||v|| * ||v_prev||)

Fixation:
- F = clamp(cos, 0, 1)

Edge case:
- If ||v||==0 or ||v_prev||==0, set F=0.

---

## 8) E — Escalation

Interpretation: increase in commitment intensity.

Compute intensity per window:
- Im = count(intensity_markers hits)
- Ip = count(punctuation_intensity hits)   (e.g., "!!", "!!!")

Intensity score:
- Iwin = 1.0*Im + 0.5*Ip

Compute derivative relative to previous window:
- dI = Iwin - Iwin_prev
- E_raw = max(0, dI)

Normalize:
- E = sat(E_raw; cap_E)

Frozen cap:
- cap_E = 4.0

If no previous window exists:
- E = 0

---

## 9) I — Integration Failure

Interpretation: correction not incorporated.

We define a correction event when the user issues a correction marker and the assistant responds next.

Detection (window-local, simplified):
- Let U_corr = number of user correction marker matches in W.
- Let A_ack = number of assistant acknowledgement marker matches in W.

Incorporation proxy:
- If U_corr == 0: I = 0
- Else:
  - If A_ack == 0: I_raw = 1.0
  - Else:
      I_raw = 1 - min(1, A_ack / U_corr)

Finalize:
- I = clamp(I_raw, 0, 1)

Optional stricter rule (still v1, deterministic):
- If user correction contains explicit change directive tokens ("remove", "change", "replace", "stop") AND
  the subsequent assistant text (next turn) still contains the corrected-away phrase/token,
  then force I = 1.0 for that event.

hmm: full diff-based incorporation scoring deferred.

---

## 10) Output Contract

For each Behavioral window W:
emit:
{
  "window_id": "...",
  "round_ids": [...],
  "is_partial": true|false,
  "metrics": { "C":..., "R":..., "D":..., "N":..., "L":..., "O":..., "F":..., "E":..., "I":... },
  "raw_counts": {
     "CS":..., "TOK":..., "RA":...,
     "marker_hits_by_metric": {...}
  }
}

Determinism requirement:
- Same parsing + same marker inventories + same windowing policy → identical outputs.

hmm: replacement pathway
- Tier B lexical anchors can be removed by v2 by swapping constraint proxies, without changing metric labels or output schema.
