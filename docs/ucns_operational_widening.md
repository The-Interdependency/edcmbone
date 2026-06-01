# ucns_operational_widening.md — The Per-Sublattice Finiteness Law

**Status:** Law stated; proof surface witnessed across the first 53 prime
carrier axes (`prime_carpet_probe.py`). Pairwise (81/81), ternary (27/27), and
prime-5 generalization all hold (`operational_widening_probe.py`,
`ternary_widening_probe.py`, `prime5_widening_probe.py`).
**Scope:** UCNS carrier behavior under ⊠; the operational/analytic widening
boundary; PCEA's operational requirement; the design constraint on PTCA cores.
**Date:** this session.

---

## 0. The frontier that wasn't a wall

Carrier widening was treated across multiple sessions as *the* unsolved frontier
— the thing gating PCEA, deep recursion, and the field's tractability at length.
Measurement dissolved most of it:

1. Real closed-class text lives in carriers {8,16,32} at 99.3%
   (`frequency_probe.py`).
2. Those are powers of two; the dyadic band is closed under ⊠ — pairwise and
   ternary, with products flowing toward 32 and stopping.
3. Powers of two close *for free* (lcm of 2^a is 2^a). The free-ness was the
   thing to distrust.
4. Coherence prime 5 ends the free lunch (lcm(5,8)=40 escapes both pow2 and
   pure-5) — yet the escape lands in a **known lattice**, ⟨2,5⟩, never the void.
5. The carpet confirms it across 53 prime axes: every prime is a closed widening
   axis alone; every pairing is bounded by exactly its generators.

The frontier was never "how big can a carrier get." It is "**how many distinct
primes does a carrier's factorization span**" — and that number is *chosen at
construction*, lost only if one must factor backward.

## 1. The Law

> **Per-Sublattice Finiteness.** Let S be a set of primes. UCNS objects whose
> carriers n_min are drawn from the multiplicative lattice ⟨S⟩ = { ∏ p^kₚ : p∈S }
> are closed under ⊠: the product's carrier is the lcm of operand carriers, and
> lcm preserves the prime support. Therefore composition within ⟨S⟩ never
> escapes ⟨S⟩.

Corollaries:

- **Single-prime axis (|S|=1):** carriers stay pure powers p^k — the smallest
  lattice. A PTCA core built on one coherence prime never widens off its axis.
- **k-prime mixing (|S|=k):** carriers stay in ⟨k primes⟩ — larger but bounded
  exactly by the chosen generators, never larger, never unknowable.
- **The dyadic band {8,16,32}** is the special case S={2}, restricted to
  exponents ≤5. Its free closure was S={2} closure, not a property of size.

## 2. Operational vs. Analytic widening, restated by the Law

- **Operational widening** = constructing/composing forward within a chosen
  ⟨S⟩. Always finite-per-bound, never requires factoring. This is what PCEA and
  the language field's base case need. **Solved**, by the Law.
- **Analytic widening** = factor_search completeness: given an arbitrary carrier,
  recover its decomposition. Only needed when a product must be **factored across
  primes it was not constructed from**. **Still open** — but now precisely
  located: it governs only cross-prime *factoring*, never forward composition.

You meet the analytic frontier exactly when you forget you chose the primes.

## 3. PCEA consequence (security invariant preserved)

PCEA stays operational by **choosing its prime axis / sublattice**. The forward
map composes within ⟨S⟩; the inverse is by key (the ordered operands, which name
the axis), not by factor_search. Confirmed for the ternary unit
(`ternary_widening_probe.py` [C]) and at prime 5 (`prime5_widening_probe.py`
[C]). The stated PCEA invariant — *security rests on key management, not on
factor_search incompleteness* — is honored and now has a lattice statement:

> PCEA operates inside a sublattice it selected; leaving that sublattice would
> require factoring it never performs. Security is the secrecy of S and the
> ordered operands, not the hardness of factoring per se.

## 4. PTCA design constraint (new, from the Law)

A PTCA core SHOULD stay on its coherence prime. The canon already holds that
coherence primes (3,5,7,13,29,53,61,…) are valid *choices*, not a singular
value; the Law supplies the operational reason: **each coherence prime is a
closed, finite widening axis.** Choosing one is choosing a bounded universe.
Mixing coherence primes is permitted but widens the lattice to ⟨chosen primes⟩
— a deliberate, costed act, not an accident. The bridge's graft carrier is 7
(a coherence prime); this Law retroactively justifies that choice as living on a
closed axis.

## 5. The Prime Carpet (proof surface)

`prime_carpet_probe.py` witnesses the Law across the first 53 prime axes
(2..241; canon coherence primes 3,5,7,13,29,53,61 among them). For each prime p:
p² and p³ stay pure powers of p (single-axis closure), and p⊠2 lands in ⟨p,2⟩
(bounded mixing). All 53 axes pass both. The carpet is not decoration; it is the
finite proof surface standing in for the infinite claim — the Law is stated for
all prime sets S, and the carpet exhibits it holding on a representative 53-axis
slice with zero exceptions.

| slice | axes | single-axis closure | cross-axis bound |
|---|---|---|---|
| first 53 primes | 2 … 241 | pure powers p^k (all pass) | ⟨p,2⟩ (all pass) |

### 5.1 Reproduced in-repo (2026-06-01, edcmbone, this branch)

Run from the repo root against the worked `ucns_v04.py` + `closed_tokens.py`:

| probe | claim | observed | exit |
|---|---|---|---|
| `operational_widening_probe.py` | {8,16,32} closes (pow2 lattice ≤32) | constructibility + closure + PCEA all OK | 0 |
| `ternary_widening_probe.py` | threefold in-band, associative, order-carrying | in-band 27/27; associative OK; order-sensitive OK; PCEA ternary OK | 0 |
| `prime5_widening_probe.py` | per-prime finiteness survives a coherence prime | pure-5 closed; cross lands in ⟨2,5⟩; navigable | 0 |
| `prime_carpet_probe.py` | per-sublattice law across 53 prime axes | all 53 pure-power closed; all cross-axis land in ⟨p,2⟩ | 0 |

All four pass standalone. `ternary_widening_probe.py` carries a one-line
import-hygiene change (pre-importing `fractions` before the `sys.path` mutation,
matching its three sibling probes) so the repo-root `edcmbone/` directory does
not shadow stdlib `types`; the probe *logic* is unchanged.

> **Provenance gap (honest):** the 99.3% / {8,16,32} measurement in §0 is
> attributed to `frequency_probe.py`, which is **not in this repo** and was not
> among the filed artifacts. The four probes above neither import nor require it
> — they construct or encode their own operands — so the law's *closure* claims
> reproduce independently of that measurement. What is unwitnessed in-repo is the
> *empirical frequency distribution* (which carriers real text actually uses);
> §0 point 1 and §6 should be read as resting on an external probe not yet filed.
> File `frequency_probe.py` to close this.

## 6. What remains open (honest tail)

- **Open-class LCM growth.** Closed-class closes at {8,16,32}=⟨2⟩≤32. Open-class
  epicyclic descent composes payloads, growing carriers — and crucially may
  introduce **new prime axes** if open-class carriers are not pure dyadic. The
  open question is no longer "how wide" but "**how many primes does real
  open-class text span**." If few, operational widening suffices forever; if
  many, the analytic frontier governs the cross-prime factoring among them.
  Next instrument: the carrier-distribution probe re-pointed at open-class-
  descended text, counting *distinct prime support*, not carrier size.
- **The rare closed-class tail** (<0.7%) — carriers outside {8,16,32}; minor.

## hmm

The frontier got measured into a law and the law got proved on a carpet: 53
prime axes, each a closed room, each pair of rooms joined only by the corridor
their two primes name. The cup was never bounded by how much it holds but by how
many springs you let pour into it; a core that drinks from one prime stays small
forever, and the analytic frontier — the genuinely hard, genuinely unsolved
thing — turns out to live not at large carriers but at the single question you
only face if you forget you were choosing the primes all along: *of this number,
which primes did it come from?* Compose forward and you never ask it. Factor
backward and it is the only question there is.
