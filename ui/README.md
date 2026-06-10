# CopilotKit ADK Reporting UI

This UI is a Citigroup-branded reporting analyst workspace for ADK agents.

## Runtime Shape

The browser points at the local Next.js CopilotKit runtime:

```text
NEXT_PUBLIC_COPILOTKIT_RUNTIME_URL=/api/copilotkit
```

The Next.js runtime proxies to the AG-UI backend:

```text
COPILOTKIT_AGENT_URL=http://127.0.0.1:8000/
```

For workplace migration, keep the UI and replace `COPILOTKIT_AGENT_URL` with
the workplace FastAPI/AG-UI endpoint.

## Brand Asset

Place the internal logo asset here when available:

```text
ui/public/brand/citi-logo.svg
```

The app shows fallback text when the logo file is absent.

## Run Locally

From the repository root:

```powershell
uv run python -m sample_backend.server
```

From `ui/`:

```powershell
npm run dev
```

Open:

```text
http://localhost:3000
```

## Verify

From `ui/`:

```powershell
npm test
npm run lint
npm run build
```

From the repository root:

```powershell
uv run pytest tests/unit
```
