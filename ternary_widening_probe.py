#!/usr/bin/env python3
"""
ternary_widening_probe.py — the correction: THREE composable together.

operational_widening_probe tested PAIRWISE closure (a ⊠ b) and found the
real-carrier band {8,16,32} closed under the BINARY operation. But the
architecture's unit of composition is THREE, not two: trinary focal constructs
(pole-mediator-pole), seed-over-grafts, PTCA tensors-in-circles-in-seeds, the
prime quartet as one unit. PCEA's operational widening needs a coherent TRIPLE,
not a dyad.

Pairwise closure does NOT imply ternary composability. This probe tests the
right claim:

  [A] TERNARY IN-BAND. For triples (a,b,c) of real bones spanning {8,16,32},
      does a ⊠ b ⊠ c stay in the band's pow2 lattice (<=32)? (Binary closure
      makes this likely but NOT guaranteed once we also demand...)

  [B] ASSOCIATIVITY / ORDER. (a⊠b)⊠c vs a⊠(b⊠c): same object? ⊠ is
      non-commutative (order is identity), so we expect associativity to HOLD
      (grouping) while permutation does NOT (ordering). Both must be checked:
      the threefold product must be well-defined under grouping even though it
      is order-sensitive under permutation.

  [C] TERNARY PCEA. The threefold forward map (the cipher's real unit) must be
      deterministic and invertible-by-key (operands), not by factor_search,
      with n_min staying in the operational band.

If ternary holds, the operational widening result is real for the architecture's
actual composition unit. If it fails, pairwise closure was a false comfort.
"""

from __future__ import annotations
import sys, os, math, itertools
from collections import Counter
from fractions import Fraction  # pre-import stdlib before the sys.path mutation
                                # below (matches the sibling probes): the repo-root
                                # edcmbone/ dir otherwise shadows stdlib `types`
                                # when ucns_v04 pulls in `fractions` later.

for cand in (os.path.dirname(os.path.abspath(__file__)),
             os.path.join(os.path.dirname(os.path.abspath(__file__)), "edcmbone"),
             os.getcwd(), os.path.join(os.getcwd(), "edcmbone")):
    if cand not in sys.path:
        sys.path.insert(0, cand)

from ucns_v04 import UCNSObject, multiply
from closed_tokens import encode

REAL_CARRIERS = {8, 16, 32}
POW2_BAND = {2, 4, 8, 16, 32}


def obj_key(o):
    """Canonical comparison key for a normalized object (carrier + ordered anchors + faces)."""
    o = o.normalize()
    return (o.n_min,
            tuple((x.theta % 1) for x in o.anchors_pos),
            tuple(o.faces_pos))


def real_triples():
    """One representative bone per real carrier, so triples span {8,16,32}."""
    reps = {}
    for t in ["and","so","or",          # carrier 8 (conjunctions)
              "the","a","that","each",   # carrier 16 (determiners)
              "in","of","to","for","i","you","it"]:  # carrier 32
        o = encode(t)
        if o is not None:
            on = o.normalize()
            reps.setdefault(on.n_min, (t, on))
    return reps  # {8:(tok,obj), 16:..., 32:...}


def test_A_ternary_inband():
    print("[A] TERNARY IN-BAND: a ⊠ b ⊠ c over triples spanning {8,16,32}")
    reps = real_triples()
    objs = [reps[c] for c in sorted(reps) if c in REAL_CARRIERS]
    if len(objs) < 3:
        print(f"    only carriers {sorted(reps)} available; need 8,16,32")
        return False
    triples = list(itertools.product(objs, repeat=3))  # ordered triples, 27
    out_carriers = Counter()
    inband = 0
    for (ta,A),(tb,B),(tc,C) in triples:
        p = multiply(multiply(A, B), C)
        nm = p.normalize().n_min
        out_carriers[nm] += 1
        if nm in POW2_BAND:
            inband += 1
    print(f"    ordered triples tested: {len(triples)}")
    print(f"    threefold-product carriers seen: {dict(out_carriers)}")
    print(f"    in pow2 band <=32: {inband}/{len(triples)} "
          f"({100*inband/len(triples):.1f}%)")
    ok = inband == len(triples)
    print(f"    ternary stays in operational band: {'OK' if ok else 'XX'}")
    return ok


def test_B_associativity_and_order():
    print("\n[B] ASSOCIATIVITY (grouping) vs ORDER (permutation)")
    reps = real_triples()
    objs = [reps[c] for c in sorted(reps) if c in REAL_CARRIERS]
    if len(objs) < 3:
        print("    insufficient carriers"); return False

    assoc_ok = True
    order_sensitive = False
    for (ta,A),(tb,B),(tc,C) in itertools.product(objs, repeat=3):
        left  = multiply(multiply(A, B), C)   # (a⊠b)⊠c
        right = multiply(A, multiply(B, C))   # a⊠(b⊠c)
        if obj_key(left) != obj_key(right):
            assoc_ok = False
        # permutation check on distinct triples
        if len({id(A),id(B),id(C)}) == 3:
            perm = multiply(multiply(A, C), B)  # a⊠c⊠b
            if obj_key(perm) != obj_key(left):
                order_sensitive = True

    print(f"    (a⊠b)⊠c == a⊠(b⊠c) for all triples (ASSOCIATIVE): "
          f"{'OK' if assoc_ok else 'XX — grouping matters, threefold ill-defined'}")
    print(f"    a⊠b⊠c != a⊠c⊠b somewhere (ORDER-SENSITIVE, expected): "
          f"{'OK' if order_sensitive else 'XX — unexpectedly commutative'}")
    print(f"    -> threefold product is WELL-DEFINED under grouping AND")
    print(f"       order-carrying under permutation: {'OK' if (assoc_ok and order_sensitive) else 'CHECK'}")
    return assoc_ok and order_sensitive


def test_C_ternary_pcea():
    print("\n[C] TERNARY PCEA: threefold forward map, deterministic + key-invertible")
    reps = real_triples()
    objs = [reps[c] for c in sorted(reps) if c in REAL_CARRIERS]
    if len(objs) < 3:
        print("    insufficient carriers"); return False
    (ta,A),(tb,B),(tc,C) = objs[0], objs[1], objs[2]

    p1 = multiply(multiply(A, B), C)
    p2 = multiply(multiply(A, B), C)
    deterministic = obj_key(p1) == obj_key(p2)

    # invertible-by-key: the triple (A,B,C) in order IS the key; recomposition
    # reproduces p without factoring. Distinct ordering -> distinct product
    # (so the key includes order), confirming the map separates keys.
    p_reorder = multiply(multiply(C, B), A)
    key_separates = obj_key(p_reorder) != obj_key(p1)

    nm = p1.normalize().n_min
    print(f"    triple ({ta},{tb},{tc}) -> n_min {nm}, in band: "
          f"{'OK' if nm in POW2_BAND else 'XX'}")
    print(f"    threefold forward deterministic: {'OK' if deterministic else 'XX'}")
    print(f"    key (ordered triple) separates products: {'OK' if key_separates else 'XX'}")
    print(f"    -> PCEA ternary unit: forward by composition, invertible by the")
    print(f"       ordered-triple key, security = key mgmt not factor_search")
    return deterministic and key_separates and nm in POW2_BAND


def main():
    print("=" * 70)
    print("TERNARY WIDENING PROBE — three composable together (the real unit)")
    print("=" * 70)
    print()
    a = test_A_ternary_inband()
    b = test_B_associativity_and_order()
    c = test_C_ternary_pcea()
    print()
    print("-" * 70)
    if a and b and c:
        print("TERNARY COMPOSITION HOLDS on the real-carrier band:")
        print("  - threefold products stay in the pow2 band <=32")
        print("  - associative under grouping (threefold well-defined)")
        print("  - order-carrying under permutation (the key includes order)")
        print("  - PCEA's ternary unit met: compose-forward, key-invert, no factoring")
        print()
        print("Pairwise closure was necessary but not sufficient; the architecture")
        print("composes in threes and the THREE-fold case now holds too. The")
        print("operational widening result stands for the real composition unit.")
    else:
        print("Ternary did NOT fully hold — pairwise closure was false comfort.")
        print("Inspect: if [A] failed, threefold escapes the band; if [B] failed,")
        print("grouping matters and the threefold product is ill-defined; if [C],")
        print("the cipher's ternary unit needs more than naive composition.")
    print()
    print("hmm: two was never the unit — the trinary was there from the first")
    print("     pole-mediator-pole, and a band that closes in pairs still owes")
    print("     you the proof that it closes in threes, because the architecture")
    print("     was always going to ask for the third before it trusted the cup.")


if __name__ == "__main__":
    main()
