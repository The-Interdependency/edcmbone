---
name: new-retain-old
description: Preserve the prior implementation while creating a replacement implementation with explicit rollback, archive, metadata, tests, docs, and hmmm boundaries. Use when a user asks to replace, rewrite, rebuild, redesign, rename current to *_old, archive old backend/frontend/module/service, create new while retaining old, or when friction shows the old behavior must remain available during a new implementation.
---

# new-retain-old — create new while retaining old

## Purpose

Use this skill when the change is not a simple edit: it creates a new active
surface while keeping the prior surface available as an explicit rollback and
reference object.

The goal is to prevent three failures:

1. deleting useful old behavior before the replacement is proven;
2. hiding uncertainty about what moved, changed, or stayed unresolved;
3. making the new path technically correct but hard to run, test, or review.

## Workflow

1. **Name the active and retained surfaces.**
   - Active path: the new implementation users should use now.
   - Retained path: the old implementation, usually `<name>_old`, `legacy/`, or
     `archive/<date>-<name>`.
   - If the user named the retained path, use that exact name.

2. **Inventory before moving.**
   - Inspect package metadata, imports, tests, docs, examples, data files, and
     entry points.
   - Identify what must remain runnable from the retained path.
   - Record unknowns as `hmmm`; do not invent certainty.

3. **Move old first, then build new.**
   - Preserve the old tree with history-friendly renames where possible.
   - Do not leave the active path half-old and half-new unless the user asked
     for an incremental migration.
   - Keep licenses and data files with the retained implementation unless there
     is a clear reason not to.

4. **Declare the new module beside the code.**
   - Add `MODULE_BUILD` for the new active module.
   - Add `CONTRACTS` for tests the module promises.
   - Add `DEPENDENCIES` when imports/calls matter.
   - Add `BOUNDARIES` when runtime effects, data, permissions, storage,
     network, or admin behavior matter.
   - Add `DOCS` when public usage guidance exists or should exist.

5. **Make the new path few-click usable.**
   - Provide a copy-paste install/run path.
   - Include a smoke example or minimal demo.
   - Test the new path from outside the repo root when packaging matters.
   - Avoid relying on ambient `PYTHONPATH` unless explicitly documented as a
     temporary hmmm boundary.

6. **Test both the promise and the transition.**
   - Test core new behavior.
   - Test import/dependency boundaries that motivated the rewrite.
   - Test that the retained path exists.
   - Test docs/examples when they are the user entry point.

7. **Report with a boundary object.**
   - Delivered: what is now active, retained, tested, and documented.
   - hmmm: unresolved constraints, compatibility gaps, migration risks, or next
     continuation steps.

## Required checks before commit

- `git status --short` shows only intentional active/new/retained changes.
- New active path has usage guidance.
- Retained path is named clearly and mentioned in docs or PR text.
- Tests cover at least one behavior of the new path and one transition invariant
  such as import hygiene, package self-containment, or retained-path presence.
- Any unresolved behavior is written as `hmmm`, not omitted.

## PR body checklist

Include:

```text
active_path: <path>
retained_path: <path>
rollback: restore retained_path or switch import/entry point back
few_click_path: <commands or hmmm>
tests: <commands>
hmmm: <unresolved constraints or non-empty continuation note>
```

## Anti-patterns

- Calling the old path “backup” without documenting how to restore it.
- Replacing package metadata but not testing installation.
- Adding examples that only work because the agent shell has special paths.
- Flattening `hmmm` into prose that cannot be tested or carried forward.
- Treating archived old code as dead if users still need it for comparison,
  rollback, or migration.
