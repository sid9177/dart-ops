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
