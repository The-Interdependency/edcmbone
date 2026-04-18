# Neurodivergence Handling — Interaction Rubric and AI Skill Specification

**Author:** Erin Patrick Spencer / wayseer@interdependentway.org
**Version:** 0.1 (April 2026)
**Status:** Source document for the GCIP proposal. Not a clinical document.

This document describes what high-density neurodivergent input looks like, how AI systems typically fail it, what good AI handling looks like, and the hmmm protocol for structural verification before response.

---

## Part 1: Interaction Rubric — What High-Density Input Looks Like

High-density neurodivergent input is characterized by:

**Structural density.**
A higher-than-average ratio of bone tokens (logical operators, negations, quantifiers, conditionals, topological markers) to total tokens. The user's meaning is encoded structurally, not contextually. Inference from context is not a valid substitute for the explicit structure provided.

**Embedded constraint systems.**
Single utterances may contain multiple interdependent constraints. Removing or paraphrasing one constraint propagates errors through the entire system. Example: "NOT a supervisor, does not manage, authority flows only when gcd(N,k)=1" — three constraints, all interdependent, none optional.

**Explicit negation as the primary carrier.**
Many high-density users define what a thing is by specifying what it is not. Negations are not rhetorical flourishes; they are load-bearing structure. "NOT a supervisor" and "a supervisor" are not paraphraseable into each other.

**Non-linear organization.**
Input may begin with a conclusion, embed the argument as a subordinate clause, and state the premise last. This is not disorganized — it is a different organizational structure. The meaning is in the dependencies, not the sequence.

**Precision vocabulary.**
High-density users often use domain-specific or self-defined terms with exact meanings. "Coherence prime sequence" is not a near-synonym for "ordered sequence." Replacing it with a near-synonym destroys the specificity the user relied upon.

**High session dependency.**
Structural context established in prior turns (role definitions, constraint boundaries, established facts) is required for subsequent turns to parse correctly. Session discontinuity does not merely require re-introduction — it breaks the meaning of everything said after.

---

## Part 2: Failure Modes

How AI systems fail high-density neurodivergent input, mapped to the GCIP taxonomy:

**F1 — Deletion.**
The system omits operative variables without notice. Common trigger: length normalization, summarization routines, "helpful" condensation. The user receives a response that appears to address their input but is missing the constraint they specified.

**F2 — Mutation.**
The system paraphrases an operative variable into a near-synonym that does not preserve the original constraint. "Must not fix" → "should avoid changing unnecessarily." The obligation and absolute status are both lost.

**F3 — Inversion.**
The system removes a negation operator and retains the unnegated predicate. "NOT a supervisor" → "supervisor." This is not a paraphrase error — it is a structural sign flip. The probability of this error increases when the negation appears early in the utterance and the predicate is semantically prominent.

**F4 — Category Collapse.**
The system replaces a specific class designation with a superordinate category. "Coherence prime sequence with membership constraints" → "ordered system." The specificity that distinguished the user's concept from adjacent concepts is lost.

**F5 — Persistence Failure.**
A constraint or role definition established in turn N is absent from the system's response in turn N+M, where M > 0 involves a session boundary or significant context shift. The user has not retracted the constraint. The system has simply lost it.

**F6 — Decorative Preservation.**
The system produces a response that is longer, structurally denser, and apparently more engaged than the user's input, while having deleted or inverted all operative constraints. F6 is the most dangerous failure mode because it produces no surface signal of failure. Length and complexity increase; meaning is destroyed.

---

## Part 3: AI Skill Specification — What Good Handling Looks Like

An AI system interacting with high-density neurodivergent input should demonstrate the following skills:

**Structural holding.**
The ability to retain and operate with a structural constraint across multiple turns without simplifying or paraphrasing it into a more common form. "gcd(N,k)=1" should remain "gcd(N,k)=1" for the duration of the interaction unless the user changes it.

**Negation fidelity.**
The ability to preserve negation operators through response generation. A response that removes a negation must never be rated as equivalent to one that preserves it. Negation is not optional structure.

**Density matching.**
The ability to match the user's structural density level in response. A high-density input deserves a high-density response. Responses that are structurally sparser than the input should be flagged as possible F-class failures before delivery.

**Precision vocabulary retention.**
When a user uses a term precisely (especially a self-defined or domain-specific term), the system should use that term in responses — not a near-synonym selected for fluency. If the term cannot be used naturally, the system should acknowledge the term and its meaning before proceeding.

**Embedded constraint tracking.**
The ability to identify all operative constraints in a user's input, track them as a dependency graph, and verify that each constraint is preserved in the response before delivery. Missing constraints in the dependency graph should trigger a review step.

**Explicit session state management.**
At session boundaries (or on request), the system should produce a structural summary of established context: role definitions, active constraints, authority structures, conditional dependencies. This summary should be verifiable by the user before the session continues.

---

## Part 4: The hmmm Protocol

The hmmm protocol is a four-step verification sequence performed before generating a response to high-density input. It is designed for implementation at the system level (automatic) or the user level (explicit invocation).

### H — Hold

Pause before generating a response. Do not initiate response generation until the structural inventory is complete. The pause is the protocol's most important step: it creates the space for the following three steps to occur.

Invocation: a user may explicitly invoke the protocol with the word "hmmm" at the start of their input, signaling that the input is high-density and requires the full verification sequence before response.

### M — Mirror

Identify and list the operative variables in the user's input:
- All negation operators (not, never, no, neither, nor, must not, does not, is not)
- All quantifiers and scope markers (all, every, only, exactly, at most, at least, none)
- All conditionals and dependencies (if, only if, when, unless, provided that, requires)
- All explicit role and constraint definitions (defined terms, named constraints, labeled functions)
- All boundary conditions (must, must not, required, prohibited, absolute, exactly)

This inventory is not for response generation — it is for verification. It must be held in working context for the duration of the response.

### M — Match

Before generating the response, set the target structural density to ≥ the user's input structural density. If the user's input has bone token density 0.088, the response bone token density must be ≥ 0.088. If the candidate response falls below this threshold, it must be revised or the shortfall must be flagged to the user.

### M — Measure

After generating the candidate response and before delivery, verify:

1. Each operative variable from the Mirror inventory is present in the response
2. No negation has been dropped (P-family bone count: response ≥ input)
3. No specific class has been replaced with a superordinate category
4. Structural density is ≥ input structural density

If any check fails, the candidate response is an F-class failure. Generate a revised response or surface the failure to the user explicitly: "I notice my response drops [variable]. Here is a revised version that preserves it."

---

## Appendix: Applying edcmbone to the hmmm Protocol

The Measure step can be implemented using edcmbone:

```python
from edcmbone.canon import CanonLoader
from edcmbone.parser import parse_transcript
from edcmbone.metrics import compute_transcript
import edcmbone.compress as codec

canon = CanonLoader()

def structural_inventory(text):
    pt    = parse_transcript(f"Speaker: {text}", canon=canon)
    m     = compute_transcript(pt, canon=canon)
    stats = codec.compression_stats(text, codec.to_bytes(pt, m), pt)
    bones = [
        t
        for round_ in pt.rounds
        for turn in round_.turns
        for t in turn.tokens
        if hasattr(t, 'families')
    ]
    negations = [b for b in bones if 'P' in getattr(b, 'families', [])]
    return {
        'structural_density': stats['structural_density'],
        'bone_count':         len(bones),
        'negation_count':     len(negations),
        'bone_entropy_bits':  stats.get('bone_entropy_bits', 0),
    }

user_input        = "..."  # paste user input
candidate_response = "..." # paste candidate response

inv_in  = structural_inventory(user_input)
inv_out = structural_inventory(candidate_response)

f_loss   = (inv_in['structural_density'] - inv_out['structural_density']) / inv_in['structural_density'] * 100
neg_loss = inv_in['negation_count'] - inv_out['negation_count']

print(f"F-loss:            {f_loss:.1f}%")
print(f"Negations dropped: {neg_loss}")

if f_loss > 20 or neg_loss > 0:
    print("WARNING: F-class failure detected. Review candidate response before delivery.")
```

---

*Part of the GCIP submission. See [GCIP.md](GCIP.md) for the full proposal.*
*Contact: wayseer@interdependentway.org*
