# Project Context System (PCS)

**Project Context System** — переносимая система постоянного контекста для AI-first разработки.

PCS решает простую проблему: рабочее состояние проекта не должно зависеть от памяти конкретного чата, ChatGPT/Codex-сессии или отдельного разработчика.

> **CHAT IS WORKSPACE. GIT IS MEMORY. DOCS ARE CURRENT KNOWLEDGE.**

PCS является **Git-native + GitHub-first** системой: ядро контекста хранится прямо в репозитории и работает без GitHub UI, а GitHub используется как удобный operational layer для Issues, Projects, PR, Actions и governance.

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

## Как встроить PCS в новый проект

Создай обычный GitHub-репозиторий для продукта и клонируй PCS рядом. Затем:

```bash
python scripts/install_pcs.py /path/to/your-product --profile standard
```

После установки в **самом репозитории продукта** появятся PCS-файлы, Issue Forms, PR/CI настройки и GitHub manifests. Никакой отдельный runtime-сервис PCS для этого не нужен.

Дальше:

```text
1. Заполнить PROJECT_STATE / ARCHITECTURE / ROADMAP реальными данными.
2. Проверить AGENTS.md и CODEOWNERS.
3. Выполнить validate_context.py.
4. Commit initial PCS context baseline.
5. Push продукта в GitHub.
6. При желании применить labels через setup_github.py.
7. Создавать разработку через Issues -> branch/task -> PR -> CI.
8. Не подключать сервер, пока продукт не дошёл до отдельного Live gate.
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

```bash
python scripts/validate_context.py /path/to/project
```

Для безопасных GitHub-настроек после проверки:

```bash
python scripts/setup_github.py /path/to/project --apply-labels
```

Rulesets/Project governance в V1 представлены декларативными manifest-файлами и не применяются автоматически, потому что они меняют правила merge и должны быть явно просмотрены.

## Документация GitHub integration

См. `docs/GITHUB_INTEGRATION.md`.
