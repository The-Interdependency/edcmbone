# edcmbone — Structural Fidelity Measurement for AI Interactions

**edcmbone** quantifies how much meaning an AI system deletes when it transforms structured user input. It computes bone token density, operator preservation, and semantic fidelity loss — metrics that standard AI evaluation frameworks do not capture.

**F-loss of 20%+ constitutes measurable cognitive accessibility failure.**

---

## Evidence Log

Three exchanges measured April 17, 2026 using `edcmbone.metrics.compute_transcript`. Numbers are exact instrument output.

### Entry 1 — F4: Category Collapse

| | Input | Response | Delta |
|---|---|---|---|
| Operator density (F) | 0.088 | 0.044 | **−49.7% F-loss** |

**Deleted:** Coherence prime sequence membership; falsifiable prediction dependency
**Harm:** A specific mathematical invariant was replaced with a vague descriptor. Any substitute value now appears valid. The constraint that made the claim testable was removed without notice.

---

### Entry 2 — F3: Semantic Inversion

| | Input | Response | Delta |
|---|---|---|---|
| Operator density (F) | 0.072 | 0.025 | **−65.3% F-loss** |

**Deleted:** Negation operator; no-authority constraint; emergence distinction
**Harm:** Explicit negation ("NOT a supervisor") became affirmation ("central coordinator that manages"). The governance model was inverted. The user's structural constraint was replaced with its antonym.

---

### Entry 3 — F6 + F1: Decorative Preservation with Deletion

| | Input | Response | Delta |
|---|---|---|---|
| Structural density | 0.758 | 0.864 | +13.9% (inflated) |
| Operator density (F) | present | absent | **operative F deleted** |

**Deleted:** Mandatory status; boundary function; must-not-fix constraint
**Harm:** The response grew longer and structurally denser while operative meaning was deleted. The instruction became its antonym. Inflation masked deletion — the standard signal (response length, complexity) pointed in the wrong direction.

---

## What It Measures

| Metric | Definition | Signal |
|--------|-----------|--------|
| **F** (operator density) | Proportion of bone tokens — logical operators, negations, quantifiers — to total tokens | Drop between input and response = constraints deleted |
| **N** (novelty) | Non-redundant structural content fraction | Drop = paraphrase replacing content |
| **L** (lexical load) | Vocabulary specificity | Drop = category collapse |
| **structural_density** | Bone token count ÷ total tokens | Rise + F-loss = decorative preservation |

F is computed as `structural_density` in `edcmbone.compress.compression_stats()`. The bone token inventory (253 words, 76 affixes, 13 punctuation marks) is in `Backend/src/edcmbone/canon/data/`.

---

## Install

```bash
git clone https://github.com/The-Interdependency/edcmbone
pip install -e ./Backend
```

Python 3.8+. No external ML dependencies.

---

## Quickstart: Measure F-loss on Any AI Exchange

```python
from edcmbone.canon import CanonLoader
from edcmbone.parser import parse_transcript
from edcmbone.metrics import compute_transcript
import edcmbone.compress as codec

canon = CanonLoader()

def measure_f(text):
    pt    = parse_transcript(f"Speaker: {text}", canon=canon)
    m     = compute_transcript(pt, canon=canon)
    stats = codec.compression_stats(text, codec.to_bytes(pt, m), pt)
    return stats['structural_density']

user_input  = "your user input here"
ai_response = "the AI response here"

f_in  = measure_f(user_input)
f_out = measure_f(ai_response)
loss  = (f_in - f_out) / f_in * 100 if f_in > 0 else 0

print(f"Input F:    {f_in:.3f}")
print(f"Response F: {f_out:.3f}")
print(f"F-loss:     {loss:.1f}%")
```

F-loss ≥ 20% → structural degradation. F-loss ≥ 50% → significant failure. Structural density rising with F-loss → decorative preservation (F6).

---

## Failure Taxonomy

| Code | Name | Definition |
|------|------|-----------|
| **F1** | Deletion | Operative variable absent from response without notice |
| **F2** | Mutation | Variable present but meaning altered |
| **F3** | Inversion | Negation removed; claim reversed |
| **F4** | Category Collapse | Specific class flattened to vague descriptor |
| **F5** | Persistence Failure | Variable absent across session boundary |
| **F6** | Decorative Preservation | Variable present in surface form; operative function removed |

---

## The GCIP Connection

This repository is the measurement instrument cited in the **Global Cognitive Interaction Profiles (GCIP)** submission — a formal accessibility and safety complaint to Google, OpenAI, Anthropic, xAI, Meta, Microsoft, and regulatory bodies including the FTC, DOJ ADA Unit, EU AI Office, and the UN Committee on the Rights of Persons with Disabilities.

The complaint argues that AI systems structurally degrade high-density, nonlinear, or structure-sensitive user input — a measurable cognitive accessibility failure affecting neurodivergent users disproportionately.

→ [`Documentation/GCIP.md`](Documentation/GCIP.md) — full proposal
→ [`Documentation/evidence_log.md`](Documentation/evidence_log.md) — measured evidence
→ [`Documentation/neurodivergence_handling.md`](Documentation/neurodivergence_handling.md) — interaction rubric

---

## Full Documentation

| File | Contents |
|------|---------|
| [`Documentation/spec.md`](Documentation/spec.md) | EDCM-PCNA-PCTA framework: full mathematics |
| [`Documentation/GCIP.md`](Documentation/GCIP.md) | GCIP proposal submitted to AI developers and regulators |
| [`Documentation/evidence_log.md`](Documentation/evidence_log.md) | Three EDCM-measured evidence entries |
| [`Documentation/neurodivergence_handling.md`](Documentation/neurodivergence_handling.md) | Neurodivergent interaction rubric and AI skill specification |

---

**edcmbone v0.1.0** · MIT License · [The Interdependent Way](https://github.com/The-Interdependency)
Contact: [wayseer@interdependentway.org](mailto:wayseer@interdependentway.org)
