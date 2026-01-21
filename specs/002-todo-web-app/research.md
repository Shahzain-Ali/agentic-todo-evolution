# Research: Technology Decisions for Full-Stack Todo Application

**Feature**: 002-todo-web-app
**Date**: 2026-01-14
**Status**: Completed

## Overview

This document captures the research and decision-making process for technology choices in the full-stack todo application. All decisions are based on project requirements, team expertise, deployment constraints, and industry best practices.

## Frontend Technology Stack

### Decision 1: Next.js 16+ with App Router

**Chosen**: Next.js 16+ with App Router

**Rationale**:
- **Requirement**: Modern React framework with server-side rendering capabilities
- **App Router Benefits**: File-based routing, React Server Components, improved performance
- **Developer Experience**: Excellent TypeScript support, hot reload, built-in optimizations
- **Deployment**: Zero-config deployment on Vercel (requirement)
- **Ecosystem**: Large community, extensive documentation, mature tooling

**Alternatives Considered**:
- **Create React App**: Rejected - deprecated, no SSR, poor performance
- **Vite + React Router**: Rejected - requires more configuration, no built-in SSR
- **Remix**: Rejected - less mature ecosystem, steeper learning curve

**Best Practices**:
- Use Server Components by default for better performance
- Mark interactive components with `'use client'` directive
- Leverage Next.js Image component for optimized images
- Use App Router layouts for shared UI elements
- Implement route protection via middleware

### Decision 2: Better Auth for Authentication

**Chosen**: Better Auth

**Rationale**:
- **Requirement**: JWT-based authentication with frontend integration
- **Simplicity**: Handles token storage, refresh, and session management
- **Security**: HttpOnly cookies, CSRF protection, secure defaults
- **Integration**: Works seamlessly with Next.js App Router
- **Flexibility**: Supports custom backend APIs (FastAPI in our case)

**Alternatives Considered**:
- **NextAuth.js**: Rejected - primarily designed for OAuth providers, overkill for simple email/password
- **Custom Implementation**: Rejected - reinventing the wheel, security risks
- **Auth0/Clerk**: Rejected - third-party dependency, cost, vendor lock-in

**Best Practices**:
- Store JWT tokens in httpOnly cookies (not localStorage)
- Implement automatic token refresh before expiration
- Use middleware for route protection
- Handle 401 responses globally (redirect to login)

### Decision 3: Tailwind CSS for Styling

**Chosen**: Tailwind CSS 4+

**Rationale**:
- **Requirement**: Responsive, accessible, mobile-first design
- **Productivity**: Utility-first approach speeds up development
- **Consistency**: Design system built into the framework
- **Performance**: Purges unused CSS, small bundle size
- **Accessibility**: Easy to implement WCAG-compliant designs

**Alternatives Considered**:
- **CSS Modules**: Rejected - more boilerplate, harder to maintain consistency
- **Styled Components**: Rejected - runtime overhead, larger bundle size
- **Material-UI**: Rejected - opinionated design, harder to customize

**Best Practices**:
- Define custom theme in tailwind.config.ts (colors, spacing, typography)
- Use responsive modifiers (sm:, md:, lg:, xl:)
- Implement dark mode support (optional future enhancement)
- Use @apply for repeated utility combinations
- Follow mobile-first approach

## Backend Technology Stack

### Decision 4: FastAPI for Backend API

**Chosen**: FastAPI 0.100+

**Rationale**:
- **Requirement**: Python-based async web framework
- **Performance**: Async/await support, comparable to Node.js/Go
- **Developer Experience**: Automatic OpenAPI documentation, type hints, validation
- **Modern**: Built on Pydantic v2 and Starlette
- **Ecosystem**: Large community, extensive middleware, good testing support

**Alternatives Considered**:
- **Flask**: Rejected - synchronous by default, less modern, manual validation
- **Django**: Rejected - too heavy for simple API, includes unnecessary features (admin, templates)
- **Express.js (Node)**: Rejected - requirement specifies Python

**Best Practices**:
- Use async def for all route handlers
- Leverage dependency injection for auth, database sessions
- Organize routes into modular routers
- Use Pydantic models for request/response validation
- Implement proper error handling with HTTPException

### Decision 5: SQLModel for ORM

**Chosen**: SQLModel 0.14+

**Rationale**:
- **Requirement**: Type-safe ORM with Pydantic integration
- **Simplicity**: Combines SQLAlchemy and Pydantic in one model
- **Type Safety**: Full IDE autocomplete and type checking
- **Validation**: Automatic validation via Pydantic
- **Async Support**: Works with async SQLAlchemy

**Alternatives Considered**:
- **SQLAlchemy alone**: Rejected - requires separate Pydantic models, more boilerplate
- **Django ORM**: Rejected - tied to Django framework
- **Tortoise ORM**: Rejected - less mature, smaller community

**Best Practices**:
- Define models with proper type hints
- Use relationships for foreign keys
- Implement proper indexes for query performance
- Use Alembic for migrations
- Separate table models from API schemas

### Decision 6: JWT with python-jose

**Chosen**: python-jose for JWT handling

**Rationale**:
- **Requirement**: JWT token generation and verification
- **Standards**: Implements RFC 7519 (JWT) and RFC 7515 (JWS)
- **Algorithms**: Supports HS256, RS256, and other algorithms
- **Integration**: Works well with FastAPI
- **Security**: Well-tested, actively maintained

**Alternatives Considered**:
- **PyJWT**: Rejected - less feature-complete, fewer algorithms
- **Authlib**: Rejected - overkill for simple JWT needs
- **Custom Implementation**: Rejected - security risks, reinventing the wheel

**Best Practices**:
- Use HS256 algorithm for symmetric signing
- Store secret key in environment variable
- Set appropriate expiration (24 hours)
- Include minimal claims (user_id, exp, iat)
- Verify signature and expiration on every request

### Decision 7: Passlib with Bcrypt for Password Hashing

**Chosen**: Passlib with bcrypt

**Rationale**:
- **Requirement**: Secure password hashing
- **Security**: Bcrypt is industry standard, resistant to rainbow tables
- **Salting**: Automatic salt generation (12 rounds)
- **Future-Proof**: Easy to migrate to newer algorithms if needed
- **Integration**: Works seamlessly with FastAPI

**Alternatives Considered**:
- **Argon2**: Rejected - newer but less battle-tested, higher memory requirements
- **PBKDF2**: Rejected - older, less secure than bcrypt
- **Scrypt**: Rejected - less widely adopted

**Best Practices**:
- Use 12 salt rounds (balance between security and performance)
- Never store passwords in plain text
- Never return passwords in API responses
- Hash passwords before database insertion
- Use constant-time comparison for verification

## Database Technology Stack

### Decision 8: Neon Serverless PostgreSQL

**Chosen**: Neon Serverless PostgreSQL 15+

**Rationale**:
- **Requirement**: Managed PostgreSQL database
- **Serverless**: Auto-scaling, pay-per-use, no manual management
- **Performance**: Connection pooling, fast cold starts
- **Developer Experience**: Easy setup, generous free tier
- **Compatibility**: Standard PostgreSQL, works with all tools

**Alternatives Considered**:
- **Supabase**: Rejected - includes unnecessary features (auth, storage, realtime)
- **AWS RDS**: Rejected - requires manual management, higher cost
- **PlanetScale**: Rejected - MySQL-based, not PostgreSQL

**Best Practices**:
- Use connection pooling to handle serverless constraints
- Store connection string in environment variable
- Implement health check endpoint
- Use indexes for frequently queried columns
- Enable automatic backups

### Decision 9: Alembic for Migrations

**Chosen**: Alembic

**Rationale**:
- **Requirement**: Version-controlled schema changes
- **Integration**: Official migration tool for SQLAlchemy/SQLModel
- **Features**: Auto-generation, rollback support, branching
- **Reliability**: Battle-tested, widely used
- **Team Workflow**: Clear migration history, code review

**Alternatives Considered**:
- **Manual SQL**: Rejected - error-prone, no version control
- **SQLAlchemy-Migrate**: Rejected - deprecated
- **Django Migrations**: Rejected - tied to Django

**Best Practices**:
- Generate migrations automatically from model changes
- Review generated migrations before applying
- Test migrations in development before production
- Keep migrations small and focused
- Document complex migrations

## Testing Technology Stack

### Decision 10: Pytest for Backend Testing

**Chosen**: Pytest with pytest-asyncio

**Rationale**:
- **Requirement**: Async test support for FastAPI
- **Features**: Fixtures, parametrization, plugins
- **Integration**: Works seamlessly with FastAPI TestClient
- **Ecosystem**: Large plugin ecosystem
- **Developer Experience**: Clear output, easy to write tests

**Alternatives Considered**:
- **Unittest**: Rejected - more verbose, less features
- **Nose**: Rejected - deprecated
- **Robot Framework**: Rejected - overkill for unit/integration tests

**Best Practices**:
- Use fixtures for test data and database setup
- Use TestClient for API endpoint testing
- Separate unit tests from integration tests
- Use in-memory SQLite for test database
- Aim for 80%+ code coverage

### Decision 11: Jest + React Testing Library for Frontend

**Chosen**: Jest + React Testing Library

**Rationale**:
- **Requirement**: Component testing for React
- **Integration**: Built into Next.js, zero config
- **Philosophy**: Test user behavior, not implementation details
- **Accessibility**: Encourages accessible component design
- **Community**: Industry standard for React testing

**Alternatives Considered**:
- **Enzyme**: Rejected - deprecated, implementation-focused
- **Cypress Component Testing**: Rejected - heavier, slower
- **Vitest**: Rejected - less mature, smaller ecosystem

**Best Practices**:
- Test user interactions, not implementation
- Use screen queries (getByRole, getByLabelText)
- Mock API calls with MSW (Mock Service Worker)
- Test accessibility (keyboard navigation, ARIA)
- Aim for 70%+ code coverage

## Deployment Technology Stack

### Decision 12: Vercel for Frontend Deployment

**Chosen**: Vercel

**Rationale**:
- **Requirement**: Zero-config Next.js deployment
- **Performance**: Global CDN, edge functions, automatic optimization
- **Developer Experience**: Git integration, preview deployments, instant rollback
- **Cost**: Generous free tier, predictable pricing
- **Reliability**: 99.99% uptime SLA

**Alternatives Considered**:
- **Netlify**: Rejected - less optimized for Next.js
- **AWS Amplify**: Rejected - more complex setup
- **Self-hosted**: Rejected - requires DevOps expertise

**Best Practices**:
- Use environment variables for configuration
- Enable preview deployments for branches
- Set up custom domain
- Monitor performance with Vercel Analytics
- Use edge functions for dynamic content

### Decision 13: Railway/Render for Backend Deployment

**Chosen**: Railway or Render

**Rationale**:
- **Requirement**: Containerized FastAPI deployment
- **Simplicity**: Git-based deployment, automatic builds
- **Cost**: Affordable pricing, free tier available
- **Features**: Health checks, auto-restart, logs, metrics
- **Flexibility**: Supports Docker, multiple languages

**Alternatives Considered**:
- **Heroku**: Rejected - expensive, removed free tier
- **AWS ECS**: Rejected - complex setup, requires DevOps expertise
- **Fly.io**: Alternative option - similar features, good choice

**Best Practices**:
- Use Dockerfile for consistent builds
- Set up health check endpoint
- Configure auto-restart on failure
- Use environment variables for secrets
- Monitor logs and metrics

## Security Decisions

### Decision 14: HTTPS/TLS Everywhere

**Chosen**: Enforce HTTPS for all communications

**Rationale**:
- **Requirement**: Protect JWT tokens in transit
- **Security**: Prevents man-in-the-middle attacks
- **Compliance**: Industry standard, required for production
- **Automatic**: Provided by Vercel and Railway/Render

**Best Practices**:
- Redirect HTTP to HTTPS
- Use HSTS headers
- Ensure all API calls use HTTPS
- Never send tokens over HTTP

### Decision 15: CORS Configuration

**Chosen**: Restrict CORS to frontend origin only

**Rationale**:
- **Security**: Prevent unauthorized domains from accessing API
- **Flexibility**: Allow credentials (cookies)
- **Control**: Explicit whitelist of allowed origins

**Best Practices**:
- Whitelist specific frontend domain (not wildcard)
- Allow credentials for cookie-based auth
- Restrict HTTP methods to necessary ones
- Set appropriate headers (Content-Type, Authorization)

## Performance Decisions

### Decision 16: Connection Pooling

**Chosen**: SQLModel connection pooling

**Rationale**:
- **Performance**: Reuse database connections
- **Scalability**: Handle concurrent requests efficiently
- **Serverless**: Critical for Neon Serverless PostgreSQL

**Best Practices**:
- Configure pool size based on expected load
- Set appropriate timeout values
- Monitor connection usage
- Use async sessions for non-blocking I/O

### Decision 17: Async/Await Throughout

**Chosen**: Async endpoints and database operations

**Rationale**:
- **Performance**: Non-blocking I/O for better concurrency
- **Scalability**: Handle more concurrent users
- **Modern**: Industry best practice for web APIs

**Best Practices**:
- Use async def for all route handlers
- Use async database sessions
- Avoid blocking operations in async code
- Use asyncio for concurrent operations

## Summary

All technology decisions are aligned with project requirements, security best practices, and modern web development standards. The chosen stack (Next.js + FastAPI + PostgreSQL) provides:

- **Type Safety**: TypeScript + Python type hints + SQLModel
- **Performance**: Async/await, connection pooling, CDN
- **Security**: JWT, bcrypt, HTTPS, CORS, input validation
- **Developer Experience**: Hot reload, auto-documentation, type checking
- **Scalability**: Serverless database, auto-scaling deployments
- **Maintainability**: Clear architecture, comprehensive testing, version control

**Next Steps**: Proceed to Phase 1 (Design) to create data models and API contracts.
