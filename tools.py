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
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def export_report_to_pptx(content: str, filepath: str):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
