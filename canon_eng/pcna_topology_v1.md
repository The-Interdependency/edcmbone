# edcmbone — PCNA Topology v1 (Static)
GPT generated; context, prompt Erin Spencer

## Freeze
- Prime count **N = 53** (canonical-first; coheres with the separator prime note)
- Node set is the **first 53 primes**.

hmm: N is now frozen for v1. A future v2 may define alternate N profiles (31 mobile, 127 cloud).

## Node set (ordered)
Index i = 0..52, node label p[i]:

2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
233, 239, 241

## Circular embedding
Each node i has angle:
θ_i = 2π * i / N

Circular distance between nodes i and j:
d(i,j) = min(|i-j|, N-|i-j|)

## Edge layers (deterministic)

PCNA graph G = (V, E) is the union of these edge layers:

### Layer L0 — Ring adjacency (always on)
Edges:
(i) ↔ (i+1 mod N)

Weight:
w0(i,j) = 1.0 for ring neighbors

### Layer L1 — Heptagram step edges (unicursive-friendly)
Steps set (frozen):
k ∈ {2, 3, 5}

Edges:
i ↔ (i+k mod N) for each k in {2,3,5}

Weights:
w1(i,j) = 1 / k

Notes:
- This defines three rotational sub-graphs on the same circle.
- Using multiple k values provides multi-scale routing without semantics.

### Layer L2 — Twin-prime pairing edges (within node set only)
If both p[i] and p[j] are in the node set and |p[i] - p[j]| = 2,
add edge i ↔ j.

Weight:
w2(i,j) = 0.75

### Layer L3 — Prime-gap band edges (index-space)
For band steps b ∈ {7, 11, 13} (frozen):
i ↔ (i+b mod N)

Weight:
w3(i,j) = 1 / b

## Final weight (combined)
If multiple layers connect the same (i,j), weights add:

W_ij = Σ_layer w_layer(i,j)

Optionally normalize outgoing weights per node:
P(j|i) = W_ij / Σ_j W_ij

## Node state and update (static neural step)
Each node holds x_i ∈ ℝ^d.
Update:
x_i(t+1) = σ( Σ_j W_ij x_j(t) + b_i )

σ and d are implementation choices; topology is fixed here.

## PCTA interface (consumption only)
PCTA consumes state vector s(W) and routes activation across this topology.
PCNA does not modify upstream metrics.

hmm: adjacency variants deferred
- geometry-weighted edges based on prime gaps (value-space)
- learned edge weights
- sentinel overlays / nine-child sentinels mapping
