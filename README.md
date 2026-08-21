# Project Context System (PCS)

**Project Context System** — переносимая система постоянного контекста для AI-first разработки.

PCS решает простую проблему: рабочее состояние проекта не должно зависеть от памяти конкретного чата, ChatGPT/Codex-сессии или отдельного разработчика.

> **CHAT IS WORKSPACE. GIT IS MEMORY. DOCS ARE CURRENT KNOWLEDGE.**

PCS является **Git-native + GitHub-first** системой: ядро контекста хранится прямо в репозитории и работает без GitHub UI, а GitHub используется как удобный operational layer для Issues, Projects, PR, Actions и governance.

## Установка одной фразой через AI

Это целевой UX PCS.

Если AI/coding agent имеет доступ к текущему проекту и GitHub/Git, пользователю достаточно сказать:

> **Бро, добавь в проект систему контекста https://github.com/bakunity/Project-Context-System**

После этого агент должен сам:

1. открыть PCS и прочитать `AGENT_INSTALL.md` / `pcs-manifest.json`;
2. определить текущий project repository;
3. установить профиль `standard`;
4. изучить реальный код, docs, tests и Git state проекта;
5. заполнить `PROJECT_STATE`, `ARCHITECTURE`, `ROADMAP`, `ACTIVE_WORK` реальными подтверждёнными данными;
6. не додумывать отсутствующие факты и не ходить на сервер;
7. выполнить structural validation;
8. выполнить `validate_context.py --ready`;
9. проверить diff и сохранить baseline согласно Git workflow проекта;
10. написать `PCS READY` только если readiness validation действительно прошёл.

Канонический протокол для агента: [`AGENT_INSTALL.md`](AGENT_INSTALL.md).
Машиночитаемый entrypoint: [`pcs-manifest.json`](pcs-manifest.json).

После этого новый AI-чат должен иметь возможность восстановить проект из самого repository и продолжить разработку без обязательного доступа к прошлому диалогу.

## Что хранит PCS

| Тип знания | Источник |
| --- | --- |
| Правила работы AI | `AGENTS.md` |
| Что истинно о проекте сейчас | `docs/PROJECT_STATE.md` |
| Что делается прямо сейчас | `docs/ACTIVE_WORK.md` |
| Архитектура | `docs/ARCHITECTURE.md` |
| Будущее направление | `docs/ROADMAP.md` |
| Почему принято решение | `docs/ADR/` |
| Ошибки и root cause | `docs/INCIDENTS/` |
| Что реально проверено | `docs/EVIDENCE.md` |
| Машинный bootstrap/freshness | `.project/state.json` |
| История изменений | Git |
| Единица работы | GitHub Issue |
| Оперативная доска | GitHub Project |
| Временные мысли | chat/session |

## Основные принципы

1. Repository state beats chat memory.
2. Один тип truth хранится в одном authoritative месте.
3. Контекст обновляется вместе с кодом при semantic state transition.
4. `Done` без tests/smoke/evidence не считается доказательством.
5. AI работает относительно явного base commit.
6. Missing project truth не додумывается.
7. Handoff — derived artifact, не второй source of truth.
8. Project-specific `memories/` не используется.
9. Issues/Projects координируют работу, но не заменяют repository truth.
10. Server/runtime access никогда не подразумевается автоматически.

## Bootstrap новой AI-сессии

```text
1. Read AGENTS.md
2. Read .project/state.json
3. Read docs/PROJECT_STATE.md
4. Read docs/ARCHITECTURE.md
5. Read docs/ACTIVE_WORK.md
6. Read relevant ADR / CONTEXT only
7. Inspect git status and recent commits
8. Compare HEAD with state_based_on_commit
9. Inspect drift if needed
10. Read linked Issue/task brief
11. Summarize understanding
12. Only then plan work
```

## Как встроить PCS вручную/скриптом

Создай обычный GitHub-репозиторий для продукта и клонируй PCS рядом. Затем:

```bash
python scripts/install_pcs.py /path/to/your-product --profile standard
```

После установки в **самом репозитории продукта** появятся PCS-файлы, Issue Forms, PR/CI настройки и GitHub manifests. Никакой отдельный runtime-сервис PCS для этого не нужен.

Дальше:

```text
1. Заполнить PROJECT_STATE / ARCHITECTURE / ROADMAP реальными данными.
2. Проверить AGENTS.md и CODEOWNERS.
3. Выполнить structural validation.
4. Выполнить readiness validation (--ready).
5. Commit initial PCS context baseline.
6. Push продукта в GitHub.
7. При желании применить labels через setup_github.py.
8. Создавать разработку через Issues -> branch/task -> PR -> CI.
9. Не подключать сервер, пока продукт не дошёл до отдельного Live gate.
```

## Development first, server later

Рекомендуемый процесс для нового продукта:

```text
GitHub repository
  -> PCS baseline
  -> Issues / agent tasks
  -> implementation
  -> tests + CI
  -> PR / review
  -> product milestone
  -> explicit staging/server task
  -> live verification
```

Это позволяет агенту спокойно разрабатывать продукт и не путать repository acceptance с live deployment.

## Профили

### minimal

- `AGENTS.md`
- `.project/state.json`
- `PROJECT_STATE.md`
- `ARCHITECTURE.md`
- `ROADMAP.md`
- `ADR/`

### standard

Дополнительно:

- `ACTIVE_WORK.md`
- `INCIDENTS/`
- `EVIDENCE.md`
- GitHub Issue Forms
- PR template
- CODEOWNERS
- GitHub Actions context check
- labels / Project / ruleset manifests
- `setup_github.py`

### large

Дополнительно:

- `CONTEXT/PRODUCT.md`
- `CONTEXT/BACKEND.md`
- `CONTEXT/FRONTEND.md`
- `CONTEXT/INFRASTRUCTURE.md`
- `research/`

## Проверка

Структурная проверка:

```bash
python scripts/validate_context.py /path/to/project
```

Проверка готовности после заполнения реального контекста:

```bash
python scripts/validate_context.py /path/to/project --ready
```

`--ready` специально падает, если шаблонные bootstrap-подсказки ещё не заменены или state всё ещё имеет bootstrap-статус.

Для безопасных GitHub-настроек после проверки:

```bash
python scripts/setup_github.py /path/to/project --apply-labels
```

Rulesets/Project governance в V1 представлены декларативными manifest-файлами и не применяются автоматически, потому что они меняют правила merge и должны быть явно просмотрены.

## Документация GitHub integration

См. `docs/GITHUB_INTEGRATION.md`.
