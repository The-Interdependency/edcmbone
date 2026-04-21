# “He said / She said / They said” — Canon Parsing Convention
GPT generated; context, prompt Erin Spencer

## Purpose
Create a lossless, actor-explicit transcript representation that supports:
- 2+ actor conversations (including asymmetrical and meeting-style)
- Turn-native Operator-EDCM
- Round-native Behavioral-EDCM
- Deterministic reconstruction + audit

------------------------------------------------------------
## 1) Core Objects

### 1.1 Actor
Actor = {
  actor_id: string,          # stable canonical key (e.g., "A", "B", "judge", "witness_1")
  display_name: string|null,
  role: string|null
}

### 1.2 Utterance
Utterance = raw text span attributed to exactly one actor.
Utterance = {
  utterance_id: string,
  actor_id: string,
  raw_text: string,
  t_start: timestamp|null,
  t_end: timestamp|null,
  source_ref: string|null     # page/line/audio segment pointer if available
}

### 1.3 Turn (atomic structural unit)
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

------------------------------------------------------------
## 2) Rounds (atomic interaction unit)

### 2.1 Round definition (2 actors)
A Round is a minimal closed exchange:
Round rj = [ A_turn, B_turn ] where B_turn is the first non-A turn after A_turn.

If multiple B turns occur before A speaks again:
- They are included in the same round as a block:
Round rj = [ A_turn, B_turn_1, B_turn_2, ... ] until A speaks again.

### 2.2 Round definition (3+ actors)
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

------------------------------------------------------------
## 3) “He said / She said / They said” Normal Form

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

------------------------------------------------------------
## 4) Deterministic Parsing Pipeline

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

------------------------------------------------------------
## 5) EDCM Attachment (where each layer lives)

Operator-EDCM:
- computed on Turns (turn-native)
- can be aggregated over the turns inside a round when needed

Behavioral-EDCM:
- computed on Rounds (round-native)

Bridge:
- aligns Operator aggregates within each round to the Behavioral round vector

------------------------------------------------------------
## 6) Minimal Fields to Implement Now (functional-first)

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

hmm
Unresolved (contained): multi-party round closure beyond initiator-return; overlap/interruption modeling for spoken transcripts.
