"use client";

import { CopilotChat, useDefaultRenderTool } from "@copilotkit/react-core/v2";

const starterPrompts = [
  "Summarize the top operational risks.",
  "Draft an executive risk report.",
  "Compare issue trends by business unit.",
  "Generate a report outline from the latest metrics.",
];

export function ChatPanel() {
  useDefaultRenderTool();

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <p className="eyebrow dark">Copilot</p>
        <h2>Risk Reporting Assistant</h2>
      </div>
      <div className="starter-prompts">
        {starterPrompts.map((prompt) => (
          <button key={prompt} type="button">
            {prompt}
          </button>
        ))}
      </div>
      <div className="chat-frame">
        <CopilotChat
          agentId="ops-risk-reporting"
          labels={{
            welcomeMessageText:
              "Ask for analysis, report drafts, data tables, charts, or file links.",
          }}
        />
      </div>
    </div>
  );
}
