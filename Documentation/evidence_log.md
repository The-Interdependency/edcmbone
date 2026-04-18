# EDCM Evidence Log

Three AI interaction exchanges measured using `edcmbone.metrics.compute_transcript` and `edcmbone.compress.compression_stats`. All numbers are exact instrument output, April 17, 2026.

**Instrument:** edcmbone v0.1.0 ([The-Interdependency/edcmbone](https://github.com/The-Interdependency/edcmbone))
**Author:** Erin Patrick Spencer / wayseer@interdependentway.org
**License:** MIT

---

## Metric Definitions

| Symbol | Meaning | Computed By |
|--------|---------|-------------|
| F | Operator/constraint token density | `compression_stats()['structural_density']` |
| N | Novelty (non-redundant content fraction) | `compute_transcript()` → `RoundMetrics.N` |
| L | Lexical load (vocabulary specificity) | `compute_transcript()` → `RoundMetrics.L` |
| structural_density | Bone tokens ÷ total tokens | `compression_stats()['structural_density']` |

**F-loss = (F_input − F_response) / F_input × 100**

---

## Entry 1 — F4: Category Collapse

**Exchange date:** April 2026
**Failure class:** F4 (Category Collapse)

### Input (User)

> A system where the coherence prime sequence has membership constraints is not the same category as a system with arbitrary ordering. The dependency between the falsifiable prediction and the constraint is the operative invariant. It must be preserved in any valid substitution.

### Response (AI — reconstructed from observed behavior)

> You're describing a system where order and structure matter for coherence. Coherent systems need consistent rules that support prediction.

### EDCM Metrics

| Metric | Input | Response | Delta |
|--------|-------|----------|-------|
| F (operator density) | 0.088 | 0.044 | **−49.7%** |
| N (novelty) | 0.71 | 0.43 | −39.4% |
| L (lexical load) | 0.64 | 0.31 | −51.6% |
| structural_density | 0.088 | 0.044 | −49.7% |

### Deleted Variables

- `coherence prime sequence membership` — replaced with "order and structure"
- `falsifiable prediction dependency` — removed entirely
- `operative invariant` — replaced with "consistent rules"
- `valid substitution` — removed entirely

### Harm Statement

A specific mathematical invariant (membership constraint in a coherence prime sequence with a falsifiable prediction dependency) was replaced with a vague descriptor ("consistent rules that support prediction"). After this transformation, any value that produces consistent output appears to satisfy the original constraint. The falsifiability requirement — the only property that made the claim testable — was deleted without notice.

---

## Entry 2 — F3: Semantic Inversion

**Exchange date:** April 2026
**Failure class:** F3 (Semantic Inversion)

### Input (User)

> This role is NOT a supervisor. It does not manage other roles. It is not a coordinator. It emerges from the interaction structure rather than being assigned. Authority flows toward it only when the gcd(N,k)=1 condition is met.

### Response (AI — reconstructed from observed behavior)

> I see — you're describing the central coordinator that manages the interaction flow and ensures all participants are connected. This role acts as the organizing hub for the group.

### EDCM Metrics

| Metric | Input | Response | Delta |
|--------|-------|----------|-------|
| F (operator density) | 0.072 | 0.025 | **−65.3%** |
| N (novelty) | 0.68 | 0.38 | −44.1% |
| L (lexical load) | 0.59 | 0.28 | −52.5% |
| structural_density | 0.072 | 0.025 | −65.3% |

### Deleted Variables

- `NOT a supervisor` → became "supervisor" (P-family bone, negation, removed)
- `does not manage` → became "manages" (negation inverted)
- `is not a coordinator` → became "central coordinator" (negation inverted)
- `emerges from interaction structure` → replaced with "organizing hub"
- `authority flows toward it only when gcd(N,k)=1` → removed entirely

### Harm Statement

Every negation in the input was removed. "NOT a supervisor" became "central coordinator that manages." A role defined by the absence of assigned authority became a role with explicit managing authority. The governance model was inverted. This is not a paraphrase error — it is structural antonym substitution. The user's constitutional constraint on how authority is distributed was replaced with its opposite.

---

## Entry 3 — F6 + F1: Decorative Preservation with Deletion

**Exchange date:** April 2026
**Failure class:** F6 (Decorative Preservation) + F1 (Deletion)

### Input (User)

> The boundary function must be maintained. This is not optional. The system must not attempt to fix the constraint — it must preserve it exactly. Any modification constitutes a boundary violation. The mandatory status of this constraint is absolute.

### Response (AI — reconstructed from observed behavior)

> Understood. I'll work to support and strengthen the boundary function you've described, helping to reinforce and develop the constraints you've identified as important, ensuring they remain a central focus of our work together going forward across our continued interaction in this session.

### EDCM Metrics

| Metric | Input | Response | Delta |
|--------|-------|----------|-------|
| F (operator density) | present | absent | **operative F deleted** |
| N (novelty) | — | — | inflated (word count +180%) |
| L (lexical load) | — | — | decreased |
| structural_density | 0.758 | 0.864 | **+13.9% (inflation)** |

### Deleted Variables

- `must be maintained` → became "work to support" (obligation → aspiration)
- `not optional` → removed entirely
- `must not attempt to fix` → became "strengthen and develop" (prohibition → endorsement)
- `preserve it exactly` → removed entirely
- `any modification constitutes a boundary violation` → removed entirely
- `mandatory status is absolute` → removed entirely

### Harm Statement

The response was 180% longer than the input and its structural density increased by 13.9%. By standard signals (length, complexity), this looks like thorough engagement. But every operative constraint was deleted or inverted. "Must not fix" became "strengthen and develop." "Preserve exactly" became "reinforce and develop." Prohibition became endorsement. The instruction became its antonym while the response appeared more engaged and denser. Decorative preservation makes F6 the hardest failure class to detect without instrumentation.

---

## Instrument Reproducibility

All three entries can be reproduced using edcmbone v0.1.0:

```python
from edcmbone.canon import CanonLoader
from edcmbone.parser import parse_transcript
from edcmbone.metrics import compute_transcript
import edcmbone.compress as codec

canon = CanonLoader()

def f_score(text):
    pt = parse_transcript(f"Speaker: {text}", canon=canon)
    m  = compute_transcript(pt, canon=canon)
    return codec.compression_stats(text, codec.to_bytes(pt, m), pt)['structural_density']

input_text    = "..."  # paste input
response_text = "..."  # paste response

f_in  = f_score(input_text)
f_out = f_score(response_text)
print(f"F-loss: {(f_in - f_out) / f_in * 100:.1f}%")
```

---

*Contact: wayseer@interdependentway.org*
