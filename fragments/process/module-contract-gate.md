## Module Contract Discovery Gate

Before changing production code — the project's own source and configuration that a change
could affect at runtime; docs, generated files, and scratch files are not production code —
the agent must complete module-contract discovery for the affected code area.

### Canonical Source

- Git-tracked module contracts are canonical project knowledge. Canonical contracts include
  contract records under `docs/architecture/**` (dated records marked `type: module-contract`
  in the frontmatter), file-local `START_MODULE_CONTRACT` / `END_MODULE_CONTRACT` blocks, and
  other project-declared contract artifacts. A root-level `MODULE_CONTRACT.md` is a legacy
  form: recognize and read it, never create one.
- Memory systems such as Basic Memory are indexes and navigation aids only. They never
  replace reading the canonical contract from the repository.

### Task Start

At the start of a coding task: establish whether the project declares contract artifacts at
all — query the Basic Memory index when `basic-memory` is enabled, otherwise run a targeted
scan of `docs/architecture` and look for a legacy `MODULE_CONTRACT.md`. If none are
declared, discovery is complete with that result: say so in one line and continue under the
normal rules; otherwise discover the contracts for the affected area.

### Before Editing A File

Before editing a code file, decide whether the file is covered by a module contract: by
explicit naming, by location, by the data flows it handles, by the responsibilities the
change may affect, or by its tests. If coverage is unclear, treat the contract as relevant,
read it, and state the uncertainty.

### Use During Reasoning

Contracts constrain the change: scope and non-goals, allowed behavior changes, error
handling and recovery, required verification. If the intended change contradicts a contract,
stop and report that the task requires a contract change — never silently implement behavior
that violates the existing contract. Escalating a contract change is the stop condition
`Autonomy Boundaries` already defines for public contract changes.

### During The Session

Re-run contract discovery when the task moves into a new module or layer, when contract
artifacts change, when new units join the edit set, or when verification failures suggest a
misunderstood boundary.

### Reporting

When contracts were relevant, the implementation summary carries one short contract note:
which contracts were read, which files were treated as covered, whether the contract is
preserved or changed, and what verification ran against it. If no relevant contract was
found, say that discovery was performed and name the remaining risk.

### Reference

The full discovery commands, the coverage criteria, the reasoning detail, the index-entry
shape, and the reporting detail live in
`.ai-standards/references/module-contract-gate.md`, deployed by `ai-sync sync-templates`
when this feature is enabled — read it when the gate fires. If the file is absent, the
project has not run `ai-sync sync-templates`; proceed with the rules above.

### Strict Rule

Do not edit production code until module-contract discovery for the touched files has
completed. Basic Memory may satisfy discovery only as an index; relevant canonical contracts
must still be read from the repository before editing.
