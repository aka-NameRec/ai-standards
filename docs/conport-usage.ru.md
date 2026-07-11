# Руководство по использованию ConPort

Англоязычная оригинальная версия: [conport-usage.md](conport-usage.md)

Это руководство объясняет, как использовать фичу `conport` из `ai-standards` в downstream-проектах.

`conport` стандартизует ConPort как transient operational memory для active context, недавнего прогресса, состояния исследования и session handoff'ов — не считая его каноническим источником durable project truth.

## Цели

Используйте `conport`, когда хотите, чтобы агент или команда:

- сохраняли active context и недавний прогресс между сессиями
- передавали состояние исследования между агентами или чатами без пере-вывода
- держали durable architectural knowledge в Git-tracked Markdown, а не в ConPort
- извлекали целевой оперативный контекст вместо выгрузки всего

Типичные результаты:

- более быстрый перезапуск сессий с точным контекстом
- меньше потерь состояния исследования между handoff'ами
- более чёткое разделение transient memory и reviewed truth

## Что покрывает фича

Фича стандартизует общую политику для:

- использования ConPort как transient operational memory и handoff-хранилища
- отношения к Git-tracked Markdown как к каноническому источнику durable truth
- targeted retrieval вместо больших context-выгрузок
- фиксации durable lessons только когда они предотвращают класс ошибок

Она намеренно не стандартизует:

- одну обязательную схему ConPort для каждого проекта
- конкретный confirmation-workflow (проекты могут подключать локально)
- автоматическое продвижение заметок ConPort в каноническую документацию

## Идентичность рабочего пространства

ConPort идентифицирует рабочее пространство по корневому пути. Используйте абсолютный путь корня проекта как `workspace_id`:

- рабочее пространство — корневой каталог проекта
- `context_portal/` находится в корне проекта и является gitignored runtime-состоянием

Создайте `context_portal/` до опоры на определение рабочего пространства ConPort. Без него detection может подняться по дереву каталогов к родителю (например, к домашнему каталогу) и привязать рабочее пространство к неверному корню.

## Transient memory, а не каноническая истина

ConPort — transient operational memory. Durable architectural, operational и module-boundary knowledge принадлежит Git-tracked Markdown-артефактам:

- decision records (`docs/decisions/**`)
- module contracts (`MODULE_CONTRACT.md`)
- architecture docs (`docs/architecture/**`)

ConPort дополняет эти артефакты; он их не заменяет. Продвигайте durable-выводы из ConPort в каноническую документацию только по явному запросу пользователя.

## Durable lessons

После значимых исправлений или повторяющихся ошибок фиксируйте только durable lessons, способные предотвратить тот же класс ошибок. Записывайте паттерн, превентивное правило и область применения. Не создавайте механический memory-churn для разовых или низкосигнальных исправлений.

## Связь с другими фичами

- `basic-memory` — retrieval-слой над Git-tracked Markdown-документацией.
- `chroma` — слой семантического поиска по исходным файлам.
- `structured-artifacts` определяет, какие Markdown-артефакты считаются планами, decision records и module contracts.
- `session-hygiene` определяет, когда перезагружать релевантный durable context между фазами или чатами.

`conport` дополняет эти фичи, сохраняя transient operational context и handoff'ы. Он не заменяет reviewable-документацию или явные человеческие решения.

## Пример манифеста

```toml
features = [
  "conport",
  "basic-memory",
  "chroma",
  "structured-artifacts",
  "session-hygiene",
]
```

## Практические подсказки для промптов

Хорошие промпты:

- `Загрузи active context ConPort в начале этой задачи.`
- `Запиши этот прогресс и следующий шаг в ConPort для handoff'а.`
- `Зафиксируй это как durable lesson только если это предотвращает класс ошибок.`

Избегать:

- `Считай ConPort источником истины для архитектуры.`
- `Выгружай всю базу ConPort в контекст.`
- `Продвигай заметки ConPort в docs/decisions без явного одобрения.`

Предпочитать:

- `Targeted retrieval релевантного контекста ConPort, затем действуй.`
