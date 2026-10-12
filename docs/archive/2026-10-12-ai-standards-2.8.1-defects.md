---
title: 'ai-standards 2.8.1: дефекты и противоречия'
permalink: devcats/ai/2026-10-12-ai-standards-2.8.1-defects
---

# ai-standards 2.8.1: дефекты и противоречия

Версия 2.8.1, метка `2.8.1-2026-10-11`. Правила сверены и с `main` на коммите `50ab280`: после метки там менялись только документы и журнал изменений. Всё нашлось при обновлении проекта с 2.5.0 на 2.8.1. В проекте работают агенты Claude и Cursor, включены фичи `code-review`, `autonomy-boundaries`, `knowledge-capture` и `basic-memory`, а `project-memory` выключена.

Самое срочное - первый пункт: с 2.6.0 Claude, Cursor и Codex проводят код-ревью без части правил.

## 1. Процедуру код-ревью получает только kilo

В 2.6.0 (коммит `34baa19`, этап M1) подробная процедура код-ревью и правила правок во время ревью переехали из `fragments/process/code-review.md` в шаблон `templates/code-review/standard-code-review.procedure.md`. По таблице шаблонов в `scripts/ai_sync.py` этот файл разворачивается только для `kilo`: в `.agents/skills/code-review/standard-code-review/references/procedure.md`.

| Агент | Что разворачивается | Куда отсылает текст навыка |
|---|---|---|
| `codex` | `.codex/skills/code-review/standard-code-review/SKILL.md` | в `references/procedure.md`, которого рядом нет |
| `claude` | `.claude/commands/standard-code-review.md` | в «the rendered rules in `AGENTS.md`», где подробностей уже нет |
| `cursor` | `.cursor/rules/standard-code-review.mdc` | туда же, куда `claude` |

Шаблоны для Claude и Cursor с 2.5.0 не менялись. При этом фрагмент `code-review` теперь сам отсылает к файлу, которого у них нет: «When the `standard-code-review` skill is deployed, its `references/procedure.md` holds the full pass-by-pass procedure».

В результате Claude, Cursor и Codex не видят трёх правил, которые раньше стояли в `AGENTS.md`, а теперь есть только в процедуре:

- какие правки проверяющий вносит сам, без спроса: переводы, опечатки в строках для пользователя и в комментариях, защитное ужесточение, которое не меняет поведение на текущих данных, недостающая строка в `.gitignore`, явное расхождение с соседним кодом вроде не того импорта или не той константы;
- порядок «сначала ревью, потом правки, потом отчёт» и отдельный перечень сделанных правок в чате;
- требование оценивать затраты на реальных объёмах данных и прямо говорить, если сейчас они бесплатны.

До них не доходит и правило, которое 2.6.0 добавила прямо в процедуру, в проход Correctness: «Read the changed conditions and their boundaries against the behavior the surrounding code and tests imply».

Как должно быть: там, где развёрнут `standard-code-review`, агент получает и процедуру, а каждая ссылка в тексте навыка ведёт на существующий файл. Как это сделать, решать вам. Например, процедуру можно разворачивать общим справочником в `.ai-standards/references/`, как уже сделано с `code-review-reporting.md`, и ссылаться на него из всех четырёх вариантов навыка.

Проверка: в проекте с `tooling.agents = ["codex", "claude", "cursor", "kilo"]` и включённой `code-review` выполнить `ai-sync sync-templates`. После этого каждая развёрнутая копия `standard-code-review` ссылается на существующий файл, а строка «Safe to fix without asking» находится в файле, до которого доходит каждый агент.

## 2. Автономный запуск коммитит без согласования, а `capture-knowledge` это запрещает

Шаг 6 навыка `autonomous-task-run`: «Commit without pausing for per-commit message approval: the instruction to run autonomously is the standing approval of the commit flow». По решению `docs/decisions/2026-10-11-adopt-autonomous-task-run-skill.md` вторая половина этой фразы и есть правило старшинства, которое делает навык совместимым с `core/git-workflow` («Always ask the user to approve the commit message text before committing»).

Навык `capture-knowledge` этим решением не охвачен. В его разделе «Never» сказано: «Never push or commit without explicit user approval of the message». Шаг 7 того же запуска требует зафиксировать знания «the standard way», а по фрагменту `knowledge-capture` это и есть `capture-knowledge` («capture session knowledge the standard way ... follow the feature-gated `capture-knowledge` skill»). Общее согласие на поток коммитов не равно явному согласию на текст сообщения, так что на шаге 7 агент получает запрет, который противоречит разрешению шага 6.

Тот же довод относится и к `core/git-workflow`: там требуется согласовать текст сообщения, а оговорка навыка говорит о потоке коммитов. Исключение видно только из текста навыка, в самом `core/git-workflow` его нет.

Как должно быть: в `capture-knowledge` и рядом с правилом в `core/git-workflow` прямо сказано, что во время автономного запуска действует согласие, данное при его запуске.

## 3. Шаг фиксации знаний в автономном запуске не учитывает настройки проекта

`autonomous-task-run` привязан только к фиче `autonomy-boundaries`. Его шаг 7 требует «decision records, a task record, a local working-memory update», а условие завершения включает «knowledge is captured».

- Навык `capture-knowledge` разворачивается только при включённой `knowledge-capture`. Без неё шагу 7 нечем выполнять «the standard way».
- Папка для локальной памяти (`docs/local/**`) есть только при `project-memory`. В разделе `Route By Content` навыка `capture-knowledge` это обновление помечено «when the project enables it», а шаг 7 требует его без оговорки.
- Запись задачи `capture-knowledge` кладёт в `docs/tasks/`. Это место задано текстом навыка и фрагмента `knowledge-capture`, ключа в манифесте для него нет. Проект, где записи задач лежат в папках по ключу задачи из трекера, получает две папки для записей о задачах: свою и `docs/tasks/`.

Как должно быть: шаг 7 выполняет только те части, для которых в проекте включены фичи, а для выключенных говорит, что делать. Например, пропустить и отметить в отчёте или не начинать запуск. Место записей задач проект задаёт сам, как уже задаёт место локальной памяти ключом `project_memory.local_tree`.

## 4. Имя ветки в автономном запуске не берётся из правил проекта

Шаг 1: «Create a branch `<purpose>/<task_id>-<slug>` from the merge-target branch». Форма совпадает с той, из которой `core/git-workflow` извлекает номер задачи. Но для коммитов навык отсылает к правилам проекта («the project's standard form»), для слияния тоже («by the project standard»), а форму ветки задаёт сам. Проект, который переопределил её у себя, например называет ветки `fix/<KEY>` без описания, получит ветку не по своим правилам.

Как должно быть: имя ветки берётся из правил проекта, как формат коммитов и порядок слияния.

## 5. Локальные заметки: исключение шире, чем сказано в журнале изменений

В разделе `Basic Memory Usage` файла `fragments/tools/basic-memory.md`:

- второй пункт: «Treat `docs/local/**` as agent-managed working memory rather than canonical truth; canonical-note rules do not apply there, and notes without canonical shape are expected, not defects»;
- раздел Note Shape: «local working-memory notes carry the same date prefix (`YYYY-MM-DD-<topic>.md`, see Project Memory)».

По журналу изменений на `main` (раздел 2.8.0) исключение для `docs/local/**` сузили до требований к телу заметки, а имя с датой стало обязательным. Второй пункт этого не отражает и по-прежнему снимает с `docs/local/**` все правила канонических заметок, в том числе правило имени. Кроме того, «see Project Memory» ведёт в раздел, которого нет в `AGENTS.md` проекта с выключенной `project-memory`.

Как должно быть: второй пункт снимает только требования к телу заметки, разделы `## Observations` и `## Relations`, как в `fragments/tools/project-memory.md`, а ссылка не ведёт в отсутствующий раздел.

## 6. Новый навык приходит при обновлении без вопроса

Навык `update-ai-standards` запрещает включать фичу без согласия («Never enable a feature without the user's explicit confirmation in this run»), а уже включённые обновляет молча: «Refresh enabled features silently», без подтверждения проходят «Text updates to already-enabled features». О новых навыках он велит рассказать на шаге 6 («Cover notable skill and workflow additions»), но к этому моменту шаг 5 уже развернул их через `sync-templates`, и согласия никто не спрашивает.

Так в 2.8.0 пришёл `autonomous-task-run`, который ослабляет уже действующее правило о согласовании коммитов. Он развернулся вместе с включённой `autonomy-boundaries`. Отказаться от него можно только вместе со всей фичей: в манифесте нет ключа, которым отключается отдельный шаблон.

Как должно быть: навык, который отменяет или ослабляет действующее правило, при обновлении объявляется и подтверждается до развёртывания, как новая фича, или манифест позволяет от него отказаться.
