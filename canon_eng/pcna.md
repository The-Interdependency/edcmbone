# PCNA — Prime Circular Neural Architecture
GPT generated; context, prompt Erin Spencer

## 1. Domain

PCNA is a static graph-based architecture.

Nodes arranged on circular prime index set:

V = {p1, p2, ..., pN}

Edges E defined by:
- Prime gaps
- Modular adjacency
- Heptagram projection rules

Graph:
G = (V, E)

-----------------------------------------
## 2. Node State

Each node i holds state vector:

x_i ∈ ℝ^d

Update rule:

x_i(t+1) =
  σ( Σ_j W_ij x_j(t) + b_i )

Where:

W_ij = weight determined by prime distance
σ = activation function

-----------------------------------------
## 3. Helical Projection

Optional 7-phase rotation:

θ_i(t) = (θ_i(0) + ωt) mod 2π

Heptagram routing defined by:
i → (i + k) mod N
where k ∈ {2,3,5} depending on projection layer

-----------------------------------------
## 4. Relationship to PCTA

PCNA = static structural graph
PCTA = dynamic transport over that graph

PCNA defines topology.
PCTA defines flow.

-----------------------------------------
## 5. Minimal Implementation

- Prime-indexed circular array
- Deterministic adjacency rule
- Multi-layer rotation mapping

hmm
Unresolved: optimal prime density vs computational load tradeoff.
