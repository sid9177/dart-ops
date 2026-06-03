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
