from __future__ import annotations

from pathlib import Path
from typing import Any

import uvicorn
import yaml
from ag_ui_adk import ADKAgent, AGUIToolset, add_adk_fastapi_endpoint
from fastapi import FastAPI
from google.adk.agents import LlmAgent

from sample_backend.demo_data import build_demo_artifacts, build_demo_statuses

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config" / "reporting_agent.yaml"
PROMPT_PATH = ROOT / "prompts" / "reporting_agent.md"


def load_agent_config() -> dict[str, Any]:
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


def load_agent_prompt() -> str:
    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    statuses = build_demo_statuses()
    artifacts = build_demo_artifacts()
    return (
        prompt
        + "\n\nUse these deterministic sample status payloads when demonstrating "
        + f"activity trace updates:\n{statuses}\n\n"
        + "Use these deterministic sample artifact payloads when demonstrating "
        + f"the reporting workspace:\n{artifacts}\n"
    )


def create_root_agent() -> LlmAgent:
    config = load_agent_config()
    return LlmAgent(
        name=config["name"],
        model=config["model"],
        instruction=load_agent_prompt(),
        tools=[AGUIToolset()],
    )


def create_app() -> FastAPI:
    config = load_agent_config()
    root_agent = create_root_agent()
    adk_agent = ADKAgent(
        adk_agent=root_agent,
        app_name=config["app_name"],
        user_id=config["user_id"],
        session_timeout_seconds=3600,
        use_in_memory_services=True,
    )

    app = FastAPI(title="Sample Ops Risk Reporting AG-UI Backend")
    add_adk_fastapi_endpoint(app, adk_agent, path="/")
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("sample_backend.server:app", host="127.0.0.1", port=8000, reload=True)
