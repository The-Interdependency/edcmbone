#!/usr/bin/env python3
"""
phi_compose_probe.py — The keystone test.

Question (eng_ucns_spec.md §2.2.3): does the field embedding Phi compose?
i.e. is Phi(A ⊠ B) recoverable from Phi(A) and Phi(B) by a FIXED operation,
with no per-pair tuning and no training step?

This script does NOT assume the right Phi. It proposes the simplest honest
candidate, then tests three candidate composition laws against a battery of
real A ⊠ B pairs built from the existing closed-token encoder. It reports
which (if any) law holds EXACTLY, holds approximately, or fails.

Three outcomes, all informative:
  - EXACT law found    -> Layer 2 inherits the algebra; "derived not learned" holds.
  - APPROX / lossy      -> field is a readout; weaken the claim honestly.
  - NO law              -> Phi is the wrong abstraction; rethink the embedding.

Run from the repo root (where ucns_v04.py and closed_tokens.py live):
    python phi_compose_probe.py
Termux-ready. Stdlib only.
"""

from __future__ import annotations
from fractions import Fraction
from math import gcd
from functools import reduce
from itertools import product as iproduct
import sys, os

# Make the repo importable regardless of where this file sits.
HERE = os.path.dirname(os.path.abspath(__file__))
for cand in (HERE, os.getcwd(), os.path.join(HERE,'edcmbone'), os.path.join(os.getcwd(),'edcmbone')):
    if cand not in sys.path:
        sys.path.insert(0, cand)

try:
    from ucns_v04 import UCNSObject, multiply
    from closed_tokens import encode, DISPATCH
except ImportError as e:
    print("FATAL: run this from the repo root (needs ucns_v04.py + closed_tokens.py).")
    print(f"  import error: {e}")
    sys.exit(1)


# ------------------------------------------------------------------
# Phi — the simplest honest candidate embedding.
#
# A UCNS object's intrinsic geometry lives in its host anchors (mod 1 turn)
# and the carrier n_min they sit on. The simplest field coordinate that is
# DERIVED (not learned) and respects the spec's "carrier = identity" rule:
#
#   For each prime p dividing n_min, record the multiset of anchor residues
#   {round(theta * p) mod p} — i.e. where the anchors land on the p-gon
#   sub-lattice. Phi is the prime-indexed dict of these residue-count vectors.
#
# This is deliberately minimal: no payload descent (depth-0 host probe first),
# no face channel (independent by construction). If composition fails even
# here, deeper Phi won't rescue it; if it holds, we earn the right to enrich.
# ------------------------------------------------------------------

def primes_of(n: int):
    """Distinct prime factors of n."""
    out, d = [], 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def phi(obj: UCNSObject):
    """
    Field embedding: { p : tuple(count of anchors at each residue k mod p) }.
    Host-level only, anchors projected to [0,1) turns.
    """
    o = obj.normalize()
    thetas = [ap.theta % 1 for ap in o.anchors_pos]
    n = o.n_min
    feat = {}
    for p in primes_of(n) or [1]:
        counts = [0] * p
        for t in thetas:
            # residue on the p-gon: nearest lattice index
            k = round(float(t) * p) % p
            counts[k] += 1
        feat[p] = tuple(counts)
    return feat


# ------------------------------------------------------------------
# Candidate composition laws: predict Phi(A⊠B) from Phi(A), Phi(B).
# Each returns a dict in the same {p: tuple} format, or None if undefined.
# ------------------------------------------------------------------

def _align(va, vb):
    """Tile two residue vectors to a common length (lcm) for elementwise ops."""
    la, lb = len(va), len(vb)
    L = la * lb // gcd(la, lb)
    A = [va[i % la] for i in range(L)]
    B = [vb[i % lb] for i in range(L)]
    return A, B, L


def law_lcm_merge(fa, fb):
    """Carrier-wise union; on shared primes, tile-and-add residue counts."""
    keys = set(fa) | set(fb)
    out = {}
    for p in keys:
        if p in fa and p in fb:
            A, B, L = _align(fa[p], fb[p])
            out[p] = tuple(A[i] + B[i] for i in range(L))
        else:
            out[p] = fa.get(p, fb.get(p))
    return out


def law_concat(fa, fb):
    """Concatenate residue vectors on shared primes (ordered, like ⊠)."""
    keys = set(fa) | set(fb)
    out = {}
    for p in keys:
        if p in fa and p in fb:
            out[p] = tuple(fa[p]) + tuple(fb[p])
        else:
            out[p] = fa.get(p, fb.get(p))
    return out


def law_tensor(fa, fb):
    """Outer-product counts on shared primes, flattened (multiplicative mix)."""
    keys = set(fa) | set(fb)
    out = {}
    for p in keys:
        if p in fa and p in fb:
            out[p] = tuple(a * b for a in fa[p] for b in fb[p])
        else:
            out[p] = fa.get(p, fb.get(p))
    return out


LAWS = {
    "lcm_merge": law_lcm_merge,
    "concat":    law_concat,
    "tensor":    law_tensor,
}


# ------------------------------------------------------------------
# Comparison. A law "holds exactly" on a pair if its prediction equals
# the actual Phi(A⊠B) on the SHARED prime keys (the dimensions both share).
# We report exact-match rate and the carrier-key match separately.
# ------------------------------------------------------------------

def feats_equal(f1, f2):
    if set(f1) != set(f2):
        return False
    return all(f1[p] == f2[p] for p in f1)


def shared_key_equal(pred, actual):
    """Do the predicted carriers match the actual carrier set?"""
    return set(pred) == set(actual)


# ------------------------------------------------------------------
# Battery: build real objects from the closed-token vocabulary.
# ------------------------------------------------------------------

def build_battery(max_pairs=400):
    toks = sorted(DISPATCH.keys())
    objs = []
    for t in toks:
        o = encode(t)
        if o is not None:
            objs.append((t, o.normalize()))
    pairs = []
    # Diverse sample: stride through the vocabulary so we mix classes.
    n = len(objs)
    step = max(1, (n * n) // max_pairs)
    c = 0
    for i in range(n):
        for j in range(n):
            if (i * n + j) % step == 0:
                pairs.append((objs[i], objs[j]))
                c += 1
                if c >= max_pairs:
                    return objs, pairs
    return objs, pairs


def main():
    print("=" * 72)
    print("Phi COMPOSITION PROBE — the keystone (eng_ucns_spec.md §2.2.3)")
    print("=" * 72)

    objs, pairs = build_battery()
    print(f"\nVocabulary objects encoded: {len(objs)}")
    print(f"Test pairs (A,B): {len(pairs)}")
    print(f"Candidate Phi: prime-indexed residue-count vectors (host-level, depth-0)\n")

    results = {name: {"exact": 0, "carrier": 0} for name in LAWS}
    total = 0

    for (ta, A), (tb, B) in pairs:
        try:
            P = multiply(A, B)
        except Exception:
            continue
        fa, fb, fp = phi(A), phi(B), phi(P)
        total += 1
        for name, law in LAWS.items():
            pred = law(fa, fb)
            if shared_key_equal(pred, fp):
                results[name]["carrier"] += 1
            if feats_equal(pred, fp):
                results[name]["exact"] += 1

    print("-" * 72)
    print(f"{'law':<12} {'exact match':>16} {'carrier-set match':>20}")
    print("-" * 72)
    for name in LAWS:
        e = results[name]["exact"]
        c = results[name]["carrier"]
        print(f"{name:<12} {e:>6}/{total:<6} ({100*e/total:5.1f}%) "
              f"{c:>6}/{total:<6} ({100*c/total:5.1f}%)")
    print("-" * 72)

    # Verdict.
    best = max(LAWS, key=lambda k: results[k]["exact"])
    be = results[best]["exact"]
    bc = results[best]["carrier"]
    print("\nVERDICT")
    if be == total:
        print(f"  EXACT law found: '{best}' holds on all {total} pairs.")
        print("  -> Phi composes. Layer 2 inherits the algebra. 'Derived not")
        print("     learned' is defensible at depth-0. Next: enrich Phi with")
        print("     payload descent and re-run; then define the metric.")
    elif bc == total and be < total:
        print(f"  CARRIER law holds ('{best}': dimensions compose exactly),")
        print(f"  but residue counts do not ({be}/{total} exact).")
        print("  -> The FIELD (which primes are active) composes; the COORDINATES")
        print("     within each prime do not under this Phi. Field is partially")
        print("     derived. Either refine the coordinate, or accept a readout.")
    elif be > 0:
        print(f"  PARTIAL: '{best}' holds on {be}/{total}. A law exists on a")
        print("  subdomain. Characterize where it holds vs. fails before claiming.")
    else:
        print("  NO clean law at depth-0 under this Phi.")
        print("  -> This Phi is the wrong abstraction, OR composition lives in the")
        print("     payload/face channel this probe ignored. Informative either way:")
        print("     the host-residue picture alone does not carry composition.")
    print("\nhmm: depth-0 host probe only. Payload and face channels untested here")
    print("     by design — a clean 'no' here scopes the next probe, a 'yes' earns")
    print("     the right to go deeper.")


if __name__ == "__main__":
    main()
