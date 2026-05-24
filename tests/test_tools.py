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

def test_export_report_to_pdf_fallback(tmp_path):
    pdf_path = tmp_path / "report_fallback.pdf"
    # Mock reportlab modules to be unavailable
    with patch.dict('sys.modules', {
        'reportlab': None,
        'reportlab.lib.pagesizes': None,
        'reportlab.lib': None,
        'reportlab.platypus': None,
        'reportlab.lib.styles': None
    }):
        # Reload/re-import tools under the mocked environment
        if 'tools' in sys.modules:
            del sys.modules['tools']
        from tools import export_report_to_pdf
        
        markdown = "# Citi Test Report\n## Executive Summary\n* Key finding 1\n* Key finding 2"
        export_report_to_pdf(markdown, str(pdf_path))
        
    assert pdf_path.exists()
    content = pdf_path.read_text(encoding="utf-8")
    assert "PDF FALLBACK - MOCK GENERATED" in content
    assert "Citi Test Report" in content
    assert "Key finding 1" in content

def test_export_report_to_pptx_fallback(tmp_path):
    pptx_path = tmp_path / "report_fallback.pptx"
    # Mock pptx modules to be unavailable
    with patch.dict('sys.modules', {
        'pptx': None,
        'pptx.util': None,
        'pptx.dml.color': None
    }):
        if 'tools' in sys.modules:
            del sys.modules['tools']
        from tools import export_report_to_pptx
        
        markdown = "# Title\n* Point A\n* Point B"
        export_report_to_pptx(markdown, str(pptx_path))
        
    assert pptx_path.exists()
    content = pptx_path.read_text(encoding="utf-8")
    assert "PPTX FALLBACK - MOCK GENERATED" in content
    assert "Title" in content
    assert "Point A" in content

def test_export_report_to_pdf_success(tmp_path):
    pdf_path = tmp_path / "report_real.pdf"
    
    # Mock reportlab modules so that even if reportlab is not installed,
    # the success path runs and uses our mocked reportlab API.
    mock_reportlab = MagicMock()
    mock_pagesizes = MagicMock()
    mock_colors = MagicMock()
    mock_platypus = MagicMock()
    mock_styles = MagicMock()
    
    mock_styles.getSampleStyleSheet.return_value = MagicMock()
    
    with patch.dict('sys.modules', {
        'reportlab': mock_reportlab,
        'reportlab.lib.pagesizes': mock_pagesizes,
        'reportlab.lib': mock_colors,
        'reportlab.platypus': mock_platypus,
        'reportlab.lib.styles': mock_styles
    }):
        if 'tools' in sys.modules:
            del sys.modules['tools']
        from tools import export_report_to_pdf
        
        markdown = "# Citi Test Report\n## Executive Summary\n* Key finding 1\nRegular paragraph text"
        export_report_to_pdf(markdown, str(pdf_path))
        
    mock_platypus.SimpleDocTemplate.assert_called_once()
    mock_platypus.SimpleDocTemplate.return_value.build.assert_called_once()

def test_export_report_to_pptx_success(tmp_path):
    pptx_path = tmp_path / "report_real.pptx"
    
    mock_pptx = MagicMock()
    mock_util = MagicMock()
    mock_color = MagicMock()
    
    mock_pres = MagicMock()
    mock_pptx.Presentation.return_value = mock_pres
    
    mock_slide1 = MagicMock()
    mock_slide2 = MagicMock()
    mock_pres.slides.add_slide.side_effect = [mock_slide1, mock_slide2]
    
    mock_shape1 = MagicMock()
    mock_slide1.shapes.add_textbox.return_value = mock_shape1
    mock_shape1.text_frame = MagicMock()
    mock_shape1.text_frame.paragraphs = [MagicMock()]
    
    mock_pres.slide_layouts = [MagicMock() for _ in range(10)]
    mock_slide2.shapes.placeholders = [MagicMock(), MagicMock()]
    mock_slide2.shapes.title = MagicMock()
    
    with patch.dict('sys.modules', {
        'pptx': mock_pptx,
        'pptx.util': mock_util,
        'pptx.dml.color': mock_color
    }):
        if 'tools' in sys.modules:
            del sys.modules['tools']
        from tools import export_report_to_pptx
        
        markdown = "# Title\n* Point A\n* Point B"
        export_report_to_pptx(markdown, str(pptx_path))
        
    mock_pptx.Presentation.assert_called_once()
    mock_pres.save.assert_called_once_with(str(pptx_path))

# Clean up sys.modules after tests run to not pollute the global module namespace
@pytest.fixture(autouse=True)
def clean_tools_module():
    yield
    if 'tools' in sys.modules:
        del sys.modules['tools']
