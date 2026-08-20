# DECISION: think-anywhere-local-reasoning-checkpoints

Англоязычный оригинал: [2026-04-21-think-anywhere-local-reasoning-checkpoints.md](2026-04-21-think-anywhere-local-reasoning-checkpoints.md)

## Статус

Accepted

## Дата

2026-04-21

## Контекст

Статья `Think-Anywhere` о генерации кода показывает, что reasoning особенно полезен тогда, когда он включается по требованию в точках локальной неопределённости, а не только в одном upfront-блоке планирования. Существующие process features `reasoning-hygiene` и `autonomy-boundaries` уже покрывали пошаговый анализ и стоп-условия, но пока не фиксировали явно, что нетривиальная реализация должна повторно проверять предположения внутри текущего слайса.

## Решение

Расширить process standards так, чтобы:

- `reasoning-hygiene` требовала локальной переоценки во время реализации, особенно в рискованных фрагментах и в логике, чувствительной к границам;
- `autonomy-boundaries` требовала локальных checkpoint'ов внутри слайса, а не только проверки в конце слайса, и останавливала автономию, когда локальные исправления перестают сходиться;
- англоязычные и русскоязычные usage guides явно объясняли этот паттерн reasoning во время реализации.

## Почему

- это соответствует главному практическому выводу статьи без копирования model-specific training details
- это удерживает reasoning в местах, где риск ошибки наиболее высок
- это естественно ложится на уже существующее разделение между качеством анализа и границами автономии
- это делает стандарты более прикладными для агентов, которые работают короткими implementation slices

## Рассмотренные альтернативы

### Оставить текущие рекомендации без изменений

Отклонено, потому что текущие правила уже поддерживают пошаговое reasoning в общем виде, но не делают паттерн локальных checkpoint'ов в реализации явным.

### Создать отдельный feature для slice-level reasoning checkpoints

Отклонено, потому что новая рекомендация естественно помещается в существующее разделение `reasoning-hygiene` и `autonomy-boundaries`.

## Последствия

### Плюсы

- у агентов появляется более ясное ожидание повторно проверять предположения во время реализации
- review становится проще, потому что точки локального риска проявляются раньше
- автономия останавливается раньше, когда слайс перестаёт сходиться

### Минусы или цена

- стандарты становятся чуть более детализированными
- downstream prompts может понадобиться небольшой апдейт под новый language локальных checkpoint'ов

## Затронутые модули

- `fragments/process/reasoning-hygiene.md`
- `fragments/process/autonomy-boundaries.md`
- `docs/reasoning-hygiene-usage.md`
- `docs/reasoning-hygiene-usage.ru.md`
- `docs/autonomy-boundaries-usage.md`
- `docs/autonomy-boundaries-usage.ru.md`
- `AGENTS.md`

## Инварианты и ограничения

- shared standards должны оставаться короткими и переиспользуемыми между проектами
- локальные checkpoint'ы должны оставаться фокусом на риск корректности, а не превращаться в общие правила verbosity
- границы автономии по-прежнему зависят от явного session envelope и reviewable stop conditions

## Проверка

- обновлённые фрагменты попадают в `AGENTS.md` при render
- англоязычные и русскоязычные usage guides описывают локальное reasoning и checkpoint'ы внутри слайса
- `scripts/ai_sync.py render` и `scripts/ai_sync.py check` проходят успешно

## Связанные артефакты

- [../0tdtl1j-log-arxiv.org-2603.29957.md](../../temp/0tdtl1j-log-arxiv.org-2603.29957.md)
- [../reasoning-hygiene-usage.md](../reasoning-hygiene-usage.md)
- [../autonomy-boundaries-usage.md](../autonomy-boundaries-usage.md)
