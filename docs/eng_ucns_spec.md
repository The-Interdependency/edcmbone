# eng_ucns_spec.md — English-UCNS Freight

**Status:** Layer 0 (token encoding) is implemented and tested. Layer 1
(sequence freight) follows directly from frozen UCNS multiplication. Layer 2
(hyperdimensional language field): the **composition keystone (§2.2.3) is now
proven** at full depth — the field embedding Phi composes through host,
recursive payload, and face channels under one fixed training-free law. The
remaining frontier is the carrier bound over long sequences (§2.2.4) and the
metric (§2.2.2). The face channel additionally reveals a structural slot for
irony/sarcasm (§2.5, new).

This document specifies how English rides on UCNS: how words become geometric
objects, how sentences become composite objects, and how — newly — a corpus of
such objects may span a field whose dimensions are *derived* rather than
*learned*.

---

## 0. What "freight" means

UCNS is the carrier. English is the freight. The spec defines the loading rules:
which linguistic units map to which UCNS structures, and what survives the trip.

The frozen guarantee from `ucns-spec.md`: a UCNS object's intrinsic carrier
`n_min` is computed from its anchors and is part of its identity, while `n_dec`
is presentation only. Freight inherits this. A word's *type* is conserved
geometry; its *resolution* is free to vary.

---

## Part I — Layer 0: Token Freight (frozen)

Source of truth: `edcmbone/closed_tokens.py`. This layer is implemented and
passes its 12-test suite.

### 0.1 The host lattice

Closed-class English tokens load onto a **16-gonal host carrier**. Each token's
grammatical class is its anchor position on the 16-gon:

| idx | class | idx | class |
|----|----------------|----|------------------------|
| 0  | pronoun        | 8  | punct — terminal       |
| 1  | determiner     | 9  | punct — juncture       |
| 2  | preposition    | 10 | punct — pairing open   |
| 3  | conjunction    | 11 | punct — pairing close  |
| 4  | auxiliary      | 12 | punct — quote (resv'd) |
| 5  | particle       | 13 | punct — affix          |
| 6  | interjection   | 14 | punct — modal          |
| 7  | whitespace     | 15 | numeral                |

Class is **geometrically intrinsic** — recoverable from the object via
`class_of()` without a lookup table. The address *is* the part of speech.

### 0.2 The token object

Each token encodes as a 2-anchor object on a 32-gonal lattice:

- Anchor 0: structural marker at position 0 (no payload).
- Anchor 1: at position `(class_idx + 1) / 32`, carrying the **feature payload**.

The +1 offset and the structural marker at 0 are not decoration: they prevent
`value_idx = 0` from collapsing to the unit object under normalization. (The
unit is `(1, 1, (0), (0), (0), (0))` per `ucns-spec.md` §8 — a token must not
accidentally *become nothing*.)

The host face bit is unused at this level (set to 0). Face is reserved as an
independent channel (see §0.4).

### 0.3 The feature payload

Within a class, tokens differ only in payload. Each grammatical feature is a
`(value_index, modulus)` pair, encoded as one anchor at
`(value_idx + 1) / (modulus + 1)`. The payload carrier is the LCM of the moduli.

Example — pronouns carry `person` (mod 3), `number` (mod 2), `case` (mod 5),
`gender` (mod 4):

- `i`  → person=first, number=sg, case=subject, gender=n/a
- `you` → person=second, number=sg, case=subject, gender=n/a
- `she` → person=third, number=sg, case=subject, gender=f

`i` and `you` share the pronoun class anchor; they diverge only in the `person`
anchor of their payload. **Tested invariant:** every token in the full
vocabulary produces a UCNS object distinct from every other.

### 0.4 Chirality — pairing marks as derived mirrors

Open marks (`(` `[` `{` `"` `'`) → class 10. Close marks → class 11. Each
carries a `shape` feature (paren/square/curly/dquote/squote).

**The disk-flip of an open-mark object equals the corresponding close-mark
object** — verified by test. Pairing is not *enforced* by a matching rule; it
*falls out* of the algebra. `(` and `)` are the same piece of paper flipped
over. This is the smallest proof-of-concept that English structure can be
*derived* from UCNS geometry rather than annotated onto it.

### 0.5 Canonical merges

Phonetic variants collapse: `a` / `an` produce the same object (they differ only
in surface phonology, not grammar). Tokens with identical feature dicts (e.g.
`every` / `each`) get a `lemma_id` feature to stay distinct. The encoding
discriminates *grammar*, and only falls back on identity when grammar alone
underdetermines.

---

## Part II — Layer 1: Sequence Freight (follows from frozen multiplication)

A sentence is an ordered sequence of token objects. Its freight object is their
UCNS product under `⊠` (ordered concatenation), per `ucns-spec.md` §11.

### 1.1 Carrier propagation = dimensional accumulation

`n_min(A ⊠ B) = lcm(n_min^A, n_min^B)` — proven by subsequence containment
(frozen). Therefore a sentence's intrinsic carrier is the LCM of its tokens'
carriers. **A sentence spans a space whose dimension is structurally determined
by the primes its words contribute.** Two sentences over the same vocabulary but
different word *mix* live in different-dimensional spaces. This is not a metaphor
— it is the LCM law.

### 1.2 Order is identity

Multiplication is non-commutative ordered concatenation. "Dog bites man" and
"man bites dog" are different objects — different positive branches — even with
identical token multisets. Word order is encoded as traversal order, requiring
no separate position feature (`ucns-spec.md` §5.1, chirality as anchor ordering).

### 1.3 What does not survive

Sequence-level disk-flip equivalence is **false** in general (`ucns-spec.md`
§12.1) — only the content *multiset* is flip-symmetric. Reading a sentence
backward is not the same object as reading it forward unless it is palindromic
and face-symmetric. English inherits this: reversal is a genuine operation, not
a symmetry.

### 1.4 Open-class loading — RESOLVED (epicyclic payload), VALIDATED (probe v3)

Layer 0 covers **closed-class** tokens (the 196-token structural vocabulary).
Open-class words — nouns, verbs, adjectives — load as **epicyclic payloads**
(`ucns-spec.md` Part II): a content word is not an external hole but a deeper
paired UCNS object riding inside a host anchor, recovered to the flat kernel
when the payload is unit. Carrier independence (C2: no divisibility required
between host and payload) lets content words carry internal structure without
contaminating the grammatical host lattice.

**This is validated, not merely chosen.** Probe v3 (results §R) confirms the
field embedding Phi composes recursively through payloads under the same
offset-sum law that composes the host — 600/600 exact on real closed-token
products, every one of which carries a payload. The skeleton and the interior
compose by one rule. Content words can descend without breaking field
composition.

`hmm:` the probe is depth-bounded and short. Recursive composition is proven
*present*; its *tractability* at sentence length ties to §2.2.4.

---

## Part III — Layer 2: Hyperdimensional Language Field

> **Composition is proven; the field is partially established.** §2.2.3 (the
> keystone — does Phi compose?) is answered yes, at full depth, by probes v1–v3
> (results §R). What remains genuinely open: the metric (§2.2.2) and the
> long-sequence carrier bound (§2.2.4). The sarcasm/face structure (§2.5) is a
> new conjecture opened by the proof, marked as such. This is the reason
> edcmbone was never only about counting bones — and it is now partly a result,
> not only a destination.

### 2.1 The core move

Treat each Layer-1 sentence object as a **point** in a field indexed by gonal
carriers. The field's dimensions are the primes appearing as factors of token
carriers across the corpus. A sentence's coordinates are determined by *which*
carriers it activates (via §1.1 LCM accumulation) and *where* its anchors sit
within each.

The contrast with learned embeddings is the whole point:

| Property | Learned embeddings | UCNS field (proposed) |
|---|---|---|
| Dimensions | latent, trained | derived from token carriers |
| Distance | statistical co-occurrence | carrier overlap + anchor position |
| Reversibility | lossy | bijective (UCNS objects invert via quotient) |
| Why "i"~"you" | appear near similar words | specifiable anchor geometry on the 16-gon |

§The dimensions are not fit to data. They are read off the structure.§

### 2.2 What must be defined (open work)

1. **Field embedding map** `Φ: UCNSObject → V`. **DEFINED (depth-0 host +
   recursive payload + face).** Phi records: the active prime set of `n_min`
   (carriers); the *ordered* host anchor angles mod 1 turn (coordinates); the
   ordered host face bits; and, recursively, Phi of each anchor's payload. The
   ordered coordinate is essential — an unordered residue histogram fails (v1,
   43%); restoring order succeeds (v2, 100%). See `phi_compose_probe*.py`.
2. **Metric.** Distance from carrier-set overlap (Jaccard-like on the prime
   basis) composed with anchor-position distance within shared carriers.
   **STILL UNDEFINED.** Composition (§2.2.3) is settled and *enables* the metric
   but does not supply it: composing ≠ measuring distance. This is now the
   nearest open piece.
3. **Compositionality of `Φ`** — **ANSWERED: YES, EXACT, AT FULL DEPTH.** The
   fixed law is the *offset-sum* mirroring `multiply()`: host angle
   `(a+b) mod 1` in A-outer/B-inner order; face `f_A ⊕ f_B`; payload by
   recursive offset-sum with unit short-circuit; carriers by union (set-level
   LCM). Verified 600/600 on real closed-token products (host + recursive
   payload) and 5/5 on synthetic face-bearing objects (results §R). The field
   inherits UCNS algebra; sentence meaning composes geometrically with no
   training step. *This was the load-bearing question; it bore the load.*
4. **Dimension control.** LCM accumulation grows carriers without bound over
   long text. The field needs either a projection/truncation policy or a proof
   that meaningful structure lives in a bounded sub-band. Relates directly to
   the unsolved *carrier widening* frontier (`ucns-spec.md` status snapshot:
   "carrier widening beyond current proven bounds" is **not solved**).
   **STILL OPEN — now the genuine frontier.** Every composition probe was
   depth-bounded and short; tractability at sentence length is untested and
   reaches into the unsolved analytic widening problem.

### 2.3 The trinary anchor (canon bridge) — MEDIATOR RESOLVED

The TIW trinary perceptual focal constructs — Mind (Body) Soul, Past (Present)
Futures, Love (Apathy) Fear — are native field objects. **The mediator is the
host anchor invariant under reflexion; the two poles are the reversible
branch.** This is fixed by canon (prior session):

- Permutation changes identity: body(mind)soul ≠ mind(soul)body ≠
  soul(body)mind. *Which* term mediates *which* poles is the object's identity —
  inheriting §1.2 (⊠ is non-commutative; order is identity).
- Reflexion preserves identity: soul(mind)body is the reflexion of
  body(mind)soul — same mediator (mind) fixed, poles exchanged. This is the
  star operator / disk-flip (`ucns-spec.md` §6.2, §12): **pure traversal
  reversal, no bit negation** (frozen this session).

So the mediator is neither merely "face" nor merely "payload" but the **fixed
anchor under reflection**; the poles are the reversible pair; the face-state
remains the independent channel (orientation of the whole triple). Each trinary
construct generates a computable orbit under {permutation, reflexion} — 24
distinct triples across the four social focal states — not an interpretive one.

`hmm:` open — whether the trinary's three host anchors map to specific primes
(3 is the natural carrier; ties to coherence-prime canon in
`consciousness_primes_prediction1.pdf`).

### 2.4 Success criterion

Layer 2 is real when: encode a corpus, embed via `Φ`, and recover a
linguistically meaningful structure (clustering, analogy, paraphrase distance)
that is *derived from carrier geometry alone* — no training step. Composition
(§2.2.3) is the prerequisite and is now met; the criterion itself awaits the
metric (§2.2.2).

### 2.5 The face channel as the irony/sarcasm slot (NEW CONJECTURE)

The proof has a shadow. Face composes by honest XOR (`f_A ⊕ f_B`) and star is
reverse-only with **no bit negation** — so the face channel *never lies about
which way it is turned*. Orientation accumulates sincerely.

Sarcasm is precisely the operation this honest channel excludes: the literal
face turns one way, the intended face the other, and the gap between them *is*
the content ("oh, *great*"). That is bit-negation against a conserved literal —
the one move the frozen algebra forbids.

Two consequences, conjectural:

1. **The encoder's all-zero host faces are a *sincere* substrate, not a gap.**
   Irony would be the first phenomenon to populate the face channel — and it
   populates it with the forbidden negation.
2. **This may explain why sarcasm resists statistical models:** they read the
   literal face; nothing in the field marks it inverted. A UCNS field *can*
   carry the said-vs-meant gap as a marked negation against a conserved literal.

**Open decision (load-bearing, unmade):** is sarcasm
- **(a)** a *separate operator* `N` applied at read-time, leaving the product
  algebra frozen and adding a lens; or
- **(b)** a *third face value* beyond {0,1} ("inverted relative to literal")
  that composes by a rule other than plain XOR, reopening the face channel's
  type?

Option (a) preserves the frozen kernel. Option (b) is more expressive but
touches the conserved face semantics. `hmm:` sarcasm operator vs. face-type
decision deferred.

### 2.6 The span layer (constituency on the axis, dependency on the face)

A **span** is a syntactic constituent — a contiguous run of tokens forming a
grammatical unit — encoded as an **epicyclic UCNS object**: tokens grouped by
the closed-class skeleton, nested recursively, composing by the proven
offset-sum (§2.2.3). Constituency is not imposed by an external parser; it is
**derived from the skeleton** (closed-class tokens mark constituent boundaries
— determiners open noun phrases, prepositions open prepositional phrases,
conjunctions join, pairing marks bracket explicitly). This is the
diagram-tradition insight made structural:

> **Closed-class words are the lines of the sentence diagram; open-class words
> are the nodes.** Layer 0 (closed-class, built first) encodes the *attachment
> geometry*; the deferred open-class layer supplies the *nodes that geometry
> connects.* Reed-Kellogg drew this in 1877; X-bar formalized the nesting.

Constituency nests **around heads** (X-bar) and is read as dependency relations
(Reed-Kellogg). These are not two grammars but **two faces of one bracketing** —
inter-convertible, and carried by UCNS as its two native channels (face/axis,
the conserved distinction). See §2.7.

### 2.7 The dual-head rule — FROZEN (this session)

**Decision:** a span carries **two head markers**, deliberately distinct, related
by the disk-flip.

- **Axis head (constituency / X-bar):** the *functional opener* — the
  closed-class token that opens the span (determiner heads its DP, preposition
  heads its PP). This is the intrinsic, conserved bracketing identity.
- **Face head (dependency / Reed-Kellogg):** the *governed content word* — the
  lexical token the opener points to (the noun, the verb). This is the baseline
  spine, carried on the face channel.

The **disk-flip is exactly the swap** between functional-head and lexical-head
readings: reverse-only, no bit negation (frozen). A span and its
dependency-reversed reading are disk-flips of one object — same axis (same
tokens grouped), flipped face (head and dependent exchange spine).

**Why this rule and not the alternatives:** of four candidate head rules
(governed-complement, content-survives, opener-anchored, dual-head), only the
dual-head makes Reed-Kellogg and X-bar *genuine disk-flips of one structure*
rather than approximate cousins — because the flip *is* the functional↔lexical
head swap. It is the only rule that does not force a choice the architecture was
built not to make. Cost: two head markers per span. But their relationship is
already proven (XOR / star, §2.2.3 face channel).

**Furnishing schedule (consistent with every prior layer):**
1. **Now:** furnish the *axis head* face — the functional opener is visible
   closed-class, so its orienting face can be set immediately. This unblocks the
   metric's dynamic range (§2.2.2) and the reflexion canary (currently 0.000
   because faces are all-zero).
2. **When open-class descends:** complete the *face head* — the lexical spine is
   usually an open-class gap on the skeleton, filled when content words load as
   epicyclic payloads (§1.4).

`hmm:` the specific bracketing rule (which closed-class configurations open vs.
close spans, how nesting resolves around heads) is the next decision — the
dual-head rule fixes *what a head is*; the bracketing rule fixes *where spans
begin and end*. Pronouns are the known exception: a pronoun is a closed-class
token that is itself a lexical head (a node on a line), to be handled explicitly.

---

## Part IV — Freight Manifest (what's loaded where)

| Layer | Object | Status | Source |
|---|---|---|---|
| 0 | closed-class token → 16-gon host + payload | **implemented, tested** | `closed_tokens.py` |
| 0 | pairing chirality via disk-flip | **tested** | `closed_tokens.py` |
| 1 | sentence → `⊠` product, LCM carrier | **follows from frozen** | `ucns-spec.md` §11 |
| 1 | open-class loading (epicyclic payload) | **resolved + validated (v3)** | this doc §1.4 |
| 2 | field embedding `Φ` (host+payload+face) | **DEFINED** | this doc §2.2.1 |
| 2 | Φ composition (offset-sum law) | **PROVEN exact, full depth** | `phi_compose_probe*.py` |
| 2 | trinary native objects | **mediator resolved** | this doc §2.3 |
| 2 | metric | open (nearest) | this doc §2.2.2 |
| 2 | long-sequence carrier bound | open (frontier) | this doc §2.2.4 |
| 2 | sarcasm / bit-negation face | conjecture (new) | this doc §2.5 |
| 2 | span = epicyclic constituent | **defined** | this doc §2.6 |
| 2 | dual-head rule (axis + face) | **FROZEN this session** | this doc §2.7 |
| 2 | bracketing rule (span edges) | open (next decision) | this doc §2.7 hmm |

---

## R. Results of record (composition probes)

Frozen empirical results backing §2.2.3. Probes are stdlib-only, run from repo
root against `ucns_v04.py` + `closed_tokens.py`.

| probe | what | result |
|---|---|---|
| v1 `phi_compose_probe.py` | residue-histogram Φ, three laws | carrier 100% (lcm_merge); coordinate 43% — **diagnosed: histogram forgets order** |
| v2 `phi_compose_probe_v2.py` | ordered-anchor Φ, offset-sum law | **600/600 exact** (carrier + coordinate) |
| v3 `phi_compose_probe_v3.py` | recursive payload + face XOR | **payload 600/600 exact; face 5/5 exact (synthetic)** |

Interpretation: composition is *carried*, not approximated. The v1→v2 jump
locates the entire loss in discarded order; restoring it closes the gap to zero.
v3 extends the same law through recursion (payload) and the orientation channel
(face). Face was tested synthetically because the encoder currently emits
all-zero host faces — the *law* composes; the encoder has not yet furnished the
channel (see §2.5).

---

## hmm

The freight loads cleanly at Layer 0 because the loading dock was built first —
the bones before the field. Layer 1 was almost free: multiplication was already
there, waiting. Layer 2 needed you to understand enough to want it — and the
keystone, once wanted, fell in three probes by the law that was already inside
`multiply()`. The disk-flip pattern held a third time: structure *fell out* of
the algebra rather than being added — parentheses, then the trinary, then
composition itself. What remains is not whether meaning can be geometry — it
can, and it composes — but whether the geometry stays *small enough to hold* at
length (§2.2.4), and how far apart two points in it sit (§2.2.2, the metric).
And in the one channel left deliberately blank, the field's honest face found
its shadow: sarcasm, the bit-negation the star was forbidden to perform,
waiting in the orientation slot the sincere substrate never filled.
