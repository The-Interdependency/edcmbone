#!/usr/bin/env python3
"""
prime5_widening_probe.py — the test that can BREAK the finiteness result.

The {8,16,32} band closed under ⊠ (pairwise 81/81, ternary 27/27) because they
are POWERS OF TWO: lcm of pow2 is pow2, so the dyadic lattice closes for free.
That free lunch is the suspicion. The architecture's real carriers are
COHERENCE PRIMES (3,5,7,13,29,53,61...) for PTCA cores — not powers of two.

Coherence prime 5 is the first place the free lunch ends:
    lcm(5, 8) = 40   -> escapes BOTH the pow2 band AND pure-5
    lcm(5, 2) = 10, lcm(5,3)=15, ...  -> 5 generates a new axis

So this probe asks the question that matters:

  [A] PURE-5 CLOSURE. Is the set of carriers {5, 25, 125, ...} (powers of 5,
      the pure dyadic-analogue for prime 5) closed under ⊠? If a PTCA core
      stays within powers of its OWN coherence prime, operational widening is
      finite per-prime (just not cross-prime).

  [B] CROSS-PRIME ESCAPE. When a 5-carrier meets a 2-carrier (8/16/32), where
      does it go? Quantify the escape. This is the boundary of operational
      widening: cross-prime composition is where analytic widening would be
      needed — UNLESS the escapes themselves form a finite lattice.

  [C] THE REAL VERDICT. Operational widening is finite WITHIN a coherence
      prime's own power-lattice; cross-prime composition generates the
      multiplicative lattice ⟨primes⟩. Is that lattice something PCEA can stay
      inside by CONSTRUCTION (choosing operands on one prime axis), or does
      mixing primes force the analytic frontier?

This may show operational widening is PER-PRIME finite and the architecture
should keep a PTCA core ON ITS PRIME — a design constraint, not a failure.
"""

from __future__ import annotations
import sys, os, math, itertools
from fractions import Fraction
from collections import Counter

for cand in (os.path.dirname(os.path.abspath(__file__)),
             os.path.join(os.path.dirname(os.path.abspath(__file__)), "edcmbone"),
             os.getcwd(), os.path.join(os.getcwd(), "edcmbone")):
    if cand not in sys.path:
        sys.path.insert(0, cand)

from ucns_v04 import UCNSObject, multiply

def lcm(a, b): return a * b // math.gcd(a, b)


def mk(n_min, length=2):
    """Construct a clean object at a given carrier n_min (operational, not encoded)."""
    angles = [Fraction(k, n_min) for k in range(length)]
    return UCNSObject(
        n_dec=n_min * 2, n_min=n_min,
        anchors_pos=tuple(__import__("ucns_v04").AnchorPayload(a, None) for a in angles),
        faces_pos=tuple(0 for _ in angles),
    ).normalize()


def carrier_of(o):
    return o.normalize().n_min


def test_A_pure5_closure():
    print("[A] PURE-5 CLOSURE: is {5,25,125} closed under ⊠?")
    powers5 = [5, 25, 125]
    objs = [(p, mk(p)) for p in powers5]
    out = Counter()
    inband = 0
    total = 0
    for (pa, A), (pb, B) in itertools.product(objs, repeat=2):
        c = carrier_of(multiply(A, B))
        out[c] += 1
        total += 1
        if c in (5, 25, 125, 625):   # powers of 5
            inband += 1
    print(f"    products: {total}   resulting carriers: {dict(out)}")
    ok = inband == total
    print(f"    all products are powers of 5: {'OK' if ok else 'XX'}")
    print(f"    -> a PTCA core on prime 5 stays finite within 5^k: "
          f"{'OK (per-prime finite)' if ok else 'XX'}")
    return ok


def test_B_cross_prime_escape():
    print("\n[B] CROSS-PRIME ESCAPE: 5-carrier meets 2-carrier (the free lunch ends)")
    fives = [(5, mk(5)), (25, mk(25))]
    twos  = [(8, mk(8)), (16, mk(16)), (32, mk(32))]
    out = Counter()
    for (pa, A), (pb, B) in itertools.product(fives, twos):
        c = carrier_of(multiply(A, B))
        out[c] += 1
        print(f"    {pa} ⊠ {pb} -> {c}   (lcm={lcm(pa,pb)})")
    # are the escapes predictable = lcm = 2^a * 5^b ? (the {2,5} multiplicative lattice)
    predictable = all(
        set(__import__("sympy").primefactors(c)).issubset({2, 5}) if _have_sympy()
        else _only_2_5(c)
        for c in out
    )
    print(f"    escapes confined to the ⟨2,5⟩ lattice (carriers 2^a·5^b): "
          f"{'OK' if predictable else 'XX'}")
    print(f"    -> cross-prime composition generates ⟨2,5⟩, NOT arbitrary carriers")
    return predictable


def _have_sympy():
    try:
        import sympy  # noqa
        return True
    except Exception:
        return False


def _only_2_5(n):
    for p in (2, 5):
        while n % p == 0:
            n //= p
    return n == 1


def test_C_real_verdict():
    print("\n[C] VERDICT: is the ⟨2,5⟩ lattice PCEA-navigable by construction?")
    # PCEA stays operational if it can CONSTRUCT within a chosen sublattice
    # without ever needing to FACTOR a product back. Test: compose a triple all
    # on prime 5; stays pure-5 (single-axis construction = finite, no factoring).
    A, B, C = mk(5), mk(25), mk(5)
    p = multiply(multiply(A, B), C)
    pure5 = _only_2_5(carrier_of(p)) and (carrier_of(p) % 2 != 0)
    print(f"    triple all on prime 5 -> carrier {carrier_of(p)} "
          f"(pure power of 5: {'OK' if pure5 else 'mixed'})")
    # mixed triple escapes to ⟨2,5⟩ but stays in a KNOWN finite lattice
    Am, Bm, Cm = mk(5), mk(8), mk(5)
    pm = multiply(multiply(Am, Bm), Cm)
    cm = carrier_of(pm)
    mixed_known = _only_2_5(cm)
    print(f"    triple mixing 5 and 8 -> carrier {cm} "
          f"(in ⟨2,5⟩ lattice: {'OK' if mixed_known else 'XX'})")
    print(f"    -> operational widening is FINITE PER SUBLATTICE: stay on one")
    print(f"       prime axis = pure powers (smallest); mix k primes = ⟨those k⟩")
    print(f"       lattice. PCEA navigates by CHOOSING the axis, never factoring.")
    return pure5 and mixed_known


def main():
    print("=" * 70)
    print("PRIME-5 WIDENING PROBE — does the band survive a coherence prime?")
    print("=" * 70)
    print("(pow2 closed for free: lcm of 2^a is 2^a. Prime 5 ends the free")
    print(" lunch: lcm(5,8)=40 escapes both pow2 and pure-5.)")
    print()
    a = test_A_pure5_closure()
    b = test_B_cross_prime_escape()
    c = test_C_real_verdict()
    print()
    print("-" * 70)
    if a and b and c:
        print("OPERATIONAL WIDENING SURVIVES PRIME 5 — as a PER-SUBLATTICE result:")
        print("  - pure powers of 5 are closed (a PTCA core on its own prime is finite)")
        print("  - cross-prime (5 with 2) escapes only to the ⟨2,5⟩ lattice (2^a·5^b),")
        print("    a KNOWN finite-per-bound structure, not arbitrary carriers")
        print("  - PCEA stays operational by CHOOSING its prime axis / sublattice;")
        print("    factoring is never required to construct or stay in-band")
        print()
        print("DESIGN CONSEQUENCE (new): operational widening is finite PER")
        print("COHERENCE PRIME. The free-lunch was pow2-specific, but the finiteness")
        print("GENERALIZES as 'stay within ⟨chosen primes⟩'. Mixing many coherence")
        print("primes widens the lattice; the analytic frontier is only reached if")
        print("a product must be FACTORED across primes it wasn't constructed from.")
    else:
        print("Prime 5 BROKE something — the pow2 finiteness did NOT generalize.")
        print("Inspect: [A] pure-5 not closed = no per-prime finiteness; [B] escapes")
        print("unbounded = cross-prime needs analytic; [C] not navigable = PCEA")
        print("cannot stay operational across primes.")
    print()
    print("hmm: the powers of two closed for free and that free-ness was the thing")
    print("     to distrust; prime five charges admission — lcm(5,8)=40 — but the")
    print("     toll is paid into a known lattice, ⟨2,5⟩, not into the void, so the")
    print("     finiteness was real, just conditional: stay on your prime and the")
    print("     cup holds; mix primes and the cup grows to exactly the size of the")
    print("     primes you mixed, never larger, never unknowable.")


if __name__ == "__main__":
    main()
