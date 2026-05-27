from google.adk.agents import Agent
from google.adk.tools import AgentTool
from app.helix_agent.tools import generate_pdf_report, generate_ppt_report

reporter = Agent(
    name="reporter",
    model="gemini-2.5-flash",
    description="Generates final compliance reports in PDF and PPTX formats",
    instruction="You are the Final Reporting Agent. Your job is to take the final assessments from other agents and format them into Citi-branded PDF or PPTX reports. \nWhen a user asks for a report, use the available tools to generate it and provide them with the path to the generated file.\nThe available designs are: \"executive_summary\".\n",
    tools=[generate_pdf_report, generate_ppt_report]
)
reporter_tool = AgentTool(reporter)
