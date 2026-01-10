---
description: "Task list for Phase I Console Todo Application implementation"
---

# Tasks: Console Todo Application

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: TDD approach requested - tests will be included and written before implementation

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths based on plan.md structure: `src/todo/` for application code, `tests/` for tests

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan in src/todo/
- [ ] T002 Initialize Python 3.13+ project with UV dependencies in pyproject.toml
- [ ] T003 [P] Configure linting and formatting tools (black, flake8, mypy)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 [P] Create base project structure: src/todo/__init__.py
- [ ] T005 [P] Create models module in src/todo/models.py
- [ ] T006 [P] Create storage module in src/todo/storage.py
- [ ] T007 [P] Create operations module in src/todo/operations.py
- [ ] T008 [P] Create validators module in src/todo/validators.py
- [ ] T009 [P] Create formatters module in src/todo/formatters.py
- [ ] T010 [P] Create CLI module in src/todo/cli.py
- [ ] T011 Create main entry point in src/main.py
- [ ] T012 Create pyproject.toml with project metadata and dependencies
- [ ] T013 Create basic README.md with setup instructions

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View All Todos (Priority: P1) 🎯 MVP

**Goal**: Enable users to see all their tasks in a clear, organized list to understand what needs to be done and track progress

**Independent Test**: Launch the application and view an empty or pre-populated list. Should show task overview with status indicators.

### Tests for User Story 1 (TDD approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T014 [P] [US1] Unit test for empty todo list display in tests/unit/test_formatters.py
- [ ] T015 [P] [US1] Unit test for single todo display in tests/unit/test_formatters.py
- [ ] T016 [P] [US1] Unit test for multiple todo display in tests/unit/test_formatters.py
- [ ] T017 [P] [US1] Unit test for status indicators (pending/completed) in tests/unit/test_formatters.py
- [ ] T018 [P] [US1] Integration test for list command in tests/integration/test_cli_integration.py

### Implementation for User Story 1

- [ ] T019 [P] [US1] Create Todo dataclass in src/todo/models.py with id, title, description, status, timestamps
- [ ] T020 [P] [US1] Create TodoStorage class in src/todo/storage.py with get_all() method
- [ ] T021 [US1] Implement list operation in src/todo/operations.py
- [ ] T022 [US1] Create formatter functions in src/todo/formatters.py for displaying todo lists
- [ ] T023 [US1] Add list command to CLI in src/todo/cli.py
- [ ] T024 [US1] Update main.py to handle list command
- [ ] T025 [US1] Add validation for list command parameters in src/todo/validators.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Add New Todo (Priority: P1)

**Goal**: Enable users to create a new task by providing a title and description so they can track work items

**Independent Test**: Add a new todo and verify it appears in the list. Delivers value by enabling users to capture tasks for tracking.

### Tests for User Story 2 (TDD approach) ⚠️

- [ ] T026 [P] [US2] Unit test for adding todo with title only in tests/unit/test_storage.py
- [ ] T027 [P] [US2] Unit test for adding todo with title and description in tests/unit/test_storage.py
- [ ] T028 [P] [US2] Unit test for validation of empty title in tests/unit/test_validators.py
- [ ] T029 [P] [US2] Unit test for validation of title length in tests/unit/test_validators.py
- [ ] T030 [P] [US2] Integration test for add command in tests/integration/test_cli_integration.py

### Implementation for User Story 2

- [ ] T031 [P] [US2] Add add() method to TodoStorage in src/todo/storage.py
- [ ] T032 [US2] Implement add operation in src/todo/operations.py
- [ ] T033 [US2] Add validation functions for add command in src/todo/validators.py
- [ ] T034 [US2] Create formatter for add success message in src/todo/formatters.py
- [ ] T035 [US2] Add add command to CLI in src/todo/cli.py
- [ ] T036 [US2] Update main.py to handle add command
- [ ] T037 [US2] Add ID generation logic to TodoStorage in src/todo/storage.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Todo Complete/Incomplete (Priority: P2)

**Goal**: Enable users to mark tasks as complete or revert them to pending to track progress and completion status

**Independent Test**: Create a todo, mark it complete, and verify status change. Delivers value by enabling progress tracking.

### Tests for User Story 3 (TDD approach) ⚠️

- [ ] T038 [P] [US3] Unit test for marking todo as complete in tests/unit/test_storage.py
- [ ] T039 [P] [US3] Unit test for marking todo as incomplete in tests/unit/test_storage.py
- [ ] T040 [P] [US3] Unit test for validation of invalid ID in tests/unit/test_validators.py
- [ ] T041 [P] [US3] Unit test for toggle status functionality in tests/unit/test_operations.py
- [ ] T042 [P] [US3] Integration test for complete/incomplete commands in tests/integration/test_cli_integration.py

### Implementation for User Story 3

- [ ] T043 [P] [US3] Add toggle_status() method to TodoStorage in src/todo/storage.py
- [ ] T044 [US3] Implement toggle status operation in src/todo/operations.py
- [ ] T045 [US3] Add validation functions for toggle commands in src/todo/validators.py
- [ ] T046 [US3] Create formatters for toggle status messages in src/todo/formatters.py
- [ ] T047 [US3] Add complete command to CLI in src/todo/cli.py
- [ ] T048 [US3] Add incomplete command to CLI in src/todo/cli.py
- [ ] T049 [US3] Update main.py to handle complete/incomplete commands

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Update Todo Details (Priority: P3)

**Goal**: Enable users to modify the title or description of an existing task to correct errors or update requirements

**Independent Test**: Create a todo, update its details, and verify the changes. Delivers value by allowing task refinement without recreation.

### Tests for User Story 4 (TDD approach) ⚠️

- [ ] T050 [P] [US4] Unit test for updating todo title in tests/unit/test_storage.py
- [ ] T051 [P] [US4] Unit test for updating todo description in tests/unit/test_storage.py
- [ ] T052 [P] [US4] Unit test for updating both title and description in tests/unit/test_storage.py
- [ ] T053 [P] [US4] Unit test for validation of empty title during update in tests/unit/test_validators.py
- [ ] T054 [P] [US4] Integration test for update command in tests/integration/test_cli_integration.py

### Implementation for User Story 4

- [ ] T055 [P] [US4] Add update() method to TodoStorage in src/todo/storage.py
- [ ] T056 [US4] Implement update operation in src/todo/operations.py
- [ ] T057 [US4] Add validation functions for update command in src/todo/validators.py
- [ ] T058 [US4] Create formatters for update messages in src/todo/formatters.py
- [ ] T059 [US4] Add update command to CLI in src/todo/cli.py
- [ ] T060 [US4] Update main.py to handle update command

---

## Phase 7: User Story 5 - Delete Todo (Priority: P3)

**Goal**: Enable users to remove completed or unnecessary tasks to keep their list focused and relevant

**Independent Test**: Create a todo, delete it by ID, and verify removal. Delivers value by enabling list cleanup.

### Tests for User Story 5 (TDD approach) ⚠️

- [ ] T061 [P] [US5] Unit test for deleting existing todo in tests/unit/test_storage.py
- [ ] T062 [P] [US5] Unit test for validation of invalid ID for deletion in tests/unit/test_validators.py
- [ ] T063 [P] [US5] Unit test for delete confirmation logic in tests/unit/test_operations.py
- [ ] T064 [P] [US5] Integration test for delete command in tests/integration/test_cli_integration.py
- [ ] T065 [P] [US5] Unit test for delete without confirmation flag in tests/unit/test_cli.py

### Implementation for User Story 5

- [ ] T066 [P] [US5] Add delete() method to TodoStorage in src/todo/storage.py
- [ ] T067 [US5] Implement delete operation in src/todo/operations.py
- [ ] T068 [US5] Add validation functions for delete command in src/todo/validators.py
- [ ] T069 [US5] Create formatters for delete messages in src/todo/formatters.py
- [ ] T070 [US5] Add delete command to CLI in src/todo/cli.py with confirmation
- [ ] T071 [US5] Update main.py to handle delete command

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T072 [P] Documentation updates in README.md with all command usage examples
- [ ] T073 [P] Add help command implementation in src/todo/cli.py and src/main.py
- [ ] T074 [P] Add error handling and user-friendly messages throughout application
- [ ] T075 [P] Add exit code handling per CLI contracts specification
- [ ] T076 [P] Add status indicator formatting per CLI contracts (✓ for completed, ○ for pending)
- [ ] T077 [P] Add proper argparse setup with all commands and arguments
- [ ] T078 [P] Additional unit tests in tests/unit/ to achieve >80% coverage
- [ ] T079 [P] Run quickstart.md validation and update as needed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Unit test for empty todo list display in tests/unit/test_formatters.py"
Task: "Unit test for single todo display in tests/unit/test_formatters.py"
Task: "Unit test for multiple todo display in tests/unit/test_formatters.py"
Task: "Unit test for status indicators (pending/completed) in tests/unit/test_formatters.py"
Task: "Integration test for list command in tests/integration/test_cli_integration.py"

# Launch all implementation for User Story 1 together:
Task: "Create Todo dataclass in src/todo/models.py with id, title, description, status, timestamps"
Task: "Create TodoStorage class in src/todo/storage.py with get_all() method"
Task: "Implement list operation in src/todo/operations.py"
Task: "Create formatter functions in src/todo/formatters.py for displaying todo lists"
Task: "Add list command to CLI in src/todo/cli.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Phase 9: User Story 6 - Interactive Menu Experience (Priority: P2)

**Goal**: Provide an intuitive, visually appealing menu system that guides users through all todo operations with rich visual feedback and easy navigation

**Independent Test**: Navigate through the main menu, select different options, and verify all interactive features work correctly with visual feedback.

### Tests for User Story 6 (TDD approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T072 [P] [US6] Unit test for rich CLI initialization in tests/unit/test_rich_cli.py
- [ ] T073 [P] [US6] Unit test for welcome screen display in tests/unit/test_rich_cli.py
- [ ] T074 [P] [US6] Unit test for menu display functionality in tests/unit/test_rich_cli.py
- [ ] T075 [P] [US6] Integration test for interactive menu flow in tests/integration/test_rich_cli_integration.py

### Implementation for User Story 6

- [ ] T076 [P] [US6] Create rich CLI module in src/todo/rich_cli.py
- [ ] T077 [US6] Implement welcome screen with ASCII art in src/todo/rich_cli.py
- [ ] T078 [US6] Implement colorful menu system in src/todo/rich_cli.py
- [ ] T079 [US6] Add loading indicators and progress spinners in src/todo/rich_cli.py
- [ ] T080 [US6] Implement visual feedback system in src/todo/rich_cli.py
- [ ] T081 [US6] Add keyboard navigation support in src/todo/rich_cli.py
- [ ] T082 [US6] Update main.py to switch between classic and rich CLI

---

## Phase 10: User Story 7 - Statistics and Analytics (Priority: P3)

**Goal**: Provide users with statistics about their todos to track productivity and completion rates with visual representations

**Independent Test**: Add various completed and pending tasks, then view statistics to verify accurate calculation and visual representation.

### Tests for User Story 7 (TDD approach) ⚟️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T083 [P] [US7] Unit test for statistics calculation in tests/unit/test_rich_cli.py
- [ ] T084 [P] [US7] Unit test for statistics display formatting in tests/unit/test_formatters.py
- [ ] T085 [P] [US7] Integration test for statistics functionality in tests/integration/test_rich_cli_integration.py

### Implementation for User Story 7

- [ ] T086 [P] [US7] Add statistics calculation functions in src/todo/rich_cli.py
- [ ] T087 [US7] Implement statistics display with progress bars in src/todo/rich_cli.py
- [ ] T088 [US7] Add visual progress representation in src/todo/formatters.py
- [ ] T089 [US7] Create statistics dashboard in src/todo/rich_cli.py

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T090 [P] Update README.md with enhanced user experience features
- [ ] T091 [P] Add rich dependencies to pyproject.toml
- [ ] T092 [P] Update documentation to reflect interactive menu system
- [ ] T093 [P] Add help command implementation in src/todo/cli.py and src/main.py
- [ ] T094 [P] Add error handling and user-friendly messages throughout application
- [ ] T095 [P] Add exit code handling per CLI contracts specification
- [ ] T096 [P] Add status indicator formatting per CLI contracts (✅ for completed, ⏳ for pending)
- [ ] T097 [P] Add proper argparse setup with all commands and arguments
- [ ] T098 [P] Add additional unit tests in tests/unit/ to achieve >80% coverage
- [ ] T099 [P] Run quickstart.md validation and update as needed
- [ ] T100 [P] Update spec.md with enhanced user experience requirements
- [ ] T101 [P] Update plan.md with rich interface requirements
- [ ] T102 [P] Update data-model.md with visual representation details
- [ ] T103 [P] Update contracts/ with interactive mode features

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
