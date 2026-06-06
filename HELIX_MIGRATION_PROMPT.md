# Helix Migration Prompt

*Copy and paste the following prompt to your Helix coding agent to automatically migrate the Zero-Chat / Action-Only UI paradigm and Citigroup design system into your environment.*

***

We are undertaking a full UI and architectural revamp of our Copilot application. The goal is twofold: 
1. Implement a modern 'Triple-Pane' UI using precise Citigroup brand colors and the 'Overpass' font. 
2. Implement a 'Zero-Chat / Action-Only' Generative UI paradigm. The chat window must NEVER contain standard text; all text must route to the center dashboard, while the chat window is exclusively for displaying clickable follow-up buttons.

Please execute the following three steps immediately to implement this:

### Step 1: Update the Python ADK Backend
Create two new tools: `display_in_center(analysis_text: str)` and `provide_suggestions(prompts: list[str])`. Then, heavily restrict the root agent's `instructions` so it NEVER outputs standard conversational text. It MUST always route its text output to `display_in_center` and route follow-up questions to `provide_suggestions`.

**Reference Code:**
```python
from google.adk.tools import tool

@tool
def display_in_center(analysis_text: str) -> str:
    """Displays analysis text in the center dashboard. Use for all conversational text."""
    return "Displayed."

@tool
def provide_suggestions(prompts: list[str]) -> str:
    """Displays clickable follow-up prompts in the chat sidebar. Provide 2-3 suggestions."""
    return "Suggestions rendered."
```

### Step 2: Merge the Design Tokens into the Main Global Stylesheet
Carefully locate our existing global CSS file (it might be named `index.css`, `App.css`, `globals.css`, or similar). Integrate the following Citigroup CSS variables, fonts, and layout classes. Do NOT blindly overwrite the file; merge these tokens with our existing styles, ensuring the new `triple-pane-layout` and CSS variables take precedence for the main application layout:
```css
@import url('https://fonts.googleapis.com/css2?family=Overpass:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap');

:root {
  --citi-dark-navy: #0f1632;
  --citi-brand-blue: #0041a5;
  --citi-interactive-blue: #255be3;
  --citi-red: #b60000;
  --bg-primary: #f0f5f7;
  --bg-surface: #ffffff;
  --text-primary: #0f1632;
  --text-secondary: #606466;
  --border-color: #d8d8d8;
}

body {
  margin: 0;
  font-family: 'Overpass', 'Citi-Sans-Text-Regular', sans-serif;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
}

.triple-pane-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.pane-workflow {
  width: 350px;
  background: var(--bg-surface);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
}

.pane-main {
  flex: 1;
  padding: 40px;
  overflow-y: auto;
}

.pane-copilot {
  width: 400px;
  background: var(--bg-surface);
  border-left: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
}

.citi-header {
  background-color: var(--citi-dark-navy);
  color: white;
  padding: 20px;
  font-weight: 600;
  font-size: 15px;
  letter-spacing: 0.5px;
  border-bottom: 2px solid var(--citi-brand-blue);
}

/* CopilotKit overrides */
.copilotKitButton {
  background-color: var(--citi-interactive-blue) !important;
  color: white !important;
  border-radius: 4px !important;
}
```

### Step 3: Refactor the Main Copilot Dashboard Component for Action-Only UI
Carefully locate our existing main Copilot UI component (it might be `App.tsx`, `Dashboard.tsx`, `page.tsx`, or similar). Instead of overwriting the file, surgically integrate the `useCopilotAction` hooks to intercept the backend tools. 
1. Ensure `TextMessage` and `MessageRole` are imported from `@copilotkit/runtime-client-gql`.
2. Implement the `display_in_center` hook to catch text and render it in our center dashboard.
3. Implement the `provide_suggestions` hook to render clickable buttons in the Copilot chat.

Use the following prototype code as a strict reference for the logic and aesthetics you must merge into our existing application:
```tsx
"use client";
import { CopilotChat } from "@copilotkit/react-ui";
import { useCopilotAction, useCopilotChat } from "@copilotkit/react-core";
import { TextMessage, MessageRole } from "@copilotkit/runtime-client-gql";
import { useState } from "react";

export default function OperationalRiskDashboard() {
  const { appendMessage } = useCopilotChat();
  const [centerText, setCenterText] = useState("Awaiting agent analysis...");

  // 1. Intercept the display_in_center tool to update the dashboard
  useCopilotAction({
    name: "display_in_center",
    description: "Renders analysis text in the center dashboard",
    parameters: [{ name: "analysis_text", type: "string", description: "The text to display" }],
    handler: async () => {},
    render: ({ args }) => {
      if (args.analysis_text) setCenterText(args.analysis_text);
      return <div className="hidden" style={{ display: 'none' }} />;
    }
  });

  // 2. Intercept provide_suggestions tool to render clickable buttons in chat
  useCopilotAction({
    name: "provide_suggestions",
    description: "Renders clickable follow-up prompts in the chat",
    parameters: [{ name: "prompts", type: "string[]", description: "The follow up prompts" }],
    handler: async () => {},
    render: ({ args }) => {
      if (!args.prompts || args.prompts.length === 0) return <></>;
      
      return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', padding: '10px 0' }}>
          <strong style={{ fontSize: '13px', color: 'var(--citi-dark-navy)', marginBottom: '4px' }}>
            Recommended Actions:
          </strong>
          {args.prompts.map((prompt, i) => (
            <button 
              key={i}
              onClick={() => appendMessage(new TextMessage({ content: prompt, role: MessageRole.User }))}
              style={{ 
                background: 'var(--bg-surface)', 
                color: 'var(--citi-interactive-blue)',
                border: '1px solid var(--citi-brand-blue)',
                padding: '10px 14px',
                borderRadius: '6px',
                textAlign: 'left',
                cursor: 'pointer',
                fontSize: '14px',
                transition: 'background 0.2s'
              }}
              onMouseOver={(e) => e.currentTarget.style.background = '#f0f5f7'}
              onMouseOut={(e) => e.currentTarget.style.background = 'var(--bg-surface)'}
            >
              {prompt}
            </button>
          ))}
        </div>
      );
    }
  });

  return (
    <div className="triple-pane-layout">
      <div className="pane-workflow">
        <div className="citi-header">Agent Workflow Trace</div>
        <div style={{ padding: '24px', fontSize: '15px', color: 'var(--text-secondary)' }}>
          <div style={{ paddingBottom: '16px', borderBottom: '1px solid var(--border-color)', marginBottom: '16px' }}>
            <strong>[System]</strong> Backend ready for Action-Only paradigm.
          </div>
        </div>
      </div>

      <div className="pane-main">
        <h1 style={{ color: 'var(--citi-dark-navy)', borderBottom: '2px solid var(--citi-red)', paddingBottom: '12px', margin: '0 0 32px 0', fontSize: '28px', fontWeight: '600' }}>
          Citigroup Operational Risk Hub
        </h1>
        
        <div style={{ background: 'var(--citi-dark-navy)', color: 'white', padding: '24px', borderRadius: '12px', marginBottom: '32px', boxShadow: '0 4px 12px rgba(15, 22, 50, 0.1)' }}>
          <h2 style={{ margin: '0 0 12px 0', fontSize: '18px', color: '#b8c8d8' }}>Agent Insights</h2>
          <div style={{ fontSize: '16px', lineHeight: '1.6' }}>{centerText}</div>
        </div>

        <div style={{ background: 'var(--bg-surface)', padding: '32px', borderRadius: '12px', boxShadow: '0 4px 12px rgba(15, 22, 50, 0.05)', border: '1px solid var(--border-color)' }}>
          <h2 style={{ margin: '0 0 24px 0', color: 'var(--citi-dark-navy)', fontSize: '20px', fontWeight: '600' }}>Risk Metrics Overview</h2>
          <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse', fontSize: '15px' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid var(--citi-brand-blue)', color: 'var(--text-secondary)' }}>
                <th style={{ padding: '16px 12px', fontWeight: '600' }}>Risk ID</th>
                <th style={{ padding: '16px 12px', fontWeight: '600' }}>Severity</th>
                <th style={{ padding: '16px 12px', fontWeight: '600' }}>Description</th>
                <th style={{ padding: '16px 12px', fontWeight: '600', textAlign: 'right' }}>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: '16px 12px', fontWeight: '600', color: 'var(--citi-interactive-blue)' }}>RSK-001</td>
                <td style={{ padding: '16px 12px', fontWeight: '600', color: 'var(--citi-red)' }}>High</td>
                <td style={{ padding: '16px 12px' }}>Trading anomaly detected in Equities Desk</td>
                <td style={{ padding: '16px 12px', textAlign: 'right' }}><span style={{ background: '#ffebee', color: 'var(--citi-red)', padding: '4px 8px', borderRadius: '4px', fontSize: '13px', fontWeight: '600' }}>Active</span></td>
              </tr>
              <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: '16px 12px', fontWeight: '600', color: 'var(--citi-interactive-blue)' }}>RSK-002</td>
                <td style={{ padding: '16px 12px', fontWeight: '600', color: 'var(--text-primary)' }}>Medium</td>
                <td style={{ padding: '16px 12px' }}>Unusual transaction volume observed</td>
                <td style={{ padding: '16px 12px', textAlign: 'right' }}><span style={{ background: '#e3f2fd', color: 'var(--citi-brand-blue)', padding: '4px 8px', borderRadius: '4px', fontSize: '13px', fontWeight: '600' }}>Investigating</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div className="pane-copilot">
        <div className="citi-header">Risk Copilot</div>
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
          <CopilotChat labels={{ initial: "I am ready. Use the prompts below to begin." }} />
        </div>
      </div>
    </div>
  );
}
```

Please overwrite these files immediately, ensure there are no TypeScript errors, and verify that our `app/layout.tsx` is properly wrapping `{children}` inside the `<CopilotKit>` component with the correct `runtimeUrl` for our ADK backend.
***
