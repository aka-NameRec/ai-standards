## Rule Engineering

Normative knowledge earns its place through engineering, not through import.
Whatever the source — external best practices, project-internal insights,
reasoning rules, review rules, architecture rules, harness rules, or skill
content — every rule passes through the same process before it becomes part of
the standards, and an existing rule passes through it again when it materially
changes.

Apply the full flow when adding normative rules from any source and when
materially changing existing ones. A small, evidence-backed wording correction
of an existing rule does not require the full flow.

### Rule Quality Properties

A rule is acceptable only when all of the following hold:

- **Atomic** — one normative requirement per rule. Parts that can be violated
  independently become separate rules.
- **Unambiguous** — the wording leaves as few reasonable interpretations as
  possible. Replace vague preferences with observable procedure: not "use
  existing abstractions where appropriate", but "before introducing a new
  abstraction, inspect the relevant scope for one serving the same
  responsibility, and reuse it unless a documented incompatibility prevents
  reuse".
- **Actionable** — the rule states what the agent must do or must not do.
- **Properly scoped** — applicability conditions and boundaries are explicit.
- **Observable** — compliance has a formulatable criterion: an observable
  state or behavior, even when automatic checking is impossible.
- **Unique** — no existing rule already demands the same observable behavior
  under the same preconditions. Check overlap at three levels — lexical,
  semantic, behavioral — and let behavioral overlap decide.
- **Non-conflicting** — under the same conditions the rule is co-satisfiable
  with existing rules, or an explicit precedence rule says which one wins.
- **Correct abstraction level** — the rule lives at the most general level
  where it stays true; project-specific, stack-specific, and universal process
  knowledge are not mixed.
- **Portable** — a shared rule assumes no particular agent, vendor, or model;
  agent-specific mechanics live in adapters.

### Interpretation Surface

Prefer the wording that minimizes the **interpretation surface**: the number
of material decisions an agent must invent between reading a rule and acting
on it. Minimize it wherever reproducible behavior is required, and do not
force it down where the task genuinely requires contextual judgment.

### Engineering Flow

```text
candidate normative knowledge
    → extract candidate behaviors
    → make each requirement atomic
    → clarify preconditions and scope
    → check interpretation ambiguity
    → check lexical / semantic / behavioral overlap
    → check conflicts and precedence
    → select abstraction level
    → select context layer
    → define observable behavior
    → define validation
    → accept / adapt / reject
```

Validation is chosen per rule — static validation, deterministic assertion,
behavioral scenario, human rubric, or cross-agent comparison; at least one
must be formulatable, and a rule without any stays out of the standards.
Reject vague, redundant, and conflicting candidates, and state why each
notable candidate was rejected.

### Context Placement

Place knowledge at the layer that delivers it at the right moment, not the
layer that loads it earliest: always-loaded rules only for what correct
behavior selection requires everywhere; repeatable procedures with
recognizable triggers as skills; conditional detail as skill references;
large or searchable corpora through retrieval; deterministic or fragile
operations as scripts and tools; durable project truth as project knowledge;
harness-specific mechanics in adapters. Reducing always-loaded content is a
consequence of this placement, never a goal in itself, and never at the cost
of an unverified behavior change.
