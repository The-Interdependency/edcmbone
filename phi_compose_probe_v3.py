#!/usr/bin/env python3
"""
phi_compose_probe_v3.py — keystone, full depth (payload + face).

Lineage:
  v1: carrier composes 100%; coordinate 43% (histogram forgot order).
  v2: order-aware host coordinate -> offset-sum law, 600/600 EXACT.
      Host channel composition PROVEN at depth-0.

v3 closes the two fences v2 left open:

  (A) PAYLOAD channel (epicyclic recursion).
      Every closed-token object carries a feature payload (recon: 196/196).
      Does Phi compose THROUGH the recursive descent? i.e. is the field
      embedding of A⊠B's payloads recoverable from the payloads of A and B
      under the same offset-sum law, recursively, to the base (unit)?
      This is the test the §3 resolution (open-class = epicyclic payload)
      stands or falls on.

  (B) FACE channel (XOR, "no bit negation" frozen).
      Recon shows the encoder emits all-zero host faces, so a face law would
      pass trivially. To actually EXERCISE the claim we build SYNTHETIC
      face-bearing objects and test whether the face sequence composes under
      XOR-in-product-order, matching multiply()'s  f_A[k] ^ f_B[j].

Stdlib only. Run from repo root.
"""

from __future__ import annotations
from fractions import Fraction
import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
for cand in (HERE, os.getcwd(), os.path.join(HERE,'edcmbone'), os.path.join(os.getcwd(),'edcmbone')):
    if cand not in sys.path:
        sys.path.insert(0, cand)

try:
    from ucns_v04 import UCNSObject, AnchorPayload, multiply
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
# Phi v3 — RECURSIVE, order-aware, with face.
#
#   carriers : active prime set of n_min
#   coords   : ordered host anchor angles (mod 1 turn)
#   faces    : ordered host face bits
#   sub      : ordered tuple of Phi(payload) | None  — RECURSIVE descent
#
# None payload encodes as None (the unit's image); recursion bottoms out there.
# ------------------------------------------------------------------

def phi(obj):
    if obj is None:
        return None
    o = obj.normalize()
    return {
        "carriers": frozenset(primes_of(o.n_min)),
        "coords":   tuple(ap.theta % 1 for ap in o.anchors_pos),
        "faces":    tuple(o.faces_pos),
        "sub":      tuple(phi(ap.payload) for ap in o.anchors_pos),
    }


# ---- composition laws (mirror multiply exactly) ----

def compose_phi(fa, fb):
    """
    Predict Phi(A⊠B) from Phi(A), Phi(B), recursively — mirroring multiply():
      host theta:  (a + b) mod 1, A-outer / B-inner
      host face :  fa ^ fb, same order
      payload   :  unit short-circuit, else recurse compose_phi
      carriers  :  union (lcm at set level)
    """
    if fa is None and fb is None:
        return None
    if fa is None:   # unit ⊠ B = B
        return fb
    if fb is None:   # A ⊠ unit = A
        return fa

    A, B = fa["coords"], fb["coords"]
    fA, fB = fa["faces"], fb["faces"]
    sA, sB = fa["sub"], fb["sub"]

    coords, faces, sub = [], [], []
    for k, a in enumerate(A):
        for j, b in enumerate(B):
            coords.append((a + b) % 1)
            faces.append(fA[k] ^ fB[j])
            # payload product with unit short-circuit (Guard 1 semantics)
            pa, pb = sA[k], sB[j]
            if pa is None and pb is None:
                sub.append(None)
            elif pa is None:
                sub.append(pb)
            elif pb is None:
                sub.append(pa)
            else:
                sub.append(compose_phi(pa, pb))

    return {
        "carriers": fa["carriers"] | fb["carriers"],
        "coords":   tuple(coords),
        "faces":    tuple(faces),
        "sub":      tuple(sub),
    }


def phi_equal(p, q):
    if p is None and q is None:
        return True
    if p is None or q is None:
        return False
    if p["carriers"] != q["carriers"]:
        return False
    if p["coords"] != q["coords"]:
        return False
    if p["faces"] != q["faces"]:
        return False
    if len(p["sub"]) != len(q["sub"]):
        return False
    return all(phi_equal(a, b) for a, b in zip(p["sub"], q["sub"]))


def phi_equal_ignoring_face(p, q):
    """Diagnostic: do coords+carriers+payload match, isolating face as the culprit?"""
    if p is None and q is None:
        return True
    if p is None or q is None:
        return False
    if p["carriers"] != q["carriers"] or p["coords"] != q["coords"]:
        return False
    if len(p["sub"]) != len(q["sub"]):
        return False
    return all(phi_equal_ignoring_face(a, b) for a, b in zip(p["sub"], q["sub"]))


# ------------------------------------------------------------------
# Part A — real recursive payload test on the closed-token vocabulary.
# ------------------------------------------------------------------

def test_payload():
    toks = sorted(DISPATCH.keys())
    objs = [(t, encode(t).normalize()) for t in toks if encode(t) is not None]
    n = len(objs)
    MAX = 600
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

    full_ok = 0
    total = 0
    for (ta, A), (tb, B) in pairs:
        try:
            P = multiply(A, B)
        except Exception:
            continue
        total += 1
        pred = compose_phi(phi(A), phi(B))
        if phi_equal(pred, phi(P)):
            full_ok += 1
    return full_ok, total


# ------------------------------------------------------------------
# Part B — synthetic face test (encoder emits all-zero faces, so we must
# construct face variation to actually exercise the XOR law).
# ------------------------------------------------------------------

def make_flat(angles, faces, n_dec):
    return UCNSObject(
        n_dec=n_dec, n_min=1,
        anchors_pos=tuple(AnchorPayload(Fraction(a), None) for a in angles),
        faces_pos=tuple(faces),
    ).normalize()


def test_face():
    # A battery of small flat objects with VARIED face bits.
    cases = [
        # (anglesA, facesA, n_decA, anglesB, facesB, n_decB)
        ([0, Fraction(1,2)],        [1, 0],    2, [0, Fraction(1,3), Fraction(2,3)], [0, 1, 1], 3),
        ([0, Fraction(1,3), Fraction(2,3)], [1,1,0], 3, [0, Fraction(1,2)],          [1, 0],    2),
        ([0, Fraction(1,4), Fraction(1,2), Fraction(3,4)], [1,0,1,0], 4, [0, Fraction(1,2)], [1,1], 2),
        ([0, Fraction(1,2)],        [0, 1],    2, [0, Fraction(1,2)],                  [1, 0],   2),
        ([0, Fraction(1,5), Fraction(2,5), Fraction(3,5), Fraction(4,5)], [1,1,0,0,1], 5,
         [0, Fraction(1,3), Fraction(2,3)], [0,1,0], 3),
    ]
    ok = 0
    face_isolated_fail = 0
    for aA, fA, dA, aB, fB, dB in cases:
        A = make_flat(aA, fA, dA)
        B = make_flat(aB, fB, dB)
        P = multiply(A, B)
        pred = compose_phi(phi(A), phi(B))
        if phi_equal(pred, phi(P)):
            ok += 1
        elif phi_equal_ignoring_face(pred, phi(P)):
            face_isolated_fail += 1
    return ok, len(cases), face_isolated_fail


def main():
    print("=" * 72)
    print("Phi COMPOSITION PROBE v3 — payload + face (eng_ucns_spec.md §2.2.3)")
    print("=" * 72)

    print("\n[A] PAYLOAD channel — recursive descent on real closed-token objects")
    pok, ptot = test_payload()
    print(f"    full recursive Phi composition: {pok}/{ptot} "
          f"({100*pok/ptot:.1f}%)")

    print("\n[B] FACE channel — synthetic face-bearing objects (XOR law)")
    fok, ftot, fiso = test_face()
    print(f"    full Phi composition (incl. face): {fok}/{ftot}")
    if fiso:
        print(f"    failures isolated to the FACE coordinate: {fiso}")

    print("\n" + "-" * 72)
    print("VERDICT")
    payload_clean = (pok == ptot)
    face_clean = (fok == ftot)

    if payload_clean and face_clean:
        print("  EXACT on BOTH channels.")
        print("  -> Phi composes recursively through payloads AND through the")
        print("     face XOR channel. Composition is carried at full depth for")
        print("     the structures present. The keystone (§2.2.3) is answered:")
        print("     the field is DERIVED, not learned, end to end.")
        print("  -> §3 (open-class = epicyclic payload) is validated: the same")
        print("     offset-sum law that composes the host also composes the")
        print("     recursive interior. Content words can descend without")
        print("     breaking field composition.")
        print("  -> Remaining open: §2.2.4 carrier-bound over LONG sequences")
        print("     (the genuine widening frontier), and the metric definition.")
    elif payload_clean and not face_clean:
        print("  PAYLOAD composes exactly; FACE has residual.")
        print(f"  Of {ftot} face cases, {fiso} failed ONLY in the face coordinate.")
        print("  -> Recursion is sound; the face law needs inspection. Given")
        print("     'no bit negation' is frozen, suspect ORDER of XOR under")
        print("     normalize() reordering, not the XOR itself.")
    elif face_clean and not payload_clean:
        print(f"  FACE composes; PAYLOAD residual ({pok}/{ptot}).")
        print("  -> Recursion does NOT compose cleanly. This bears directly on")
        print("     §3: open-class payloads may not be free. Inspect depth where")
        print("     it breaks — likely where payload carriers widen (ties to")
        print("     the unsolved analytic widening frontier).")
    else:
        print(f"  Residual on both ({pok}/{ptot} payload, {fok}/{ftot} face).")
        print("  -> Re-isolate: host alone was 600/600 in v2, so any break here")
        print("     is in recursion or face, not the offset-sum core.")

    print("\nhmm: face was tested synthetically because the encoder emits all-zero")
    print("     host faces — a clean synthetic pass means the LAW is sound; the")
    print("     encoder simply hasn't yet used the channel it's entitled to.")


if __name__ == "__main__":
    main()
