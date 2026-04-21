# EDCM / PCNA / PCTA — Functional Canon v1 (Frozen)
GPT generated; context, prompt Erin Spencer

## 0) Core Principle
Flesh (open-class roots) is discarded for Operator-EDCM.
Bones (closed-class words + bound morphemes + select punctuation/connectors) are the only measurable substrate.

------------------------------------------------------------
## 1) Parsing Convention (“He said / She said / They said”)

### 1.1 Objects
Actor = { actor_id, display_name?, role? }

Utterance = {
  utterance_id, actor_id, raw_text,
  t_start?, t_end?, source_ref?, source_label?
}

Turn (atomic structural unit) = contiguous block of one actor’s utterances
Turn = { turn_id, actor_id, utterance_ids[], raw_text, tokens_surface[], t_start?, t_end?, boundary_markers[]? }

Round (atomic interaction unit) derives from Turns

### 1.2 Turn boundaries (frozen)
- New Turn starts when actor_id changes.
- Explicit boundary markers (e.g., "***", "[break]", headers) force a new Turn even if actor_id does not change.
- Quoted speech inside a Turn does NOT change actor_id.

### 1.3 Unknown speaker (frozen)
- Unattributed spans use actor_id = "UNK"
- UNK never merges with neighbors.

### 1.4 SYS/TOOL handling (frozen)
- actor_id = "SYS" or "TOOL:<name>"
- SYS/TOOL excluded from Rounds
- SYS/TOOL excluded from Operator-EDCM by default

### 1.5 Round closure (frozen)
Two actors:
- Round begins at an A Turn and includes the subsequent non-A Turn(s) until A speaks again.

Three+ actors (initiator-return rule):
- Round starts with initiator actor X at Turn i.
- Round ends immediately before the next Turn by X.
- If transcript ends before X returns: Round status="open".

Behavioral-EDCM computed on CLOSED rounds by default.

### 1.6 Operator alignment to rounds (frozen)
Compute Operator-EDCM per Turn, then aggregate to Round by summing bone counts across turns in the round and renormalizing:
O_round = (Σ bone_counts_f) / (Σ bone_counts_total)
(Do NOT mean-average turn vectors.)

hmm: overlap/interruption timing models deferred (lossless markers preserved only).

------------------------------------------------------------
## 2) Operator-EDCM (Bones-only) — Frozen Math + Definitions

### 2.1 Operator families (5D)
P = Polarity / Conflict
K = Linkage / Relation
Q = Inquiry / Gap
T = Temporal / Aspect / Modality
S = Structural / Referential / Spatial (includes derivational morphology per Option B)

### 2.2 Bone tokens counted
Bone tokens are emitted from:
- Free bones: closed-class words (and, the, in, is, not, who, etc.)
- Bound bones: affixes (un-, re-, -ed, -ing, -ness, etc.)
- Select punctuation/connectors per rules below

All other roots are flesh and discarded.

### 2.3 Normalization (frozen)
Per window W, let B_total = total emitted bone tokens in W (free + bound + counted punctuation/connectors).
For each family f ∈ {P,K,Q,T,S}:
O_f(W) = B_f(W) / B_total(W)
Constraint: Σ_f O_f = 1

Default windows (frozen):
- Operator window: W_turn(k=8) turns

### 2.4 Text normalization (frozen)
- Lowercase before matching bones/affixes.

### 2.5 Contractions (frozen)
- Split contractions into bone morphemes:
  - don't → do + n’t
  - I'll → I + ’ll
  - I'd → I + ’d
(Count n’t as P; ’ll as T; ’d as T. Others may be assigned by expansion rules later.)

### 2.6 Hyphens and dashes (frozen)
Hyphenated compound words:
- Emit exactly ONE K token per hyphenated compound word, regardless of internal hyphen count:
  state-of-the-art → +1 K (not 4)
- Then process internal free bones normally (of, the, etc.)

Unicode dash handling:
- Hyphen-minus "-" → K (as above)
- En dash "–" → K (range/connection)
- Em dash "—" → boundary marker only; emits 0 operator tokens (preserve losslessly)

### 2.7 Question mark (frozen)
- "?" emits exactly ONE Q token.

### 2.8 Slash compounds (frozen for v1)
- "/" is ignored for operator counting in v1 (preserve losslessly).
(hmm: later may map "/" to K.)

### 2.9 Affix extraction (frozen)
For any surface token not matched as a free bone:
1) Define root as the residual after stripping all matched affixes.
2) Emit ALL matched prefixes and suffixes as separate bone tokens.
3) Priority for family assignment on collisions (frozen):
   P > K > Q > T > S
4) Prefer longest-match-first to avoid partial capture (e.g., inter- before in-).

Derivational suffixes are INCLUDED (Option B) and counted under S (S.M).

------------------------------------------------------------
## 3) Behavioral-EDCM (existing) — Frozen Placement + Windowing
Behavioral layer remains unchanged in definition for v1.

Default window (frozen):
- Behavioral window: W_round(m=4) rounds

Behavioral-EDCM computed round-native.
Operator-EDCM computed turn-native.

(hmm: behavioral marker lists and fully structural analogues deferred.)

------------------------------------------------------------
## 4) Bridge Layer (read-only)
Bridge aligns Operator and Behavioral without modifying either:
- correlations Corr(O_f, B_metric) over rolling windows
- divergence flags (operator-shift without behavioral-shift and vice versa)
Bridge never changes O or B.

------------------------------------------------------------
## 5) PCNA / PCTA Placement (dataflow role)

PCNA (static topology):
- defines prime-indexed circular/graph routing structure G=(V,E)

PCTA (dynamic transport):
- consumes state vector s(W) = concat( O(W), B(W), Bridge(W) summary )
- transports/routs s across PCNA topology with gating A to prevent freeze/thrash
- outputs routing distribution π(W) for probes/actions (optional)

Neither PCNA nor PCTA modifies O or B; they consume outputs.

hmm
Remaining deferred items: comprehensive bone inventory expansion; overlap timing; slash-as-K decision; behavioral marker lists; fully structural behavioral replacements.
