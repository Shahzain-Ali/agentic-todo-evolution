Language:Reply me always in roman urdu
@AGENTS.md

## Security Rules (MANDATORY)
- **NEVER** read, open, or display contents of `.env`, `.env.local`, `.env.prod`, or any file containing real secrets
- **NEVER** display secret values (API keys, passwords, tokens, database credentials) in output
- **ONLY** refer to `.env.example` files for environment variable structure
- **NEVER** hardcode secrets, API keys, passwords, or database URLs as fallback defaults in code
- **ALWAYS** use `os.getenv()` without insecure fallback values for sensitive config
- **NEVER** commit `.mcp.json`, `.claude/settings.local.json`, or credential files
- **ALWAYS** check `.gitignore` before committing new config files