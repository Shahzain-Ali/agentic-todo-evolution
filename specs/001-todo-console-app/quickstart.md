# Quickstart Guide: Console Todo Application

**Feature**: 001-todo-console-app
**Date**: 2026-01-08
**Purpose**: Step-by-step setup and usage instructions

---

## Prerequisites

Before you begin, ensure you have:
- **Python 3.13+** installed
- **UV** (Python package manager) installed
- **Git** (for cloning the repository)
- A terminal/command-line interface

---

## Installation Steps

### Step 1: Install Python 3.13+

#### macOS/Linux
```bash
# Check current Python version
python3 --version

# If < 3.13, install via pyenv or system package manager
# Example with pyenv:
pyenv install 3.13.0
pyenv global 3.13.0
```

#### Windows
```powershell
# Download from python.org or use winget
winget install Python.Python.3.13

# Verify installation
python --version
```

### Step 2: Install UV

UV is a fast Python package manager that replaces pip/poetry/pipenv.

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

### Step 3: Clone the Repository

```bash
git clone <repository-url>
cd agentic-todo-evolution
git checkout 001-todo-console-app
```

### Step 4: Set Up Development Environment

```bash
# Create virtual environment with UV
uv venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# Install dependencies
uv pip install -e ".[dev]"
```

---

## Project Structure

After setup, your directory should look like:

```
agentic-todo-evolution/
├── src/
│   └── todo/
│       ├── __init__.py
│       ├── models.py
│       ├── storage.py
│       ├── operations.py
│       ├── cli.py
│       ├── validators.py
│       └── formatters.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── specs/
│   └── 001-todo-console-app/
│       ├── spec.md
│       ├── plan.md
│       ├── research.md
│       ├── data-model.md
│       ├── quickstart.md (this file)
│       └── contracts/
├── pyproject.toml
├── README.md
└── CLAUDE.md
```

---

## Running the Application

### Basic Usage

```bash
# Run from project root
python src/main.py <command> [arguments]

# Or if installed as package
todo <command> [arguments]
```

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add` | Create new todo | `python src/main.py add "Buy milk"` |
| `list` | Show all todos | `python src/main.py list` |
| `complete` | Mark as done | `python src/main.py complete 1` |
| `incomplete` | Mark as pending | `python src/main.py incomplete 1` |
| `update` | Edit todo | `python src/main.py update 1 --title "New title"` |
| `delete` | Remove todo | `python src/main.py delete 1` |
| `help` | Show help | `python src/main.py help` |

---

## Quick Examples

### Example 1: Create and View Todos

```bash
# Create your first todo
python src/main.py add "Buy groceries" "Milk, eggs, bread"

# Output:
# ✓ Todo created successfully.
#   ID: 1
#   Title: Buy groceries
#   Description: Milk, eggs, bread
#   Status: Pending

# Create another todo
python src/main.py add "Finish report"

# View all todos
python src/main.py list

# Output:
# Your Todos:
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ID | Status | Title           | Description
# ───┼────────┼─────────────────┼──────────────
# 1  | ○      | Buy groceries   | Milk, eggs, bread
# 2  | ○      | Finish report   |
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Total: 2 todos (0 completed, 2 pending)
```

### Example 2: Complete and Update Todos

```bash
# Mark todo as complete
python src/main.py complete 1

# Output:
# ✓ Todo #1 marked as completed.
#   Title: Buy groceries

# Update todo description
python src/main.py update 2 --description "Q4 financial summary"

# Output:
# ✓ Todo #2 updated successfully.
#   Title: Finish report
#   Description: Q4 financial summary
#   Status: Pending

# View updated list
python src/main.py list

# Output shows todo 1 with ✓ (completed) and todo 2 with ○ (pending)
```

### Example 3: Filter and Delete Todos

```bash
# Show only pending todos
python src/main.py list --status pending

# Show only completed todos
python src/main.py list --status completed

# Delete a todo (with confirmation)
python src/main.py delete 1

# Output:
# ⚠ Are you sure you want to delete todo #1: "Buy groceries"? (y/n): y
# ✓ Todo #1 deleted successfully.

# Delete without confirmation
python src/main.py delete 2 --confirm
```

---

## Running Tests

### Run All Tests

```bash
# Run entire test suite
pytest

# Run with coverage report
pytest --cov=src/todo --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/unit/test_models.py

# Specific test function
pytest tests/unit/test_models.py::test_todo_creation
```

### Test Output Example

```
================================ test session starts ================================
collected 45 items

tests/unit/test_models.py ............                                        [ 26%]
tests/unit/test_storage.py ..........                                         [ 48%]
tests/unit/test_operations.py ........                                        [ 66%]
tests/unit/test_validators.py .......                                         [ 82%]
tests/integration/test_cli_integration.py ........                            [100%]

================================ 45 passed in 0.23s =================================
```

---

## Development Workflow

### Step 1: Read the Spec

```bash
# Review feature requirements
cat specs/001-todo-console-app/spec.md

# Review technical plan
cat specs/001-todo-console-app/plan.md
```

### Step 2: Follow TDD (Test-Driven Development)

```bash
# 1. Write a failing test
# Edit tests/unit/test_models.py

# 2. Run test to confirm it fails
pytest tests/unit/test_models.py -v

# 3. Implement minimum code to pass
# Edit src/todo/models.py

# 4. Run test to confirm it passes
pytest tests/unit/test_models.py -v

# 5. Refactor if needed
# 6. Repeat for next feature
```

### Step 3: Use Claude Code for Implementation

```bash
# Activate Claude Code (if using)
# Follow CLAUDE.md instructions

# Example Claude Code workflow:
# User: "Implement the Todo model according to data-model.md"
# Claude: Reads spec, writes tests, implements code, runs tests
```

---

## Common Issues & Troubleshooting

### Issue 1: Python Version Too Old

**Error**: `SyntaxError` or `ImportError` related to type hints

**Solution**:
```bash
python --version  # Check version
# If < 3.13, upgrade Python (see Installation Steps)
```

### Issue 2: UV Not Found

**Error**: `command not found: uv`

**Solution**:
```bash
# Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (if needed)
export PATH="$HOME/.cargo/bin:$PATH"  # macOS/Linux
```

### Issue 3: Module Not Found

**Error**: `ModuleNotFoundError: No module named 'todo'`

**Solution**:
```bash
# Ensure you're in project root
pwd

# Reinstall in editable mode
uv pip install -e ".[dev]"
```

### Issue 4: Tests Failing

**Error**: Multiple test failures after implementation

**Solution**:
```bash
# Run tests in verbose mode to see details
pytest -v

# Check if implementation matches spec
diff <(cat specs/001-todo-console-app/data-model.md) <(python -c "import todo; help(todo)")

# Review test expectations vs implementation
```

---

## Configuration Files

### pyproject.toml

The `pyproject.toml` file defines project metadata and dependencies:

```toml
[project]
name = "todo-console-app"
version = "0.1.0"
description = "Console-based todo application with in-memory storage"
requires-python = ">=3.13"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
]

[project.scripts]
todo = "todo.cli:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "-ra",
]

[tool.coverage.run]
source = ["src/todo"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

---

## Next Steps

After completing the quickstart:

1. ✅ **Environment set up** - Python, UV, dependencies installed
2. ✅ **Project structure understood** - Know where files live
3. ✅ **Basic usage tested** - Can run commands manually
4. ➡️ **Ready for /sp.tasks** - Generate implementation tasks
5. ➡️ **Ready for /sp.implement** - Begin TDD implementation

---

## Additional Resources

- **Spec**: See `specs/001-todo-console-app/spec.md` for requirements
- **Plan**: See `specs/001-todo-console-app/plan.md` for technical approach
- **Data Model**: See `specs/001-todo-console-app/data-model.md` for entity structures
- **CLI Contracts**: See `specs/001-todo-console-app/contracts/cli-commands.md` for command details
- **Research**: See `specs/001-todo-console-app/research.md` for technical decisions

---

## Getting Help

If you encounter issues:

1. Check this quickstart guide
2. Review the spec and plan documents
3. Run `python src/main.py help`
4. Check test output: `pytest -v`
5. Review CLAUDE.md for development guidance

**Happy coding! 🚀**
