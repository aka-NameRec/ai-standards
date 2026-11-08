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

### Progressive Disclosure Default

- Every addition to the standards, and every amendment of existing content, is placed by default at the latest-loading layer able to carry it: a skill, a skill reference, a deployed reference file (reference disclosure mode), or retrieval. The user's context budget is the protected resource; the always-loaded surface grows only by exception.
- Inline always-loaded placement is that exception: it requires the control-plane test to pass and a recorded reason no later-loading layer can guarantee the content arrives when needed. "The content is a new rule", "the table is convenient here", or "the pointer adds a hop" are not such reasons.
- When amending content that is already always-loaded, new detail goes to the later-loading layer the procedure provides, and the always-loaded text keeps the trigger and the invariant. Growth of the always-loaded surface within a change is a placement defect fixed in that same change, not deferred.

### Control Plane Invariant

Always-loaded instructions stay a control plane: they carry universal invariants, routing, mandatory gates, precedence, discovery instructions, and minimum completion requirements — never task-specific operational detail. Reducing always-loaded content is a consequence of this placement and is performed only with a behavior-preserving comparison against the current state, so context savings never buy lost behavior.
