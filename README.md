# 📋 Agentic Todo Evolution

A progressive todo application demonstrating evolution from console app to modern full-stack web application.

## 🎯 Project Overview

This project showcases systematic application development through two phases:
- **Phase 1**: Console application with in-memory storage
- **Phase 2**: Full-stack web application with modern UI and database persistence

---

## 🚀 Phase 2: Full-Stack Web Application (Current)

A modern, production-ready todo web application with beautiful UI inspired by Todoist and Microsoft To Do.

### ✨ Features

- 🎨 **Modern UI Design**: Clean, minimal interface with smooth animations
- 🔐 **JWT Authentication**: Secure user authentication with bcrypt password hashing
- ✅ **Full CRUD Operations**: Create, read, update, and delete tasks
- 🎯 **Custom Checkboxes**: Circular design with smooth transitions
- 👁️ **Hover Actions**: Edit and delete buttons appear on hover
- 📱 **Responsive Design**: Optimized for mobile, tablet, and desktop
- ⚡ **Real-time Updates**: Instant UI feedback with optimistic updates
- 🌈 **Smooth Animations**: Fade-in, slide-in effects throughout
- 🔒 **User Isolation**: Each user sees only their own tasks
- 📊 **Loading States**: Beautiful skeleton loaders and spinners

### 🛠️ Tech Stack

**Frontend**: Next.js 16+ • React 19+ • TypeScript 5+ • Tailwind CSS 4+

**Backend**: FastAPI 0.100+ • SQLModel 0.14+ • Python 3.11+ • JWT • Pydantic v2

**Database**: PostgreSQL 15+ • Neon Serverless • Alembic migrations

### 🚀 Quick Start

**Backend Setup:**
```bash
cd apps/backend
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv && source .venv/bin/activate
uv pip install -e .
cp .env.example .env  # Configure DATABASE_URL and SECRET_KEY
alembic upgrade head
uvicorn app.main:app --reload
```
Backend: http://localhost:8000 | API Docs: http://localhost:8000/docs

**Frontend Setup:**
```bash
cd apps/frontend
npm install
cp .env.example .env.local  # Configure NEXT_PUBLIC_API_URL
npm run dev
```
Frontend: http://localhost:3000

### 📚 Documentation

- **[Quickstart Guide](specs/002-todo-web-app/quickstart.md)** - Detailed setup and deployment
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs
- **[Specification](specs/002-todo-web-app/spec.md)** - Requirements and user stories
- **[Architecture](specs/002-todo-web-app/plan.md)** - Technical decisions
- **[Tasks](specs/002-todo-web-app/tasks.md)** - Implementation breakdown (121/133 completed)

### 🔐 API Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login (returns JWT)
- `GET /api/tasks` - Get all user tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `GET /health` - Health check

### 🎨 UI Design Highlights

**Inspired by Todoist and Microsoft To Do:**
- Clean, minimal layout with focus on tasks
- Custom circular checkboxes with smooth animations
- Hover interactions for cleaner interface
- Subtle fade-in and slide-in effects
- Modern typography with proper spacing
- Responsive cards with rounded corners and shadows
- Skeleton loaders matching content structure
- Friendly empty states with icons

---

## 📋 Phase 1: Todo Console Application

A beautiful and user-friendly command-line todo application with in-memory storage, featuring rich visual elements and an intuitive interactive menu system.

## ✨ Features

- 🎨 **Rich Visual Interface**: Beautiful colorful UI with tables, panels, and progress bars
- 🎯 **Interactive Menu**: Easy-to-use menu system with visual navigation
- 📊 **Statistics Dashboard**: Track your productivity with visual statistics
- 🎭 **ASCII Art**: Stylish ASCII art welcome screens
- ⚡ **Loading Indicators**: Progress spinners for smooth user experience
- ✅ **Visual Feedback**: Color-coded status indicators and success messages
- 🔍 **Filtering Options**: Easily view pending, completed, or all todos
- 🛡️ **Confirmation Dialogs**: Prevent accidental deletions
- 🎮 **Keyboard Navigation**: Easy menu navigation with arrow keys
- 📈 **Progress Tracking**: Visual completion rates and progress bars

## Prerequisites

- Python 3.12+
- UV package manager

## Setup

1. Install UV:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## Quick Start

1. Clone the repository and navigate to the project directory
2. Install UV package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. Create virtual environment: `python3 -m venv venv`
4. Activate virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -e ".[dev]"`
6. Launch the application: `python src/main.py`

## Usage

### Interactive Mode (Recommended)
```bash
python src/main.py
```
Starts the beautiful interactive menu system with full visual experience. The interactive mode provides:
- ASCII art welcome screen with "TODO APP" banner
- Colorful menu options with emoji icons and color coding
- Loading spinners during operations
- Visual feedback with color-coded status indicators
- Statistics dashboard with visual completion rates
- Confirmation dialogs to prevent accidental deletions
- Filtering options to view pending, completed, or all todos
- Responsive tables with well-formatted todo listings
- Keyboard navigation support

### Command Line Mode
```bash
# Add a new todo
python src/main.py add "Buy groceries" "Milk, eggs, bread"

# List all todos
python src/main.py list

# List only pending todos
python src/main.py list --status pending

# List only completed todos
python src/main.py list --status completed

# Mark a todo as complete
python src/main.py complete 1

# Mark a todo as incomplete
python src/main.py incomplete 1

# Update a todo title
python src/main.py update 1 --title "New title"

# Update a todo description
python src/main.py update 1 --description "New description"

# Update both title and description
python src/main.py update 1 --title "New title" --description "New description"

# Delete a todo (with confirmation prompt)
python src/main.py delete 1

# Delete a todo without confirmation
python src/main.py delete 1 --confirm

# Show help
python src/main.py --help
```

## Commands

- `add <title> [description]` - Create a new todo task
- `list [--status pending|completed|all]` - Display all todos (default: all)
- `complete <id>` - Mark a todo as completed
- `incomplete <id>` - Mark a todo as pending
- `update <id> [--title] [--description]` - Modify a todo
- `delete <id> [--confirm]` - Remove a todo
- `help` - Show this help message
- `--help` or `-h` - Show this help message

## Interactive Menu Options

When running in interactive mode (`python src/main.py`), the following menu options are available:

1. **➕ Add Todo** - Create a new todo with title and description
2. **📋 List Todos** - View all todos with filtering options (all, pending, completed)
3. **✅ Complete Todo** - Mark a todo as completed
4. **↩️ Mark Incomplete** - Mark a completed todo as pending again
5. **✏️ Update Todo** - Modify the title or description of a todo
6. **🗑️ Delete Todo** - Remove a todo with confirmation dialog
7. **📊 View Stats** - See statistics dashboard with completion rates
8. **🚪 Exit** - Close the application with goodbye message

## 🎨 User Experience Features

- **Colorful Menu System**: Navigate with emoji icons and colored options
- **Visual Status Indicators**: ✅ for completed, ⏳ for pending
- **Progress Spinners**: Visual feedback during operations
- **Confirmation Dialogs**: Prevent accidental deletions
- **Statistics Dashboard**: Visual completion rates and progress bars
- **Responsive Tables**: Well-formatted todo listings
- **Error Handling**: Friendly error messages with suggestions
- **ASCII Art Welcome**: Stylish application branding
- **Keyboard Navigation**: Easy menu navigation with arrow keys

## 🧪 Testing

Run all tests to verify functionality:
```bash
python -m pytest tests/ -v
```

## 📁 Project Structure

```
src/todo/
├── models.py          # Data models and storage
├── operations.py      # Business logic
├── validators.py      # Input validation
├── formatters.py      # Output formatting
├── cli.py            # Classic command-line interface
├── rich_cli.py       # Enhanced visual interface
└── __init__.py
```

## 🚀 Phase I: Todo In-Memory Python Console App

This application serves as the foundation for the 5-phase todo application project, featuring:
- In-memory storage for learning core concepts
- Complete CRUD operations (Add, List, Complete, Update, Delete)
- Enhanced user experience with rich visual interface
- Proper error handling and validation
- Comprehensive test coverage