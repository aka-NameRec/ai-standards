---
title: Задачи GitHub на русском и предложения сентября 2026
permalink: ai-standards/tasks/rules-change-russian-github-issues.ru
---

# Задачи GitHub на русском и предложения сентября 2026

Задача `rules-change` (2026-09-17): три незакоммиченных предложения сентября 2026 из `docs/archive/` изучены и оформлены как задачи GitHub; новым правилом проекта закреплён язык задач.

## Что сделано

- Изучены три предложения: реорганизация memory/retrieval; Rule/Skill Engineering + Context Architecture + Standard Evals; спецификация `ai-standards-evals`.
- Созданы задачи на русском: #16 (реорганизация memory/retrieval), #17 (Rule Engineering / Context Architecture / Skill Engineering / Standard Evals), #18 (спецификация `ai-standards-evals`); #17 и #18 связаны перекрёстными ссылками, поскольку репозиторий evals реализует исполнимую половину предложения по Rule Engineering.
- В `ai/project-rules.md` добавлено правило «Issue Tracker Language», в русскую пару `ai/project-rules.ru.md` — «Язык задач в трекере»: задачи создаются исключительно на русском языке, включая title и description; технические имена приводятся дословно, без перевода.
- `AGENTS.md` перегенерирован через `ai-sync render`; `ai-sync check` проходит.
- Commit `4b1aaba` на `main`: изменение правил плюс четыре файла в `docs/archive/` (три предложения и один лог обсуждения).

## Наблюдения

- [fact] Три предложения сентября 2026 оформлены как задачи #16/#17/#18 на рассмотрение, а не приняты; направление ещё не выбрано, поэтому decision record по ним не создаётся.
- [fact] Задачи #17 и #18 разведены отдельно, чтобы методологию (стандарты) и инфраструктуру (репозиторий evals) можно было принимать или отклонять независимо.
- [decision] Задачи GitHub в этом репозитории создаются исключительно на русском языке — и title, и description; технические имена приводятся дословно, без перевода (правило «Issue Tracker Language» в `ai/project-rules.md`).
- [fact] Конвенция коммитов `task_id. (commit_type) message.` приняла `rules-change` как id задачи для этого набора изменений.

## Связи

- localized counterpart of [[Russian GitHub issues and September 2026 proposals]]