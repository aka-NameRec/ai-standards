(0tkgv3m) Контекст

[28.07.2026 08:25] Дмитрий Скоробогатов: Коротко: сам факт, что Basic Memory MCP настроен, ещё не гарантирует, что я всегда буду его трогать. Но если в проектных правилах закрепить, что Basic Memory является входным индексом/памятью по docs/architecture, тогда да: я буду использовать его по умолчанию в начале задачи и перед правками.
Сейчас в этой сессии я проверил discovery: отдельные Basic Memory tools мне не exposed. Доступен ConPort, и его я уже обязан использовать по правилам проекта.
Как я бы правильно встроил Basic Memory:
docs/architecture/** остаётся каноническим источником истины.
Basic Memory используется как быстрый индекс: какие contracts есть, к каким модулям/классам они относятся, какие недавно менялись.
В начале задачи: поискать в Basic Memory записи по проекту broadleaf, docs/architecture, module contract, текущему task id и затрагиваемым модулям.
Перед правкой файла: искать в Basic Memory по имени класса/пакета/модуля, а найденный contract всё равно читать из repo, если он существует.
В процессе сессии: live-изменения лучше ловить через git status, git diff, rg --files docs/architecture, потому что MCP-память может отставать от файловой системы, если её не обновили.
То есть Basic Memory я бы считал не заменой чтению docs/architecture, а входным навигатором: “куда смотреть, что важно, что изменилось”. Чтобы это стало стабильным поведением в новых сессиях, лучше добавить в AGENTS.md явное правило вроде: “At task start, if Basic Memory MCP is available, query it for Broadleaf architecture/module-contract context before code discovery.”
[28.07.2026 08:30] Сергей Штуркин: <Попробуйте такой prompt:>
<начало цитаты>
> Коротко: сам факт, что Basic Memory MCP настроен, ещё не гарантирует, что я всегда буду его трогать. Но если в проектных правилах закрепить, что Basic Memory является входным индексом/памятью по docs/architecture, тогда да: я буду использовать его по умолчанию в начале задачи и перед правками.

Смотри: проект растёт, и я не могу себе позволить "косячить" с такими вещами, как реиндекс, который запросто упадёт в production только из-за того, что мы упустили module contract, который был по факту, но не не был использован при внесении изменений.
Предложи пожалуйста правила (я включу его в ai-standards), чтобы module contracts гарантированно учитывались при внесении изменений в код, и использовался Basic Memory для оптимизации, если он установлен.
И ещё: если индекса по module contracts нет, то чтобы ты сообщал мне, что тебе приходится лопатить каталог и жечь мои токены: я тогда испугаюсь, и настрою Basic Memory MCP.
Так мы решим проблему?
<конец цитаты>
[28.07.2026 08:36] Дмитрий Скоробогатов: [ module-contract-discovery-gate.md ]

Да, так проблему можно сильно снизить. “Гарантия” здесь должна быть не через надежду на мою память, а через обязательный contract discovery gate перед правками кода.
Ниже текст правила, который можно вставить в ai-standards.

Я бы ещё добавил это как короткое “жёсткое” правило рядом с существующим Module Contracts:
Do not edit production code until module-contract discovery for the touched files has completed. Basic Memory may satisfy discovery only as an index; relevant canonical contracts must still be read from the repository before editing.
Это не сделает меня пассивным watcher’ом файлов, но создаст обязательный шлюз: перед правками я должен либо найти и прочитать контракт, либо явно сказать, что индекса нет и приходится сканировать репозиторий напрямую. Это как раз закрывает риск “контракт был, но агент его не учёл”.

(0tkgv30) Правила

# Module Contract Discovery Gate

Before changing production code, the agent must complete module-contract discovery for the affected code area.

## Canonical Source

- Git-tracked module contracts are canonical project knowledge.
- Canonical module contracts include:
  - `MODULE_CONTRACT.md`
  - `docs/architecture/**/*contract*.md`
  - file-local `START_MODULE_CONTRACT` / `END_MODULE_CONTRACT` blocks
  - other project-declared module contract artifacts
- Memory systems such as Basic Memory are indexes and navigation aids only. They do not replace reading the canonical contract from the repository when a relevant contract is found.

## Task Start

At the start of every coding task, the agent must:

1. Load project rules and active operational context.
2. Discover whether a module-contract index is available through Basic Memory or another configured MCP memory.
3. If Basic Memory is available, query it for:
   - the project name/repository
   - `module contract`
   - `docs/architecture`
   - the task id or branch id when available
   - names of modules/classes/packages likely to be touched
4. If no module-contract index is available, stale, inaccessible, or insufficient, the agent must say so before broad discovery, for example:
   `Module-contract index is unavailable or incomplete; I need to scan docs/architecture and contract markers directly, which may use extra context/tokens.`
5. Then perform repository discovery with targeted commands such as:
   - `rg --files docs/architecture`
   - `rg --files -g MODULE_CONTRACT.md`
   - `rg -n "START_MODULE_CONTRACT|module contract|контракт модуля"`

## Before Editing A File

Before editing any code file, the agent must decide whether the file is covered by a module contract.

A file is covered when any of these are true:

- the contract explicitly names the class, function, package, module, endpoint, job, table, event, or adapter;
- the file is inside a directory/module declared by the contract;
- the file produces, consumes, validates, caches, persists, transforms, or transports data described by the contract;
- the change may affect contract responsibilities, inputs, outputs, invariants, side effects, error boundaries, recovery behavior, observability, or verification requirements;
- tests for the file are named in or directly exercise behavior named in the contract.

If coverage is unclear, the agent must treat the contract as potentially relevant, read it, and state the uncertainty.

## Use During Reasoning

For every relevant contract, the agent must use it to constrain:

- change scope and non-goals;
- allowed behavior changes;
- error handling and recovery rules;
- backward compatibility expectations;
- required tests or smoke checks;
- whether a proposed change is ordinary implementation work or a contract change.

If the intended code change contradicts a contract, the agent must stop and report that the task requires a module-contract change. It must not silently implement behavior that violates the existing contract.

## During The Session

The agent must re-run contract discovery when:

- the task moves into a new module or layer;
- `git status` or `git diff` shows changes under `docs/architecture/**` or `MODULE_CONTRACT.md`;
- a new class/package/module becomes part of the edit set;
- verification failures suggest a misunderstood boundary or invariant.

## Basic Memory Index Requirements

When Basic Memory is available, module-contract notes should include:

- repository/project name;
- source contract path;
- last observed commit hash or file hash when available;
- covered modules, packages, classes, jobs, endpoints, or data flows;
- responsibilities and explicit non-goals;
- invariants and error boundaries;
- verification requirements;
- links to related decisions or module contracts.

If the Basic Memory entry has no source path or freshness marker, the agent must treat it as a hint and read the repository file before relying on it.

## Reporting

In implementation summaries, the agent must include a short contract note when contracts were relevant:

- which contracts were read;
- which files were considered covered;
- whether the change preserves or changes the contract;
- which verification was run against contract requirements.

If no relevant contract was found, the agent must state that discovery was performed and name the remaining risk.

## Strict Rule

Do not edit production code until module-contract discovery for the touched files has completed. Basic Memory may satisfy discovery only as an index; relevant canonical contracts must still be read from the repository before editing.
