---
title: 'План миграции: классификация по context architecture (issue #17)'
permalink: ai-standards/artifacts/2026-09-21-context-architecture-migration-plan.ru
---

# План миграции: классификация по context architecture (issue #17)

Статус: завершено (2026-09-21, ветка `rules-change/17-rule-engineering`).
Фаза 4 плана изменений
`docs/artifacts/2026-09-19-rule-engineering-change-plan.ru.md`: формальная
модель размещения поставляется как feature `context-architecture`, текущий
self-hosted `AGENTS.md` классифицирован по ней, план миграции зафиксирован —
**без физических переносов в этой фазе**.

## Что поставлено

- Feature `context-architecture` (`process/context-architecture.md`):
  семислоевая модель размещения, упорядоченные placement-вопросы с тай-брейком
  «загружает позже» и инвариант control plane с гейтом сокращения
  (`CA-001`–`CA-005` в `rule_map.toml`).
- Заметка об уникальности: принцип размещения внутри потока Rule Engineering
  (`RE-006`) и правила этого feature — принцип и инструмент, а не дубликаты:
  `RE-006` фиксирует шаг в потоке, `CA-002`–`CA-003` — формальные вопросы, к
  которым шаг обращается. Precedence: решают вопросы.

## Классификация self-hosted AGENTS.md

Замер до рендера этого feature: 63 530 байт / 37 секций (feature добавит одну).
Размещение по модели:

| Группа | Секций | Слой сегодня | Решение |
|---|---|---|---|
| Ядро-инварианты (Engineering Workflow, Completion Discipline, DRY, Git Workflow, Architecture & Layering, Error Handling, Language & Communication) | 8 | always-loaded | оставить — универсальные инварианты, control plane по определению |
| Маршрутизация, гейты, управление (Retrieval Routing, Autonomy Boundaries, Session Hygiene, Agent Usage Hygiene, Design-First + Planning, Reasoning Hygiene, Module Contract Discovery Gate) | 7 | always-loaded | оставить — правила маршрутизации и обязательные гейты принадлежат control plane; только сжатие прозы, см. M2/M3 |
| Политика слоёв знания (Basic Memory Usage, Project Memory, Chroma Usage) | 3 | always-loaded | оставить — политика оперирования retrieval-слоями является маршрутизацией; механика уже в skills/адаптерах |
| Политика инженерных артефактов (Structured Artifacts, Change Plans, Module Contracts, Decision Records, Canonical Documentation policies, Optional Maps, Rejected Formalism, Knowledge Capture) | 8 | always-loaded | оставить — долговременная политика; длинные перечисления — кандидаты M3 на сжатие |
| Review-процесс (Code Review) | 1 | always-loaded | **M1 — главный кандидат на перенос**; условная процедурная задача с триггером на естественном языке |
| Features инициативы (Rule Engineering, Context Architecture) | 2 | always-loaded | оставить — процессные инварианты |
| Стек (Python Stack) | 1 | always-loaded | оставить — условность на уровне проекта (проект выбрал стек), не per-task знание |
| Self-hosted overrides (Documentation Language Policy, Documentation Scope, Workflow, Issue Tracker Language, Release Workflow) | 5 | always-loaded | оставить — по определению project knowledge, но рендеренный файл и есть средство доставки собственных правил репозитория |

## План миграции (исполняется в фазе 8, не сейчас)

Каждый перенос под гейтом: сравнение поведения baseline против candidate на
зафиксированных сценариях (`docs/scenarios/CR-001`–`CR-003` плюс поздние
пополнения), исполняется `ai-standards-evals` (issue #18). Перенос без
прошедшего сравнения отклоняется.

- **M1 — процедурное тело Code Review → skill reference.** Always-loaded
  сохраняет инварианты отчётности (доказательность, запрет накрутки, семантика
  маркеров, указатель на форму); проход за проходом уходит в reference навыка
  `standard-code-review`. Предусловие: activation evals фазы 7 показывают
  надёжное срабатывание навыка на голые review-запросы минимум на двух
  harness.
- **M2 — детали Module Contract Discovery Gate → skill reference.** Сам гейт
  (обязателен в момент правки) остаётся always-loaded как правило
  маршрутизации; критерии покрытия и детали отчёта уходят в reference,
  загружаемый при срабатывании гейта. Предусловие: тот же eval-гейт.
- **M3 — проход сжатия прозы** по самым длинным always-loaded секциям
  (перечисления формы отчёта, перечисления политики артефактов): тот же
  контент, меньше токенов; под тем же гейтом сравнений.

## Не-цели

- Никаких переносов, удалений и изменений рендерера в фазе 4.
- Никаких изменений для нижестоящих проектов: адаптеры не затронуты, пока не
  включат feature и не проведут собственную классификацию.

## Проверки

- `uv run pytest` (включая новые render/fragment тесты feature и policy-тесты
  карты для `CA-*`)
- `uv run ai-sync render --project-root .` идемпотентен; `ai-sync doctor` —
  ноль ошибок
- Классификация воспроизводима: список секций через `rg -n '^## ' AGENTS.md`
