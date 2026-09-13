# External Work Orchestration

Этот документ описывает опциональный orchestration-слой поверх PCS для AI-first разработки, когда координация работы ведётся не только через GitHub Issues / Projects.

## Цель

PCS остаётся системой project truth, а внешние task-management инструменты используются как координационный слой.

Ключевой принцип:

> **Git / repository хранит истину. Jira и Trello координируют работу. ChatGPT оркестрирует изменения.**

Внешняя система задач не должна становиться вторым источником истины для архитектуры, состояния продукта, решений или доказательств готовности.

## Bakunity Development System v1

Рекомендуемая схема:

```text
User
  -> ChatGPT
      -> Trello      portfolio / personal Kanban
      -> Jira        engineering work management
      -> GitHub      code / PR / review / CI / releases
          -> PCS     authoritative project context
          -> Actions automated quality gates
```

Confluence не является обязательной частью модели. Документация проекта по умолчанию хранится в repository вместе с PCS. Confluence может использоваться только как дополнительная human-facing wiki, если это действительно нужно команде.

## Ответственность систем

### ChatGPT

Orchestration layer.

ChatGPT может:

- переводить пользовательскую цель в конкретную работу;
- создавать и обновлять Jira work items;
- создавать и обновлять Trello cards;
- работать с GitHub branches, PR, Issues, Actions и repository files;
- поддерживать PCS context при semantic state transitions;
- сверять фактическое состояние между системами;
- не считать изменение статуса в Jira/Trello доказательством готовности продукта.

### Trello

Portfolio / personal Kanban layer.

Назначение:

- быстрый intake идей;
- верхнеуровневые project/milestone cards;
- личные приоритеты;
- визуальный поток работы;
- межпроектный обзор.

Стандартные колонки:

```text
Backlog
-> To Do
-> In Progress
-> Review / QA
-> Done

Blocked используется как отдельное состояние исключения.
```

Trello не должен содержать полный технический decomposition, если он уже хранится в Jira.

### Jira

Engineering work-management layer.

Назначение:

- Epic / Story / Task / Bug / Sub-task;
- приоритеты;
- зависимости;
- ownership;
- workflow status;
- releases и engineering planning;
- детальный backlog.

Jira не является authoritative source для архитектуры, product state, ADR или evidence.

### GitHub

Engineering execution layer.

Назначение:

- repository;
- branches;
- commits;
- pull requests;
- code review;
- releases;
- CI/CD;
- automated tests;
- deployment workflows;
- evidence links.

### PCS

Authoritative project context.

PCS хранит:

- текущее подтверждённое состояние проекта;
- active work context;
- architecture;
- roadmap;
- ADR;
- incidents;
- evidence;
- agent instructions.

Если Jira/Trello конфликтуют с repository truth, repository truth имеет приоритет.

## Source-of-truth rules

| Информация | Authoritative source |
| --- | --- |
| Код | GitHub repository |
| Архитектура | PCS / `docs/ARCHITECTURE.md` |
| Текущее состояние проекта | PCS / `docs/PROJECT_STATE.md` |
| Текущая работа в контексте проекта | PCS / `docs/ACTIVE_WORK.md` |
| Решения | PCS / `docs/ADR/` |
| Evidence / verification | PCS / `docs/EVIDENCE.md` + CI |
| Engineering task state | Jira |
| Portfolio / personal priority | Trello |
| CI/CD state | GitHub Actions |
| История реализации | Git |

## Work-item hierarchy

Рекомендуемая модель:

```text
Trello card
  -> project milestone / initiative

Jira Epic
  -> крупная capability / stage

Jira Story / Task / Bug
  -> единица engineering work

GitHub branch / PR
  -> конкретная реализация

PCS update
  -> только если изменился project truth
```

Не каждая Jira task требует отдельной Trello card.
Не каждый commit требует PCS update.
PCS обновляется при semantic state transition, а не на каждый технический шаг.

## Standard flow

```text
1. User формулирует цель обычным языком.
2. ChatGPT читает PCS и проверяет фактическое состояние repository.
3. ChatGPT определяет, нужна ли новая Trello card, Jira Epic/Task или обе сущности.
4. Engineering work переводится в In Progress.
5. Реализация идёт через branch -> code -> tests -> PR.
6. GitHub Actions выполняет quality gates.
7. После merge выполняется deploy, если он входит в scope.
8. При наличии runtime/deployment выполняются post-deploy smoke/E2E checks.
9. PCS обновляется, если изменился подтверждённый state/architecture/roadmap/evidence.
10. Jira work item переводится в Done только после выполнения Definition of Done.
11. Верхнеуровневая Trello card закрывается, когда завершён соответствующий milestone/initiative.
```

## Definition of Ready

Engineering work можно начинать, когда:

- понятна цель;
- определён scope;
- известны acceptance criteria или ожидаемый результат;
- определён relevant project context;
- отсутствует критическая неизвестность, которая делает реализацию преждевременной.

Для маленьких задач formal DoR не должен создавать лишнюю бюрократию.

## Definition of Done

`Done` означает не «код написан», а подтверждённый результат.

Минимально:

- implementation завершена;
- relevant tests проходят;
- CI green;
- review/QA выполнены, если применимо;
- deployment выполнен, если он входил в scope;
- smoke/E2E verification выполнены, если требуются;
- PCS актуализирован при semantic state transition;
- evidence сохранён или доступен через CI/PR/runtime verification.

## CI/CD ownership

Автоматические проверки принадлежат GitHub Actions, а не Jira, Trello или Confluence.

Рекомендуемый pipeline:

```text
PR
-> lint
-> type/static checks
-> unit tests
-> integration tests
-> build
-> security checks where applicable
-> PCS validation
-> merge
-> deploy
-> post-deploy smoke/E2E
```

Jira/Trello могут отражать результат pipeline, но не заменяют его.

## Synchronization contract

### Trello -> Jira

Trello содержит верхнеуровневое намерение.
Если карточка превращается в реальную engineering initiative, ChatGPT создаёт или связывает соответствующий Jira Epic.

### Jira -> GitHub

Jira task должна быть связана с реализацией там, где это полезно:

- branch;
- PR;
- commit;
- release.

### GitHub -> PCS

Merge сам по себе не требует переписывать весь PCS.
PCS обновляется, если merge изменил project truth.

### CI -> Jira/Trello

Failed verification может вернуть работу в Review / QA или Blocked.
Successful verification позволяет завершить engineering item, если выполнены остальные DoD conditions.

## AI operating rules

AI/ChatGPT должен:

1. сначала читать repository truth;
2. не создавать дублирующие task entities без необходимости;
3. не копировать полную документацию между Jira, Trello и PCS;
4. использовать Jira description как task brief, а не как второй ARCHITECTURE.md;
5. использовать Trello description как executive summary, а не engineering spec;
6. обновлять PCS только при semantic state transition;
7. проверять CI/evidence перед объявлением работы Done;
8. явно отмечать divergence между Jira/Trello и repository truth;
9. предпочитать ссылки между системами вместо копирования больших блоков текста;
10. не использовать Confluence по умолчанию, если документация уже canonical в repository.

## Для одного разработчика

При solo-разработке модель должна оставаться лёгкой:

- Trello: межпроектный обзор и личный Kanban;
- Jira: только реальная engineering decomposition;
- GitHub + PCS: вся разработка и truth;
- минимум ceremony;
- без обязательных Scrum-ритуалов;
- Kanban как default workflow.

Если Jira начинает создавать больше административной работы, чем пользы, допускается временно вести отдельный маленький проект через Trello + GitHub/PCS без Jira.

## Рост команды

При росте команды модель расширяется без смены source of truth:

- Jira становится основной engineering board;
- ownership и dependencies становятся обязательнее;
- Trello может остаться portfolio/executive layer;
- PCS продолжает быть repository truth;
- GitHub Actions остаётся quality gate;
- Confluence добавляется только для human-facing knowledge base, onboarding или non-technical documentation.

## Антипаттерны

Не делать:

- одинаковую архитектурную документацию одновременно в PCS и Confluence;
- одинаковый детальный backlog одновременно в Trello и Jira;
- считать `Done` в Jira доказательством работающего production;
- хранить единственную копию важного решения только в комментарии Jira;
- использовать Trello как замену Git history;
- переносить CI/test execution в Confluence;
- обновлять PCS на каждый commit без semantic state change.

## Default policy

Для Bakunity default stack:

```text
ChatGPT + Trello + Jira + GitHub + PCS + GitHub Actions
```

Confluence: optional / disabled by default.

Methodology: Kanban.

Repository truth всегда имеет приоритет над chat/task-manager state.
