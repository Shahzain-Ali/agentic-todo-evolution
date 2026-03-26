# Agentic Todo Evolution

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-16+-000000?logo=next.js&logoColor=white)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?logo=postgresql&logoColor=white)](https://postgresql.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-Agents_SDK-412991?logo=openai&logoColor=white)](https://openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Full-stack todo app evolving from console to web with auth, AI chatbot, and modern UI (Python, FastAPI, Next.js)

<!-- Add your screenshots here -->
<!-- ![Dashboard](docs/screenshots/dashboard.png) -->
<!-- ![AI Chatbot](docs/screenshots/chatbot.png) -->

## Project Overview

This project showcases systematic application development through three phases:

| Phase | Description | Tech |
|-------|-------------|------|
| **Phase 1** | Console app with in-memory storage | Python, Rich CLI |
| **Phase 2** | Full-stack web app with auth & modern UI | FastAPI, Next.js, PostgreSQL |
| **Phase 3** | AI chatbot for natural language task management | OpenAI Agents SDK, MCP, ChatKit |

---

## Phase 2: Full-Stack Web Application

A modern, production-ready todo web application with beautiful UI inspired by Todoist and Microsoft To Do.

### Features

- Modern UI Design with clean, minimal interface and smooth animations
- Better Auth Authentication with secure sessions and bcrypt hashing
- Full CRUD Operations with optimistic UI updates
- Responsive Design for mobile, tablet, and desktop
- User Isolation - each user sees only their own tasks
- Custom Checkboxes, hover actions, skeleton loaders

### Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | Next.js 16+, React 19+, TypeScript 5+, Tailwind CSS 4+, Better Auth |
| **Backend** | FastAPI 0.100+, SQLModel 0.14+, Python 3.11+, Pydantic v2 |
| **Database** | PostgreSQL 15+, Neon Serverless, Alembic migrations |
| **AI Chat** | OpenAI Agents SDK, GPT-4o-mini, FastMCP, ChatKit |

### Quick Start

```bash
# Clone
git clone https://github.com/Shahzain-Ali/agentic-todo-evolution.git
cd agentic-todo-evolution
cp .env.example .env  # Fill in your values
```

**Backend:**
```bash
cd apps/backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Configure DATABASE_URL and SECRET_KEY
alembic upgrade head
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd apps/frontend
npm install
cp .env.example .env.local  # Configure NEXT_PUBLIC_API_URL
npm run dev
```

> Backend: `http://localhost:8000` | API Docs: `http://localhost:8000/docs` | Frontend: `http://localhost:3000`

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/sign-up/email` | User registration |
| `POST` | `/api/auth/sign-in/email` | User login |
| `GET` | `/api/tasks` | Get all user tasks |
| `POST` | `/api/tasks` | Create new task |
| `PUT` | `/api/tasks/{id}` | Update task |
| `DELETE` | `/api/tasks/{id}` | Delete task |
| `GET` | `/health` | Health check |

---

## Phase 3: AI-Powered Todo Chatbot

A natural language interface for managing todos through conversation. Instead of clicking buttons, just tell the chatbot what you want to do.

### Features

- **Natural Language Task Management**: "Add buy groceries to my list", "Show my pending tasks"
- **OpenAI Agents SDK**: GPT-4o-mini powered intent understanding and function calling
- **MCP Protocol**: Model Context Protocol server for tool-based task operations
- **ChatKit UI**: OpenAI's hosted chat interface component
- **JWT Authentication**: Each chat action validates user identity
- **User Isolation**: Users can only manage their own tasks via chat

### MCP Tools

| Tool | Description |
|------|-------------|
| `add_task` | Create a new task via natural language |
| `list_tasks` | View tasks (all, pending, or completed) |
| `complete_task` | Mark a task as done |

### Example Conversations

```
User: "Add buy milk to my list"
Bot:  Task "buy milk" has been added!

User: "What tasks do I have?"
Bot:  You have 3 tasks: 1. Buy milk (pending), 2. Fix bug (pending), 3. Read docs (completed)

User: "Mark task 1 as done"
Bot:  "Buy milk" marked as completed!
```

---

## Phase 1: Console Application

A rich CLI todo application with in-memory storage — the foundation of this project.

```bash
python3 -m venv venv && source venv/bin/activate
pip install -e ".[dev]"
python src/main.py
```

**Features:** Interactive menu, ASCII art UI, statistics dashboard, color-coded status, progress bars, filtering, keyboard navigation.

<details>
<summary>CLI Commands</summary>

```bash
python src/main.py add "Buy groceries" "Milk, eggs, bread"
python src/main.py list --status pending
python src/main.py complete 1
python src/main.py update 1 --title "New title"
python src/main.py delete 1
```

</details>

---

## Project Structure

```
agentic-todo-evolution/
├── apps/
│   ├── backend/             # FastAPI + SQLModel backend
│   │   ├── app/             # Main application (auth, models, routes)
│   │   ├── alembic/         # Database migrations
│   │   └── mcp_server/      # MCP server for AI chatbot (Phase 3)
│   └── frontend/            # Next.js frontend
│       ├── app/             # Pages, routes, API handlers
│       ├── components/      # React components (chat, UI)
│       └── lib/             # Utilities and config
├── src/                     # Phase 1 console app
├── specs/                   # Spec-driven development docs
├── .env.example             # Environment variable template
├── render.yaml              # Render deployment config
└── LICENSE
```

## Testing

```bash
python -m pytest tests/ -v
```

## Documentation

- [Quickstart Guide](specs/002-todo-web-app/quickstart.md) - Detailed setup and deployment
- [API Documentation](http://localhost:8000/docs) - Interactive API docs (run backend first)
- [Specification](specs/002-todo-web-app/spec.md) - Requirements and user stories
- [Architecture](specs/002-todo-web-app/plan.md) - Technical decisions

## License

[MIT](LICENSE)
