<!-- Source: https://github.com/HackSoftware/Django-Styleguide -->
<!-- Imported: 2026-04-10 -->
<!-- Adaptation: normalized for UMA2, extracted naming conventions as a composable fragment -->

## Django Naming Conventions
- Follow the `<entity>_<action>` naming convention for services and selectors (e.g., `user_create`, `order_list`).
- Follow the `<Entity><Action>Api` naming convention for API views (e.g., `UserCreateApi`, `CourseDetailApi`).
- Name test files `test_<name_of_thing_tested>.py` and test classes `<NameOfThingTested>Tests`.
