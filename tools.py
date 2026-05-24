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
    try:
        from pptx import Presentation
        from pptx.util import Inches
        from pptx.dml.color import RGBColor
    except ImportError:
        base, _ = os.path.splitext(filepath)
        filepath = base + ".txt"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return

    citi_blue = RGBColor(0x00, 0x3B, 0x70)
    citi_red = RGBColor(0xEE, 0x31, 0x24)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    current_slide = None
    current_title = ""
    paragraph_count = 0

    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue

        if line.startswith('# '):
            current_title = line[2:]
            slide_layout = prs.slide_layouts[0]
            current_slide = prs.slides.add_slide(slide_layout)
            title_shape = current_slide.shapes.title
            if title_shape:
                title_shape.text = current_title
                if title_shape.text_frame.paragraphs and title_shape.text_frame.paragraphs[0].runs:
                    title_shape.text_frame.paragraphs[0].runs[0].font.color.rgb = citi_blue
            paragraph_count = 0

        elif line.startswith('## ') or line.startswith('### '):
            if line.startswith('## '):
                current_title = line[3:]
                title_color = citi_red
            else:
                current_title = line[4:]
                title_color = citi_blue
            
            slide_layout = prs.slide_layouts[1]
            current_slide = prs.slides.add_slide(slide_layout)
            title_shape = current_slide.shapes.title
            if title_shape:
                title_shape.text = current_title
                if title_shape.text_frame.paragraphs and title_shape.text_frame.paragraphs[0].runs:
                    title_shape.text_frame.paragraphs[0].runs[0].font.color.rgb = title_color
            paragraph_count = 0

        else:
            if current_slide is None:
                current_title = "Report"
                slide_layout = prs.slide_layouts[1]
                current_slide = prs.slides.add_slide(slide_layout)
                title_shape = current_slide.shapes.title
                if title_shape:
                    title_shape.text = current_title
                    if title_shape.text_frame.paragraphs and title_shape.text_frame.paragraphs[0].runs:
                        title_shape.text_frame.paragraphs[0].runs[0].font.color.rgb = citi_blue
                paragraph_count = 0
                
            if paragraph_count >= 10:
                slide_layout = prs.slide_layouts[1]
                current_slide = prs.slides.add_slide(slide_layout)
                title_shape = current_slide.shapes.title
                if title_shape:
                    title_shape.text = current_title + " (Cont.)"
                    if title_shape.text_frame.paragraphs and title_shape.text_frame.paragraphs[0].runs:
                        title_shape.text_frame.paragraphs[0].runs[0].font.color.rgb = citi_blue
                paragraph_count = 0
                
            try:
                tf = current_slide.shapes.placeholders[1].text_frame
            except (IndexError, KeyError):
                continue
                
            if line.startswith('- '):
                text = line[2:]
            elif line.startswith('* '):
                text = line[2:]
            else:
                text = line

            if paragraph_count == 0 and not tf.text:
                p = tf.paragraphs[0]
                p.text = text
            else:
                p = tf.add_paragraph()
                p.text = text
            
            paragraph_count += 1
            
    prs.save(filepath)
