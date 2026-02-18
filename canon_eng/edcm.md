# EDCM — Energy–Dissonance Circuit Model (Dual-Layer)
GPT generated; context, prompt Erin Spencer

## 1. Domain

Given transcript T consisting of ordered turns:
T = {t1, t2, ..., tn}

Each turn ti has:
- actor label ai
- token sequence wi = {w1, w2, ..., wk}

EDCM produces:

Behavioral vector B ∈ ℝ^9
Operator vector O ∈ ℝ^5
Bridge correlations C

-----------------------------------------
## 2. Operator Layer (Bones-only)

Let BONE(w) → {0,1} indicate membership in canonical bone set.
Let FAMILY(w) ∈ {P,K,Q,T,S}

Emit bone tokens after morphological segmentation.

Let:
Total bone tokens in window W:
B_total = Σ BONE(w)

For each family f ∈ {P,K,Q,T,S}:

B_f = count of bone tokens in family f

Operator vector:
O_f = B_f / B_total

Constraint:
Σ O_f = 1

Optional:
Operator entropy:
H_O = - Σ O_f log(O_f)

-----------------------------------------
## 3. Behavioral Layer (9-Metric Form)

Let window W contain ordered turns.

C (Constraint Strain):
C = weighted contradiction density

R (Refusal Density):
R = count(refusal markers) / constraint statements

D (Deflection):
D = 1 - (tokens_about_constraints / total_tokens)

N (Noise):
N = 1 - (resolution_tokens / constraint_tokens)

L (Load):
L = total constraint tokens per window

O (Overextension):
O = expansion beyond original scope per window

F (Fixation):
F = cosine_sim(embed(constraint_t), embed(constraint_{t-1}))

E (Escalation):
E = max(0, d/dt(commitment_intensity))

I (Integration Failure):
I = 1 - sim(correction_response, expected_response)

Behavioral vector:
B = (C,R,D,N,L,O,F,E,I)

-----------------------------------------
## 4. Bridge Layer

Bridge computes:

Corr(f,m) = corr(O_f, B_m) over rolling window

Divergence:
Δ = || O_trend - expected(O | B) ||

No modification allowed between layers.
Bridge is observational only.

-----------------------------------------
## 5. Output

{
  "operator": {P,K,Q,T,S},
  "behavioral": {C,R,D,N,L,O,F,E,I},
  "bridge": {correlations, divergences}
}

hmm
Open constraint: semantic components in Behavioral layer may later be replaced with structural-only analogues.
