---
title: 'DECISION: refresh-react-vue-guidance'
permalink: ai-standards/decisions/2026-04-16-refresh-react-vue-guidance.ru
---

# DECISION: refresh-react-vue-guidance

Англоязычный оригинал: [2026-04-16-refresh-react-vue-guidance.md](2026-04-16-refresh-react-vue-guidance.md)

## Статус

Accepted

## Дата

2026-04-16

## Контекст

Существующие stack fragments `react` и `vue` в `ai-standards` поддерживались неравномерно.

Во Vue-фрагменте уже была полезная база, но в нём смешивались устойчивые framework rules с частично устаревшими или недостаточно конкретными формулировками. React-фрагмент, наоборот, был слишком тонким и не тянул на реалистичный shared baseline для современных React-проектов, которые теперь компонуются с новым стеком `typescript`.

Сверка с текущей официальной документацией React и Vue показала несколько устойчивых рекомендаций, которые стоит явно отразить:

- React делает акцент на pure rendering, вычислении derived state прямо во время render, использовании Effects только для external synchronization и отказе от лишней manual memoization.
- Современный React также даёт официальные APIs для подписки на external stores и для non-urgent rendering work; это стоит отразить в shared guidance, не превращая фрагмент в набор микропредписаний.
- Современные рекомендации Vue 3 центрируются вокруг Composition API с `<script setup>`, явных conventions для composables, computed-first derived state, SSR-safe side effects и осознанной performance-работы, включая stable props и virtualization для больших списков.

Репозиторию нужны такие фрагменты React и Vue, которые одновременно современны, practically useful, composable и свободны от недолговечной стилевой догмы.

## Решение

`ai-standards` обновляет stack fragments `react` и `vue`, чтобы привести их в соответствие с текущими official recommendations и типовыми production practices.

Обновлённый React-фрагмент теперь покрывает pure rendering, minimal и derived state, Effects как escape hatch, custom Hooks для переиспользуемой stateful logic, сдержанность в manual memoization, границы интеграции с external stores и осознанное применение transition APIs.

Обновлённый Vue-фрагмент сохраняет Composition API как baseline и добавляет `<script setup>`, computed-first state derivation, более сильные conventions для composables, SSR-safe side-effect handling, более явные component contracts и более конкретные performance-рекомендации.

## Почему

- делает стек `react` пригодным как реальный shared baseline, а не placeholder
- выравнивает framework guidance с текущими официальными рекомендациями, а не со старыми prompt-pack defaults
- улучшает композицию с общим стеком `typescript`, сохраняя language-level rules отдельно от framework rules
- добавляет устойчивые guardrails против типичных frontend-problem patterns: redundant state, чрезмерное использование Effects, unstable props и утечки side effects

## Рассмотренные альтернативы

### Оставить React и Vue fragments почти без изменений

Отклонено, потому что текущий React-фрагмент содержательно неполон, а текущему Vue-фрагменту не хватает нескольких современных conventions, которые уже достаточно устоялись для включения в shared standards.

### Расширить framework fragments проектно-специфичными архитектурными правилами

Отклонено, потому что `ai-standards` должен сохранять React- и Vue-guidance переиспользуемыми для разных frontend architectures и state-management choices.

### Добавить сильно специфичные правила для React Compiler, Server Components, Vue macros или отдельных библиотек

Отклонено, потому что такие темы либо зависят от окружения, либо слишком быстро меняются, либо слишком специфичны для durable shared baseline.

## Последствия

### Плюсы

- downstream-проекты получают более прикладной baseline для React и Vue и реже нуждаются в local patching
- React-фрагмент теперь дополняет общий стек `typescript`, а не дублирует его
- Vue-фрагмент лучше отражает текущие conventions Vue 3 и официальные performance-рекомендации

### Минусы или цена

- командам с legacy Options API или сильной зависимостью от manual memoization могут понадобиться local overrides
- репозиторию придётся и дальше отслеживать guidance фреймворков, чтобы фрагменты оставались durable и снова не деградировали

## Затронутые модули

- `fragments/stacks/react.md`
- `fragments/stacks/vue.md`
- `tests/test_ai_sync.py`

## Инварианты и ограничения

- `react` и `vue` остаются framework-specific fragments, а не местом для общих TypeScript-правил
- фрагменты остаются сфокусированными на durable conventions, а не на мимолётной toolchain-моде или style trivia
- архитектурно-специфичные решения вроде folder layout, query libraries и design systems остаются project-local, если только не становятся broadly reusable standards

## Проверка

- renderer tests проверяют новые React-формулировки про Effects и границы работы с external stores
- renderer tests проверяют новые Vue-формулировки про `<script setup>`, computed-first derivation и conventions возврата из composables
- общие проверки репозитория остаются зелёными

## Связанные артефакты

- [../../fragments/stacks/react.md](../../fragments/stacks/react.md)
- [../../fragments/stacks/vue.md](../../fragments/stacks/vue.md)
- [../../tests/test_ai_sync.py](../../tests/test_ai_sync.py)