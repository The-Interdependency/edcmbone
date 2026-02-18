# edcmbone

Energy–Dissonance Circuit Model (EDCM) with Prime Circular Tensor/Neural Architecture (PCTA/PCNA). A dual-layer framework for transcript analysis: bones-only Operator layer, 9-metric Behavioral layer, observational Bridge, and optional prime-circular routing for flow without semantic mods. Functional canon v1—structure first, no code yet.

Grok generated; context, prompt Erin Patrick Spencer.  
GitHub: erinepshovel-code  
Site: interdependentway.org

## Overview
This repo holds the frozen structural canon for EDCM-PCNA-PCTA. Focus: lossless transcript parsing into turns/rounds, Operator-EDCM (closed-class bones + morphology), Behavioral-EDCM (9 metrics on rounds), Bridge correlations/divergences, and PCNA/PCTA for gated routing. Data flow is clean, auditable, with no inter-layer modifications.

Open constraint: semantic components in Behavioral layer may later be replaced with structural-only analogues.  
Parameter tuning determines freeze vs thrash boundary.  
Unresolved: optimal prime density vs computational load tradeoff.  
Open constraint: canonical windowing scheme W (per-turn vs rolling N turns vs fixed bone-count windows).

## 1. Parsing Convention (“He said / She said / They said”)
GPT generated; context, prompt Erin Spencer.

### Purpose
Create a lossless, actor-explicit transcript representation that supports:
- 2+ actor conversations (including asymmetrical and meeting-style)
- Turn-native Operator-EDCM
- Round-native Behavioral-EDCM
- Deterministic reconstruction + audit

### Core Objects
#### Actor
Actor = {
  actor_id: string,          # stable canonical key (e.g., "A", "B", "judge", "witness_1")
  display_name: string|null,
  role: string|null
}

#### Utterance
Utterance = {
  utterance_id: string,
  actor_id: string,
  raw_text: string,
  t_start: timestamp|null,
  t_end: timestamp|null,
  source_ref: string|null     # page/line/audio segment pointer if available
}

#### Turn (atomic structural unit)
A Turn is a contiguous block of one actor’s utterances with no other actor interleaving.

Turn = {
  turn_id: string,
  actor_id: string,
  utterance_ids: [..],        # preserves original segmentation
  raw_text: string,           # concatenation with separators (frozen rule)
  tokens_surface: [..],       # tokenizer output (words + punctuation)
  t_start, t_end
}

Turn boundary rule (default):
- New turn starts when actor_id changes.
- Consecutive utterances by same actor merge into one turn unless explicit boundary markers exist.
- New Turn starts when actor_id changes.
- Explicit boundary markers (e.g., "***", "[break]", headers) force a new Turn even if actor_id does not change.
- Quoted speech inside a Turn does NOT change actor_id.

### Rounds (atomic interaction unit)
#### Round definition (2 actors)
A Round is a minimal closed exchange:
Round rj = [ A_turn, B_turn ] where B_turn is the first non-A turn after A_turn.

If multiple B turns occur before A speaks again:
- They are included in the same round as a block:
Round rj = [ A_turn, B_turn_1, B_turn_2, ... ] until A speaks again.

#### Round definition (3+ actors)
Default closure rule (initiator-return):
- Round starts with initiator actor X at turn i.
- Round ends immediately before the next turn by X.
- All intervening turns by other actors are inside the round.

Round = {
  round_id: string,
  initiator_actor_id: string,
  turn_ids: [ti, ti+1, ..., tk]  # tk is the last turn before initiator returns
}

Alternate closure rule (first-response-cycle) — optional later:
- Round ends once every “required responder role” has responded at least once.
(Not used for functional-first implementation.)

Two actors:
- Round begins at an A Turn and includes the subsequent non-A Turn(s) until A speaks again.

Three+ actors (initiator-return rule):
- Round starts with initiator actor X at Turn i.
- Round ends immediately before the next Turn by X.
- If transcript ends before X returns: Round status="open".

Behavioral-EDCM computed on CLOSED rounds by default.

No role-based “required responders” in functional-first.

### “He said / She said / They said” Normal Form
Represent the transcript as an ordered list of turns with explicit actor headers:

T_norm = [
  {actor:A, turn_id:1, text:"..."},
  {actor:B, turn_id:2, text:"..."},
  {actor:A, turn_id:3, text:"..."},
  ...
]

This normal form is:
- lossless (raw text preserved in utterances)
- actor-explicit
- deterministic (same input → same turns)
- round-derivable (rounds computed from turns)

### Deterministic Parsing Pipeline
Input sources (examples):
- chat logs with timestamps
- court transcript pages with speaker labels
- diarized audio transcript with speaker tags

Pipeline:
1) Ingest -> list of Utterances (speaker attribution must exist or be produced upstream)
2) Merge utterances into Turns (turn boundary rule)
3) Derive Rounds from Turns (closure rule)
4) Emit canonical JSON + audit log

Audit log includes:
- merge decisions
- boundary decisions
- missing timestamps or unknown speakers

### EDCM Attachment (where each layer lives)
Operator-EDCM:
- computed on Turns (turn-native)
- can be aggregated over the turns inside a round when needed

Behavioral-EDCM:
- computed on Rounds (round-native)

Bridge:
- aligns Operator aggregates within each round to the Behavioral round vector

Operator alignment to rounds (frozen):
Compute Operator-EDCM per Turn, then aggregate to Round by summing bone counts across turns in the round and renormalizing:
O_round = (Σ bone_counts_f) / (Σ bone_counts_total)
(Do NOT mean-average turn vectors.)

Aggregation Alignment Rule (Operator → Round):
- O_round(r) = aggregate of O_turn(t) over all turns inside round r
- Aggregation method (frozen default): sum bone counts across turns, then renormalize per bone token

This prevents averaging artifacts from short turns.

hmm: alternative aggregation (mean of turn-vectors) deferred.

### Minimal Fields to Implement Now (functional-first)
Required:
- actor_id
- utterance raw_text
- turn boundaries by actor switch
- rounds by initiator-return rule
- stable IDs

Optional later:
- diarization confidence
- overlapping speech
- interruption markers
- role-based “required responder” round closure

hmm: Unresolved (contained): multi-party round closure beyond initiator-return; overlap/interruption modeling for spoken transcripts.

## Canon Add-ons
GPT generated; context, prompt Erin Spencer.

### 1) Interruption + Overlap Convention (spoken / messy transcripts)
If source has interruptions/overlap:
- Primary rule: preserve speaker attribution as separate Utterances.
- If overlap is marked (e.g., “[overlapping]”), keep it as a literal marker inside raw_text.
- Turn boundaries remain actor-switch based.
- Overlap does NOT create new actors or merge turns; it is metadata only.

Optional fields:
- overlap: true/false
- interrupted_by: actor_id|null

hmm: full overlap timing model deferred.

### 2) Unknown / Unattributed Speech Convention
If a span has no clear speaker:
- actor_id = "UNK"
- do not merge UNK with neighbors even if adjacent
- keep source_ref (page/line/audio segment) if available

This preserves losslessness and avoids false attribution.

Unattributed spans use actor_id = "UNK"
- UNK never merges with neighbors.

### 3) Quoted Speech Inside a Turn (important for legal text)
If a speaker quotes another:
- Do NOT reassign actor_id.
- Quotation stays inside the current speaker’s turn.
- Optional tag: contains_quote = true

Rationale: speaker-of-record is the actor; quotation is content.

### 4) Multi-channel / System Messages
If system/tool/instruction content exists:
- Treat as actor_id = "SYS" (or "TOOL:<name>")
- SYS turns participate in ordering but are excluded from rounds by default
- Operator-EDCM may include SYS optionally; Behavioral-EDCM excludes SYS by default

hmm: whether SYS contributes to operator baseline deferred.

SYS/TOOL handling (frozen):
- actor_id = "SYS" or "TOOL:<name>"
- SYS/TOOL excluded from Rounds
- SYS/TOOL excluded from Operator-EDCM by default

### 5) Round Closure Rule (frozen default)
For 3+ actors, default closure is initiator-return:

Round starts at initiator X turn i.
Round ends immediately before next X turn.
All intervening turns are included.

No role-based “required responders” in functional-first.

### 6) Aggregation Alignment Rule (Operator → Round)
To compare Operator with Behavioral per round:
- O_round(r) = aggregate of O_turn(t) over all turns inside round r
- Aggregation method (frozen default): sum bone counts across turns, then renormalize per bone token

This prevents averaging artifacts from short turns.

hmm: alternative aggregation (mean of turn-vectors) deferred.

hmm: overlap/interruption timing models deferred (lossless markers preserved only).

## 2. EDCM — Energy–Dissonance Circuit Model (Dual-Layer)
GPT generated; context, prompt Erin Spencer.

### Domain
Given transcript T consisting of ordered turns:
T = {t1, t2, ..., tn}

Each turn ti has:
- actor label ai
- token sequence wi = {w1, w2, ..., wk}

EDCM produces:

Behavioral vector B ∈ ℝ^9
Operator vector O ∈ ℝ^5
Bridge correlations C

### Operator Layer (Bones-only)
Let BONE(w) → {0,1} indicate membership in canonical bone set.
Let FAMILY(w) ∈ {P,K,Q,T,S}

Emit bone tokens after morphological segmentation.

Let:
Total bone tokens in window W:
B_total = Σ BONE(w)

For each family f ∈ {P,K,Q,T,S}:

B_f = count of bone tokens in family f

Operator vector:
O_f = B_f / B_total

Constraint:
Σ O_f = 1

Optional:
Operator entropy:
H_O = - Σ O_f log(O_f)

#### Operator-EDCM (Bones-only) — Frozen Math + Definitions
Core Principle: Flesh (open-class roots) is discarded for Operator-EDCM.
Bones (closed-class words + bound morphemes + select punctuation/connectors) are the only measurable substrate.

##### Operator families (5D)
P = Polarity / Conflict
K = Linkage / Relation
Q = Inquiry / Gap
T = Temporal / Aspect / Modality
S = Structural / Referential / Spatial (includes derivational morphology per Option B)

##### Bone tokens counted
Bone tokens are emitted from:
- Free bones: closed-class words (and, the, in, is, not, who, etc.)
- Bound bones: affixes (un-, re-, -ed, -ing, -ness, etc.)
- Select punctuation/connectors per rules below

All other roots are flesh and discarded.

##### Normalization (frozen)
Per window W, let B_total = total emitted bone tokens in W (free + bound + counted punctuation/connectors).
For each family f ∈ {P,K,Q,T,S}:
O_f(W) = B_f(W) / B_total(W)
Constraint: Σ_f O_f = 1

Default windows (frozen):
- Operator window: W_turn(k=8) turns

##### Text normalization (frozen)
- Lowercase before matching bones/affixes.

##### Contractions (frozen)
- Split contractions into bone morphemes:
  - don't → do + n’t
  - I'll → I + ’ll
  - I'd → I + ’d
(Count n’t as P; ’ll as T; ’d as T. Others may be assigned by expansion rules later.)

##### Hyphens and dashes (frozen)
Hyphenated compound words:
- Emit exactly ONE K token per hyphenated compound word, regardless of internal hyphen count:
  state-of-the-art → +1 K (not 4)
- Then process internal free bones normally (of, the, etc.)

Unicode dash handling:
- Hyphen-minus "-" → K (as above)
- En dash "–" → K (range/connection)
- Em dash "—" → boundary marker only; emits 0 operator tokens (preserve losslessly)

##### Question mark (frozen)
- "?" emits exactly ONE Q token.

##### Slash compounds (frozen for v1)
- "/" is ignored for operator counting in v1 (preserve losslessly).
(hmm: later may map "/" to K.)

##### Affix extraction (frozen)
For any surface token not matched as a free bone:
1) Define root as the residual after stripping all matched affixes.
2) Emit ALL matched prefixes and suffixes as separate bone tokens.
3) Priority for family assignment on collisions (frozen):
   P > K > Q > T > S
4) Prefer longest-match-first to avoid partial capture (e.g., inter- before in-).

Derivational suffixes are INCLUDED (Option B) and counted under S (S.M).

hmm: Remaining deferred items: comprehensive bone inventory expansion; overlap timing; slash-as-K decision; behavioral marker lists; fully structural behavioral replacements.

### Behavioral Layer (9-Metric Form)
Let window W contain ordered turns.

C (Constraint Strain):
C = weighted contradiction density

R (Refusal Density):
R = count(refusal markers) / constraint statements

D (Deflection):
D = 1 - (tokens_about_constraints / total_tokens)

N (Noise):
N = 1 - (resolution_tokens / constraint_tokens)

L (Load):
L = total constraint tokens per window

O (Overextension):
O = expansion beyond original scope per window

F (Fixation):
F = cosine_sim(embed(constraint_t), embed(constraint_{t-1}))

E (Escalation):
E = max(0, d/dt(commitment_intensity))

I (Integration Failure):
I = 1 - sim(correction_response, expected_response)

Behavioral vector:
B = (C,R,D,N,L,O,F,E,I)

#### Behavioral-EDCM (existing) — Frozen Placement + Windowing
Behavioral layer remains unchanged in definition for v1.

Default window (frozen):
- Behavioral window: W_round(m=4) rounds

Behavioral-EDCM computed round-native.
Operator-EDCM computed turn-native.

(hmm: behavioral marker lists and fully structural analogues deferred.)

Notice: per-turn only metrics are in Operator layer; Behavioral is round-native.

### Bridge Layer
Bridge computes:

Corr(f,m) = corr(O_f, B_m) over rolling window

Divergence:
Δ = || O_trend - expected(O | B) ||

No modification allowed between layers.
Bridge is observational only.

Bridge aligns Operator and Behavioral without modifying either:
- correlations Corr(O_f, B_metric) over rolling windows
- divergence flags (operator-shift without behavioral-shift and vice versa)
Bridge never changes O or B.

### Output
{
  "operator": {P,K,Q,T,S},
  "behavioral": {C,R,D,N,L,O,F,E,I},
  "bridge": {correlations, divergences}
}

## 3. PCTA — Prime Circular Tensor Architecture
GPT generated; context, prompt Erin Spencer.

### Domain
PCTA models dynamic transport on a circular prime-indexed lattice.

Let:
θ ∈ [0, 2π)
Discretized into N nodes indexed by primes:
{p1, p2, ..., pN}

State variable:
U(θ, t) = activation density

Gate variable:
A(θ, t) = adaptive braking field

### Transport Equation
Base transport:

∂U/∂t =
  - b(A) ∂U/∂θ
  + k(A) ∂²U/∂θ²
  + S(θ,t)
  - R(U)

Where:

b(A) = 1 / (1 + λA)   (drift brake)
k(A) = 1 / (1 + λA)   (diffusion brake)

S(θ,t) = stimulus input
R(U) = nonlinear decay term

### Gate Dynamics
Gate evolves via:

∂A/∂t =
  α * coherence(U)
  - β * overload(U)
  - γA

Where:

coherence(U) = local triadic alignment
overload(U) = magnitude variance or constraint density
γ = leakage constant

### Stability Condition
CFL constraint:

Δt ≤ (Δθ²) / (2k_max)

High λ → freeze regime
Low λ → oscillatory regime

### Interpretation
- U = circulating energy field
- A = adaptive constraint brake
- Prime indexing prevents periodic aliasing
- Circular topology enforces conservation

hmm: Parameter tuning determines freeze vs thrash boundary.

## 4. PCNA — Prime Circular Neural Architecture
GPT generated; context, prompt Erin Spencer.

### Domain
PCNA is a static graph-based architecture.

Nodes arranged on circular prime index set:

V = {p1, p2, ..., pN}

Edges E defined by:
- Prime gaps
- Modular adjacency
- Heptagram projection rules

Graph:
G = (V, E)

### Node State
Each node i holds state vector:

x_i ∈ ℝ^d

Update rule:

x_i(t+1) =
  σ( Σ_j W_ij x_j(t) + b_i )

Where:

W_ij = weight determined by prime distance
σ = activation function

### Helical Projection
Optional 7-phase rotation:

θ_i(t) = (θ_i(0) + ωt) mod 2π

Heptagram routing defined by:
i → (i + k) mod N
where k ∈ {2,3,5} depending on projection layer

### Relationship to PCTA
PCNA = static structural graph
PCTA = dynamic transport over that graph

PCNA defines topology.
PCTA defines flow.

### Minimal Implementation
- Prime-indexed circular array
- Deterministic adjacency rule
- Multi-layer rotation mapping

hmm: Unresolved: optimal prime density vs computational load tradeoff.

## 5. Data Flow — PCNA / PCTA / EDCM (Dual-Layer)
GPT generated; context, prompt Erin Spencer.

### 0) Inputs
Primary input is a transcript stream:

T = sequence of turns
ti = {turn_id, timestamp, actor_id, raw_text}

Optional metadata:
- channel (sms/email/court transcript)
- speaker role tags
- tool events (web/tool calls)
- system/instruction blocks (if present)

### 1) Ingest + Normalization (lossless)
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

### 2) Parallel Feature Extraction (no cross-dependency)
#### 2A) Operator-EDCM Extractor (bones-only)
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

#### 2B) Behavioral-EDCM Extractor (canon 9 metrics)
Input: T_norm (+ optional parsing results)

Steps (high-level):
- identify constraint-bearing spans (per canon rules)
- compute 9 metrics over window W:
  B(W) = {C,R,D,N,L,O,F,E,I}

Output per window W:
B(W)

NOTE: Behavioral layer remains unchanged by Operator layer.

### 3) Bridge Builder (read-only crosswalk)
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

### 4) PCNA / PCTA Routing Layer (optional orchestration)
Purpose: treat metrics as state and route “attention” or “agent actions” without semantic interpretation.

#### 4A) PCNA topology (static)
Defines a graph G=(V,E) and routing map R:
- nodes correspond to prime-indexed positions / heptagram phases / sentinel children
- edges define allowed propagation

#### 4B) PCTA transport (dynamic)
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

PCNA (static topology):
- defines prime-indexed circular/graph routing structure G=(V,E)

PCTA (dynamic transport):
- consumes state vector s(W) = concat( O(W), B(W), Bridge(W) summary )
- transports/routs s across PCNA topology with gating A to prevent freeze/thrash
- outputs routing distribution π(W) for probes/actions (optional)

Neither PCNA nor PCTA modifies O or B; they consume outputs.

### 5) Downstream Actions (optional)
Depending on π(W):
- choose which probe to run next
- choose which transcript slice to examine
- choose which UI panel to surface
- choose alert thresholds to display

Output artifacts:
- dashboard JSON
- alert events
- reproducible logs

### 6) Storage (auditable)
Persist:
- raw transcript (immutable)
- normalized transcript (versioned)
- O(W), B(W), Bridge(W) per window (versioned)
- PCNA/PCTA routing logs (if used)

hmm: Open constraint: canonical windowing scheme W (per-turn vs rolling N turns vs fixed bone-count windows).

## 6. EDCM / PCNA / PCTA — Functional Canon v1 (Frozen)
GPT generated; context, prompt Erin Spencer.

### 0) Core Principle
Flesh (open-class roots) is discarded for Operator-EDCM.
Bones (closed-class words + bound morphemes + select punctuation/connectors) are the only measurable substrate.

(Full details integrated above.)

## Deferred / Unresolved Items
- Comprehe# EDCM-PCNA-PCTA Framework Specification (Canon)
