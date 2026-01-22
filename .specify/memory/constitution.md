# Agentic Todo Evolution - Project Constitution

## Purpose

This constitution defines the **immutable principles and standards** that govern the development of the 5-Phase Todo Application. These principles apply across all phases and supersede all other practices.

**Project Vision**: Build a production-grade Todo application through 5 progressive phases, demonstrating mastery of the Agentic Dev Stack (AGENTS.md + Spec-KitPlus + Claude Code) and modern software engineering practices.

---

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

**Principle**: No code is written until the specification is complete, approved, and validated.

**Rules**:
- Every feature starts with a specification in `specs/<feature>/spec.md`
- Every specification must have an architectural plan in `specs/<feature>/plan.md`
- Every plan must be broken down into tasks in `specs/<feature>/tasks.md`
- Every task must have clear acceptance criteria and test cases
- Implementation begins only after human approval of spec, plan, and tasks

**Rationale**: Prevents "vibe coding," ensures alignment, and guarantees traceability from requirements to code.

**Enforcement**:
- Code reviews must verify task references
- PRs without task IDs are rejected
- Agents must stop and request specs if missing

---

### II. Test-Driven Development (NON-NEGOTIABLE)

**Principle**: Tests are written before implementation code. Red-Green-Refactor cycle is mandatory.

**Rules**:
1. **Red**: Write a failing test that defines the desired behavior
2. **Green**: Write the minimum code to make the test pass
3. **Refactor**: Improve the code while keeping tests green
4. **Repeat**: Continue until all acceptance criteria are met

**Test Coverage Requirements**:
- Minimum 80% code coverage
- 100% coverage for critical paths (auth, data persistence, security)
- Unit tests for all business logic
- Integration tests for component interactions
- E2E tests for critical user journeys

**Test Organization**:
```
tests/
├── unit/           # Test individual functions/methods
├── integration/    # Test component interactions
└── e2e/           # Test full user journeys
```

**Rationale**: Ensures code correctness, prevents regressions, and serves as living documentation.

**Enforcement**:
- CI/CD pipeline fails if tests don't pass
- PRs without tests are rejected
- Coverage reports required for all PRs

---

### III. Security by Design (NON-NEGOTIABLE)

**Principle**: Security is built into every layer, not added as an afterthought.

**Rules**:

1. **Authentication & Authorization**:
   - Use industry-standard auth (JWT, OAuth, etc.)
   - Implement role-based access control (RBAC)
   - Session management with secure tokens
   - Password hashing with bcrypt/argon2

2. **Input Validation**:
   - Validate all user inputs
   - Sanitize data before processing
   - Use parameterized queries (prevent SQL injection)
   - Escape output (prevent XSS)

3. **Secrets Management**:
   - Never commit secrets to version control
   - Use `.env` files (gitignored)
   - Use environment variables in production
   - Rotate secrets regularly

4. **API Security**:
   - Implement rate limiting
   - Use CORS with restricted origins
   - HTTPS only in production
   - API versioning for breaking changes

5. **Data Protection**:
   - Encrypt sensitive data at rest
   - Use TLS for data in transit
   - Implement proper error handling (no stack traces to users)
   - Log security events

**Rationale**: Security breaches are costly and damage trust. Prevention is cheaper than remediation.

**Enforcement**:
- Security review required for all PRs
- Automated security scanning in CI/CD
- Penetration testing before production deployment

---

### IV. Simplicity and YAGNI (You Aren't Gonna Need It)

**Principle**: Build only what is needed now. Avoid premature optimization and over-engineering.

**Rules**:
- Implement only features in the current spec
- No "future-proofing" without explicit requirements
- Prefer simple solutions over complex ones
- Refactor when complexity is justified by actual needs
- Delete unused code immediately

**Examples**:
- ✅ Simple in-memory storage for Phase I
- ❌ Building a distributed cache system for Phase I
- ✅ Basic CRUD operations
- ❌ Adding GraphQL when REST is sufficient

**Rationale**: Complexity is expensive to build, maintain, and debug. Start simple, evolve as needed.

**Enforcement**:
- Code reviews reject over-engineered solutions
- Complexity must be justified in ADRs
- Regular code cleanup sprints

---

### V. Documentation as Code

**Principle**: Documentation is maintained alongside code and is always up-to-date.

**Rules**:

1. **Code Documentation**:
   - Type hints for all functions (Python/TypeScript)
   - Docstrings for all public APIs
   - Comments explain WHY, not WHAT
   - Examples in docstrings

2. **API Documentation**:
   - OpenAPI/Swagger for REST APIs
   - Auto-generated from code
   - Include request/response examples
   - Document error codes

3. **Architecture Documentation**:
   - Specs in `specs/<feature>/spec.md`
   - Plans in `specs/<feature>/plan.md`
   - ADRs in `history/adr/`
   - Diagrams for complex flows

4. **User Documentation**:
   - README.md with quickstart
   - QUICKSTART.md for each phase
   - Deployment guides
   - Troubleshooting guides

**Rationale**: Good documentation reduces onboarding time, prevents misunderstandings, and serves as a contract.

**Enforcement**:
- PRs without documentation updates are rejected
- Documentation reviewed alongside code
- Broken links fail CI/CD

---

### VI. Observability and Debugging

**Principle**: Systems must be observable, debuggable, and monitorable in production.

**Rules**:

1. **Logging**:
   - Structured logging (JSON format)
   - Log levels: DEBUG, INFO, WARN, ERROR, CRITICAL
   - Include context (user_id, request_id, timestamp)
   - No sensitive data in logs (passwords, tokens)

2. **Metrics**:
   - Track key performance indicators (KPIs)
   - Response times (p50, p95, p99)
   - Error rates
   - Resource usage (CPU, memory, disk)

3. **Tracing**:
   - Distributed tracing for multi-service architectures
   - Request correlation IDs
   - Trace critical paths

4. **Error Handling**:
   - Explicit error handling (no silent failures)
   - User-friendly error messages
   - Detailed error logs for debugging
   - Error taxonomy with status codes

**Rationale**: You can't fix what you can't see. Observability is essential for production systems.

**Enforcement**:
- Logging required for all critical operations
- Monitoring dashboards for production
- Alerting for critical errors

---

### VII. Code Quality and Consistency

**Principle**: Code is written for humans first, machines second. Consistency matters.

**Rules**:

1. **Formatting**:
   - Python: Black, isort
   - TypeScript: Prettier
   - Consistent indentation (4 spaces for Python, 2 for TS)
   - Line length: 88 characters (Python), 100 (TypeScript)

2. **Linting**:
   - Python: Ruff, Pylint, mypy
   - TypeScript: ESLint
   - Zero linting errors allowed

3. **Naming Conventions**:
   - Python: snake_case for functions/variables, PascalCase for classes
   - TypeScript: camelCase for functions/variables, PascalCase for classes/interfaces
   - Descriptive names (no single letters except loop counters)
   - Boolean variables: is_*, has_*, can_*

4. **Code Structure**:
   - Single Responsibility Principle (SRP)
   - Don't Repeat Yourself (DRY)
   - Keep functions small (<50 lines)
   - Keep files focused (<500 lines)

5. **Type Safety**:
   - Python: Type hints everywhere
   - TypeScript: Strict mode enabled
   - No `any` types without justification

**Rationale**: Consistent, high-quality code is easier to read, maintain, and debug.

**Enforcement**:
- Pre-commit hooks for formatting/linting
- CI/CD fails on linting errors
- Code reviews enforce standards

---

### VIII. Performance and Scalability

**Principle**: Build for current needs, but design for future scale.

**Rules**:

1. **Performance Targets**:
   - API response time: <200ms (p95)
   - Database queries: <100ms (p95)
   - Page load time: <2s (p95)
   - Time to interactive: <3s

2. **Optimization Strategy**:
   - Measure before optimizing
   - Optimize critical paths first
   - Use caching strategically
   - Implement pagination for large datasets

3. **Database Performance**:
   - Index frequently queried columns
   - Use connection pooling
   - Avoid N+1 queries
   - Use database migrations (Alembic)

4. **Frontend Performance**:
   - Code splitting
   - Lazy loading
   - Image optimization
   - Minimize bundle size

**Rationale**: Performance impacts user experience and operational costs.

**Enforcement**:
- Performance testing in CI/CD
- Monitoring in production
- Performance budgets for critical paths

---

### IX. Versioning and Breaking Changes

**Principle**: Changes are versioned, and breaking changes are communicated clearly.

**Rules**:

1. **Semantic Versioning** (MAJOR.MINOR.PATCH):
   - MAJOR: Breaking changes
   - MINOR: New features (backward compatible)
   - PATCH: Bug fixes (backward compatible)

2. **API Versioning**:
   - Version in URL: `/api/v1/tasks`
   - Support N-1 versions
   - Deprecation warnings before removal
   - Migration guides for breaking changes

3. **Database Migrations**:
   - Use Alembic for schema changes
   - Reversible migrations
   - Test migrations on staging first
   - Backup before production migrations

4. **Git Workflow**:
   - Semantic commit messages
   - Feature branches
   - Pull requests for all changes
   - Squash commits before merging

**Rationale**: Versioning enables safe evolution and clear communication of changes.

**Enforcement**:
- CI/CD enforces semantic versioning
- Breaking changes require ADR
- Migration scripts required for schema changes

---

### X. Continuous Integration and Deployment

**Principle**: Automate testing, building, and deployment to reduce human error.

**Rules**:

1. **CI Pipeline**:
   - Run on every commit
   - Execute all tests
   - Check code quality (linting, formatting)
   - Security scanning
   - Build artifacts

2. **CD Pipeline**:
   - Deploy to staging automatically
   - Deploy to production manually (with approval)
   - Rollback capability
   - Blue-green or canary deployments

3. **Environments**:
   - Development: Local machines
   - Staging: Mirrors production
   - Production: Live system

4. **Quality Gates**:
   - All tests must pass
   - Code coverage ≥80%
   - No critical security vulnerabilities
   - Performance benchmarks met

**Rationale**: Automation reduces errors, speeds up delivery, and ensures consistency.

**Enforcement**:
- CI/CD required for all projects
- Failed pipelines block merges
- Production deployments require approval

---

## Phase-Specific Standards

### Phase I: Console App
- **Tech Stack**: Python 3.13+, built-in libraries only
- **Storage**: In-memory (lists/dictionaries)
- **Testing**: pytest
- **Focus**: Core CRUD operations, CLI interface

### Phase II: Full-Stack Web App
- **Backend**: FastAPI, SQLModel, Alembic, Pydantic
- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **Database**: Neon Serverless PostgreSQL 15+
- **Auth**: Better Auth with JWT
- **Testing**: pytest (backend), Jest/Vitest (frontend)

### Phase III: AI Chatbot
- **AI**: Claude API, LangChain (or similar)
- **Integration**: With Phase II backend
- **Testing**: Include AI response validation

### Phase IV: Local Kubernetes
- **Orchestration**: Minikube, Helm Charts
- **Tools**: kubectl-ai, Docker Desktop
- **Testing**: Integration tests in K8s environment

### Phase V: Cloud Deployment
- **Cloud**: AWS/GCP/Azure (TBD)
- **Monitoring**: Prometheus, Grafana
- **Testing**: Load testing, chaos engineering

---

## Architectural Constraints

### Technology Choices

1. **Backend**:
   - Python 3.13+ (for Python services)
   - FastAPI (for REST APIs)
   - SQLModel (for ORM)
   - Alembic (for migrations)

2. **Frontend**:
   - Next.js 15+ (React framework)
   - TypeScript (type safety)
   - Tailwind CSS (styling)

3. **Database**:
   - PostgreSQL 15+ (relational data)
   - Neon Serverless (managed PostgreSQL)

4. **Authentication**:
   - Better Auth (auth framework)
   - JWT (token-based auth)

5. **Testing**:
   - pytest (Python)
   - Jest/Vitest (JavaScript/TypeScript)

### Forbidden Practices

❌ **Never**:
- Commit secrets to version control
- Use `eval()` or `exec()` with user input
- Ignore errors silently
- Use `SELECT *` in production queries
- Deploy without testing
- Hardcode configuration
- Use deprecated libraries
- Skip code reviews
- Merge failing tests
- Deploy on Fridays (unless emergency)

---

## Quality Gates

### Definition of Done (DoD)

A task is complete when:

✅ All acceptance criteria met
✅ All tests pass (unit, integration, E2E)
✅ Code coverage ≥80%
✅ No linting errors
✅ Documentation updated
✅ Code reviewed and approved
✅ Security scan passed
✅ Performance benchmarks met
✅ Deployed to staging
✅ Human validation completed

### Code Review Checklist

Reviewers must verify:

- [ ] Task ID referenced in code
- [ ] Tests included and passing
- [ ] Documentation updated
- [ ] No security vulnerabilities
- [ ] Follows code quality standards
- [ ] No unnecessary complexity
- [ ] Error handling implemented
- [ ] Logging added for critical operations
- [ ] Performance acceptable
- [ ] Backward compatibility maintained (or breaking change documented)

---

## Governance

### Amendment Process

1. **Proposal**: Document proposed change with rationale
2. **Discussion**: Team reviews and discusses
3. **Approval**: Requires unanimous consent
4. **Documentation**: Update constitution and create ADR
5. **Migration**: Update existing code if needed
6. **Communication**: Announce to all stakeholders

### Conflict Resolution

**Hierarchy** (highest to lowest):
1. Constitution (this document)
2. Specification (`specs/<feature>/spec.md`)
3. Plan (`specs/<feature>/plan.md`)
4. Tasks (`specs/<feature>/tasks.md`)
5. Code

**Process**:
- If conflict arises, refer to hierarchy
- If unclear, escalate to human decision-maker
- Document resolution in ADR
- Update relevant artifacts

### Compliance

- All PRs must verify compliance with this constitution
- Violations must be corrected before merging
- Repeated violations trigger team discussion
- Constitution supersedes all other practices

### Review Cycle

- Review constitution quarterly
- Update based on lessons learned
- Archive old versions with rationale for changes

---

## Success Metrics

### Project Success

- All 5 phases completed
- All acceptance criteria met
- Test coverage ≥80%
- Zero critical security vulnerabilities
- Performance targets met
- Documentation complete
- Production deployment successful

### Code Quality

- Linting errors: 0
- Test coverage: ≥80%
- Code review approval rate: 100%
- Bug escape rate: <5%
- Mean time to resolution (MTTR): <24 hours

### Process Quality

- Spec approval time: <2 days
- PR review time: <1 day
- Deployment frequency: Daily (staging), Weekly (production)
- Change failure rate: <10%
- Rollback rate: <5%

---

## References

- **AGENTS.md**: Agent behavior and workflow
- **Hackathon Guide**: 47-page reference guide
- **Spec-KitPlus**: Spec-driven development toolkit
- **Claude Code**: Agentic development environment

---

## Appendix: Glossary

- **SDD**: Spec-Driven Development
- **TDD**: Test-Driven Development
- **ADR**: Architectural Decision Record
- **PHR**: Prompt History Record
- **YAGNI**: You Aren't Gonna Need It
- **DRY**: Don't Repeat Yourself
- **SOLID**: Single responsibility, Open-closed, Liskov substitution, Interface segregation, Dependency inversion
- **CRUD**: Create, Read, Update, Delete
- **JWT**: JSON Web Token
- **CORS**: Cross-Origin Resource Sharing
- **API**: Application Programming Interface
- **CI/CD**: Continuous Integration/Continuous Deployment
- **E2E**: End-to-End
- **ORM**: Object-Relational Mapping

---

**Version**: 1.0.0
**Ratified**: 2026-01-22
**Last Amended**: 2026-01-22
**Next Review**: 2026-04-22
**Maintained By**: Project Team
**Status**: Active

---

## Signature

This constitution has been reviewed and approved by the project team. All contributors agree to abide by these principles.

**"Spec first, code second. Quality always."**
