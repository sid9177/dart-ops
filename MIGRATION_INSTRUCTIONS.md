# Helix Migration Instructions

Because your Helix environment has drifted from this staging repository, **do not perform a 1:1 copy of the files.** Instead, manually apply the following structural and logical updates to your environment to sync the new capabilities without overwriting your custom logic.

## 1. Tools Architecture Refactor
We shifted away from a monolithic `tools.py` file to a scalable `tools/` package.

**What you need to do:**
1. Create a `tools/` directory inside your agent app folder.
2. Split your existing tools into domain-specific files (e.g., `duckdb_tool.py` for database queries, `report_tool.py` for PPTX/PDF generation).
3. Create a `tools/__init__.py` file to re-export your tools and maintain your `REGISTRY` map. For example:
   ```python
   from .duckdb_tool import execute_duckdb_query
   from .report_tool import generate_pdf_report, generate_ppt_report

   REGISTRY = {
       "execute_duckdb_query": execute_duckdb_query,
       "generate_pdf_report": generate_pdf_report,
       "generate_ppt_report": generate_ppt_report,
   }
   ```
4. Delete your old monolithic `tools.py` file and verify all agent imports point to the new package (e.g., `from app.helix_agent.tools import execute_duckdb_query`).

## 2. Removal of Dynamic Skill Reading
We determined that agents dynamically scanning the filesystem for their instructions (`list_skills`, `read_skill`) is an anti-pattern. Context should be injected directly into the agent's prompts.

**What you need to do:**
1. **Delete Tool Implementations**: Remove `list_skills`, `read_skill`, and `get_skills_dir` from your tools entirely.
2. **Update Agent Tool Lists**: Go into your agent definitions (specifically the orchestrator and any chapter agents like `issues_chapter`) and remove the skill reading tools from their `tools=[...]` array.
3. **Update Agent Instructions**: Edit the `instruction` or `system_prompt` for these agents. Remove any text that instructs the agent to "use list_skills to consult guidelines" or "read skills from the filesystem."
4. **Shift to Injection**: Instead of the agent fetching skills at runtime, ensure your application logic injects the contents of those markdown guidelines directly into the agent's instruction string when initializing the agent.

## 3. Dependency Updates
Ensure your environment's `pyproject.toml` or `requirements.txt` matches any new dependencies required by the decoupled tools.
- Verify `duckdb`, `pandas`, `xhtml2pdf`, `jinja2`, and `python-pptx` are installed.

## 4. Critical Edge Cases
- **DuckDB Pathing**: If your agents use relative paths (like `data/issues.csv`) in their instructions, ensure the DuckDB tool is aware of the exact working directory your Helix application boots from to prevent file-not-found crashes.

## 5. Lightweight Observability Plugin
We added native ADK observability to provide clean terminal output showing agent handoffs, tool usage, and LLM reasoning without massive data dumps.

**What you need to do:**
1. **Create the Plugin**: Add a `plugins.py` file to your agent directory containing a custom `LightweightObservabilityPlugin` class that inherits from `google.adk.plugins.base_plugin.BasePlugin`.
2. **Implement Callbacks**: In your custom plugin, override `before_agent_callback`, `before_tool_callback`, and `after_model_callback` to print concise logs (e.g., `print(f"[OBSERVABILITY] Agent '{callback_context.agent_name}' taken over")`). Ensure you gracefully handle missing attributes since the context models may occasionally lack them.
3. **Register the Plugin**: In your main application file (e.g., `agent.py`), import your new plugin and pass it to the `App` configuration:
   ```python
   from .plugins import LightweightObservabilityPlugin

   app = App(
       name="OpsDART",
       root_agent=root_agent,
       plugins=[LightweightObservabilityPlugin()]
   )
   ```
