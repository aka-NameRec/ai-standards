## ConPort Usage
- At the start of each task or session, load relevant ConPort context when the MCP server is available.
- Use ConPort for transient operational memory such as active context, recent progress, investigation state, and session handoffs.
- Do not treat ConPort as the canonical source of durable project truth.
- Record durable architectural, operational, and module-boundary knowledge in Git-tracked Markdown artifacts such as decision records and module contracts.
- Prefer targeted retrieval over large context dumps.
- Before logging substantial new knowledge, align with the user if the workspace follows a confirmation-based ConPort workflow.
- After significant work, update ConPort with the result, rationale, and next steps when the user wants the memory synchronized.

## Durable Lessons
- After meaningful corrections or repeated mistakes, capture only durable lessons that can prevent the same class of error.
- Record the pattern, the preventive rule, and the scope where it applies.
- Do not create mechanical memory churn for one-off or low-signal corrections.
