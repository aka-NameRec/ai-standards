---
name: skill-engineering
description: Engineer, validate, and evolve agent skills as portable knowledge packages — authoring through Rule Engineering, progressive disclosure, context economy, degrees of freedom, portable core, the four validation questions, and lifecycle states. Use when the user asks to create a skill («создай skill», "create a skill", «оформи навык»), edit or refactor an existing skill, or decide whether a recurring task deserves a skill at all.
argument-hint: [what to engineer]
---
# Skill Engineering

One domain for creating and maintaining skills. A skill is justified only when four things exist together: a recognizable trigger, a repeatable procedure, non-trivial reusable guidance, and observable completion criteria. Otherwise the better layer is an always-loaded invariant or the agent's own ability — adding a skill then only grows the surface the standard must maintain.

## Authoring (skill-authoring)

Author every skill through Rule Engineering: candidate guidance from any source → extract atomic behaviors → uniqueness and conflict check → portability check → context placement → observable behavior → accept / adapt / reject. For a non-trivial skill, record the worksheet as an artifact next to the decision records.

1. **Structure and activation.** Frontmatter carries `name` (kebab-case) and a `description` that does two jobs: states what the skill does and carries the concrete phrases that should and should not trigger it. Positive and negative triggers written down here are the basis of later activation testing.
2. **Progressive disclosure.** Metadata selects the skill; the body guides execution; detail beyond the critical path goes to reference sections — or reference files, where the deployment model supports them. Never front-load everything the skill will ever need.
3. **Context economy.** Include only what changes decisions or improves execution. Do not explain what capable models already reliably know; restating general knowledge spends context without changing behavior.
4. **Degrees of freedom.** Match determinism to risk: heuristics for low-risk judgment calls, structured procedures for repeatable flows, deterministic scripts or tools for fragile or exact operations. A script beats a paragraph when the operation must not vary.
5. **Portable core.** The skill body assumes no specific agent, vendor, or harness: no invocation syntax, UI, hooks, or tool-specific commands. Agent-specific mechanics live in adapters. Activation phrases may name harness idioms; the procedure may not depend on them.
6. **Self-containment.** A deployed skill carries the procedure it needs and never points into standards-repository internals; where it enforces normative rules, it restates them rather than referencing them.
7. **Observable completion.** The skill states what counts as done, concretely enough that a scenario can verify execution from the outcome alone.

## Validation

Four independent questions, in order — answering one says nothing about the next:

- **Structural validity** — frontmatter, naming, sections present. The only question a static validator answers; it proves nothing about quality.
- **Activation correctness** — positive, negative, and boundary triggers; activation recall and precision measured against the triggers written in the description.
- **Behavioral correctness** — task scenarios with expected invariants: activation is not execution, and the outcome is judged, not the wording.
- **Behavioral efficacy** — with-skill versus without-skill on the same task, model and environment held constant. Activation without improvement is surface area, not value.

## Lifecycle

```text
candidate → draft → structurally validated → activation-tested
→ behavior-tested → project-local → stabilized → generalized
→ shared → observed → revised / deprecated
```

A skill advances only when the corresponding validation question has been answered. Deprecation records the reason and keeps the rationale readable; a retired skill's ID and name are not reused.

## Relationship To Other Layers

- The standards' rules are authored by Rule Engineering; a skill packages a repeatable procedure. If the content is an invariant that must always hold, it belongs in a fragment, not in a skill.
- Splitting this domain into separate skills (authoring, validation, lifecycle) happens only when real usage shows independent triggers and workflows — not in advance.
