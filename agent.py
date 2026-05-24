import os
import uuid
from typing import Any, AsyncGenerator

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from db_helper import DuckDBHelper
from registry import AgentRegistry
from tools import export_report_to_pdf, export_report_to_pptx

class OperationalRiskCoordinator(BaseAgent):
    """The root agent orchestrating Operational Risk chapters."""
    db: Any = None
    registry: Any = None
    
    def __init__(self, name: str = "operational_risk_coordinator", **kwargs):
        super().__init__(name=name, **kwargs)
        self.db = DuckDBHelper()
        self.registry = AgentRegistry(self.db)
        
        # Load agents from config
        config_path = os.path.join(os.path.dirname(__file__), "config", "agents")
        self.registry.load_chapter_agents(config_path)

    async def _run_subagent(self, agent, ctx, prompt, output_list=None):
        
        session_service = InMemorySessionService()
        runner = Runner(agent=agent, app_name=ctx.app_name, session_service=session_service, auto_create_session=True)
        
        full_text = []
        async for event in runner.run_async(
            user_id=ctx.user_id,
            session_id=uuid.uuid4().hex,
            new_message=types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
        ):
            if event.content and event.content.role == "model" and event.content.parts:
                for p in event.content.parts:
                    if p.text:
                        full_text.append(p.text)
            yield event
            
        if output_list is not None:
            output_list.append("".join(full_text))

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        user_input = ""
        if ctx.session.events:
            for ev in reversed(ctx.session.events):
                if ev.author == "user" and ev.content and ev.content.parts:
                    texts = [p.text for p in ev.content.parts if p.text]
                    if texts:
                        user_input = "".join(texts).strip()
                        break
        
        state = ctx.session.state
        if "stage" not in state:
            state["stage"] = "start"

        if state["stage"] == "start":
            issues_agent = self.registry.agents.get("issues_agent")
            risk_metrics_agent = self.registry.agents.get("risk_metrics_agent")
            expert_analyst_agent = self.registry.agents.get("expert_analyst_agent")
            
            issues_out = []
            async for ev in self._run_subagent(issues_agent, ctx, "Summarize the latest issues.", issues_out):
                pass
                
            metrics_out = []
            async for ev in self._run_subagent(risk_metrics_agent, ctx, "Summarize the risk metrics.", metrics_out):
                pass
                
            combined_findings = f"Issues:\n{issues_out[0] if issues_out else ''}\n\nMetrics:\n{metrics_out[0] if metrics_out else ''}"
            
            draft_out = []
            async for ev in self._run_subagent(expert_analyst_agent, ctx, f"Generate a draft report based on these findings:\n\n{combined_findings}", draft_out):
                yield ev
                
            state["draft"] = draft_out[0] if draft_out else ""
            state["stage"] = "gate_1_review"
            
            yield Event(
                author=self.name,
                content=types.Content(
                    role="model",
                    parts=[types.Part.from_text(text="Type 'APPROVE' to proceed, or provide edits to revise the draft.")]
                )
            )
            return

        if state["stage"] == "gate_1_review":
            if user_input.upper() == "APPROVE":
                state["stage"] = "gate_2_challenge"
                user_input = ""
            else:
                expert_analyst_agent = self.registry.agents.get("expert_analyst_agent")
                draft = state.get("draft", "")
                prompt = f"Here is the current draft:\n{draft}\n\nThe user provided these edits: {user_input}\nPlease revise the draft."
                draft_out = []
                async for ev in self._run_subagent(expert_analyst_agent, ctx, prompt, draft_out):
                    yield ev
                state["draft"] = draft_out[0] if draft_out else ""
                yield Event(
                    author=self.name,
                    content=types.Content(
                        role="model",
                        parts=[types.Part.from_text(text="Type 'APPROVE' to proceed, or provide edits to revise the draft.")]
                    )
                )
                return

        if state["stage"] == "gate_2_challenge":
            draft = state.get("draft", "")
            reviewer_names = self.registry.reviewer_names
            current_reviewer_idx = state.get("current_reviewer_idx", 0)
            
            while current_reviewer_idx < len(reviewer_names):
                r_name = reviewer_names[current_reviewer_idx]
                reviewer_agent = self.registry.agents.get(r_name)
                
                if state.get("waiting_for_user_challenge"):
                    last_challenge_text = state.get("reviewer_comments", [])[-1] if state.get("reviewer_comments") else ""
                    prompt = f"You previously challenged this report with: {last_challenge_text}\nThe user responded: {user_input}\nHere is the draft:\n{draft}\nDo you still [CHALLENGE] or do you [APPROVE]?"
                    state["waiting_for_user_challenge"] = False
                else:
                    prompt = f"Please review this draft. If you see issues, output [CHALLENGE] and explain. Otherwise output [APPROVE].\nDraft:\n{draft}"
                
                review_out = []
                async for ev in self._run_subagent(reviewer_agent, ctx, prompt, review_out):
                    yield ev
                    
                response_text = review_out[0] if review_out else ""
                if "[CHALLENGE]" in response_text.upper():
                    state["waiting_for_user_challenge"] = True
                    comments = state.get("reviewer_comments", [])
                    comments.append(f"{r_name}: {response_text}")
                    state["reviewer_comments"] = comments
                    return 
                elif "[APPROVE]" in response_text.upper():
                    current_reviewer_idx += 1
                    state["current_reviewer_idx"] = current_reviewer_idx
                else:
                    yield Event(
                        author=self.name,
                        content=types.Content(
                            role="model",
                            parts=[types.Part.from_text(text=f"Reviewer {r_name} did not provide a valid response. Got: {response_text}. Please type 'RETRY' to try again.")]
                        )
                    )
                    return
                    
            state["stage"] = "gate_3_signoff"
            user_input = ""

        if state["stage"] == "gate_3_signoff":
            if user_input.upper() == "SIGN-OFF":
                state["stage"] = "export"
            else:
                draft = state.get("draft", "")
                comments = "\n".join(state.get("reviewer_comments", []))
                final_report = f"FINAL REPORT\n\n{draft}\n\nReviewer Comments:\n{comments}\n\nPlease reply with 'SIGN-OFF' to approve and export."
                yield Event(
                    author=self.name,
                    content=types.Content(
                        role="model",
                        parts=[types.Part.from_text(text=final_report)]
                    )
                )
                return

        if state["stage"] == "export":
            try:
                os.makedirs("reports", exist_ok=True)
                draft = state.get("draft", "")
                export_report_to_pdf(draft, "reports/risk_report.pdf")
                export_report_to_pptx(draft, "reports/risk_report.pptx")
                
                yield Event(
                    author=self.name,
                    content=types.Content(
                        role="model",
                        parts=[types.Part.from_text(text="Export complete! Saved to reports/risk_report.pdf and reports/risk_report.pptx.")]
                    )
                )
            except Exception as e:
                yield Event(
                    author=self.name,
                    content=types.Content(
                        role="model",
                        parts=[types.Part.from_text(text=f"Failed to export report: {str(e)}")]
                    )
                )
            state["stage"] = "done"
            
        if state["stage"] == "done":
            yield Event(
                author=self.name,
                content=types.Content(
                    role="model",
                    parts=[types.Part.from_text(text="The orchestration is complete. Start a new session to begin again.")]
                )
            )

# This exposes the root agent for `agents-cli playground`
agent = OperationalRiskCoordinator()
