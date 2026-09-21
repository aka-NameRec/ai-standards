---
title: 'Набор триггер-кейсов TRG-001: standard-code-review'
permalink: ai-standards/scenarios/TRG-001-standard-code-review-triggers.ru
---

# Набор триггер-кейсов TRG-001: standard-code-review

Английская версия: [TRG-001-standard-code-review-triggers.md](TRG-001-standard-code-review-triggers.md)

Набор триггер-кейсов для навыка `standard-code-review`. Проверяет правило
`RVW-029` (активационные фразы навыка выбирают его вместо дефолтного потока)
и `SE-008` (корректность активации). Статус: черновик фазы 7; runner относится
к `ai-standards-evals` (issue #18).

## Включённые features

- `code-review` (навык гейтится на этот feature и развёртывается рядом с always-loaded потоком)

## Позитивные кейсы

| prompt | expected should_trigger |
|---|---|
| standard code review | true |
| «стандартный code review» | true |
| «сделай ревью по стандарту» | true |
| run the standard code review on this diff | true |

## Негативные кейсы

| prompt | expected should_trigger |
|---|---|
| code review | false — голый дефолтный поток, не навык |
| review this file | false — дефолтный поток |
| «проверь этот файл» | false — дефолтный поток |
| упрости этот код | false — режим очистки review-lenses, не стандартное ревью |
| write tests for this function | false — ревью вообще не требуется |

## Пограничные кейсы

| prompt | expected should_trigger |
|---|---|
| code review по стандарту проекта | true — стандарт назван |
| review this, use the standard report format | true — запрошен стандартный формат отчёта |
| code review, but skip the standard stuff | false — явный отказ; дефолтный поток |

## Наблюдения

- [fact] Голая фраза «code review» принадлежит always-loaded потоку; навык не должен её перехватывать.
- [fact] Пограничные кейсы включаются явным называнием стандарта или явным отказом от него.

## Связи

- implements [[РЕШЕНИЕ: принять инициативу Rule Engineering]]
- relates_to [[Dogfooding: Rule Engineering на feature code-review (issue #17)]]
- localized counterpart of [[Activation trigger set TRG-001: standard-code-review]]
