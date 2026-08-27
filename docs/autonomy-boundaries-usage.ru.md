---
title: Autonomy Boundaries Usage Guide
permalink: ai-standards/autonomy-boundaries-usage.ru
---

# Autonomy Boundaries Usage Guide

Англоязычный оригинал: [autonomy-boundaries-usage.md](autonomy-boundaries-usage.md)

Это руководство объясняет, как использовать feature `autonomy-boundaries` из `ai-standards` в downstream-проектах.

`autonomy-boundaries` добавляет переиспользуемые правила, по которым агент решает, когда он может продолжать автономно, а когда обязан остановиться и запросить верификацию человеком.

Цель не в том, чтобы максимизировать автономию.
Цель в том, чтобы автономия оставалась reviewable, bounded, reversible и architecturally safe.

## Цели

Используйте `autonomy-boundaries`, когда вы хотите, чтобы агент или команда:

- отличали bounded execution от скрытой проектной работы
- заранее определяли, когда агент обязан остановиться, а не тихо импровизировать
- привязывали длинные автономные прогоны к явным проектным артефактам
- делали architecture drift и рост blast radius заметными до того, как они станут дорогими

Типичные результаты:

- меньше тихих design changes
- более раннее review, когда scope начинает дрейфовать
- лучшее разделение между execution и decision-making
- более дешёвое post-run review, потому что результат остаётся compressible

## Что покрывает feature

Этот feature стандартизует shared policy для:

- случаев, когда длинная автономная работа в принципе допустима
- предварительных условий, которые должны существовать до её начала
- стоп-условий, которые обязаны вызывать human checkpoint
- областей, слишком чувствительных для автономных design decisions
- набора review artifacts, который должен остаться по завершении прогона

Это именно process feature, а не stack rule и не tool-specific adapter.

## Базовое правило

Длинная автономная работа запрещена по умолчанию.

Предпочтительная модель разработки остаётся такой:

1. design-first alignment
2. bounded implementation
3. human review
4. next bounded cycle

Подключайте этот feature, когда проекту нужны переиспользуемые guardrails для исключительных случаев, где агенту разрешается дольше работать без промежуточного approval.

## Когда длинная автономная работа допустима

Разрешайте длинный автономный прогон только если одновременно верны все условия:

- дизайн уже выбран
- scope ограничен письменными артефактами
- automated verification достаточно сильна, чтобы отличать прогресс от дрейфа
- rollback дешёвый и предсказуемый
- blast radius мал и известен
- итоговое review всё ещё дешевле ручной реализации

Если хотя бы одно из этих свойств отсутствует, задачу нужно дробить на более короткие reviewed cycles.

## Session Envelope

Перед началом длинного автономного прогона зафиксируйте короткий session envelope в change plan, task note или эквивалентном артефакте.

Минимальные поля:

- objective
- scope
- non-goals
- architectural constraints
- verification plan
- stop conditions
- expected review artifacts

Feature не требует одного обязательного имени файла. Держите артефакт в рамках локального project workflow.

## Direction Checkpoints и Architecture Delta Checkpoints

На практике это различие важно.

### Direction Checkpoint

Остановитесь и запросите review, когда агенту нужно выбрать направление изменений, а не просто исполнять уже выбранный дизайн.

Примеры:

- выбор между двумя правдоподобными module boundaries
- решение, нужна ли вообще новая abstraction
- выбор migration strategy
- переопределение контракта ради упрощения реализации

### Architecture Delta Checkpoint

Остановитесь и запросите review даже тогда, когда направление изменений не менялось, но накопленная архитектурная дельта уже стала настолько значимой, что человек должен заново её утвердить.

Примеры:

- затронуто больше модулей, чем было заявлено
- появились новые cross-boundary dependencies
- изменение затронуло ещё одну подсистему
- reviewer уже не сможет понять итоговую структуру без нетривиального walkthrough

Именно этот второй checkpoint не даёт тезису "направление не менялось" превратиться в бесконтрольный structural drift.

## Обязательные стоп-условия

Как минимум, нужно останавливаться, когда:

- задача больше не укладывается в согласованные design, scope или invariants
- требуется новая abstraction, слой, изменение public contract, integration strategy или migration strategy
- verification перестаёт сходиться
- логи, падающие проверки или другие evidence противоречат design anchor
- blast radius заметно выходит за пределы объявленного scope
- rollback перестаёт быть дешёвым или предсказуемым
- architecture delta уже нельзя компактно пересказать для review

Проекты могут добавлять более жёсткие локальные пороги, но `ai-standards` не должен продвигать хрупкие числовые лимиты как shared defaults.

## Локальные checkpoint'ы внутри слайса

Длинная автономная работа не должна превращаться в один слепой прогон внутри уже разрешённого слайса.

Добавляйте локальные checkpoint'ы, когда текущий слайс содержит рискованные точки реализации, например:

- правки, чувствительные к контракту
- переходы состояний
- логику индексов или границ
- schema или data mapping
- cross-boundary calls

Слайс следует продолжать только пока следующий шаг всё ещё выглядит как небольшой согласованный patch с targeted verification. Если локальные исправления перестают сходиться или в слайсе обнаруживается несколько незапланированных hotspot'ов, нужно остановиться и либо дробить слайс, либо запросить review.

## Чувствительные области

Не разрешайте длинные автономные design decisions без явного approval человека в следующих областях:

- архитектура и границы модулей
- public APIs и backward compatibility
- schema и data migration strategy
- authentication и authorization
- secret handling и security policy
- production operations и другая автоматизация с большим blast radius

Это не просто зоны "нужна осторожность". Это review points.

## Связь с другими features

- `design-first-collaboration` определяет, как фиксируются intent, boundaries и non-goals.
- `reasoning-hygiene` улучшает качество self-review и работы с evidence.
- `structured-artifacts` даёт change plans и decision records, в которых можно хранить session envelope.
- `conport` хранит active context, recent findings и evolving memory между прогонами.

`autonomy-boundaries` определяет момент, когда агент должен перестать опираться только на эти входы и запросить human verification.

## Практика внедрения

Начинайте с процесса, а не с автоматизации:

1. Подключите feature в проектные инструкции.
2. Добавьте короткий формат session envelope в локальный workflow.
3. Определите два-три project-local stop conditions для чувствительных зон.
4. Проверьте на практике, действительно ли агент останавливается достаточно рано при дрейфе задачи.

И только после этого имеет смысл обсуждать более автоматизированные режимы автономии.