## Structural Code Intelligence (Experimental)

This capability is experimental. It is not part of the recommended stack: enable it only deliberately, after the A/B/C evaluation shows its measured improvement justifies deployment and maintenance cost.

- Prefer structural code intelligence when the question is primarily about relationships between known or discoverable code entities rather than semantic similarity: call paths, dependency paths, module relationships, impact analysis across modules, architecture traversal, structural navigation of a large codebase.
- Typical questions: what calls this; what depends on this module; which path connects endpoint X to persistence Y; what can be affected by changing class Z.
- Structural results narrow the candidate set; they do not prove completeness. Exhaustive or correctness-critical claims require exact search plus build, type, or static checks, and final verification happens at the authoritative layer — canonical docs, source code, and tests.
- Refresh the structural index before relationship queries, in the same event-driven way as the other retrieval indexes: after VCS operations and structural changes, never as a session ritual.
- The capability is implementation-neutral: a graph tool (Graphify is one possible backend) implements it, and the standards never encode a specific tool's commands.
- Do not treat a structural graph as a normative module contract: the graph captures what the code structurally is; contracts state what it should be.
