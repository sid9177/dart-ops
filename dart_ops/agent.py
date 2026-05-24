import os
import re
from typing import AsyncGenerator
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from registry import AgentRegistry
from tools import execute_python_code, export_report_to_pdf, export_report_to_pptx

class OperationalRiskCoordinator(BaseAgent):
    def __init__(self, name="coordinator_agent", description="Citi Operational Risk Coordinator"):
        super().__init__(name=name, description=description)
        # Initialize registry as a private attribute to avoid Pydantic field validation
        self._registry = AgentRegistry(config_dir="config")
        self._registry.load_configs()
        
    def _make_event(self, text: str, state_delta: dict = None) -> Event:
        from google.genai import types
        from google.adk.events.event_actions import EventActions
        actions = EventActions(state_delta=state_delta) if state_delta else EventActions()
        return Event(
            author=self.name,
            content=types.Content(
                role="model",
                parts=[types.Part.from_text(text=text)]
            ),
            actions=actions
        )

    async def _run_subagent(self, agent, ctx: InvocationContext, prompt: str) -> str:
        import asyncio
        from google.adk.runners import Runner
        from google.genai import types
        
        temp_session_id = f"{ctx.session.id}_sub_{agent.name}"
        
        # Ensure temporary session exists
        try:
            await ctx.session_service.create_session(
                app_name=ctx.session.app_name,
                user_id=ctx.session.user_id,
                session_id=temp_session_id
            )
        except Exception:
            pass
            
        sub_runner = Runner(
            agent=agent,
            app_name=ctx.session.app_name,
            session_service=ctx.session_service
        )
        
        new_msg = types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        )
        
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                response_text = ""
                async for event in sub_runner.run_async(
                    user_id=ctx.session.user_id,
                    session_id=temp_session_id,
                    new_message=new_msg
                ):
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if part.text:
                                response_text += part.text
                return response_text
            except Exception as e:
                err_msg = str(e)
                if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg or "quota" in err_msg.lower():
                    # Parse retry delay if possible, or use exponential backoff
                    delay = 2 ** attempt + 5
                    match = re.search(r"retry in ([\d\.]+)s", err_msg)
                    if match:
                        try:
                            delay = float(match.group(1)) + 1.0
                        except ValueError:
                            pass
                    print(f"Rate limit hit. Retrying subagent {agent.name} call in {delay:.2f} seconds (attempt {attempt + 1}/{max_attempts})... Error: {err_msg}")
                    await asyncio.sleep(delay)
                else:
                    raise
        raise Exception(f"Failed to run subagent {agent.name} after {max_attempts} attempts due to rate limits.")
        
    def _get_agent(self, name: str):
        if name not in self._registry.agents:
            from google.adk.agents import Agent
            # Dynamic fallback creation
            self._registry.agents[name] = Agent(
                name=name,
                model="gemini-2.5-flash",
                instruction=f"You are the default {name}.",
                description=f"Fallback agent {name}."
            )
        return self._registry.agents[name]

    def _is_challenge(self, text: str) -> bool:
        if "[CHALLENGE]" in text or "[GATE 2]" in text:
            return True
        text_lower = text.lower()
        if "challenge" in text_lower:
            if "no challenge" in text_lower or "without challenge" in text_lower or "no-challenge" in text_lower:
                return False
            return True
        return False

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        state = ctx.session.state
        
        # Get the latest message from user
        user_message = ""
        if ctx.session.events:
            # Locate the last user event
            for ev in reversed(ctx.session.events):
                if ev.author == "user" and ev.content and ev.content.parts:
                    texts = [p.text for p in ev.content.parts if p.text]
                    if texts:
                        user_message = "".join(texts).strip()
                        break
        
        stage = state.get("stage", "start")
        
        if stage == "start":
            yield self._make_event("Initializing report generation...")
            
            # Step 1: Run chapter agents
            issues_agent = self._get_agent("issues_agent")
            metrics_agent = self._get_agent("risk_metrics_agent")
            
            issues_result = await self._run_subagent(issues_agent, ctx, "Analyze high severity open issues in issues table")
            metrics_result = await self._run_subagent(metrics_agent, ctx, "Analyze Amber or Red metrics in risk_metrics table")
            
            # Step 2: Run expert analyst
            expert_analyst_agent = self._get_agent("expert_analyst_agent")
            analyst_prompt = f"Synthesize a draft risk report using the following findings:\n\nIssues:\n{issues_result}\n\nMetrics:\n{metrics_result}"
            draft = await self._run_subagent(expert_analyst_agent, ctx, analyst_prompt)
            
            state["draft_report"] = draft
            state["stage"] = "gate_1_review"
            state["satisfied_reviewers"] = []
            state["reviewer_comments"] = {}
            
            yield self._make_event(
                f"### DRAFT REPORT FOR REVIEW\n\n{draft}\n\n---\n**Gate 1 (Draft Review)**: Please review the draft above. Type 'APPROVE' to proceed to LOD review, or enter your edits/feedback to revise it.",
                state_delta={
                    "stage": "gate_1_review",
                    "draft_report": draft,
                    "satisfied_reviewers": [],
                    "reviewer_comments": {}
                }
            )
            
        elif stage == "gate_1_review":
            if user_message.upper() == "APPROVE":
                yield self._make_event("Draft approved! Starting Lines of Defense (LOD) reviews...")
                
                draft = state["draft_report"]
                reviewer_names = self._registry.reviewer_names
                if not reviewer_names:
                    # If there are no reviewer configs, default to second_lod_agent
                    reviewer_names = ["second_lod_agent"]
                
                state.setdefault("satisfied_reviewers", [])
                state.setdefault("reviewer_comments", {})
                
                all_clear = True
                for r_name in reviewer_names:
                    if r_name in state["satisfied_reviewers"]:
                        continue
                    
                    reviewer = self._get_agent(r_name)
                    review_result = await self._run_subagent(reviewer, ctx, f"Review this draft report:\n{draft}")
                    
                    if self._is_challenge(review_result):
                        state["active_reviewer"] = r_name
                        state["pending_reviewer"] = r_name  # Support both keys
                        state["pending_challenge"] = review_result
                        state["stage"] = "gate_2_challenge"
                        all_clear = False
                        yield self._make_event(
                            f"{r_name} raised a challenge: {review_result}\n\nWhat is your response?",
                            state_delta={
                                "stage": "gate_2_challenge",
                                "active_reviewer": r_name,
                                "pending_reviewer": r_name,
                                "pending_challenge": review_result,
                                "satisfied_reviewers": state["satisfied_reviewers"],
                                "reviewer_comments": state["reviewer_comments"]
                            }
                        )
                        break
                    else:
                        state["satisfied_reviewers"].append(r_name)
                        state["reviewer_comments"][r_name] = review_result
                
                if all_clear:
                    # All reviewers satisfied
                    comments_section = ""
                    for name, comment in state["reviewer_comments"].items():
                        comments_section += f"\n\n### {name} Review Comments\n\n{comment}"
                    
                    state["final_report"] = f"{draft}\n\n### LOD Review Comments{comments_section}"
                    state["stage"] = "gate_3_signoff"
                    yield self._make_event(
                        f"### FINAL REPORT FOR SIGN-OFF\n\n{state['final_report']}\n\n---\n**Gate 3 (Final Sign-off)**: Type 'SIGN-OFF' to approve and save, or 'REVISE' to restart.",
                        state_delta={
                            "stage": "gate_3_signoff",
                            "final_report": state["final_report"],
                            "satisfied_reviewers": state["satisfied_reviewers"],
                            "reviewer_comments": state["reviewer_comments"]
                        }
                    )
            else:
                # Revise draft using user edits
                draft = state["draft_report"]
                expert_analyst_agent = self._get_agent("expert_analyst_agent")
                revision_prompt = f"Revise this draft report:\n{draft}\n\nBased on these user edits:\n{user_message}"
                new_draft = await self._run_subagent(expert_analyst_agent, ctx, revision_prompt)
                state["draft_report"] = new_draft
                yield self._make_event(
                    f"### UPDATED DRAFT REPORT\n\n{new_draft}\n\n---\n**Gate 1 (Draft Review)**: Please review the revised draft. Type 'APPROVE' to proceed, or enter more edits.",
                    state_delta={
                        "draft_report": new_draft
                    }
                )
                
        elif stage == "gate_2_challenge":
            reviewer_name = state.get("active_reviewer") or state.get("pending_reviewer")
            if not reviewer_name:
                reviewer_names = self._registry.reviewer_names
                reviewer_name = reviewer_names[0] if reviewer_names else "second_lod_agent"
                
            reviewer = self._get_agent(reviewer_name)
            draft = state["draft_report"]
            
            re_eval_prompt = f"Draft report:\n{draft}\n\nYour previous challenge: {state.get('pending_challenge', '')}\n\nUser response: {user_message}"
            new_review = await self._run_subagent(reviewer, ctx, re_eval_prompt)
            
            if self._is_challenge(new_review):
                state["pending_challenge"] = new_review
                yield self._make_event(
                    f"### REVIEWER CHALLENGE REMAINS UNRESOLVED\n\n{new_review}\n\n---\n**Gate 2 (LOD Challenge)**: Please provide an alternative or updated response.",
                    state_delta={
                        "pending_challenge": new_review
                    }
                )
            else:
                yield self._make_event("LOD Challenge successfully resolved!")
                state.setdefault("satisfied_reviewers", []).append(reviewer_name)
                state.setdefault("reviewer_comments", {})[reviewer_name] = new_review
                
                # Clear active reviewer challenge
                state.pop("active_reviewer", None)
                state.pop("pending_reviewer", None)
                state.pop("pending_challenge", None)
                
                # Resume reviewer loop
                reviewer_names = self._registry.reviewer_names
                if not reviewer_names:
                    reviewer_names = ["second_lod_agent"]
                    
                all_clear = True
                for r_name in reviewer_names:
                    if r_name in state["satisfied_reviewers"]:
                        continue
                    
                    reviewer = self._get_agent(r_name)
                    review_result = await self._run_subagent(reviewer, ctx, f"Review this draft report:\n{draft}")
                    
                    if self._is_challenge(review_result):
                        state["active_reviewer"] = r_name
                        state["pending_reviewer"] = r_name
                        state["pending_challenge"] = review_result
                        state["stage"] = "gate_2_challenge"
                        all_clear = False
                        yield self._make_event(
                            f"{r_name} raised a challenge: {review_result}\n\nWhat is your response?",
                            state_delta={
                                "stage": "gate_2_challenge",
                                "active_reviewer": r_name,
                                "pending_reviewer": r_name,
                                "pending_challenge": review_result,
                                "satisfied_reviewers": state["satisfied_reviewers"],
                                "reviewer_comments": state["reviewer_comments"]
                            }
                        )
                        break
                    else:
                        state["satisfied_reviewers"].append(r_name)
                        state["reviewer_comments"][r_name] = review_result
                
                if all_clear:
                    comments_section = ""
                    for name, comment in state["reviewer_comments"].items():
                        comments_section += f"\n\n### {name} Review Comments\n\n{comment}"
                        
                    state["final_report"] = f"{draft}\n\n### LOD Review Comments{comments_section}"
                    state["stage"] = "gate_3_signoff"
                    yield self._make_event(
                        f"### FINAL REPORT FOR SIGN-OFF\n\n{state['final_report']}\n\n---\n**Gate 3 (Final Sign-off)**: Type 'SIGN-OFF' to approve and save, or 'REVISE' to restart.",
                        state_delta={
                            "stage": "gate_3_signoff",
                            "final_report": state["final_report"],
                            "satisfied_reviewers": state["satisfied_reviewers"],
                            "reviewer_comments": state["reviewer_comments"],
                            "active_reviewer": None,
                            "pending_reviewer": None,
                            "pending_challenge": None
                        }
                    )
                    
        elif stage == "gate_3_signoff":
            if user_message.upper() == "SIGN-OFF":
                os.makedirs("reports", exist_ok=True)
                pdf_path = "reports/risk_report.pdf"
                pptx_path = "reports/risk_report.pptx"
                
                export_report_to_pdf(state["final_report"], pdf_path)
                export_report_to_pptx(state["final_report"], pptx_path)
                
                yield self._make_event(
                    f"Report signed off and saved to reports/risk_report.pdf and reports/risk_report.pptx!\n\n"
                    f"✅ **Report successfully signed off!**\n"
                    f"- Saved to: [reports/risk_report.pdf](file:///{os.path.abspath(pdf_path)})\n"
                    f"- Saved to: [reports/risk_report.pptx](file:///{os.path.abspath(pptx_path)})",
                    state_delta={
                        "stage": None,
                        "draft_report": None,
                        "final_report": None,
                        "satisfied_reviewers": None,
                        "reviewer_comments": None,
                        "active_reviewer": None,
                        "pending_reviewer": None,
                        "pending_challenge": None
                    }
                )
            elif user_message.upper() == "REVISE":
                state["stage"] = "start"
                yield self._make_event(
                    "Resetting process. Type any query to start generating a new report.",
                    state_delta={
                        "stage": "start",
                        "draft_report": None,
                        "final_report": None,
                        "satisfied_reviewers": None,
                        "reviewer_comments": None,
                        "active_reviewer": None,
                        "pending_reviewer": None,
                        "pending_challenge": None
                    }
                )
            else:
                yield self._make_event("Invalid input. Please type 'SIGN-OFF' to save or 'REVISE' to restart.")

# Boot the root coordinator
root_agent = OperationalRiskCoordinator()

from google.adk.apps import App

app = App(root_agent=root_agent, name="dart_ops")
