# 🚀 Quick Start Guide - Todo Web App

## Prerequisites
- Node.js 18+ installed
- Python 3.11+ installed
- A Neon database account (free tier) OR local PostgreSQL

---

## 🎯 Fastest Way to Get Started (5 minutes)

### Step 1: Get a Free Database (2 minutes)
1. Go to https://neon.tech
2. Sign up (free, no credit card needed)
3. Create a new project
4. Copy the connection string (it looks like this):
   ```
   postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

### Step 2: Setup Backend (2 minutes)

```bash
# Navigate to backend
cd apps/backend

# Create .env file
cp .env.example .env

# Generate a secret key
python3 -c "import secrets; print(secrets.token_hex(32))"
# Copy the output

# Edit .env file and update:
# - DATABASE_URL=<paste-your-neon-connection-string>
# - SECRET_KEY=<paste-the-generated-secret-key>

# Activate virtual environment
source .venv/bin/activate

# Run migrations
alembic upgrade head

# Start backend (keep this terminal open)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend running at: http://localhost:8000
✅ API Docs at: http://localhost:8000/docs

### Step 3: Setup Frontend (1 minute)

Open a **NEW terminal** (keep backend running):

```bash
# Navigate to frontend
cd apps/frontend

# Create .env.local file
cp .env.example .env.local

# Install dependencies (if not done)
npm install

# Start frontend
npm run dev
```

✅ Frontend running at: http://localhost:3000

---

## 🎉 Test the Application

1. Open browser: **http://localhost:3000**
2. Click **"Get Started"** button
3. Register with email: `test@example.com` and password: `password123`
4. Login with your credentials
5. Add your first task!

---

## 🎨 Features to Explore

- **Custom Checkboxes**: Click the circular checkbox to complete tasks
- **Hover Actions**: Hover over a task to see edit/delete buttons
- **Edit Tasks**: Click the edit icon to modify title/description
- **Delete Tasks**: Click the delete icon (with confirmation)
- **Smooth Animations**: Notice the fade-in effects
- **Responsive Design**: Try resizing your browser window

---

## 🐛 Troubleshooting

**Backend won't start:**
- Check if port 8000 is already in use: `lsof -i :8000`
- Make sure DATABASE_URL is correct in .env
- Verify virtual environment is activated

**Frontend won't start:**
- Check if port 3000 is already in use: `lsof -i :3000`
- Run `npm install` if you see dependency errors
- Make sure backend is running first

**Database connection errors:**
- Verify your Neon connection string includes `?sslmode=require`
- Check if the database is accessible
- Try the connection string in a PostgreSQL client

**Can't login/register:**
- Check browser console for errors (F12)
- Verify backend is running and accessible
- Check that CORS is configured correctly

---

## 📚 Next Steps

- Read the full documentation: `specs/002-todo-web-app/quickstart.md`
- Explore the API: http://localhost:8000/docs
- Check the architecture: `specs/002-todo-web-app/plan.md`
- Review completed tasks: `specs/002-todo-web-app/tasks.md`

---

## 🎯 What You Built

✅ Full-stack web application with modern UI
✅ JWT authentication with secure password hashing
✅ Complete CRUD operations for tasks
✅ User isolation (each user sees only their tasks)
✅ Responsive design (mobile, tablet, desktop)
✅ Custom UI inspired by Todoist and Microsoft To Do
✅ Production-ready with Docker and deployment configs

**Tech Stack:**
- Frontend: Next.js 16+ • React 19+ • TypeScript • Tailwind CSS
- Backend: FastAPI • SQLModel • PostgreSQL • JWT
- Database: Neon Serverless PostgreSQL

Enjoy your modern todo application! 🎉
