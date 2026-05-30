#!/usr/bin/env python3
"""
phi_compose_probe_v2.py — keystone, order-aware.

v1 finding (phi_compose_probe.py):
  - CARRIER composes 100% via lcm_merge (which primes are active — derived for free).
  - COORDINATE composed only 43% because Phi was a residue HISTOGRAM, and ⊠
    is ORDERED. The histogram forgets the one thing the product preserves.

v2 fix, scoped exactly by v1:
  - Keep lcm_merge for carriers (proven).
  - Replace the coordinate with the ORDERED anchor sequence (theta mod 1 turn),
    the faithful image of what ⊠ actually manipulates.
  - Add the true law: OFFSET-SUM in A-outer / B-inner order, mirroring
    multiply()'s  theta = a.theta + (b.theta - beta0)  with beta0 = 0.

Question: does the ordered-anchor Phi compose under the offset-sum law?
  EXACT 100% -> composition is carried; "derived not learned" holds at depth-0
               for the host channel. Earn the right to test payload + face.
  < 100%     -> residual loss remains; locate it (face? payload? normalization
               reordering?) before claiming.

Stdlib only. Run from repo root.
"""

from __future__ import annotations
from fractions import Fraction
from math import gcd
import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
for cand in (HERE, os.getcwd(), os.path.join(HERE,'edcmbone'), os.path.join(os.getcwd(),'edcmbone')):
    if cand not in sys.path:
        sys.path.insert(0, cand)

try:
    from ucns_v04 import UCNSObject, multiply
    from closed_tokens import encode, DISPATCH
except ImportError as e:
    print("FATAL: run from repo root (needs ucns_v04.py + closed_tokens.py).")
    print(f"  import error: {e}")
    sys.exit(1)


def primes_of(n: int):
    out, d = [], 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out or [1]


# ------------------------------------------------------------------
# Phi v2 — ORDER-AWARE host embedding.
#
#   carriers : the active prime set (distinct prime factors of n_min)
#   coords   : the ORDERED tuple of host anchor angles, theta mod 1 turn,
#              as exact Fractions — the faithful image of the positive branch.
#
# Carrier composition is tested with lcm_merge (v1, proven).
# Coordinate composition is tested with the offset-sum law below.
# ------------------------------------------------------------------

def phi(obj: UCNSObject):
    o = obj.normalize()
    coords = tuple(ap.theta % 1 for ap in o.anchors_pos)   # ordered, exact
    carriers = frozenset(primes_of(o.n_min))
    return {"carriers": carriers, "coords": coords}


def law_carrier(fa, fb):
    """lcm_merge at the set level: union of active primes (proven in v1)."""
    return fa["carriers"] | fb["carriers"]


def law_offset_sum(fa, fb):
    """
    Mirror multiply(): ordered Minkowski sum of the two coord sequences,
    A-outer / B-inner, each entry (a + b) mod 1 turn. beta0 = 0 after
    normalize, so the product offset is just a + b.

    NOTE: multiply() reduces mod 4pi (norm_turn -> [0,2) turns) then
    normalize() projects identity via n_min on the mod-1 lattice. We compare
    on the mod-1 projection (the carrier-relevant geometry), matching phi().
    """
    A, B = fa["coords"], fb["coords"]
    out = []
    for a in A:
        for b in B:
            out.append((a + b) % 1)
    return tuple(out)


def main():
    print("=" * 72)
    print("Phi COMPOSITION PROBE v2 — order-aware (eng_ucns_spec.md §2.2.3)")
    print("=" * 72)

    toks = sorted(DISPATCH.keys())
    objs = [(t, encode(t).normalize()) for t in toks if encode(t) is not None]

    # Battery: stride through vocab to mix classes; cap pairs.
    MAX = 600
    n = len(objs)
    step = max(1, (n * n) // MAX)
    pairs = []
    for i in range(n):
        for j in range(n):
            if (i * n + j) % step == 0:
                pairs.append((objs[i], objs[j]))
                if len(pairs) >= MAX:
                    break
        if len(pairs) >= MAX:
            break

    print(f"\nVocabulary objects: {n}   test pairs: {len(pairs)}")
    print("Phi v2: ordered host-anchor angles (mod 1 turn) + active prime set\n")

    carrier_ok = 0
    coord_ok = 0
    coord_multiset_ok = 0   # diagnostic: does it match ignoring order?
    total = 0
    fails = []

    for (ta, A), (tb, B) in pairs:
        try:
            P = multiply(A, B)
        except Exception:
            continue
        total += 1
        fa, fb, fp = phi(A), phi(B), phi(P)

        if law_carrier(fa, fb) == fp["carriers"]:
            carrier_ok += 1

        pred = law_offset_sum(fa, fb)
        if pred == fp["coords"]:
            coord_ok += 1
        else:
            if sorted(pred) == sorted(fp["coords"]):
                coord_multiset_ok += 1
            if len(fails) < 5:
                fails.append((ta, tb, pred, fp["coords"]))

    print("-" * 72)
    print(f"  carrier law (lcm_merge):      {carrier_ok}/{total} "
          f"({100*carrier_ok/total:.1f}%)")
    print(f"  coordinate law (offset-sum):  {coord_ok}/{total} "
          f"({100*coord_ok/total:.1f}%)  [exact ordered]")
    print(f"    of the misses, order-only:  {coord_multiset_ok} "
          f"(same multiset, reordered by normalize)")
    print("-" * 72)

    print("\nVERDICT")
    if coord_ok == total:
        print("  EXACT. Ordered-anchor Phi composes under offset-sum on all pairs.")
        print("  -> Host-channel composition is CARRIED, not approximated.")
        print("     'Derived not learned' holds at depth-0. Next: test whether")
        print("     payload (epicyclic) and face (XOR) channels compose too.")
    elif coord_ok + coord_multiset_ok == total:
        print("  EXACT UP TO ORDER. Every miss is a reordering, not a wrong value.")
        print("  -> The product's CONTENT composes exactly; normalize() reorders")
        print("     the sequence (it shifts first anchor to 0 + reduces mod 4pi,")
        print("     which can permute the mod-1 projection). Composition holds at")
        print("     the multiset level; ordered identity needs the pre-normalize")
        print("     sequence. This is a normalization-gauge effect, not loss.")
        print("     -> Define Phi on the pre-normalize branch, or accept multiset")
        print("        equivalence (cf. ucns-spec §12.1 disk-flip content law).")
    elif coord_ok > 0:
        print(f"  PARTIAL: offset-sum holds exactly on {coord_ok}/{total},")
        print(f"  up-to-order on {coord_ok + coord_multiset_ok}/{total}.")
        print("  -> A real residual remains beyond reordering. Inspect samples:")
        for ta, tb, pred, act in fails:
            print(f"     {ta!r} ⊠ {tb!r}:")
            print(f"        pred : {tuple(str(x) for x in pred)}")
            print(f"        true : {tuple(str(x) for x in act)}")
    else:
        print("  NO match even up to order. The offset-sum image diverges from")
        print("  the product's host anchors — likely a projection mismatch")
        print("  (mod 1 vs mod 2 turns) rather than a composition failure.")
        for ta, tb, pred, act in fails:
            print(f"     {ta!r} ⊠ {tb!r}:")
            print(f"        pred : {tuple(str(x) for x in pred)}")
            print(f"        true : {tuple(str(x) for x in act)}")

    print("\nhmm: still host-channel only. A clean result here makes the payload")
    print("     and face probes the next two questions; a gauge effect makes the")
    print("     pre-normalize-vs-multiset choice a canon decision, not a bug.")


if __name__ == "__main__":
    main()
