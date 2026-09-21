## Context Architecture

Rule Engineering ends by selecting a context layer for the accepted knowledge; this feature defines the formal model that selection uses. It applies to every addition to the standards and to every review of what is already loaded.

### Placement Model

| Layer | Purpose |
|---|---|
| always-loaded rules | universal invariants, routing rules, mandatory gates, precedence, discovery instructions, minimum completion requirements |
| skill | repeatable task-specific procedure with a recognizable trigger |
| skill reference | detailed knowledge needed only while a specific skill mode runs |
| retrieval | a large, volatile, or searchable corpus of knowledge |
| script/tool | deterministic or fragile operations |
| project knowledge | durable project truth: decisions, contracts, domain notes |
| adapter | agent- and harness-specific mechanics |

### Placement Questions

Every addition answers the questions in order, and the first match wins:

```text
Needed for almost every task?
    → always-loaded rule

Repeatable procedure with recognizable trigger?
    → skill

Detailed knowledge needed only during that procedure?
    → skill reference

Large or searchable knowledge corpus?
    → retrieval

Deterministic or fragile operation?
    → script/tool

Durable project-specific fact or decision?
    → project knowledge

Agent-specific mechanics?
    → adapter
```

When two layers seem to fit, choose the one that loads the knowledge latest while still guaranteeing it arrives when needed.

### Control Plane Invariant

Always-loaded instructions stay a control plane: they carry universal invariants, routing, mandatory gates, precedence, discovery instructions, and minimum completion requirements — never task-specific operational detail. Reducing always-loaded content is a consequence of this placement and is performed only with a behavior-preserving comparison against the current state, so context savings never buy lost behavior.
