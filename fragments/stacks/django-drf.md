<!-- Source: https://github.com/HackSoftware/Django-Styleguide -->
<!-- Imported: 2026-04-10 -->
<!-- Adaptation: normalized for UMA2, extracted DRF-specific guidance as a composable fragment -->

## Django REST Framework
- Prefer inheriting from DRF `APIView` over generic views to keep control explicit.
- Nest `InputSerializer` and `OutputSerializer` inside the API class; prefer `Serializer` over `ModelSerializer`.
- Do not reuse serializers across different APIs unless intentional.
- Validate incoming data with the input serializer, then delegate to the service or viewset save lifecycle.
