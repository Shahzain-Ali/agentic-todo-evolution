# Todo Web App - Quickstart Guide

## Overview

This guide will help you set up and deploy the full-stack Todo application.

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL database (or Neon Serverless account)
- Git

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd agentic-todo-evolution
```

### 2. Backend Setup

```bash
cd apps/backend

# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .

# Create .env file
cp .env.example .env
# Edit .env and configure:
# - DATABASE_URL (PostgreSQL connection string)
# - SECRET_KEY (generate with: openssl rand -hex 32)
# - FRONTEND_URL (http://localhost:3000)

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000
API documentation: http://localhost:8000/docs

### 3. Frontend Setup

```bash
cd apps/frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local
# Edit .env.local and set:
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Start the development server
npm run dev
```

Frontend will be available at: http://localhost:3000

## Database Setup

### Option 1: Neon Serverless PostgreSQL (Recommended)

1. Sign up at https://neon.tech
2. Create a new project
3. Copy the connection string
4. Update `DATABASE_URL` in `apps/backend/.env`

### Option 2: Local PostgreSQL

```bash
# Install PostgreSQL
# Create database
createdb todo_db

# Update DATABASE_URL in apps/backend/.env
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
```

## Production Deployment

### Backend Deployment (Railway/Render/Fly.io)

#### Using Railway

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login and deploy:
```bash
cd apps/backend
railway login
railway init
railway up
```

3. Set environment variables in Railway dashboard:
   - `DATABASE_URL` (from Neon)
   - `SECRET_KEY` (generate new one)
   - `FRONTEND_URL` (your Vercel URL)
   - `ENVIRONMENT=production`

4. Run migrations:
```bash
railway run alembic upgrade head
```

#### Using Docker

```bash
cd apps/backend

# Build image
docker build -t todo-backend .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL="your-database-url" \
  -e SECRET_KEY="your-secret-key" \
  -e FRONTEND_URL="your-frontend-url" \
  todo-backend
```

### Frontend Deployment (Vercel)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
cd apps/frontend
vercel
```

3. Set environment variables in Vercel dashboard:
   - `NEXT_PUBLIC_API_URL` (your backend URL)

4. Redeploy to apply environment variables:
```bash
vercel --prod
```

## Environment Variables Reference

### Backend (.env)

```env
DATABASE_URL=postgresql://user:password@host/database
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
FRONTEND_URL=https://your-frontend-domain.com
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
NODE_ENV=production
```

## Testing the Deployment

### 1. Health Check

```bash
curl https://your-backend-domain.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "service": "todo-api"
}
```

### 2. API Documentation

Visit: `https://your-backend-domain.com/docs`

### 3. Frontend

Visit: `https://your-frontend-domain.com`

Test the following flows:
1. Register a new account
2. Login with credentials
3. Create a task
4. Update task status
5. Edit task details
6. Delete a task

## Troubleshooting

### Backend Issues

**Database connection failed:**
- Verify `DATABASE_URL` is correct
- Check if database is accessible
- For Neon, ensure `?sslmode=require` is in connection string

**CORS errors:**
- Verify `FRONTEND_URL` matches your frontend domain
- Check CORS middleware configuration in `app/main.py`

**JWT authentication errors:**
- Ensure `SECRET_KEY` is set and consistent
- Check token expiration settings

### Frontend Issues

**API connection failed:**
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check if backend is running and accessible
- Verify CORS is configured on backend

**Build errors:**
- Run `npm run build` locally to test
- Check for TypeScript errors
- Verify all dependencies are installed

## Performance Optimization

### Backend

1. Enable database connection pooling
2. Add Redis for caching (optional)
3. Use CDN for static assets
4. Enable gzip compression

### Frontend

1. Enable Next.js image optimization
2. Use dynamic imports for large components
3. Implement code splitting
4. Enable SWR or React Query for data fetching

## Security Checklist

- [ ] Change default `SECRET_KEY` in production
- [ ] Use HTTPS for all endpoints
- [ ] Enable rate limiting on API
- [ ] Set secure cookie flags
- [ ] Implement CSRF protection
- [ ] Regular security updates
- [ ] Database backups configured
- [ ] Environment variables not committed to git

## Monitoring

### Backend Monitoring

- Health check endpoint: `/health`
- Logs: Check application logs for errors
- Database: Monitor connection pool and query performance

### Frontend Monitoring

- Vercel Analytics (built-in)
- Error tracking: Consider Sentry integration
- Performance: Use Lighthouse for audits

## Scaling Considerations

### Horizontal Scaling

- Backend: Deploy multiple instances behind load balancer
- Database: Use read replicas for read-heavy workloads
- Frontend: Vercel handles this automatically

### Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize database queries
- Add caching layer

## Support

For issues or questions:
- Check API documentation: `/docs`
- Review error logs
- Check environment variables
- Verify database connectivity

## Next Steps

1. Set up CI/CD pipeline
2. Add automated tests
3. Implement monitoring and alerting
4. Set up database backups
5. Configure custom domain
6. Add analytics tracking
