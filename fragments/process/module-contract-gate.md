<!--
Source provenance:
- Promoted from the contributor draft `docs/archive/0tkgv0g-module-contract-discovery-gate.md`
  (exchange of 2026-07-28; validated against the rule surface on 2026-08-28).
- Placement and adjustments: docs/decisions/2026-08-28-module-contract-gate-feature-placement.md.
-->

## Module Contract Discovery Gate

Before changing production code — the project's own source and configuration that a change
could affect at runtime; docs, generated files, and scratch files are not production code —
the agent must complete module-contract discovery for the affected code area.

### Canonical Source

- Git-tracked module contracts are canonical project knowledge. Canonical contracts include
  `MODULE_CONTRACT.md`, contract records under `docs/architecture/**`, file-local
  `START_MODULE_CONTRACT` / `END_MODULE_CONTRACT` blocks, and other project-declared
  contract artifacts.
- Memory systems such as Basic Memory are indexes and navigation aids only. They never
  replace reading the canonical contract from the repository.

### Task Start

At the start of a coding task:

1. Establish whether the project declares contract artifacts at all: query the Basic Memory
   index when `basic-memory` is enabled, otherwise run one cheap check such as
   `rg --files -g MODULE_CONTRACT.md` plus a look under `docs/architecture/**`.
2. If the project declares none, discovery is complete with that result: say so in one line
   and continue under the normal rules.
3. Otherwise, query the index (when available) for the project name, `module contract`,
   `docs/architecture`, the task id when available, and the modules, classes, or packages
   likely to be touched.
4. If no index is available, stale, or insufficient, say so before broad discovery — for
   example: "the module-contract index is unavailable, so I will scan `docs/architecture`
   and contract markers directly, which costs extra context" — and then scan with targeted
   commands such as `rg --files docs/architecture` and
   `rg -n "START_MODULE_CONTRACT|module contract|контракт модуля"`.

### Before Editing A File

Before editing a code file, decide whether the file is covered by a module contract. A file
is covered when any of these hold:

- the contract explicitly names the class, function, package, module, endpoint, job, table,
  event, or adapter;
- the file is inside a directory or module the contract declares;
- the file produces, consumes, validates, caches, persists, transforms, or transports data
  the contract describes;
- the change may affect the contract's responsibilities, inputs, outputs, invariants, side
  effects, error boundaries, recovery behavior, observability, or verification requirements;
- the file's tests exercise behavior the contract names.

If coverage is unclear, treat the contract as relevant, read it, and state the uncertainty.

### Use During Reasoning

For every relevant contract, use it to constrain the change: scope and non-goals; allowed
behavior changes; error handling and recovery rules; backward-compatibility expectations;
required tests or smoke checks; and whether the task is ordinary implementation work or a
contract change. If the intended change contradicts a contract, stop and report that the
task requires a contract change — never silently implement behavior that violates the
existing contract. Escalating a contract change is the stop condition `Autonomy Boundaries`
already defines for public contract changes, applied here at write time.

### During The Session

Re-run contract discovery when the task moves into a new module or layer; when `git status`
or `git diff` shows changes under `docs/architecture/**` or to `MODULE_CONTRACT.md`; when a
new class, package, or module joins the edit set; or when verification failures suggest a
misunderstood boundary or invariant.

### Index Entries

When `basic-memory` is enabled, a module-contract index entry should carry the repository
name, the source contract path, a freshness marker (commit or file hash when available), and
the covered modules, packages, or data flows. An entry without a source path or freshness
marker is a hint: read the repository file before relying on it.

### Reporting

In the implementation summary, add one short contract note when contracts were relevant:
which contracts were read, which files were treated as covered, whether the change preserves
or changes the contract, and which verification ran against contract requirements. If no
relevant contract was found, say that discovery was performed and name the remaining risk.

### Strict Rule

Do not edit production code until module-contract discovery for the touched files has
completed. Basic Memory may satisfy discovery only as an index; relevant canonical contracts
must still be read from the repository before editing.
