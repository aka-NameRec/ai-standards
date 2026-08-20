# Chat Export

## Критерии останова агента для верификации человеком в ai-standards

**Question**

(0tdo987) Пожалуйста, переключись в проект ai-standards, и ознакомься с документом `~/workspace/myself/cockpit/docs/0tdo6uk-ChatGPT-GLM-From Vibe Coding to Agentic Engineering.md`, содержащим важное обсуждение критериев допустимости т.н. "длинных сессий", когда агент автономно (без верификации человеком) вносит изменения в проект.
Я хотел бы расширить набор пратвил ai-standards критериями, руководствуясь которыми агент принимал бы самостоятельное решение, что следует остановиться, и запросить верификацию направления изхменений, и изменений, выполненных агентом в архитектуре проекта с момента получения задания.
Верифицируй обсуждение: интересут твоя оценка и предложения в свете обозначенного выше.

**Answer**

Перехожу в `ai-standards`, сначала подниму его локальные правила и ConPort, затем прочитаю указанный документ и сверю обсуждение с текущим набором норм проекта.

Нашёл репозиторий и переключаюсь на его контекст. Сейчас прочитаю `AGENTS.md` проекта `ai-standards` и загружу ConPort, чтобы оценка опиралась на его собственные правила, а не на предположения.

Контекст восстановлен. Дальше читаю сам документ обсуждения и параллельно найду в `ai-standards`, где сейчас уже описаны границы автономной работы, чтобы сравнение было точным.

В обсуждении уже видно сильную базу: запрет не на длинный горизонт как таковой, а на бесструктурную автономию. Сейчас дочитаю именно policy-часть и сравню её с существующими механизмами `ai-standards`, чтобы предложить не общие мысли, а внедряемые критерии остановки.

Переход к внешней верификации тезисов. Проверю опорные источники по GLM, Fowler и по кейсам Anthropic, чтобы отделить устойчивые инженерные выводы от маркетинга и устаревших пересказов.

**Вердикт**

Обсуждение в целом сильное. Его центральный тезис я считаю корректным: проблема не в самом `long-horizon` режиме, а в длинной автономии без внешних якорей, стоп-условий и дешёвой проверки курса. Это хорошо согласуется и с Fowler’ом про `Design-First Collaboration`, и с тем, как сами Anthropic позже описывали безопасную автономию: не как “пусть агент просто работает долго”, а как работу внутри `harness` с ограничениями, проверками и явными условиями остановки.

Но в текущем draft есть несколько мест, которые я бы усилил, прежде чем превращать это в правило `ai-standards`.

**Что в обсуждении подтверждается**

- Тезис `design first -> bounded execution -> review -> next cycle` подтверждается Fowler’ом: он прямо продвигает поэтапное выравнивание по intent, components, interactions и contracts до кодирования. Источник: Martin Fowler, `Design-First Collaboration`  
  https://martinfowler.com/articles/reduce-friction-ai/design-first-collaboration.html
- Тезис о ценности длинного инженерного цикла у GLM тоже реален, а не выдуман пересказом: в техотчёте GLM-5 framing именно такой, от `vibe coding` к `agentic engineering`. Источник: GLM-5 paper  
  https://arxiv.org/abs/2602.15763
- Идея, что длинные сессии требуют специальной обвязки, а не просто “умной модели”, тоже подтверждается. Anthropic отдельно пишут про `multi-agent` orchestration, long-running harnesses и classifier-gated autonomy, а не про безусловное доверие агенту. Источники:  
  https://www.anthropic.com/engineering/built-multi-agent-research-system  
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents  
  https://www.anthropic.com/engineering/claude-code-auto-mode
- Важный практический вывод из Anthropic на 2026-04-18: даже их `computer use` остаётся `beta`, а официальная документация прямо советует human oversight и аккуратную проверку действий и логов. Источник:  
  https://docs.anthropic.com/en/docs/build-with-claude/computer-use

**Что в обсуждении я бы поправил**

- Порог `30+ meaningful steps` полезен как локальная эвристика, но слаб как shared standard. Для `ai-standards` лучше определять “длинную автономию” не по числу шагов, а по отсутствию human checkpoint при ненулевом архитектурном или операционном риске.
- `Machine-verifiable` недостаточно само по себе. Тесты могут проходить, а архитектурный дрейф уже произошёл. Значит, нужны не только quality gates, но и отдельные `architecture stop conditions`.
- В draft пока смешаны два разных повода остановки:
  - нужно верифицировать **направление** изменений;
  - нужно верифицировать **накопившуюся архитектурную дельту** с начала задачи.
  Это разные режимы, и их лучше разделить явно.
- Кейс с “браузером Anthropic, сделанным толпой агентов” не годится как опорное доказательство допустимости длинных бесконтрольных сессий. По состоянию на 2026-04-18 я не вижу у Anthropic подтверждения истории вида “мы автономно сделали production-ready browser”. Есть:
  - multi-agent research system,
  - `computer use` beta,
  - `Claude in Chrome` как research preview/beta в 2025,
  - отдельные статьи про безопасную автономию и harnesses.
  То есть этот пример лучше либо убрать, либо ослабить до “рынок экспериментирует с browser agents, но это не доказательство безопасности длинной автономии”.

**Главное предложение для `ai-standards`**

Я бы не встраивал весь policy draft в `core`. Для shared standard это слишком тяжёлый и местами workflow-specific слой. Вместо этого предложил бы двухуровневую модель.

1. Вынести минимальное универсальное правило остановки в process-уровень, рядом с [design-first-collaboration.md](/home/shtirliz/workspace/myself/ai-standards/fragments/process/design-first-collaboration.md) и [structured-artifacts.md](/home/shtirliz/workspace/myself/ai-standards/fragments/process/structured-artifacts.md):
- stop and request review when the task no longer fits the agreed design;
- stop when a new abstraction, public contract change, or boundary change becomes necessary;
- stop when verification is non-converging or scope expands materially.

2. Полный policy оформить как отдельный opt-in feature, а не как обязательное ядро. Условное имя: `autonomy-boundaries` или `human-checkpoints`.

Это лучше ложится на текущую архитектуру `ai-standards`: сейчас там уже есть process-features вроде `design-first-collaboration`, `reasoning-hygiene`, `structured-artifacts`, `review-lenses`, но нет отдельного feature для границ автономии. Это видно по [registry.toml](/home/shtirliz/workspace/myself/ai-standards/registry.toml) и текущему [AGENTS.md](/home/shtirliz/workspace/myself/ai-standards/AGENTS.md).

**Какие критерии остановки я бы добавил обязательно**

Не “можно ли продолжать”, а именно “обязан ли агент остановиться”.

- Появилась необходимость выбрать между двумя или более правдоподобными design directions.
- Изменение выходит за заранее объявленные module boundaries, dependency boundaries или contract boundaries.
- Потребовались новая абстракция, новый слой, новая integration strategy, новая migration strategy.
- Изменение затронуло public API, schema, backward compatibility, security-sensitive path, permissions, secrets, auth/authz.
- Верификация перестала сходиться:
  repeated failing tests, contradictory logs, flaky evidence, patch-on-patch correction loop.
- Blast radius вырос относительно envelope:
  неожиданно затронуто больше файлов, модулей или подсистем, чем планировалось.
- Rollback перестал быть дешёвым.
- Архитектурную дельту с начала задачи уже нельзя компактно объяснить в коротком review artifact.
- Для продолжения нужно опереться на скрытую интерпретацию, а не на явные project artifacts.

**Что я бы добавил сверх draft**

Самое важное дополнение: разделить два checkpoint-типа.

- `Direction checkpoint`
  Когда агент понимает, что дальше надо не исполнять, а выбирать направление.
- `Architecture delta checkpoint`
  Когда агент не меняет направление, но уже накопил значимую архитектурную дельту с начала задания, и её нужно отдельно предъявить человеку.

Это прямо отвечает на твою цель: агент должен сам решать не только “я упёрся в неопределённость”, но и “я уже слишком далеко сдвинул архитектуру, чтобы продолжать без сверки”.

Для этого в session envelope я бы добавил ещё два поля:

- `allowed architecture delta`
- `review trigger budget`

Примерно в таком духе:

- allowed architecture delta: no new layers, no public contract changes, no module moves, no cross-boundary dependency additions
- review trigger budget: stop if more than 7 files outside declared scope, more than 2 subsystems, or any new boundary-crossing dependency

Числа здесь лучше оставить как local/project override, а не как shared default.

**Как это лучше встроить в репозиторий**

Я бы предложил такой shape изменений в `ai-standards`:

- Новый feature fragment: `fragments/process/autonomy-boundaries.md`
- Регистрация feature в [registry.toml](/home/shtirliz/workspace/myself/ai-standards/registry.toml)
- Usage guide:
  `docs/autonomy-boundaries-usage.md`
  `docs/autonomy-boundaries-usage.ru.md`
- В feature включить 6 коротких разделов:
  `Default Rule`, `Allowed Only When`, `Mandatory Stop Conditions`, `Sensitive Areas`, `Session Envelope`, `Review Output`
- В [fragments/process/design-first-collaboration.md](/home/shtirliz/workspace/myself/ai-standards/fragments/process/design-first-collaboration.md) добавить только короткий universal rule про обязательную остановку при design ambiguity и scope drift.
- В [fragments/process/structured-artifacts.md](/home/shtirliz/workspace/myself/ai-standards/fragments/process/structured-artifacts.md) добавить лёгкий артефакт уровня `SESSION_ENVELOPE.md` или просто описать required fields без навязывания файла.

**Итоговая оценка**

Как инженерный policy draft это уже хороший материал. По сути он правильно ставит акцент: автономия допустима не по признаку “модель сильная”, а по признаку “работа ограничена, проверяема, обратима и дёшева для review”. Это сильнее и практичнее, чем большинство разговоров про `agentic engineering`.

Если превращать это в `ai-standards`, я бы сделал две правки перед внедрением:

- убрать опору на шаговый порог как основное определение;
- добавить явное различение `direction verification` и `architecture delta verification`.

Если хочешь, следующим сообщением я могу уже предложить конкретный текст нового feature-фрагмента для `ai-standards` в стиле существующих `process/*` файлов, без лишней формальности и сразу в совместимом формате.

## Внести критерии останова в ai-standards на ветке 0tdo987 и подготовить commit

**Question**

(0tdoa6m) Внимательно изучил твои предложения.
Они соответствуют заявленным целям, поэтому думаю, тебе следует внести изменения в проект на ветке по задаче `0tdo987` с темой "Критерии останова агенты для верификации человеком".

(0tdoa9i) Пожалуйста, подготовь также commit на этой ветке.

**Answer**

Использую `commit-on-branch`, потому что ты просишь оформить изменения и commit по стандарту. Сначала проверю текущую ветку и рабочее дерево `ai-standards`, затем внесу сами правила остановки и подготовлю текст commit для твоего утверждения.

Сейчас `ai-standards` стоит на `main`, значит commit туда делать нельзя. Создам рабочую ветку под `0tdo987`, затем обновлю process-правила и связанную документацию в обеих языковых версиях, после чего покажу точный текст commit для утверждения.

Ветка создана. Сейчас добираю точные места интеграции: новый feature, его usage guide, упоминания в README, self-host manifest и тест рендера, чтобы правило было не только описано, но и действительно поддерживалось репозиторием.

Нашёл точки расширения. Буду делать это как отдельный opt-in feature `autonomy-boundaries`: короткий process-fragment, usage guides EN/RU, упоминания в README, self-host manifest, рендер тест и регенерацию `AGENTS.md`. Это лучше соответствует текущей архитектуре `ai-standards`, чем раздувать `core`.

Подготовил структуру изменений. Перед правками добавлю не только сам feature, но и decision record: здесь меняется состав shared process features, а это уже durable repository-facing choice, который потом придётся объяснять downstream-проектам.

Приступаю к правкам. Добавляю feature как opt-in process layer, а не в `core`: это оставляет правило переиспользуемым, но не навязывает тяжёлый governance всем проектам по умолчанию.

Основной patch готов. Теперь прогоняю рендер и проверки, чтобы убедиться, что feature действительно проходит через manifest -> renderer -> self-hosted `AGENTS.md`, а не остаётся только в документации.

Локально проверки упёрлись не в код, а в среду: `python3` не видит `typer`, а `pytest` вне проекта не установлен. Переключаюсь на проектный способ через `uv run`, это и соответствует правилам репозитория.

Рендер и `ai_sync check` прошли. Добиваю верификацию dev-зависимостями через `uv run --group dev`, потому что в обычной среде `pytest` не установлен.

Есть два сигнала от верификации: `mypy` зелёный, а общий `ruff` падает на уже существующей длинной строке в старом тесте вне моего diff. Для тестов запускаю точечно через `uv run --with pytest`, а линт ограничу изменёнными файлами, чтобы отделить мой patch от старого шума в дереве.

Рендер прошёл, но `uv run --with pytest pytest` в этой среде не находит бинарь `pytest`. Обойду это через `python -m pytest` и одновременно проверю статус дерева, чтобы не потерять новые файлы в commit.

Точечный `pytest` дал уже содержательный фидбек: упали не новые правила автономии, а старые ожидания в тестах, где зашит `CURRENT_AI_STANDARDS_VERSION = "1.1.0"`. Исправлю эту устаревшую константу и повторю прогон.

Исправил устаревшее ожидание версии и заодно убрал старый lint-шум в тесте. Повторно прогоняю `pytest`, `ruff` и `mypy` уже на актуальном дереве.

Изменения и проверки завершены. Сейчас соберу короткую сводку diff и предложу точный commit message по стандарту `0tdo987. (feat) ...`, после чего остановлюсь на твоё утверждение перед коммитом.

На ветке `feature/0tdo987-agent-stop-criteria` подготовлен patch под задачу `0tdo987`.

Сделано следующее: добавлен новый opt-in feature `autonomy-boundaries`, который вводит stop conditions для длинных автономных прогонов, различает `direction checkpoint` и `architecture-delta checkpoint`, описывает `session envelope`, чувствительные зоны и ожидаемый review output. Параллельно обновлены [README.md](/home/shtirliz/workspace/myself/ai-standards/README.md), [README.ru.md](/home/shtirliz/workspace/myself/ai-standards/README.ru.md), self-host manifest [ai.project.toml](/home/shtirliz/workspace/myself/ai-standards/ai.project.toml), шаблон [templates/project_manifest.toml](/home/shtirliz/workspace/myself/ai-standards/templates/project_manifest.toml), self-hosted [AGENTS.md](/home/shtirliz/workspace/myself/ai-standards/AGENTS.md), добавлены usage guides и bilingual decision record. В [tests/test_ai_sync.py](/home/shtirliz/workspace/myself/ai-standards/tests/test_ai_sync.py) добавлен рендер-тест для нового feature и поправлено устаревшее ожидание версии.

Проверки:
- `rtk uv run python scripts/ai_sync.py render --project-root /home/shtirliz/workspace/myself/ai-standards`
- `rtk uv run python scripts/ai_sync.py check --project-root /home/shtirliz/workspace/myself/ai-standards`
- `rtk uv run --with pytest python -m pytest -q /home/shtirliz/workspace/myself/ai-standards/tests/test_ai_sync.py`
- `rtk uv run --group dev ruff check /home/shtirliz/workspace/myself/ai-standards`
- `rtk uv run --group dev mypy /home/shtirliz/workspace/myself/ai-standards/scripts /home/shtirliz/workspace/myself/ai-standards/tests`

Предлагаемый commit message:
`0tdo987. (feat) add autonomy boundaries feature.`

Если утверждаешь этот текст, я сразу выполню commit.
