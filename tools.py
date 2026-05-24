import sys
import io
import os
import traceback
import html
import subprocess

def execute_python_code(code: str) -> str:
    wrapper = (
        "import sys\n"
        "import traceback\n"
        "exec_globals = {}\n"
        "try:\n"
        f"    exec({repr(code)}, exec_globals)\n"
        "except BaseException:\n"
        "    sys.stderr.write('Execution Error:\\n' + traceback.format_exc())\n"
        "    sys.exit(1)\n"
    )
    try:
        res = subprocess.run(
            [sys.executable, "-c", wrapper],
            capture_output=True,
            text=True,
            timeout=10
        )
        return res.stdout + res.stderr
    except subprocess.TimeoutExpired:
        return "Execution Error: Code execution timed out (exceeded 10 seconds)."
    except Exception as e:
        return f"Execution Error: {str(e)}"

def parse_markdown(markdown_content: str):
    elements = []
    current_paragraph = []

    def flush_paragraph():
        if current_paragraph:
            elements.append({
                "type": "paragraph",
                "text": " ".join(current_paragraph)
            })
            current_paragraph.clear()

    lines = markdown_content.split("\n")
    for line in lines:
        stripped_line = line.strip()
        
        # Empty line separates blocks
        if not stripped_line:
            flush_paragraph()
            continue
            
        # Headers
        if stripped_line.startswith("# ") or stripped_line.startswith("## ") or stripped_line.startswith("### "):
            flush_paragraph()
            if stripped_line.startswith("# "):
                level = 1
                text = stripped_line[2:]
            elif stripped_line.startswith("## "):
                level = 2
                text = stripped_line[3:]
            else:
                level = 3
                text = stripped_line[4:]
            elements.append({
                "type": "header",
                "level": level,
                "text": text
            })
            continue

        # Bullet points: e.g. "  * subbullet" or "* bullet"
        leading_spaces = len(line) - len(line.lstrip(' '))
        if stripped_line.startswith("* ") or stripped_line.startswith("- "):
            flush_paragraph()
            level = leading_spaces // 2
            text = stripped_line[2:]
            elements.append({
                "type": "bullet",
                "level": level,
                "text": text
            })
            continue

        # Normal text line - part of paragraph
        current_paragraph.append(stripped_line)

    flush_paragraph()
    return elements

def export_report_to_pdf(content: str, filepath: str):
    try:
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.colors import HexColor
    except ImportError:
        base, _ = os.path.splitext(filepath)
        filepath = base + ".txt"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return

    citi_blue = HexColor('#003B70')
    citi_red = HexColor('#EE3124')
    citi_text = HexColor('#222222')

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        textColor=citi_blue,
        fontSize=24,
        spaceAfter=12
    )
    
    h2_style = ParagraphStyle(
        'Heading2Style',
        parent=styles['Heading2'],
        textColor=citi_red,
        fontSize=18,
        spaceAfter=10
    )
    
    h3_style = ParagraphStyle(
        'Heading3Style',
        parent=styles['Heading3'],
        textColor=citi_blue,
        fontSize=14,
        spaceAfter=8
    )
    
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        textColor=citi_text,
        fontSize=11,
        spaceAfter=6
    )

    doc = SimpleDocTemplate(filepath)
    story = []

    for line in content.split('\n'):
        if line.startswith('###'):
            text = html.escape(line[3:].lstrip())
            story.append(Paragraph(text, h3_style))
        elif line.startswith('##'):
            text = html.escape(line[2:].lstrip())
            story.append(Paragraph(text, h2_style))
        elif line.startswith('#'):
            text = html.escape(line[1:].lstrip())
            story.append(Paragraph(text, title_style))
        elif not line.strip():
            story.append(Spacer(1, 12))
        else:
            text = html.escape(line)
            story.append(Paragraph(text, normal_style))

    doc.build(story)

def export_report_to_pptx(content: str, filepath: str):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
