# Ops Risk Chat UI Prompts

## Prompt 1: Master Layout & Styling

**Context & Goal:** 
Build an Enterprise-grade Chat UI with a split-screen Workspace layout (Chat on the left, Universal Artifact Viewer on the right). 
This must be built using pure HTML, CSS, and Vanilla JS (NO React, NO npm, NO build tools). The styling must be extremely premium, matching Citigroup's enterprise aesthetic.

**Instructions:**
1. **Create Base Files:**
   Create `index.html` and `style.css`. Link the CSS file in the HTML. Include a basic skeleton in `index.html`.

2. **Styling & Theme (Citigroup Enterprise Style):**
   - **Primary Color:** Citigroup Blue `#002D72`. Use this for headers, primary buttons, and key accents.
   - **Backgrounds:** Use an ultra-light gray/off-white background for the overall app (e.g., `#f4f5f7`) to keep it clean and professional.
   - **Typography:** Use a modern, clean sans-serif font (e.g., 'Inter', 'Segoe UI', or 'Roboto').
   - **Premium Effects:** Use subtle glassmorphism (translucency + background blur) where appropriate, and soft, premium drop-shadows (e.g., `box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);`) to separate panels and give depth. The UI must feel state-of-the-art, not flat or basic.

3. **Layout Structure (Flexbox):**
   - **Top Brand Bar:** A header spanning 100% width. It should feature the brand color `#002D72`, white text, and a title like "Ops Risk Assistant". Give it a premium shadow.
   - **Main Workspace:** Below the brand bar, split the screen vertically using Flexbox (`display: flex; height: calc(100vh - headerHeight);`).
   - **Left Panel (Chat):** 35% width. This will hold the chat interface (messages area and input box). Give it a clean white background with a subtle right border separating it from the right panel.
   - **Right Panel (Artifact Viewer):** 65% width. This is a universal workspace for displaying documents, data tables, or charts. It should contain a distinct, card-like container with rounded corners and a soft shadow, placed on a slightly darker background to make it the clear focal point.
   - Ensure the layout is strictly full-height (`100vh`) without page-level scrolling. Only the internal panels (like chat history or artifact content) should have `overflow-y: auto`.

**Acceptance Criteria:**
- `index.html` and `style.css` are created and linked.
- The UI features a top header and a strict 35/65 flexbox split.
- The design looks enterprise-ready, premium, and utilizes the `#002D72` color.
- The layout fills the screen without body scrolling.

## Prompt 2: The Chat Engine

**Context & Goal:**
Now that the master layout is complete, implement the chat logic and DOM rendering using Vanilla JS. The chat must look premium, handle user inputs, and auto-scroll properly.

**Instructions:**
1. **Create Base File:**
   Create `script.js` and ensure it is linked in `index.html`. If not already present, add the necessary HTML structural tags inside the Left Panel for a messages container, an input box, and a send button.
   
2. **State Management:**
   - Create a JavaScript array to hold chat messages. Each message should be an object with `role` (e.g., 'user', 'agent') and `content` (the text string).

3. **Rendering the Chat:**
   - Write a function that reads the messages array and renders them into the Left Panel's DOM.
   - **Styling the Bubbles:** Render the messages as premium-looking chat bubbles. 
     - **User Messages:** Align right, use a distinct premium color (e.g., a solid Citigroup Blue `#002D72` background with white text), and soft shadows.
     - **Agent Messages:** Align left, use a clean off-white or light gray background (e.g., `#f4f5f7` or white) with dark text, and soft shadows. Include a specific CSS animation (e.g. fade-in and slide-up) for new messages.
   - **Auto-Scrolling:** Ensure the chat container automatically scrolls to the bottom every time a new message is added or rendered.
   - **Mock Agent Response:** Generate a mock agent response (e.g., using `setTimeout` or prepopulating the state array) to verify the 'Agent Messages' styling.

4. **Event Handling:**
   - Add event listeners to the chat input area.
   - Ensure the user can send a message by pressing the `Enter` key.
   - Clear the input field after the message is submitted.

**Acceptance Criteria:**
- `script.js` is created and linked in `index.html`.
- A data structure (array) successfully stores message objects (role + content).
- A rendering function displays these messages as visually distinct, premium chat bubbles (User vs. Agent) with a fade-in and slide-up animation.
- A mock agent response is generated to verify agent styling.
- The chat container auto-scrolls to the bottom upon receiving a new message.
- Pressing `Enter` in the input field successfully sends the message and clears the input field.

## Prompt 3: Universal Artifact Renderer

**Context & Goal:**
We need to enhance the right panel (Artifact Viewer) to dynamically render complex content generated by the agent. The agent will output artifacts enclosed in XML-style tags, which should not be shown as raw text in the chat bubble. Instead, they should appear as clickable chips that render the content into the main workspace.

**Instructions:**
1. **Detecting Artifacts:**
   - Update the chat message rendering logic in `script.js` to detect XML-style blocks within an agent's response, specifically `<artifact type="markdown">`, `<artifact type="mermaid">`, or `<artifact type="data-grid">`.
   - The `<artifact>` tags will wrap the content (e.g., `<artifact type="markdown"># Hello</artifact>`).

2. **Rendering Artifact Chips in Chat:**
   - When an artifact is detected, do NOT render the raw markdown or code inside the chat bubble.
   - Instead, render a premium, clickable UI chip/button in the chat bubble (e.g., "View Artifact: [Type]").
   - The chip should be styled clearly as an interactive element (e.g., matching the Citi-blue theme with an icon, hover state, and soft shadow).

3. **External Dependencies (CDNs):**
   - Inject the necessary CDNs into `index.html` to handle rendering:
     - `marked.js` for markdown parsing (e.g., `https://cdn.jsdelivr.net/npm/marked/marked.min.js`).
     - `mermaid.min.js` for rendering flowcharts (e.g., `https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js`).

4. **Dynamic Right Panel Rendering:**
   - Implement JavaScript logic so that when an artifact chip is clicked, the corresponding content is rendered into the Right Panel (Artifact Viewer).
   - **Markdown (`type="markdown"`):** Parse the text inside the artifact using `marked` and display the resulting HTML.
   - **Mermaid (`type="mermaid"`):** Render the flowchart using the `mermaid.js` library.
   - **Data Grid (`type="data-grid"`):** 
     - The content inside the tag will be a JSON array of objects. 
     - Parse the JSON data and build a basic HTML table dynamically.
     - Apply Citi-styled CSS to the table (e.g., alternating row colors, bold Citigroup Blue `#002D72` headers, crisp borders).

**Acceptance Criteria:**
- CDNs for `marked.js` and `mermaid.min.js` are properly injected into `index.html`.
- Agent chat bubbles correctly parse XML-style `<artifact>` tags and display interactive chips instead of raw artifact text.
- Clicking an artifact chip successfully renders the content into the Right Panel.
- Markdown artifacts render as formatted HTML.
- Mermaid artifacts render as SVG flowcharts.
- Data Grid artifacts parse JSON and render as a dynamically styled HTML table with Citi-styled CSS (alternating rows, bold headers).
