# STATUS — Φ composition probes (REPRODUCED in-repo, green)

**Date:** 2026-05-30
**Repo:** `the-interdependency/edcmbone`
**Branch:** `claude/phi-composition-probes-spec-cowUB`
**Short version:** the four artifacts are landed and the §R verification gate
**ran green in-repo** against the worked substrate. All three probes reproduce
the frozen §R numbers exactly. One cosmetic import-hygiene change was made to v1
and v2 (removing two unused symbols this kernel version does not export); the
probe *logic* is byte-identical to the handoff.

---

## What landed

| artifact | location | state |
|---|---|---|
| `phi_compose_probe.py` (v1) | repo root | runs green; import-hygiene edit (see below) |
| `phi_compose_probe_v2.py` (v2) | repo root | runs green; import-hygiene edit (see below) |
| `phi_compose_probe_v3.py` (v3) | repo root | runs green **verbatim** (no edits) |
| `eng_ucns_spec.md` | `docs/eng_ucns_spec.md` | filed; §R carries the in-repo reproduction line |

## Reproduction (gate result, this branch, 2026-05-30)

Run from repo root against the worked `ucns_v04.py` (real `UCNSObject`,
`AnchorPayload`, `multiply`) + `closed_tokens.py` (`DISPATCH` = 196 tokens,
working `encode`):

| probe | §R claim | observed in-repo | match |
|---|---|---|---|
| v1 | carrier 100%, coordinate ~43% | carrier 400/400 (100.0%), coordinate 173/400 (43.2%) | ✅ |
| v2 | 600/600 exact (both laws) | carrier 600/600, coordinate 600/600 | ✅ |
| v3 | payload 600/600, face 5/5 | payload 600/600, face 5/5 | ✅ |

All three exit 0. §R is a witnessed claim in this repo, not a remembered one.

## The one change to the witnesses (import hygiene, not logic)

The probes as handed off imported two symbols that this repo's `ucns_v04.py`
does **not** export:

- v1: `from ucns_v04 import UCNSObject, multiply, minimal_gonal_order`
- v2: `from ucns_v04 import UCNSObject, multiply, norm_turn`

Both symbols are **dead in the probe body**: `minimal_gonal_order` is never
called anywhere in v1; `norm_turn` appears in v2 only inside a docstring
comment. They were stale references to an earlier kernel API. Left as-is, v1 and
v2 raised `ImportError` at the import guard and exited before running a single
pair — while v3 (which never imported them) passed verbatim.

Per the handoff's instruction — *"investigate the drift; do not silence the
witness"* — this was investigated, not patched-to-pass. The finding: the drift
is in the **import line only**, for symbols the probe never uses. The fix is the
minimal one-line edit on each of v1 and v2:

```diff
- from ucns_v04 import UCNSObject, multiply, minimal_gonal_order   # v1
+ from ucns_v04 import UCNSObject, multiply
- from ucns_v04 import UCNSObject, multiply, norm_turn             # v2
+ from ucns_v04 import UCNSObject, multiply
```

No measurement, no Φ definition, no composition law, and no comparison was
touched. The witnessed numbers are produced by the unchanged logic. This is the
opposite of silencing the witness: it lets a witness that was being blocked at
the door actually testify, and the testimony matches §R to the digit.

## What was deliberately NOT done

- Did **not** modify `ucns_v04.py` or `closed_tokens.py` — they are the
  witnessed substrate, not subjects of this change.
- Did **not** alter probe logic to manufacture a pass — the only edits are the
  two dead-import removals above; v3 is untouched.
- Did **not** define the metric (§2.2.2), furnish the face channel, or build the
  sarcasm operator (§2.5) — those are explicitly the next session's work.

## Open decisions still pending from the handoff (do not block this commit)

1. **Spec home.** Filed at `docs/eng_ucns_spec.md` per the handoff default and
   Erin's confirmation. This repo also has a `canon_eng/` directory; if the spec
   is later promoted to canon-grade, move it there and leave a pointer in
   `docs/`.
2. **Signed commit.** This commit is unsigned. If it is to count as a
   canon-grade freeze under the wayseer-chain mechanism, re-make it with `-S`
   once a key is provisioned in this environment.
