# Project Context System (PCS)

**Project Context System** — переносимая система постоянного контекста для AI-first разработки.

PCS решает простую проблему: рабочее состояние проекта не должно зависеть от памяти конкретного чата, окна ChatGPT, Codex-сессии или отдельного разработчика.

> **CHAT IS WORKSPACE. GIT IS MEMORY. DOCS ARE CURRENT KNOWLEDGE.**

## Зачем это нужно

В большом проекте AI легко теряет:

- что уже реализовано и принято;
- какой commit действительно проверен;
- что делается прямо сейчас;
- почему было принято архитектурное решение;
- какие гипотезы уже исключены;
- какие live-проверки уже были выполнены;
- что нельзя менять без отдельного approval.

PCS переносит эти знания в Git и делает их частью инженерного процесса.

## Модель PCS

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
| Временные мысли | chat/session |

## Ключевые принципы

1. **Repository state beats chat memory.**
2. Один тип truth хранится только в одном authoritative месте.
3. Контекст обновляется вместе с кодом при semantic state transition.
4. `Done` без tests/smoke/evidence не считается доказательством.
5. AI работает относительно явного base commit.
6. Если repository evidence отсутствует — project-specific truth нельзя додумывать.
7. Handoff — производный артефакт, а не второй source of truth.
8. `memories/` не используется как repository-specific truth.

## Bootstrap новой AI-сессии

```text
1. Read AGENTS.md
2. Read .project/state.json
3. Read docs/PROJECT_STATE.md
4. Read docs/ARCHITECTURE.md
5. Read docs/ACTIVE_WORK.md
6. Read only relevant ADR / CONTEXT docs
7. Inspect git status
8. Inspect recent commits
9. Compare HEAD with state_based_on_commit
10. If drift exists -> inspect diff and reconcile
11. Summarize understanding
12. Only then plan work
```

## Быстрое внедрение

После клонирования этого репозитория:

```bash
python scripts/install_pcs.py /path/to/your/project
```

По умолчанию устанавливается стандартный профиль. Доступны:

```bash
python scripts/install_pcs.py /path/to/project --profile minimal
python scripts/install_pcs.py /path/to/project --profile standard
python scripts/install_pcs.py /path/to/project --profile large
```

Установщик не перезаписывает существующие файлы без `--force`.

После установки:

```bash
python scripts/validate_context.py /path/to/project
```

## Профили

### minimal

Для небольшого приложения:

- `AGENTS.md`
- `.project/state.json`
- `PROJECT_STATE.md`
- `ARCHITECTURE.md`
- `ROADMAP.md`
- `ADR/`

### standard

Для обычного production-проекта дополнительно:

- `ACTIVE_WORK.md`
- `INCIDENTS/`
- `EVIDENCE.md`
- PR template
- context validation

### large

Для сложных систем дополнительно:

- `CONTEXT/PRODUCT.md`
- `CONTEXT/BACKEND.md`
- `CONTEXT/FRONTEND.md`
- `CONTEXT/INFRASTRUCTURE.md`
- `research/`

## Статусы знания

При восстановлении контекста AI должен различать:

- **CONFIRMED** — подтверждено repository/runtime evidence;
- **INFERRED** — следует из кода, но не зафиксировано как truth;
- **UNKNOWN** — информации нет;
- **STALE** — документ старее релевантного кода;
- **CONFLICT** — authoritative источники расходятся.

## Статус проекта

PCS находится в ранней стадии разработки. Цель V1 — сделать систему, которую можно добавить в новый репозиторий одной командой и использовать с ChatGPT, Codex и другими coding agents без привязки к конкретной AI-сессии.
