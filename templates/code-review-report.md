<!--
This file is the single definition of the code-review report shape. It is a worked example, not a
skeleton: reproduce its sections, their order, and the fields on every finding. Translate every word
into the language the session is being held in; the 🔴 🟡 🔵 ✅ markers and the `ai-standards` version
line carry no translatable words and stay as they are. The rules that govern what belongs in a
finding live in the rendered `AGENTS.md`, under `Code Review`.
-->

## Code Review

ai-standards 2.1.0

Task: ALS-4821 — https://tracker.example.com/browse/ALS-4821

### What Was Done
Payment amounts uploaded from XLSX are now validated before any row is persisted.

### How It Was Done
Parsing stays in `openpyxl`. Each row goes through `PaymentValidator`, and only accepted rows
reach `PaymentService.bulk_create`; rejected rows come back with their line numbers. Validation
reuses the existing `Money` primitive rather than comparing raw decimals.

### Correctness
- ✅ payments_uploading.py:42 — a negative amount passed validation, because the guard was `amount != 0` rather than `amount > 0` — violates: Error Handling → fixed: guard is now `amount > 0`
- 🔴 payments_uploading.py:58 — an empty file returns `200 OK` having created nothing, so the caller cannot tell a successful upload from a silently ignored one — violates: Error Handling

### Architecture & Conventions
- 🟡 payments_uploading.py:15 — the file is parsed inside the view instead of the service layer — violates: django-service-layer → left as-is: not blocking, moving it out in a follow-up
- 🟡 payments_uploading.py:22 — the change re-exports `load_workbook` from the service layer, which the module contract lists under non-goals — violates: docs/architecture/2026-08-11-module-contract-payments.md — Non-goals → left as-is: the re-export goes away together with the wrapper in the follow-up noted above

### Reuse
- 🟡 payments_uploading.py:71, imports_uploading.py:64 — this change adds the same new `_read_sheet` wrapper to both modules; neither copy is an existing primitive, so nothing was under-reused, but the duplication is new — violates: DRY → left as-is: sibling modules call `load_workbook` inline, so the wrapper should be dropped on both sides rather than shared, and that is a separate patch
- 🔵 (pre-existing) payments_uploading.py:9 — XLSX parsing duplicates `services/export.py` — violates: DRY

### Efficiency
- None found.

### Quality
- 🟡 test_payments_uploading.py — no test covers the rejected-row path, so a regression in the line numbers would stay green — violates: core/base "Add or update focused tests for bug fixes, edge cases, and error paths"

### Verification
- `uv run pytest apps/payments` — 34 passed
- migrations and the uploader UI — not checked

### Dependencies
- `payments-frontend` — rejected rows now come back with a `line` field the uploader has to render
