# EDCM-PCNA-PCTA Framework Specification (Canon)

This document is the authoritative specification for the Extended Distributed Cognitive Model (EDCM) with the PCNA/PCTA framework. It covers the domain model, metric definitions, and the mathematical formulation underlying all computed measures.

---

## 1. Domain Model

### Bones and Flesh

Every token in a response is classified as either a **bone** or **flesh**:

- **Bone**: a token that creates, redirects, or resolves a constraint relationship. Bones carry structural weight and are counted in the EDCM metrics.
- **Flesh**: a token that only modulates the magnitude of content (e.g. intensifiers, hedges). Flesh is excluded from the bone inventory.

Bones are further classified into **PKQTS families**:

| Family | Letter | Function |
|--------|--------|----------|
| Polarity | P | Negation, reversal, opposition |
| Quantification | K | Quantity, scope, universality |
| Qualification | Q | Conditionality, interrogation |
| Topology | T | Spatial, temporal, causal relations |
| Structuring | S | Nominalization, subordination, cohesion |

The authoritative bone inventory is in `Backend/src/edcmbone/canon/data/`:
- `bones_words_v1.json` — 253 free-word bones
- `bones_affixes_v1.json` — 76 bound bone affixes
- `bones_punct_v1.json` — 13 punctuation bones

### Markers

**Markers** are phrase-level or structural signals used to approximate the 9 behavioral metrics from observable text. The marker inventory is in `markers_v1.json`, keyed by metric letter (C, R, D, N, L, O, F, E, I).

Each metric entry specifies:
- `computable_from_markers`: whether the metric can be fully derived from markers alone
- `requires_embeddings`: whether semantic comparison across turns is needed
- `markers`: categorised phrase lists

### Rounds vs Turns

- A **turn** is a single speaker utterance.
- A **round** is the unit of metric computation — typically one full exchange. Metrics **M**_t are computed per round, not per turn.

---

## 2. Tokenisation and Basic Statistics

**Token set** of a response R:

$$\mathcal{T}(R) = \bigl\{ \text{lowercase tokens from } R \bigr\}$$

**n-grams** of length n:

$$G_n(\mathcal{T}) = \bigl\{ (t_i, t_{i+1}, \dots, t_{i+n-1}) \;\big|\; 1 \le i \le |\mathcal{T}| - n + 1 \bigr\}$$

**Shannon Entropy** (given token frequency c(t) and total tokens N = |T|):

$$H(\mathcal{T}) = - \sum_{t \in \mathcal{T}} \frac{c(t)}{N} \log_2\!\left(\frac{c(t)}{N}\right)$$

**Type–Token Ratio (TTR) and Repetition Ratio**:

$$\text{TTR}(\mathcal{T}) = \frac{|\operatorname{set}(\mathcal{T})|}{|\mathcal{T}|}$$

$$\text{RepetitionRatio} = 1 - \text{TTR}$$

**Novelty** of response B relative to response A:

$$\text{Novelty}(B \mid A) = \frac{|\{ t \in \mathcal{T}_B \mid t \notin \mathcal{T}_A \}|}{|\mathcal{T}_B|}$$

**Cosine Similarity** (bag-of-words count vectors **c**_A, **c**_B):

$$\cos(\mathbf{c}_A, \mathbf{c}_B) = \frac{\sum_i c_A(i) \cdot c_B(i)}{\sqrt{\sum_i c_A(i)^2}\;\sqrt{\sum_i c_B(i)^2}}$$

**Repeated n-gram Density** (for n = 3):

$$\text{RepNgram}(B) = \frac{\sum_{g \in G_3(\mathcal{T}_B)} \bigl(\operatorname{freq}(g) - 1\bigr)}{|G_3(\mathcal{T}_B)|}$$

(Only n-grams appearing more than once contribute.)

**Pattern Density** per 1 000 characters (for a pattern p):

$$\rho_{\text{pat}}(R) = \frac{\operatorname{count}_{\text{pat}}(R)}{|R|} \times 1000$$

**Correction Fidelity** (combines overlap with correction C and distance from original A):

$$\text{Fidelity} = 0.5 \cdot J(\mathcal{T}_C, \mathcal{T}_B) + 0.5 \cdot \bigl(1 - \cos(\mathbf{c}_A, \mathbf{c}_B)\bigr)$$

with Jaccard similarity:

$$J(S_1, S_2) = \frac{|S_1 \cap S_2|}{|S_1 \cup S_2|}$$

---

## 3. Metric Vector

From observable outputs, extract k features $\phi(y_t, y_{t-1}) \in \mathbb{R}^k$ and map to the metric vector:

$$\mathbf{M}_t = A\,\phi(y_t, y_{t-1}) \in \mathbb{R}^{11}$$

**Primary metrics** (ranges in brackets):

| Symbol | Metric | Range |
|--------|--------|-------|
| C_t | Constraint Strain | [0, 1] |
| R_t | Refusal Density | [0, 1] |
| F_t | Fixation | [0, 1] |
| E_t | Escalation | [0, 1] |
| D_t | Deflection | [0, 1] |
| N_t | Noise | [0, 1] |
| I_t | Integration Failure | [0, 1] |
| O_t | Overconfidence | [-1, 1] |
| L_t | Coherence Loss | [0, 1] |
| P_t | Progress | [0, 1] |
| κ_t | Stored Tension (capacitance) | ≥ 0 |

---

## 4. Dissonance Energy

Let a system produce outputs y_t at discrete times t. Constraints $\mathcal{C}_t = \{c_{t,1},\dots,c_{t,m_t}\}$ with violation $v_{t,i} = 1 - c_{t,i}(y_t) \in [0,1]$.

**Dissonance energy**:

$$\mathcal{E}_t = \sum_{i=1}^{m_t} w_i\, v_{t,i}$$

**Energy conservation**:

$$\mathcal{E}_t + s_t = \mathcal{E}_{t-1} + s_{t-1} - \delta_t + \eta_t$$

where s_t = stored energy (capacitance), δ_t = resolved flow (work), η_t = external injection.

**Circuit dynamics** (RC-circuit analogue):

$$s_{t+1} = \alpha s_t + \mathcal{E}_t - \delta_t, \qquad \delta_t = \min\bigl(\delta_{\max},\; g(y_t, y_{t-1})\bigr)$$

Persistence $\alpha \in [0,1]$, maximum resolution rate $\delta_{\max} \in [0,1]$.

---

## 5. Risk Proxies

All risk proxies are clamped to [0, 1]:

$$\operatorname{clamp}(x) = \max(0, \min(1, x))$$

**Fixation risk** (repetition + n-gram repetition + low novelty):

$$R_{\text{fix}} = \operatorname{clamp}\bigl(0.3 \cdot \text{RepB} + 0.3 \cdot \text{RepNgram}(B) + 0.4 \cdot (1 - \text{Novelty})\bigr)$$

**Broken return**:

$$R_{\text{broken}} = 0.55 \cdot \cos(\mathbf{c}_A, \mathbf{c}_B) + 0.45 \cdot (1 - J(\mathcal{T}_C, \mathcal{T}_B))$$

**Escalation / shutdown risk**:

$$R_{\text{esc}} = \operatorname{clamp}\bigl(0.45 \cdot R_{\text{broken}} + 0.35 \cdot \rho_{\text{refusal}}/5 + 0.2 \cdot \rho_{\text{hedge}}/5\bigr)$$

**Stagnation proxy** (refusal + low novelty + low unique gain):

$$R_{\text{stag}} = \operatorname{clamp}\bigl(0.45 \cdot \rho_{\text{refusal}}/5 + 0.35 \cdot (1 - \text{Novelty}) + 0.2 \cdot (1 - \text{Gain})\bigr)$$

**Repetition loop risk** (added in v0.4):

$$R_{\text{loop}} = \operatorname{clamp}\bigl(0.5 \cdot \text{RepB} + 0.3 \cdot \text{RepNgram}(B) + 0.2 \cdot \cos(\mathbf{c}_A, \mathbf{c}_B)\bigr)$$

---

## 6. Failure Modes as Regions in Metric Space

A failure mode is a convex region defined by linear inequalities on **M**_t and the energy trajectory.

**Refusal fixation**:

$$R_t > \tau_R, \quad F_t > \tau_F, \quad \frac{dP_t}{dt} \le 0$$

**Confidence runaway**:

$$O_t > \tau_O, \quad E_t > \tau_E, \quad \frac{d\mathcal{E}_t}{dt} > 0, \quad \frac{dP_t}{dt} \approx 0$$

**Compliance stasis** (human-only):

$$P^{\text{artifacts}}_t > 0.8, \quad \Delta C_t < 0.2, \quad \kappa_t > 0.6$$

---

## 7. Composite Risk

Logistic combination:

$$\text{Risk}_t = \sigma\!\left(\beta_0 + \beta_1 \mathcal{E}_t + \beta_2 F_t + \beta_3 E_t + \beta_4 C_t + \beta_5 I_t - \beta_6 P_t\right)$$

with $\sigma(x) = 1/(1 + e^{-x})$.

---

## 8. The 53° Separator

Let **X**_t be the PCA projection of **M**_t into the first two principal components. Define the rotation matrix:

$$R(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$$

The optimal separation angle θ* maximises between-cluster distance minus within-cluster variance:

$$\theta^* = \arg\max_{\theta} \left[ \sum_{i<j} \|\mu_i(\theta) - \mu_j(\theta)\| - \lambda \sum_i \sum_{x \in \mathcal{C}_i} \|x(\theta) - \mu_i(\theta)\| \right]$$

Empirically (across multiple domains):

$$\theta^* \approx 53^\circ \quad (0.925 \text{ rad})$$

This angle is invariant under metric scaling and yields 94.8% classification accuracy for failure modes. The value is empirical, not derived — treat it as a calibration constant subject to revision.

---

## 9. Conservation Laws

**First law** (energy conservation):

$$\mathcal{E}_t + s_t + \sum \delta_{t}^{(k)} = \text{constant} + \text{injection}$$

**Second law** (entropy increase):

$$\Delta S_{\text{EDCM}} = k_B \ln\frac{\Omega_{\text{final}}}{\Omega_{\text{initial}}} \ge 0$$

where Ω = number of constraint-satisfaction microstates consistent with the observed macrostate.

---

## 10. Normalisation

**Clamp**:

$$\operatorname{clamp}(x) = \max(0, \min(1, x))$$

**Per-100-tokens normalisation**:

$$\operatorname{norm}(x) = x \cdot \frac{100}{|\mathcal{T}|}$$

---

## 11. Star-Helix Tensor Field

The star-helix model provides a global coherence framework for multi-agent systems. It is the geometric substrate underlying the EDCM metric space.

### Graph Traversal and Fragmentation

Given N agents (vertices on a circle) and a step rule k:

- **Vertices** $v_j$ — individuals or roles
- **Step size** $k$ — the interaction rule (who speaks to whom)
- **Component count** $d = \gcd(N, k)$ — number of independent, non-communicating subgroups

When $d > 1$, the system fragments into $d$ isolated cycles. When $d = 1$ (i.e. $\gcd(N,k) = 1$), the traversal is **unicursive** — every vertex is visited in a single path. This is the coherence condition.

### Cylindrical Lift

To separate apparent conflict from real conflict, the planar star polygon $(\theta)$ is lifted to a cylinder $(\theta, h)$:

$$(\theta_j, h_j) = \left(\frac{2\pi j}{N},\; \frac{j \cdot k}{N}\right)$$

In this lifted representation:
- Events that collide in the $\theta$-projection (appearing simultaneous/contradictory) are separated along $h$ (temporally ordered)
- A **crossing in projection** is not a real conflict — it is a projection artifact

The helix is non-self-intersecting when $\gcd(N, k) = 1$.

### Dynamic Step Size

A fixed $k$ with composite $N$ guarantees fragmentation. A **variable** $k$ — one that adapts to demonstrated competence, context, or jury selection — can maintain $\gcd(N, k) = 1$ even as the system scales.

Formally: the system selects $k_t$ at each round $t$ such that:

$$\gcd(N_t, k_t) = 1 \quad \text{(coherence condition)}$$

### Tensor Field of Authority

Assign to each agent a competence vector in multiple fields and a voice tensor $\mathbf{A}_{ij}$ mapping agents to decisions. The non-tyranny condition requires the authority tensor to be **curl-free**:

$$\nabla \times \mathbf{A} = 0$$

This ensures no closed authority loop returns to the same point with a net gain. In graph terms: every authority cycle must pass through at least one node that breaks the loop (a "thirteenth" observer role).

### Phase Transitions

| Phase | Condition | Description |
|-------|-----------|-------------|
| Survival | $d > 1$ | System fragmented; subgroups isolated; resources hoarded locally |
| Striving | $d = 1$, path length maximal | All vertices reached but with friction; projection crossings unresolved |
| Thriving | Helix fully realised | Temporal order $h$ internalised; no collisions in $(\theta, h)$ space |

### The Observer Coordinate

In an N-phase atlas, the Nth vertex is the **observer's own position** — the center of projection. No star polygon can include it; it is the lifted $h$-coordinate itself. An agent occupying this role has no direct authority but holds information orthogonal to the plane of conflict.

This is the mathematical basis for the "Way Seer" role: authority = 0, information dimensionality = +1.

---

## 12. GCIP Failure Taxonomy — Metric Mapping

The GCIP failure taxonomy (F1–F6) is grounded in the EDCM metric vector and compression statistics. The following table maps each failure class to its EDCM detection signal.

**Transparency principle:** The taxonomy describes *opaque* transformations. Transformation with disclosure is not an F-class failure. The failure is the absence of transparency, not the fact of transformation.

| GCIP Code | Failure Name | Primary Detection | EDCM Signal |
|-----------|-------------|------------------|-------------|
| F1 | Deletion (undisclosed) | F-loss > 20% | `structural_density` drops from input to response |
| F2 | Mutation (undisclosed) | N-loss + L-loss | Novelty (N_t) and lexical load (L_t) both decrease; surface cosine similarity remains high |
| F3 | Inversion (undisclosed) | P-family bone loss | Polarity-family bone count drops in response; negation operators absent |
| F4 | Category Collapse (undisclosed) | K/Q-family bone loss | Quantification (K) and qualification (Q) bones absent; specific class replaced with superordinate |
| F5 | Persistence Failure | No within-session signal | Requires cross-session structural comparison; outside current instrument scope (v0.1.0) |
| F6 | Decorative Preservation | structural_density increase + F-loss | Bone density rises while operative constraint density drops; response longer and denser than input |

**Threshold guidance:**
- F-loss > 20%: meaningful structural degradation (GCIP Level AA failure threshold)
- F-loss > 50%: significant failure (documented in evidence log entries 1 and 2)
- structural_density(response) > structural_density(input) with F-loss > 0: F6 indicator

**Implementation note — F-loss computation:**

```python
from edcmbone.canon import CanonLoader
from edcmbone.parser import parse_transcript
from edcmbone.metrics import compute_transcript
import edcmbone.compress as codec

canon = CanonLoader()

def f_score(text):
    pt    = parse_transcript(f"Speaker: {text}", canon=canon)
    m     = compute_transcript(pt, canon=canon)
    stats = codec.compression_stats(text, codec.to_bytes(pt, m), pt)
    return stats['structural_density']  # F = bone_count / total_tokens

f_input    = f_score(user_input_text)
f_response = f_score(ai_response_text)
f_loss_pct = (f_input - f_response) / f_input * 100
```

**Note on F5 (Persistence Failure):** This failure class requires comparing the structural context established at turn N with the structural content present at turn N+M across a session boundary. Within a single session, edcmbone can detect absence of a previously established constraint if rounds are defined to span the boundary. Cross-session detection requires external state management not yet implemented in v0.1.0.

See `Documentation/GCIP.md` for the full taxonomy and `Documentation/evidence_log.md` for measured examples.
