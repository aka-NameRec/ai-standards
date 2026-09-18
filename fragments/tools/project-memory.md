## Project Memory

Local cross-session working memory keeps what the agent learned and where the work stands — outside Git history and outside canonical documentation.

- Keep local working memory under `docs/local/**`, gitignored by default (add `/docs/local/` to `.gitignore`). A project may relocate the tree via `[project_memory]` in the manifest.
- Never treat local working memory as canonical project documentation.
- Do not write temporary task state, speculative findings, or session continuation data into canonical documentation merely to preserve agent context.
- Promotion from local working memory to canonical documentation is an explicit semantic operation, never an automatic synchronization step. Promote only knowledge that has become durable, and only when the user or the project workflow permits the corresponding canonical artifact.
- Memory is a curated state store, not an execution log: record what future sessions need, not what merely happened.

### Taxonomy

- `context/` — what we are currently trying to accomplish: goal, scope, constraints, accepted direction, current phase, relevant artifacts, immediate next step. Not a transcript.
- `decisions/` — what has been decided locally and why: decision, reason, scope, and status (`provisional`, `confirmed`, `superseded`, `rejected`). Record a local decision when it materially constrains subsequent work; a local `confirmed` decision is confirmed for the current work context and does not automatically become a canonical record.
- `progress/` — where the work stopped: `done`, `current`, `blocked`, `next`. Update at meaningful phase boundaries and before ending work that is expected to continue in another session.
- `patterns/` — reusable project properties discovered during work. Treat a discovered pattern as working knowledge until validated against source code or canonical documentation; update or supersede it when contrary evidence appears; do not accumulate contradictory memories without recording their relationship.
- `investigations/` — open questions and the evidence found so far, with lifecycle `open`, `resolved`, or `abandoned`. An investigation may disappear, produce a pattern or a decision, or require human consultation.
- `handoffs/` — resume points: goal, confirmed state, current state, open questions, next action, and links to relevant memory. A handoff must be sufficient to resume the task without replaying the previous conversation, but compact enough to inspect before loading additional context.

The semantic categories are the standard; the physical split into directories may be configured per project.

### Write Policy

Write to local memory when the information will be needed in a later session, materially affects further decisions, is expensive to reconstruct, is the result of an investigation, explains the current status, captures an unresolved question or blocker, or is a confirmed reusable project pattern.

Do not write what a single obvious file already says, transient tool output, reasoning detail, what already exists canonically, a guess with no useful role, or a duplicate that changes no state.

### Read Policy

- Query local memory by the current goal, relevant entities, modules, concepts, decisions, and task identifiers — never read the whole memory tree at session start.
- To continue previous work: retrieve the relevant context, then the current progress, then the relevant decisions; open patterns and investigations only as the current step requires.

### Note Shape

- Minimal frontmatter: `title`, `type`, `status`, `updated`, plus `source` when the note records a discovered fact. Canonical-note requirements — dated file names, `## Observations` and `## Relations` sections — do not apply inside the local memory area.
- Local notes never mix into canonical zones; the knowledge-tree audit treats the local area with relaxed canonical rules.

### Durable Lessons

- After meaningful corrections or repeated mistakes, capture only durable lessons that can prevent the same class of error.
- Record the pattern, the preventive rule, and the scope where it applies.
- Do not create mechanical memory churn for one-off or low-signal corrections.

### Relationship To Basic Memory

- The taxonomy and lifecycle are tool-independent: plain files under `docs/local/**` satisfy them.
- The feature works best with `basic-memory`, which indexes the area for targeted retrieval — but it deliberately does not require it. The capability is separated from the way it is supported.
