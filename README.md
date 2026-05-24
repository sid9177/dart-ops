# dart-ops


Agent generated with `agents-cli` version `0.2.0`

## Project Structure

```
dart-ops/
├── agent.py                   # Main coordinator agent (entry point)
├── registry.py                # Agent registry - loads YAML configs & DuckDB tools
├── db_helper.py               # DuckDB database helper (CSV/Excel → SQL)
├── tools.py                   # Python execution, PDF & PPTX export tools
├── config/
│   ├── agents/                # Chapter agent configurations (YAML)
│   │   ├── issues.yaml
│   │   ├── risk_metrics.yaml
│   │   └── expert_analyst.yaml
│   └── reviewers/             # LOD reviewer configurations (YAML)
│       └── second_lod.yaml
├── data/                      # Data files (CSV/Excel) loaded into DuckDB
│   ├── issues.csv
│   └── risk_metrics.csv
├── dart_ops/                  # Package for deployment (FastAPI app & utilities)
│   ├── fast_api_app.py
│   └── app_utils/
├── reports/                   # Generated PDF/PPTX reports (output)
├── tests/                     # Unit and integration tests
├── GEMINI.md                  # AI-assisted development guide
└── pyproject.toml             # Project dependencies
```

> 💡 **Tip:** Use [Gemini CLI](https://github.com/google-gemini/gemini-cli) for AI-assisted development - project context is pre-configured in `GEMINI.md`.

## Requirements

Before you begin, ensure you have:
- **uv**: Python package manager (used for all dependency management in this project) - [Install](https://docs.astral.sh/uv/getting-started/installation/) ([add packages](https://docs.astral.sh/uv/concepts/dependencies/) with `uv add <package>`)
- **agents-cli**: Agents CLI - Install with `uv tool install google-agents-cli`
- **Google Cloud SDK**: For GCP services - [Install](https://cloud.google.com/sdk/docs/install)


## Quick Start

Install `agents-cli` and its skills if not already installed:

```bash
uvx google-agents-cli setup
```

Install required packages:

```bash
agents-cli install
```

Test the agent with a local web server:

```bash
agents-cli playground
```

You can also use features from the [ADK](https://adk.dev/) CLI with `uv run adk`.

## Commands

| Command              | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `agents-cli install` | Install dependencies using uv                                                         |
| `agents-cli playground` | Launch local development environment                                                  |
| `agents-cli lint`    | Run code quality checks                                                               |
| `uv run pytest tests/unit tests/integration` | Run unit and integration tests                                                        |

## 🛠️ Project Management

| Command | What It Does |
|---------|--------------|
| `agents-cli scaffold enhance` | Add CI/CD pipelines and Terraform infrastructure |
| `agents-cli infra cicd` | One-command setup of entire CI/CD pipeline + infrastructure |
| `agents-cli scaffold upgrade` | Auto-upgrade to latest version while preserving customizations |

---

## Development

Edit your agent logic in `agent.py` (project root) and test with `agents-cli playground` - it auto-reloads on save.

## Working with Data (CSV & Excel)

This project uses an in-memory database (DuckDB) to load and query data instantly. 

To use your own custom data:
1. **Place your data files**: Copy your `.csv`, `.xlsx`, or `.xls` files into the `data/` directory.
2. **Update Agent Configurations**: Open the corresponding YAML files in `config/agents/` (e.g., `issues.yaml` or `risk_metrics.yaml`).
3. **Point to your file**: Change the `file_path` property to point to your new file.
   ```yaml
   # Example for Excel
   file_path: "data/my_custom_data.xlsx"
   database_table: "my_table_name"
   ```
4. **Install Export Dependencies (optional)**: To enable Excel support and PDF/PPTX export:
   ```bash
   uv sync --extra export
   ```
   
The `AgentRegistry` will automatically load your specified files into DuckDB when the agent starts!

## Deployment

```bash
gcloud config set project <your-project-id>
agents-cli deploy
```

To add CI/CD and Terraform, run `agents-cli scaffold enhance`.
To set up your production infrastructure, run `agents-cli infra cicd`.

## Observability

Built-in telemetry exports to Cloud Trace, BigQuery, and Cloud Logging.
