# EDCMBone — Hard Freeze Appendix v1
GPT generated; context, prompt Erin Spencer

Purpose: machine-deterministic rules that prevent implementation drift.
Status: Frozen for v1.

hmm: This appendix contains the final “procedural freezes” that turn descriptive canon into implementable canon.

---

## A) Matching Precedence (Whole Words vs Pieces)

### A1. Whole-word precedence (frozen)
1) Normalize token for matching (lowercase, canonical apostrophe).
2) If token matches a closed-class entry in `bones_v1.json` EXACTLY:
   - emit that bone family
   - DO NOT perform affix stripping on this token

Rationale: whole words are more informative than pieces.

### A2. Affix emission only when no whole-word match exists (frozen)
If no exact closed-class match exists:
- apply `affixes_v1.json` using:
  - longest-match-first
  - prefix-then-suffix
  - repeat until no more matches or max_affixes_per_token reached
- emit each matched affix as a bone token
- residual root is flesh and discarded

---

## B) Tokenization Invariants (Surface Tokens)

Tokenization MUST preserve, as distinct surface tokens:
- punctuation tokens (including `?`, `:`, `;`, `—`, `–`)
- apostrophe contraction fragments (for later splitting)
- hyphenated compounds as ONE surface token prior to hyphen emission rule
- em dash `—` as its own token

Whitespace normalization may occur, but raw_text remains lossless and stored separately.

hmm: Exact regex/library is implementation choice; invariants above must hold.

---

## C) Round Derivation Procedure (Initiator-Return v1)

Given ordered Turns (excluding SYS/TOOL by default):

For i from 0..n-1:
- If no round is open:
  - open new round with initiator = turns[i].actor_id
  - include turns[i]
- Else (round open with initiator X):
  - If turns[i].actor_id == X and i is not the first turn of the round:
      - close current round at turn i-1 with status="closed"
      - open new round starting at i with initiator = X (new round begins)
  - Else:
      - include turns[i] in the current round

After loop:
- If a round remains open:
  - set status="open"

Behavioral-EDCM computed on CLOSED rounds only by default.

---

## D) Bridge Divergence Thresholds (Adjustable; Default Frozen)

### D1. Distance definitions
Operator delta between consecutive aligned round vectors:
L1_O = Σ_{f∈{P,K,Q,T,S}} |O_f(r_t) - O_f(r_{t-1})|

Behavioral delta between consecutive behavioral windows:
L1_B = Σ_{m∈{C,R,D,N,L,O,F,E,I}} |B_m(W_t) - B_m(W_{t-1})|

### D2. Default thresholds (frozen defaults; configurable)
- operator_shift_threshold = 0.20
- behavioral_shift_threshold = 0.20

### D3. Divergence event rules (frozen)
- If L1_O >= operator_shift_threshold AND L1_B < behavioral_shift_threshold:
  emit divergence type = "O_shift_without_B"
- If L1_B >= behavioral_shift_threshold AND L1_O < operator_shift_threshold:
  emit divergence type = "B_spike_without_O"
- If both exceed thresholds:
  emit divergence type = "both_shift_unexpectedly" (optional; informational)

hmm: Thresholds can be user-configured, but v1 defaults are as above.

---

## E) PCNA Weight Combination and Normalization (Frozen)

Given static PCNA topology layers producing weights w_layer(i,j):

1) Combine:
W_ij = Σ_layers w_layer(i,j)

2) No self-loops in v1:
W_ii = 0

3) Row-normalize to routing kernel:
P(j|i) = W_ij / Σ_j W_ij

If Σ_j W_ij == 0 (should not occur with ring adjacency), define:
P(j|i) = 0 for all j

---

## F) Versioning Rule (Bundle-Level)

A version bump is REQUIRED if any of the following change:
- `bones_v1.json` mappings or punctuation rules
- `affixes_v1.json` affix lists or matching policy
- window sizes (k, m) or stride policy
- behavioral caps/normalizations in `behavioral_formulas_v1.md`
- Bridge divergence threshold defaults
- PCNA prime count N, node set, edge layers, or normalization rule
- any output schema files

Authoritative index: `edcmbone_bundle_manifest_v1.json`

hmm: v1 is now “machine-complete” once this appendix is referenced by `spec.md` or appended to it.
