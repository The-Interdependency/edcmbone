# Data Flow — PCNA / PCTA / EDCM (Dual-Layer)
GPT generated; context, prompt Erin Spencer

## 0) Inputs
Primary input is a transcript stream:

T = sequence of turns
ti = {turn_id, timestamp, actor_id, raw_text}

Optional metadata:
- channel (sms/email/court transcript)
- speaker role tags
- tool events (web/tool calls)
- system/instruction blocks (if present)

------------------------------------------------------------
## 1) Ingest + Normalization (lossless)
Goal: preserve raw while creating stable structure.

1.1 Normalize into canonical turns:
Turn = {
  id, t, actor, raw_text,
  text_norm,              # whitespace, unicode, casing rules (frozen)
  tokens_surface,         # basic tokenization (words + punctuation)
  sentence_bounds         # optional
}

Output:
T_norm = [Turn1..Turnn]

------------------------------------------------------------
## 2) Parallel Feature Extraction (no cross-dependency)

### 2A) Operator-EDCM Extractor (bones-only)
Input: Turn.tokens_surface

Steps:
- morphological segmenter emits bound morphemes
- free-bone matcher emits closed-class tokens
- discard remaining roots
- count by family {P,K,Q,T,S}
- normalize per bone token

Output per window W:
O(W) = {P,K,Q,T,S}
O_counts(W) (optional raw counts for audit)

### 2B) Behavioral-EDCM Extractor (canon 9 metrics)
Input: T_norm (+ optional parsing results)

Steps (high-level):
- identify constraint-bearing spans (per canon rules)
- compute 9 metrics over window W:
  B(W) = {C,R,D,N,L,O,F,E,I}

Output per window W:
B(W)

NOTE: Behavioral layer remains unchanged by Operator layer.

------------------------------------------------------------
## 3) Bridge Builder (read-only crosswalk)
Input: O(W), B(W) over rolling windows

Computes:
- correlations: Corr(O_f, B_m)
- divergences: where behavioral alarms occur without operator shifts and vice versa
- flags: "inspect window", "reduce window", "per-actor split"

Output:
Bridge(W) = {
  corr_pairs[],
  divergence_events[],
  flags[]
}

RULE: Bridge does not modify O or B; it only reports.

------------------------------------------------------------
## 4) PCNA / PCTA Routing Layer (optional orchestration)
Purpose: treat metrics as state and route “attention” or “agent actions” without semantic interpretation.

### 4A) PCNA topology (static)
Defines a graph G=(V,E) and routing map R:
- nodes correspond to prime-indexed positions / heptagram phases / sentinel children
- edges define allowed propagation

### 4B) PCTA transport (dynamic)
Input state vector s(W):

s(W) = concat( O(W), B(W), summary(Bridge(W)) )

Transport:
- circulate s across prime-circle
- gate via braking field A to prevent thrash/freeze
- output stabilized routing probabilities π over nodes/actions

Outputs:
- π(W): routing distribution over sub-agents / diagnostic probes
- A(W): gate state (freeze/thrash control)
- logs of transport stability

NOTE: PCNA/PCTA do not change O or B; they consume them.

------------------------------------------------------------
## 5) Downstream Actions (optional)
Depending on π(W):
- choose which probe to run next
- choose which transcript slice to examine
- choose which UI panel to surface
- choose alert thresholds to display

Output artifacts:
- dashboard JSON
- alert events
- reproducible logs

------------------------------------------------------------
## 6) Storage (auditable)
Persist:
- raw transcript (immutable)
- normalized transcript (versioned)
- O(W), B(W), Bridge(W) per window (versioned)
- PCNA/PCTA routing logs (if used)

hmm
Open constraint: canonical windowing scheme W (per-turn vs rolling N turns vs fixed bone-count windows).
