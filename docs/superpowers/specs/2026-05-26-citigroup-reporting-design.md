# Citigroup Branded Report Generation Design

## Overview
The Reporter agent currently outputs standard markdown. This design adds the capability to generate professionally branded PDF and PowerPoint (PPTX) reports adhering to Citigroup brand standards (Primary Blue #003B70, Citi Red #D11242, and clean typography).

## Directory Structure & Templating System
A new file structure will be introduced to support a modular, "drop-in" design system:
```text
data/designs/
└── executive_summary/
    ├── template.html    # Jinja2 template with Citi CSS for PDF generation
    └── template.pptx    # Base PowerPoint file with master slides and placeholders
```
Users can add new folders under `data/designs/` to introduce new templates. The agent will dynamically map user requests to the available folder names.

## Python Libraries
The project will be updated to include the following dependencies:
*   `python-pptx`: For opening and populating PowerPoint templates.
*   `xhtml2pdf`: A pure Python library for converting HTML to PDF.
*   `Jinja2`: For rendering data into HTML templates before PDF conversion.

## New Tools (`app/helix_agent/tools.py`)
Two new ADK-registered tools will be created:

### 1. `generate_pdf_report(design_name: str, report_data: dict, output_filename: str) -> str`
*   **Purpose**: Generates a branded PDF.
*   **Flow**: 
    1. Loads `data/designs/{design_name}/template.html`.
    2. Renders the template using Jinja2 with `report_data`.
    3. Converts the resulting HTML to PDF using `xhtml2pdf`.
    4. Saves to `files/{output_filename}.pdf`.
*   **Returns**: Success message with file path.

### 2. `generate_ppt_report(design_name: str, report_data: dict, output_filename: str) -> str`
*   **Purpose**: Generates a branded PowerPoint presentation.
*   **Flow**:
    1. Loads `data/designs/{design_name}/template.pptx`.
    2. Iterates through slide placeholders and replaces them with corresponding text from `report_data`.
    3. Saves to `files/{output_filename}.pptx`.
*   **Returns**: Success message with file path.

## Agent Updates (`reporter.yaml`)
The `reporter` chapter agent will be updated to utilize these tools:
*   **Instructions**: Updated to instruct the agent to use `generate_pdf_report` or `generate_ppt_report` when the user requests a formatted file. The agent will be instructed on how to structure `report_data` to match expected template placeholders.
*   **Tools**: Add `generate_pdf_report` and `generate_ppt_report` to the `tools` array.

## Data Flow
1. Orchestrator routes report generation request to Reporter.
2. Reporter calls `list_dir` or is aware of available designs in `data/designs/`.
3. Reporter structures the data and calls the appropriate generation tool.
4. Tool outputs the file and Reporter informs Orchestrator.
5. Orchestrator presents the final file to the User.
