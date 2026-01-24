# Frontend Builder Skill

**Version**: 1.0.0
**Created**: 2026-01-14
**Feature**: 002-todo-web-app
**Owner**: frontend-subagent

## Purpose

This skill enables building Next.js 16+ frontend applications using App Router, React 19+ Server Components, TypeScript 5+, Tailwind CSS 4+, and Better Auth. It provides patterns, best practices, and code generation capabilities for modern full-stack web applications.

## Scope

### In Scope
- Next.js 16+ App Router architecture (file-based routing, layouts, pages)
- React 19+ Server Components and Client Components patterns
- TypeScript 5+ type definitions and interfaces
- Tailwind CSS 4+ styling and responsive design
- Better Auth integration for authentication flows
- API Route Handlers for backend communication
- Form handling with Server Actions
- Protected routes with middleware
- Component organization and project structure

### Out of Scope
- Backend API implementation (see `backend-api` skill)
- Database schema design (see `database-schema` skill)
- DevOps and deployment configuration
- Testing implementation (handled during implementation phase)

## Technical Context

### Technology Stack
- **Framework**: Next.js 16+ with App Router
- **UI Library**: React 19+ (Server Components by default)
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 4+
- **Authentication**: Better Auth
- **HTTP Client**: fetch API (native)
- **Form Handling**: Server Actions
- **Validation**: Zod schemas

### Project Structure

```
apps/frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Root layout (required)
│   │   ├── page.tsx                # Home page (/)
│   │   ├── (auth)/                 # Route group (no URL segment)
│   │   │   ├── login/
│   │   │   │   └── page.tsx        # /login
│   │   │   └── register/
│   │   │       └── page.tsx        # /register
│   │   ├── dashboard/
│   │   │   ├── layout.tsx          # Nested layout
│   │   │   └── page.tsx            # /dashboard (protected)
│   │   ├── api/
│   │   │   └── auth/
│   │   │       └── [...all]/
│   │   │           └── route.ts    # Better Auth API routes
│   │   └── middleware.ts           # Route protection
│   ├── components/
│   │   ├── ui/                     # Reusable UI components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   └── card.tsx
│   │   ├── tasks/                  # Feature-specific components
│   │   │   ├── task-list.tsx
│   │   │   ├── task-item.tsx
│   │   │   └── task-form.tsx
│   │   └── layout/                 # Layout components
│   │       ├── header.tsx
│   │       └── footer.tsx
│   ├── lib/
│   │   ├── auth.ts                 # Better Auth configuration
│   │   ├── api-client.ts           # Backend API client
│   │   ├── utils.ts                # Utility functions
│   │   └── definitions.ts          # TypeScript types
│   └── actions/
│       ├── auth.ts                 # Auth Server Actions
│       └── tasks.ts                # Task Server Actions
├── public/
│   └── assets/
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

## Key Patterns

### 1. Server Components vs Client Components

**Default: Server Components** (no directive needed)
- Fetch data close to the source
- Keep secrets secure (API keys, tokens)
- Reduce JavaScript bundle size
- Use async/await directly in components

```tsx
// Server Component (default)
export default async function TasksPage() {
  const tasks = await fetchTasks() // Direct data fetching
  return <TaskList tasks={tasks} />
}
```

**Client Components** (require `'use client'` directive)
- Use React hooks (useState, useEffect, useContext)
- Handle browser events (onClick, onChange)
- Access browser APIs (localStorage, window)
- Use third-party libraries with browser dependencies

```tsx
'use client'
import { useState } from 'react'

export default function TaskForm() {
  const [title, setTitle] = useState('')

  return (
    <form>
      <input value={title} onChange={(e) => setTitle(e.target.value)} />
    </form>
  )
}
```

**Composition Pattern**: Pass Server Components as children to Client Components

```tsx
// Server Component
export default async function Page() {
  const data = await fetchData()
  return (
    <ClientWrapper>
      <ServerDataDisplay data={data} />
    </ClientWrapper>
  )
}

// Client Component
'use client'
export default function ClientWrapper({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false)
  return <div>{children}</div>
}
```

### 2. Authentication with Better Auth

**Configuration** (`lib/auth.ts`):
```tsx
import { betterAuth } from "better-auth"

export const auth = betterAuth({
  database: {
    provider: "postgres",
    url: process.env.DATABASE_URL!
  },
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8
  },
  session: {
    expiresIn: 60 * 60 * 24, // 24 hours
    updateAge: 60 * 60 * 24 // Update every 24 hours
  }
})
```

**Protected Route Pattern** (middleware.ts):
```tsx
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  const session = request.cookies.get('session')

  if (!session && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  if (session && (request.nextUrl.pathname === '/login' || request.nextUrl.pathname === '/register')) {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)']
}
```

### 3. API Communication

**Backend API Client** (`lib/api-client.ts`):
```tsx
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers
    }
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`)
  }

  return response.json()
}

// Authenticated requests
export async function authenticatedRequest<T>(
  endpoint: string,
  token: string,
  options?: RequestInit
): Promise<T> {
  return apiRequest<T>(endpoint, {
    ...options,
    headers: {
      ...options?.headers,
      'Authorization': `Bearer ${token}`
    }
  })
}
```

### 4. Form Handling with Server Actions

**Server Action** (`actions/tasks.ts`):
```tsx
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createTask(formData: FormData) {
  const title = formData.get('title') as string
  const description = formData.get('description') as string

  // Validate
  if (!title || title.length < 1) {
    return { error: 'Title is required' }
  }

  // Call backend API
  const response = await fetch(`${process.env.API_URL}/api/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, description })
  })

  if (!response.ok) {
    return { error: 'Failed to create task' }
  }

  revalidatePath('/dashboard')
  redirect('/dashboard')
}
```

**Form Component**:
```tsx
'use client'

import { useFormState } from 'react-dom'
import { createTask } from '@/actions/tasks'

export default function TaskForm() {
  const [state, formAction] = useFormState(createTask, { error: null })

  return (
    <form action={formAction}>
      <input name="title" required />
      <textarea name="description" />
      {state?.error && <p className="text-red-500">{state.error}</p>}
      <button type="submit">Create Task</button>
    </form>
  )
}
```

### 5. TypeScript Definitions

**Type Definitions** (`lib/definitions.ts`):
```tsx
export interface User {
  id: string
  email: string
  created_at: string
}

export interface Task {
  id: string
  user_id: string
  title: string
  description: string | null
  status: 'pending' | 'in_progress' | 'completed'
  created_at: string
  updated_at: string
}

export interface TaskCreate {
  title: string
  description?: string
}

export interface TaskUpdate {
  title?: string
  description?: string
  status?: 'pending' | 'in_progress' | 'completed'
}

export interface AuthResponse {
  access_token: string
  token_type: string
}
```

### 6. Tailwind CSS Patterns

**Component Styling**:
```tsx
export default function Button({
  children,
  variant = 'primary'
}: {
  children: React.ReactNode
  variant?: 'primary' | 'secondary'
}) {
  const baseStyles = 'px-4 py-2 rounded-lg font-medium transition-colors'
  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300'
  }

  return (
    <button className={`${baseStyles} ${variants[variant]}`}>
      {children}
    </button>
  )
}
```

**Responsive Design**:
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Mobile: 1 column, Tablet: 2 columns, Desktop: 3 columns */}
</div>
```

## Best Practices

### Component Organization
1. **Server Components by default** - Only use `'use client'` when necessary
2. **Composition over props drilling** - Use children pattern for flexibility
3. **Colocation** - Keep related components, styles, and tests together
4. **Single responsibility** - Each component should do one thing well

### Performance
1. **Minimize client JavaScript** - Maximize Server Components usage
2. **Code splitting** - Use dynamic imports for heavy components
3. **Image optimization** - Use Next.js `<Image>` component
4. **Font optimization** - Use `next/font` for automatic font optimization

### Security
1. **Never expose secrets** - Use environment variables, keep server-only code separate
2. **Validate all inputs** - Use Zod schemas for form validation
3. **CSRF protection** - Server Actions have built-in CSRF protection
4. **XSS prevention** - React escapes content by default

### Accessibility
1. **Semantic HTML** - Use proper HTML elements
2. **ARIA labels** - Add labels for screen readers
3. **Keyboard navigation** - Ensure all interactive elements are keyboard accessible
4. **Color contrast** - Follow WCAG guidelines

## Common Tasks

### Task 1: Create a New Page
1. Create file in `app/` directory (e.g., `app/about/page.tsx`)
2. Export default async function component
3. Add metadata export for SEO
4. Implement page content

### Task 2: Add Protected Route
1. Create page in `app/dashboard/` directory
2. Add authentication check in middleware.ts
3. Fetch user-specific data in Server Component
4. Handle unauthorized access

### Task 3: Implement Form with Validation
1. Create Server Action in `actions/`
2. Add Zod schema for validation
3. Create Client Component form with `useFormState`
4. Handle success/error states

### Task 4: Call Backend API
1. Use `api-client.ts` helper functions
2. Add authentication token from session
3. Handle errors with try/catch
4. Type response with TypeScript interfaces

## Environment Variables

Required in `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
AUTH_SECRET=your-auth-secret-here
AUTH_URL=http://localhost:3000
DATABASE_URL=postgresql://user:pass@host:5432/db
NODE_ENV=development
```

## Dependencies

Core dependencies in `package.json`:
```json
{
  "dependencies": {
    "next": "^16.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^4.0.0",
    "better-auth": "^1.0.0",
    "zod": "^3.22.0"
  }
}
```

## Testing Strategy

- **Unit Tests**: Jest + React Testing Library for components
- **Integration Tests**: Test user flows with Server Actions
- **E2E Tests**: Playwright for critical paths (login, task CRUD)

## References

- [Next.js 16 Documentation](https://nextjs.org/docs)
- [React 19 Documentation](https://react.dev)
- [Better Auth Documentation](https://better-auth.com)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)

---

**Last Updated**: 2026-01-14
**Status**: Active
**Maintainer**: Development Team
