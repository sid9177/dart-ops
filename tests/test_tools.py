import sys
import pytest
from unittest.mock import patch, MagicMock
from tools import execute_python_code

def test_execute_python_code_success():
    code = "print('Hello, Citi!')"
    output = execute_python_code(code)
    assert output.strip() == "Hello, Citi!"

def test_execute_python_code_stderr():
    code = "import sys\nprint('Info message')\nprint('Error message', file=sys.stderr)"
    output = execute_python_code(code)
    # Since stdout and stderr are bound to the same buffer, they will be combined
    assert "Info message" in output
    assert "Error message" in output

def test_execute_python_code_error():
    code = "raise ValueError('Custom error message')"
    output = execute_python_code(code)
    assert "Execution Error" in output
    assert "ValueError: Custom error message" in output

def test_execute_python_code_base_exception():
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    code = "import sys\nsys.exit(42)"
    output = execute_python_code(code)
    assert sys.stdout is old_stdout
    assert sys.stderr is old_stderr
    assert "Execution Error" in output
    assert "SystemExit" in output

def test_execute_python_code_timeout():
    code = "import time\nwhile True:\n    time.sleep(0.01)"
    # We should run a shorter execution or rely on the 10-second timeout.
    # Wait, running a 10-second timeout test in standard test suite takes 10 seconds.
    # Can we mock the subprocess timeout or just let it timeout? Let's mock subprocess.run to raise TimeoutExpired or run a quick test.
    # Actually, let's patch the timeout in execute_python_code to 0.1 seconds for testing,
    # or just mock subprocess.run. Or we can just let it run. But 10 seconds is long.
    # Let's mock subprocess.run to raise subprocess.TimeoutExpired during the test, or let's test it by mocking.
    from unittest.mock import patch
    import subprocess
    with patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd=[], timeout=0.1)):
        output = execute_python_code("infinite_loop")
        assert "timed out" in output

def test_export_report_to_pdf(tmp_path):
    pdf_path = tmp_path / "test_report.pdf"
    from tools import export_report_to_pdf
    
    content = "PDF test content"
    export_report_to_pdf(content, str(pdf_path))
    
    try:
        import reportlab
        has_reportlab = True
    except ImportError:
        has_reportlab = False

    if has_reportlab:
        assert pdf_path.exists()
        # Verify it looks like a PDF (starts with %PDF)
        with open(pdf_path, 'rb') as f:
            assert f.read(4) == b'%PDF'
    else:
        # Fallback behaviour
        txt_path = tmp_path / "test_report.txt"
        assert txt_path.exists()
        assert txt_path.read_text(encoding="utf-8") == content

def test_export_report_to_pptx(tmp_path):
    pptx_path = tmp_path / "test_report.pptx"
    from tools import export_report_to_pptx
    
    content = "PPTX test content"
    export_report_to_pptx(content, str(pptx_path))
    
    assert pptx_path.exists()
    assert pptx_path.read_text(encoding="utf-8") == content

def test_parse_markdown():
    from tools import parse_markdown
    markdown = (
        "# H1 Header\n"
        "This is paragraph line 1.\n"
        "This is paragraph line 2.\n"
        "\n"
        "## H2 Header\n"
        "* Bullet level 0\n"
        "  * Bullet level 1\n"
        "    * Bullet level 2\n"
    )
    elements = parse_markdown(markdown)
    assert len(elements) == 6
    
    assert elements[0] == {"type": "header", "level": 1, "text": "H1 Header"}
    assert elements[1] == {
        "type": "paragraph",
        "text": "This is paragraph line 1. This is paragraph line 2."
    }
    assert elements[2] == {"type": "header", "level": 2, "text": "H2 Header"}
    assert elements[3] == {"type": "bullet", "level": 0, "text": "Bullet level 0"}
    assert elements[4] == {"type": "bullet", "level": 1, "text": "Bullet level 1"}
    assert elements[5] == {"type": "bullet", "level": 2, "text": "Bullet level 2"}

# Clean up sys.modules after tests run to not pollute the global module namespace
@pytest.fixture(autouse=True)
def clean_tools_module():
    yield
    if 'tools' in sys.modules:
        del sys.modules['tools']
