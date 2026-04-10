<!-- Source: internal Django projects -->
<!-- Imported: 2026-04-10 -->
<!-- Adaptation: normalized for UMA2, generalized to cover both DRF and plain Django entry points -->

## Django Save Lifecycle

### Principle
- Use the view or viewset as the orchestration point for pre-save and post-save logic instead of Django signals.
- Keep business logic functions in the services layer; the view/viewset orchestrates calls to those functions around the persistence boundary.

### DRF Viewset Pattern
- Define a base viewset with a `save(self, serializer, additional_data=None)` method called from `perform_create` and `perform_update`.
- Override `save()` in concrete viewsets to add pre-save and post-save logic; do not override `perform_create` or `perform_update` directly.
- Place validation, data normalization, and business-rule checks **before** `super().save(serializer)` (pre-save phase).
- Place side effects, derived value updates, and cross-model syncing **after** `super().save(serializer)` (post-save phase).
- Access the current model state via `serializer.instance` (`None` on create) and user-submitted data via `serializer.validated_data`.
- Use the `additional_data` parameter to inject request context (e.g., `created_by`, `updated_by`) into `serializer.save(**additional_data)`.

### Plain Django CBV Pattern
- Define a base `CreateView`/`UpdateView` with a `save(self, form, additional_data=None)` method called from `form_valid`.
- Override `save()` in concrete views to add pre-save and post-save logic.
- Place validation and business-rule checks **before** the model is persisted (pre-save phase).
- Place side effects and cross-model syncing **after** the model is persisted (post-save phase).
- Access the current model state via `form.instance` and user-submitted data via `form.cleaned_data`.
- Use `form.save(commit=False)` to apply additional fields before calling `instance.save()`.

### Signals
- With this pattern active, signals should be reserved only for cross-cutting events that must fire regardless of the entry point (audit logging, activity tracking).
- Do not duplicate save-lifecycle logic in both signals and the view/viewset `save()`.
