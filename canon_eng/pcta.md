# PCTA — Prime Circular Tensor Architecture
GPT generated; context, prompt Erin Spencer

## 1. Domain

PCTA models dynamic transport on a circular prime-indexed lattice.

Let:
θ ∈ [0, 2π)
Discretized into N nodes indexed by primes:
{p1, p2, ..., pN}

State variable:
U(θ, t) = activation density

Gate variable:
A(θ, t) = adaptive braking field

-----------------------------------------
## 2. Transport Equation

Base transport:

∂U/∂t =
  - b(A) ∂U/∂θ
  + k(A) ∂²U/∂θ²
  + S(θ,t)
  - R(U)

Where:

b(A) = 1 / (1 + λA)   (drift brake)
k(A) = 1 / (1 + λA)   (diffusion brake)

S(θ,t) = stimulus input
R(U) = nonlinear decay term

-----------------------------------------
## 3. Gate Dynamics

Gate evolves via:

∂A/∂t =
  α * coherence(U)
  - β * overload(U)
  - γA

Where:

coherence(U) = local triadic alignment
overload(U) = magnitude variance or constraint density
γ = leakage constant

-----------------------------------------
## 4. Stability Condition

CFL constraint:

Δt ≤ (Δθ²) / (2k_max)

High λ → freeze regime
Low λ → oscillatory regime

-----------------------------------------
## 5. Interpretation

- U = circulating energy field
- A = adaptive constraint brake
- Prime indexing prevents periodic aliasing
- Circular topology enforces conservation

hmm
Parameter tuning determines freeze vs thrash boundary.
