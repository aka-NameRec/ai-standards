# Module Contract Discovery Gate

Before changing production code, the agent must complete module-contract discovery for the affected code area.

## Canonical Source

- Git-tracked module contracts are canonical project knowledge.
- Canonical module contracts include:
  - `MODULE_CONTRACT.md`
  - `docs/architecture/**/*contract*.md`
  - file-local `START_MODULE_CONTRACT` / `END_MODULE_CONTRACT` blocks
  - other project-declared module contract artifacts
- Memory systems such as Basic Memory are indexes and navigation aids only. They do not replace reading the canonical contract from the repository when a relevant contract is found.

## Task Start

At the start of every coding task, the agent must:

1. Load project rules and active operational context.
2. Discover whether a module-contract index is available through Basic Memory or another configured MCP memory.
3. If Basic Memory is available, query it for:
   - the project name/repository
   - `module contract`
   - `docs/architecture`
   - the task id or branch id when available
   - names of modules/classes/packages likely to be touched
4. If no module-contract index is available, stale, inaccessible, or insufficient, the agent must say so before broad discovery, for example:
   `Module-contract index is unavailable or incomplete; I need to scan docs/architecture and contract markers directly, which may use extra context/tokens.`
5. Then perform repository discovery with targeted commands such as:
   - `rg --files docs/architecture`
   - `rg --files -g MODULE_CONTRACT.md`
   - `rg -n "START_MODULE_CONTRACT|module contract|контракт модуля"`

## Before Editing A File

Before editing any code file, the agent must decide whether the file is covered by a module contract.

A file is covered when any of these are true:

- the contract explicitly names the class, function, package, module, endpoint, job, table, event, or adapter;
- the file is inside a directory/module declared by the contract;
- the file produces, consumes, validates, caches, persists, transforms, or transports data described by the contract;
- the change may affect contract responsibilities, inputs, outputs, invariants, side effects, error boundaries, recovery behavior, observability, or verification requirements;
- tests for the file are named in or directly exercise behavior named in the contract.

If coverage is unclear, the agent must treat the contract as potentially relevant, read it, and state the uncertainty.

## Use During Reasoning

For every relevant contract, the agent must use it to constrain:

- change scope and non-goals;
- allowed behavior changes;
- error handling and recovery rules;
- backward compatibility expectations;
- required tests or smoke checks;
- whether a proposed change is ordinary implementation work or a contract change.

If the intended code change contradicts a contract, the agent must stop and report that the task requires a module-contract change. It must not silently implement behavior that violates the existing contract.

## During The Session

The agent must re-run contract discovery when:

- the task moves into a new module or layer;
- `git status` or `git diff` shows changes under `docs/architecture/**` or `MODULE_CONTRACT.md`;
- a new class/package/module becomes part of the edit set;
- verification failures suggest a misunderstood boundary or invariant.

## Basic Memory Index Requirements

When Basic Memory is available, module-contract notes should include:

- repository/project name;
- source contract path;
- last observed commit hash or file hash when available;
- covered modules, packages, classes, jobs, endpoints, or data flows;
- responsibilities and explicit non-goals;
- invariants and error boundaries;
- verification requirements;
- links to related decisions or module contracts.

If the Basic Memory entry has no source path or freshness marker, the agent must treat it as a hint and read the repository file before relying on it.

## Reporting

In implementation summaries, the agent must include a short contract note when contracts were relevant:

- which contracts were read;
- which files were considered covered;
- whether the change preserves or changes the contract;
- which verification was run against contract requirements.

If no relevant contract was found, the agent must state that discovery was performed and name the remaining risk.

## Strict Rule

Do not edit production code until module-contract discovery for the touched files has completed. Basic Memory may satisfy discovery only as an index; relevant canonical contracts must still be read from the repository before editing.
