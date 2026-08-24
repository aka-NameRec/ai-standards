# Bug: ai-sync managed-marker breaks Python and TOML templates

Status: fixed — upstream fix landed 2026-08-24 as option 1 (per-destination
comment syntax, shebang preserved as the first line). Re-running
`ai-sync sync-templates` rewrites managed headers into the valid format and
supersedes the downstream workaround. Raised 2026-08-03.

## Summary

`ai-sync sync-templates` wraps every managed template file with an HTML comment
marker:

```
<!-- Managed by ai-standards template: <source-path> -->
<!-- Do not edit manually unless you remove this marker. -->
```

This marker is only valid in Markdown/HTML. For `.py` and `.toml` managed
templates it is inserted at the top of the file and corrupts syntax, so the
generated files cannot run or be parsed.

## Reproduction

1. In a downstream project, enable the `chroma` feature in `ai.project.toml`
   and declare at least one agent under `[tooling].agents`.
2. Run `ai-sync sync-templates --project-root <project>`.
3. Inspect the generated chroma infra files:
   - `.ai-standards/scripts/code_index.py`
   - `.ai-standards/code-index.toml`

Both begin with the HTML comment marker.

### Observed failures

- `code_index.py`: first line is `<!-- Managed by ai-standards ... -->` instead
  of the `#!/usr/bin/env -S uv run --script` shebang. Running the wrapper fails:
  ```
  File ".../code_index.py", line 1
      <!-- Managed by ai-standards template: ... -->
      ^
  SyntaxError: invalid syntax
  ```
  The HTML comment is not a valid Python statement and also displaces the
  shebang from the first line.
- `code-index.toml`: `<!-- ... -->` is not a valid TOML comment, so
  `tomllib.loads(...)` raises `TOMLDecodeError` when the wrapper reads its
  config. (This is masked in practice because the Python syntax error fires
  first.)

## Root cause

`scripts/ai_sync.py`, `_build_managed_template_content`:

```python
def _build_managed_template_content(source_relative_path: str, raw_content: str) -> str:
    marker_block = (
        f"<!-- {MANAGED_TEMPLATE_MARKER_PREFIX} {source_relative_path} -->\n"
        "<!-- Do not edit manually unless you remove this marker. -->\n"
    )
    ...
    return marker_block + "\n" + raw_content   # line 479 — prepends HTML to every file
```

`_is_managed_template_content` (line 482) detects management by the presence of
`MANAGED_TEMPLATE_MARKER_PREFIX` anywhere in the content, so detection itself
is format-agnostic; only the injected marker text is the problem.

The upstream templates are correct: e.g.
`templates/ai-infrastructure/scripts/code_index.py` starts with the shebang and
has no marker. The corruption is introduced purely by `sync-templates`.

Affected file kinds today (feature-gated by `chroma`):

- `.ai-standards/scripts/code_index.py` (Python)
- `.ai-standards/code-index.toml` (TOML)

Markdown/cursor/claude templates (`.SKILL.md`, `.cursor.mdc`, `.claude.md`) are
unaffected because HTML comments are valid there.

## Workaround (applied downstream)

In `devcats-duty-leave`, replaced the HTML marker with a format valid for each
file type and restored the shebang as the first line:

- `code_index.py`:
  ```python
  #!/usr/bin/env -S uv run --script
  # Managed by ai-standards template: templates/ai-infrastructure/scripts/code_index.py
  ```
- `code-index.toml`:
  ```toml
  # Managed by ai-standards template: templates/ai-infrastructure/code-index.toml
  ```

The wrapper then builds and queries successfully (`refresh` → `records=N`,
`code-query` returns ranked chunks).

Caveat: removing the literal `<!-- Managed ... -->` string makes the file look
unmanaged to `sync-templates`, so the next `sync-templates` run will either skip
it or overwrite it with the broken marker again. This is a local stopgap until
the upstream fix lands. (Superseded: detection matches the marker text prefix,
which the `#`-form above carries, and the upstream fix now writes exactly this
form, so re-running `sync-templates` converges on the valid header.)

## Proposed fixes (choose one, or combine)

1. **Per-extension marker format.** In `_build_managed_template_content`, choose
   the comment syntax by destination extension:
   - `.py`, `.toml`, `.yaml`/`.yml`, `.sh` → `#`-line comments;
   - `.md`, `.mdc`, `.html` → `<!-- -->`;
   - shebang files: keep `#!...` first, then the marker comment.
2. **Skip non-Markdown templates.** Only inject the marker for Markdown-like
   destinations and manage code/config templates by a different signal (e.g.
   a sentinel path list) or leave them as plain upstream copies.
3. **Marker as a trailing comment / separate sidecar.** Track management via a
   sidecar manifest instead of mutating file headers, so syntax is never
   affected.

Option 1 keeps the existing single-file management model with the smallest
behaviour change and preserves the marker for Markdown templates.

## Verification the fix should pass

- After `ai-sync sync-templates` on a `chroma`-enabled project:
  - `.ai-standards/scripts/code_index.py` runs under
    `uv run --script .ai-standards/scripts/code_index.py refresh` without a
    `SyntaxError`;
  - `.ai-standards/code-index.toml` parses with `tomllib`;
  - Markdown templates still carry the HTML marker and remain recognized as
    managed by `_is_managed_template_content` (or the updated detection).
- Existing unit tests in `tests/` continue to pass; add cases covering `.py`
  and `.toml` destinations.

## Related

- Discovered while deploying the AI knowledge stack in
  `devcats-duty-leave` (cockpit project
  `devcats-duty-leave`, ConPort progress entry 2026-08-03).
