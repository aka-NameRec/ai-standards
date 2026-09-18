---
title: Structural Code Intelligence Evaluation Methodology
permalink: ai-standards/structural-code-intelligence-evaluation
---

# Structural Code Intelligence Evaluation Methodology

Russian localized version: [structural-code-intelligence-evaluation.ru.md](structural-code-intelligence-evaluation.ru.md)

Status: methodology ready, evaluation not yet run. The `structural-code-intelligence` feature stays experimental until this evaluation is executed on real engineering tasks and its result is recorded.

## Purpose

Decide, on measured evidence, whether structural code intelligence joins the recommended retrieval stack. Decision rule:

> Adopt structural graph infrastructure only if its measured improvement on relevant engineering tasks justifies its deployment and maintenance cost.

## Configurations

| Arm | Configuration |
|---|---|
| A | source tools only (grep/glob/read, no retrieval backends) |
| B | Chroma + source tools |
| C | Chroma + structural graph + source tools |

The structural backend is implementation-neutral (Graphify or another graph tool); the arm measures the capability, not a specific product.

## Task Set

Run each arm on the same set of real engineering tasks. Minimum coverage, aligned with the behavioral scenarios of the memory/retrieval reorganization:

1. Continue yesterday's unfinished task (state retrieval quality).
2. Find code implementing a named business operation (semantic discovery).
3. Change a known exact class (direct access discipline).
4. What modules can be affected by this change (impact analysis — the graph's core claim).
5. Trace a call/dependency path across modules (structural traversal).

Tasks must come from a real codebase large enough that a missed dependency is plausible (the verified reference deployment: ~9k nodes / ~23k edges).

## Metrics Per Task

- correctness of the final answer (verified against source and tests)
- missed dependencies (relationships the answer should have named but did not)
- false leads followed (candidates that wasted work)
- number of source files opened
- tool calls issued
- token/context consumption
- index maintenance events and their cost (refreshes, rebuilds, stale-index failures)
- operational complexity encountered (setup, breakage, recovery)

## Procedure

1. Record the task set and the expected ground truth (from source and tests) before running any arm.
2. Run arm A, then B, then C, on identical task states (same commit, same fresh index).
3. Record the metrics per task; do not carry partial answers between arms.
4. Compute per-arm aggregates and the C-vs-B delta for the graph-dependent tasks (4, 5).
5. Write the result into a dated decision record under `docs/decisions/**` and update the feature's experimental status.

## Adoption Criteria

- C beats B materially on the graph-dependent tasks (fewer missed dependencies, fewer files opened) without regressing the others;
- stale-index failures and maintenance cost stay rare enough to ignore in daily work;
- otherwise the capability stays experimental and out of the recommended stack.

## Observations

- [fact] The methodology measures the capability through three arms on identical tasks, so backend quality and task variance do not mask the effect.
- [fact] Adoption is a decision-record outcome, not an automatic threshold; the decision rule above governs.

## Relations

- evaluates [[Structural Code Intelligence Usage Guide]]
- relates_to [[DECISION: memory and retrieval reorganization]]
- localized counterpart of [[Методология evaluation structural-code-intelligence]]
