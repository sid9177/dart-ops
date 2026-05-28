# Citigroup Branded Reporting Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement Citigroup-branded PDF and PPTX report generation tools for the reporter agent.

**Architecture:** We use `python-pptx` to populate placeholder-based `.pptx` templates, and `Jinja2` + `xhtml2pdf` to convert HTML templates to PDFs. Templates are loaded dynamically from a `data/designs` directory.

**Tech Stack:** Python, python-pptx, xhtml2pdf, Jinja2, YAML.

---

## User Review Required
Please review the task breakdown below. Do the tool implementations and template mechanisms align with your expectations for the Citigroup reporting requirements?

## Proposed Changes

### Configuration
#### [MODIFY] pyproject.toml
Add `xhtml2pdf` and `Jinja2` to the dependencies list (since `python-pptx` is already present).

### Templates
#### [NEW] data/designs/executive_summary/template.html
#### [NEW] data/designs/executive_summary/template.pptx

### Core Implementation
#### [MODIFY] app/helix_agent/tools.py
Implement `generate_pdf_report` and `generate_ppt_report`.

#### [MODIFY] app/helix_agent/sub_agents/reporter.yaml
Add the new tools to the tools list and update the instructions.

---

### Task 1: Setup Dependencies

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Add dependencies**
Update `pyproject.toml` to include `xhtml2pdf` and `jinja2` under the `dependencies` list.

```toml
    "python-pptx>=1.0.2",
    "xhtml2pdf>=0.2.16",
    "jinja2>=3.1.4",
```

- [ ] **Step 2: Install dependencies**
Run: `uv sync`
Expected: Successfully installs new packages.

- [ ] **Step 3: Commit**
```bash
git add pyproject.toml uv.lock
git commit -m "build: add xhtml2pdf and jinja2 dependencies"
```

### Task 2: Create Template Directory Structure

**Files:**
- Create: `data/designs/executive_summary/template.html`
- Create: `data/designs/executive_summary/template.pptx`

- [ ] **Step 1: Create directories**
Run: `mkdir -p data/designs/executive_summary`

- [ ] **Step 2: Create HTML Template**
Create `data/designs/executive_summary/template.html` with basic Citi styling and Jinja variables:

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        @page { size: letter; margin: 2cm; }
        body { font-family: sans-serif; color: #333; }
        h1 { color: #003B70; } /* Citi Blue */
        .header-line { border-top: 4px solid #D11242; } /* Citi Red */
        .content { margin-top: 20px; }
    </style>
</head>
<body>
    <div class="header-line"></div>
    <h1>{{ title }}</h1>
    <p><strong>Date:</strong> {{ date }}</p>
    <div class="content">
        {{ body }}
    </div>
</body>
</html>
```

- [ ] **Step 3: Create base PPTX**
We need a base `.pptx` file. To do this programmatically for testing, run a quick Python script to generate an empty one.
Create and run `scripts/generate_base_pptx.py`:

```python
from pptx import Presentation
prs = Presentation()
title_slide_layout = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = "Citi Title Placeholder"
subtitle.text = "Citi Subtitle Placeholder"
prs.save("data/designs/executive_summary/template.pptx")
```
Run `uv run python scripts/generate_base_pptx.py`
Expected: File `data/designs/executive_summary/template.pptx` created.

- [ ] **Step 4: Commit**
```bash
git add data/designs/ scripts/
git commit -m "feat: add base reporting templates"
```

### Task 3: Implement Generation Tools

**Files:**
- Modify: `app/helix_agent/tools.py`

- [ ] **Step 1: Write `generate_pdf_report` tool**
In `app/helix_agent/tools.py`, add imports and the function:

```python
import os
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa

def generate_pdf_report(design_name: str, report_data: dict, output_filename: str) -> str:
    """Generates a PDF report using HTML templates."""
    template_dir = os.path.join("data", "designs", design_name)
    if not os.path.exists(template_dir):
        return f"Error: Design '{design_name}' not found."
        
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("template.html")
    html_content = template.render(**report_data)
    
    output_path = os.path.join("files", f"{output_filename}.pdf")
    os.makedirs("files", exist_ok=True)
    
    with open(output_path, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(html_content, dest=result_file)
        
    if pisa_status.err:
        return "Error: Failed to generate PDF."
    return f"Successfully generated PDF at {output_path}"
```

- [ ] **Step 2: Write `generate_ppt_report` tool**
In `app/helix_agent/tools.py`, add the PPTX function:

```python
from pptx import Presentation

def generate_ppt_report(design_name: str, report_data: dict, output_filename: str) -> str:
    """Generates a PPTX report using a template."""
    template_path = os.path.join("data", "designs", design_name, "template.pptx")
    if not os.path.exists(template_path):
        return f"Error: Design template '{design_name}/template.pptx' not found."
        
    prs = Presentation(template_path)
    
    # Very basic placeholder replacement logic for demonstration
    for slide in prs.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            text = shape.text
            if "Title Placeholder" in text and "title" in report_data:
                shape.text = report_data["title"]
            elif "Subtitle Placeholder" in text and "body" in report_data:
                shape.text = report_data["body"]
                
    output_path = os.path.join("files", f"{output_filename}.pptx")
    os.makedirs("files", exist_ok=True)
    prs.save(output_path)
    
    return f"Successfully generated PPTX at {output_path}"
```

- [ ] **Step 3: Register tools in `REGISTRY`**
In `app/helix_agent/tools.py`, add to `REGISTRY`:

```python
REGISTRY = {
    # ... existing tools ...
    "generate_pdf_report": generate_pdf_report,
    "generate_ppt_report": generate_ppt_report,
}
```

- [ ] **Step 4: Commit**
```bash
git add app/helix_agent/tools.py
git commit -m "feat: implement pdf and pptx generation tools"
```

### Task 4: Update Reporter Agent

**Files:**
- Modify: `app/helix_agent/sub_agents/reporter.yaml`

- [ ] **Step 1: Update YAML**
Modify `app/helix_agent/sub_agents/reporter.yaml` to include new instructions and tools:

```yaml
name: "reporter"
model: "gemini-2.5-flash"
description: "Synthesizes raw data into professional markdown reports, PDFs, and PPTs."
instruction: |
  You are a Reporting agent.
  You receive raw data from Chapter SMEs.
  If the user asks for a standard report, format it as markdown.
  If the user asks for a PDF or PowerPoint, you MUST use the `generate_pdf_report` or `generate_ppt_report` tools.
  Use `design_name: "executive_summary"`.
  Structure `report_data` with keys like `title`, `date`, and `body` based on the raw data.
  Provide the final file path to the user.
tools: 
  - generate_pdf_report
  - generate_ppt_report
```

- [ ] **Step 2: Commit**
```bash
git add app/helix_agent/sub_agents/reporter.yaml
git commit -m "feat: enable PDF and PPTX tools in reporter agent"
```
