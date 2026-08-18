<!--
This file is the single definition of the code-review report shape. It is a worked example, not a
skeleton: reproduce its sections, their order, and the fields on every finding. Translate every word
into the language the session is being held in; the 🔴 🟡 🔵 ✅ markers carry no words and stay as they
are. The rules that govern what belongs in a finding live in the rendered `AGENTS.md`, under
`Code Review`.
-->

## Code Review

Task: ALS-4821 — https://tracker.example.com/browse/ALS-4821

### What Was Done
Payment amounts uploaded from XLSX are now validated before any row is persisted.

### How It Was Done
Parsing stays in `openpyxl`. Each row goes through `PaymentValidator`, and only accepted rows
reach `PaymentService.bulk_create`; rejected rows come back with their line numbers.

### Correctness
- ✅ payments_uploading.py:42 — a negative amount passed validation, because the guard was `amount != 0` rather than `amount > 0` — violates: Error Handling → fixed: guard is now `amount > 0`
- 🔴 payments_uploading.py:58 — an empty file returns `200 OK` having created nothing, so the caller cannot tell a successful upload from a silently ignored one — violates: Error Handling

### Architecture & Conventions
- 🟡 payments_uploading.py:15 — the file is parsed inside the view instead of the service layer — violates: django-service-layer → left as-is: not blocking, moving it out in a follow-up

### Reuse / Quality / Efficiency
- 🔵 (pre-existing) payments_uploading.py:9 — XLSX parsing duplicates `services/export.py` — violates: DRY
