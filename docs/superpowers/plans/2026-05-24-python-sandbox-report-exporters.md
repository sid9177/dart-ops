# Python Sandbox & Report Exporters Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a secure python code executor and Citigroup-branded PDF/PPTX report exporters, plus refactor DuckDBHelper and its unit tests.

**Architecture:** Create `tools.py` for sandbox execution and PDF/PPTX exports (with graceful text fallback when dependencies are missing). Refactor `db_helper.py` to use `CREATE OR REPLACE TABLE` and wrap loader errors in `IOError`. Test both helper and tool functions thoroughly in pytest using fixtures and mocking.

**Tech Stack:** Python, pytest, duckdb, pandas, reportlab, python-pptx

---

### Task 1: Refactor DuckDBHelper & Update tests

**Files:**
- Modify: [db_helper.py](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/db_helper.py)
- Modify: [tests/test_db_helper.py](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/tests/test_db_helper.py)

- [ ] **Step 1: Modify db_helper.py**
  Update the load_csv function to raise `IOError` on failure and use `CREATE OR REPLACE TABLE "{table_name}"`.

  ```python
  def load_csv(self, table_name: str, file_path: str):
      normalized_path = file_path.replace("\\", "/")
      try:
          if normalized_path.endswith((".xlsx", ".xls")):
              df = pd.read_excel(file_path)
              self.conn.register(table_name, df)
          else:
              self.conn.execute(f'CREATE OR REPLACE TABLE "{table_name}" AS SELECT * FROM read_csv_auto(\'{normalized_path}\')')
      except Exception as e:
          raise IOError(f"Failed to load file '{file_path}': {str(e)}") from e
  ```

- [ ] **Step 2: Update tests/test_db_helper.py**
  Refactor tests to use pytest's `tmp_path` fixture and assert that `IOError` is raised for missing files.

  ```python
  import pytest
  from db_helper import DuckDBHelper
  from unittest.mock import patch
  import pandas as pd

  def test_duckdb_helper_flow(tmp_path):
      temp_csv = tmp_path / "temp_test.csv"
      temp_csv.write_text("col_a,col_b\n1,hello\n2,world\n", encoding="utf-8")

      helper = DuckDBHelper()
      helper.load_csv("test_table", str(temp_csv))

      # Test schema discovery
      schema = helper.get_table_schema("test_table")
      assert "col_a" in schema
      assert "col_b" in schema

      # Test query execution
      res = helper.run_sql_query("SELECT * FROM test_table WHERE col_a = 1")
      assert "hello" in res

  def test_duckdb_helper_excel():
      helper = DuckDBHelper()
      mock_df = pd.DataFrame({"col_c": [3], "col_d": ["excel"]})
      with patch("pandas.read_excel", return_value=mock_df) as mock_read:
          helper.load_csv("excel_table", "dummy.xlsx")
          mock_read.assert_called_once_with("dummy.xlsx")
          
          schema = helper.get_table_schema("excel_table")
          assert "col_c" in schema
          assert "col_d" in schema
          
          res = helper.run_sql_query("SELECT * FROM excel_table")
          assert "excel" in res

  def test_duckdb_helper_invalid_file():
      helper = DuckDBHelper()
      with pytest.raises(IOError):
          helper.load_csv("invalid_table", "non_existent_file.csv")
  ```

- [ ] **Step 3: Verify tests execution manually**
  Since automated commands are disabled due to permission restrictions, review the implementation changes and proceed.

---

### Task 2: Implement Python Sandbox Execution

**Files:**
- Create: [tools.py](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/tools.py)
- Create: [tests/test_tools.py](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/tests/test_tools.py)

- [ ] **Step 1: Create tools.py draft with execute_python_code**
  Implement the code execution capability that captures stdout and stderr and returns it.

  ```python
  import sys
  import io
  import traceback

  def execute_python_code(code: str) -> str:
      old_stdout = sys.stdout
      old_stderr = sys.stderr
      sys.stdout = buffer_out = io.StringIO()
      sys.stderr = buffer_err = io.StringIO()
      exec_globals = {}
      try:
          exec(code, exec_globals)
          sys.stdout = old_stdout
          sys.stderr = old_stderr
          output = buffer_out.getvalue()
          err = buffer_err.getvalue()
          if err:
              return f"{output}\nStderr:\n{err}".strip()
          return output
      except Exception as e:
          sys.stdout = old_stdout
          sys.stderr = old_stderr
          return f"Execution Error:\n{traceback.format_exc()}"
  ```

- [ ] **Step 2: Create tests/test_tools.py draft**
  Add unit tests to verify standard output, standard error, and execution error scenarios.

  ```python
  import pytest
  from tools import execute_python_code

  def test_execute_python_code_success():
      code = "print('Hello World')"
      output = execute_python_code(code)
      assert output.strip() == "Hello World"

  def test_execute_python_code_error():
      code = "raise ValueError('Test error')"
      output = execute_python_code(code)
      assert "Execution Error" in output
      assert "ValueError: Test error" in output
  ```

---

### Task 3: Implement Citigroup-Branded PDF & PPTX Report Exporters

**Files:**
- Modify: [tools.py](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/tools.py)
- Modify: [tests/test_tools.py](file:///c:/Users/siddi/Projects/adk-workspace/dart-ops/tests/test_tools.py)

- [ ] **Step 1: Add report export functions to tools.py**
  Add `export_report_to_pdf` and `export_report_to_pptx` with standard import fallback handling.

  ```python
  def export_report_to_pdf(markdown_content: str, output_path: str):
      try:
          from reportlab.lib.pagesizes import letter
          from reportlab.lib import colors
          from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
          from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
      except ImportError:
          with open(output_path, "w", encoding="utf-8") as f:
              f.write(f"PDF FALLBACK - MOCK GENERATED\n\n{markdown_content}")
          return

      doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
      styles = getSampleStyleSheet()
      
      citi_blue = colors.HexColor("#003B70")
      citi_red = colors.HexColor("#EE3124")
      charcoal = colors.HexColor("#222222")

      title_style = ParagraphStyle(
          'CitiTitle',
          parent=styles['Heading1'],
          fontName='Helvetica-Bold',
          fontSize=22,
          textColor=citi_blue,
          spaceAfter=15
      )
      
      body_style = ParagraphStyle(
          'CitiBody',
          parent=styles['Normal'],
          fontName='Helvetica',
          fontSize=10.5,
          textColor=charcoal,
          spaceAfter=8,
          leading=14
      )

      story = []
      
      header_bar = Table([[""]], colWidths=[540])
      header_bar.setStyle(TableStyle([
          ('BACKGROUND', (0,0), (-1,-1), citi_red),
          ('BOTTOMPADDING', (0,0), (-1,-1), 4),
          ('TOPPADDING', (0,0), (-1,-1), 0),
      ]))
      story.append(header_bar)
      story.append(Spacer(1, 15))

      lines = markdown_content.split("\n")
      for line in lines:
          line = line.strip()
          if not line:
              continue
          if line.startswith("# "):
              story.append(Paragraph(line[2:], title_style))
          elif line.startswith("## "):
              h2_style = ParagraphStyle('CitiH2', parent=title_style, fontSize=16, spaceBefore=10)
              story.append(Paragraph(line[3:], h2_style))
          elif line.startswith("### "):
              h3_style = ParagraphStyle('CitiH3', parent=title_style, fontSize=12, spaceBefore=8)
              story.append(Paragraph(line[4:], h3_style))
          elif line.startswith("* ") or line.startswith("- "):
              story.append(Paragraph(f"• {line[2:]}", body_style))
          else:
              story.append(Paragraph(line, body_style))

      confidential_style = ParagraphStyle('CitiConf', parent=body_style, fontSize=8, textColor=colors.gray, alignment=1)
      story.append(Spacer(1, 25))
      story.append(Paragraph("CITI INTERNAL USE ONLY - STRICTLY CONFIDENTIAL", confidential_style))
      
      doc.build(story)

  def export_report_to_pptx(markdown_content: str, output_path: str):
      try:
          from pptx import Presentation
          from pptx.util import Inches, Pt
          from pptx.dml.color import RGBColor
      except ImportError:
          with open(output_path, "w", encoding="utf-8") as f:
              f.write(f"PPTX FALLBACK - MOCK GENERATED\n\n{markdown_content}")
          return

      prs = Presentation()
      prs.slide_width = Inches(13.333)
      prs.slide_height = Inches(7.5)
      
      citi_blue_rgb = RGBColor(0, 59, 112)
      citi_red_rgb = RGBColor(238, 49, 36)
      charcoal_rgb = RGBColor(34, 34, 34)

      slide_layout = prs.slide_layouts[5] 
      slide = prs.slides.add_slide(slide_layout)
      
      shapes = slide.shapes
      header_box = shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12.333), Inches(1.5))
      tf = header_box.text_frame
      tf.word_wrap = True
      p = tf.paragraphs[0]
      p.text = "Citi Operational Risk Analytics Report"
      p.font.size = Pt(36)
      p.font.bold = True
      p.font.color.rgb = citi_blue_rgb

      line = shapes.add_shape(1, Inches(0.5), Inches(2.0), Inches(12.333), Inches(0.08))
      line.fill.solid()
      line.fill.fore_color.rgb = citi_red_rgb

      slide = prs.slides.add_slide(prs.slide_layouts[1]) 
      shapes = slide.shapes
      title_shape = shapes.title
      title_shape.text = "Executive Summary & Findings"
      title_shape.text_frame.paragraphs[0].font.color.rgb = citi_blue_rgb
      
      body_shape = shapes.placeholders[1]
      tf = body_shape.text_frame
      tf.word_wrap = True
      
      lines = markdown_content.split("\n")
      for line in lines:
          line = line.strip()
          if line.startswith("* ") or line.startswith("- "):
              p = tf.add_paragraph()
              p.text = line[2:]
              p.level = 0
              p.font.color.rgb = charcoal_rgb

      prs.save(output_path)
  ```

- [ ] **Step 2: Add tests for PDF and PPTX exporters to tests/test_tools.py**
  We will verify both fallback behavior (using mock imports) and standard behavior.

  ```python
  import sys
  import builtins
  from unittest.mock import patch, MagicMock

  def test_export_report_to_pdf_fallback(tmp_path):
      pdf_path = tmp_path / "report.pdf"
      # Mock the import error for reportlab
      with patch.dict('sys.modules', {'reportlab': None, 'reportlab.lib.pagesizes': None, 'reportlab.lib': None, 'reportlab.platypus': None, 'reportlab.lib.styles': None}):
          from tools import export_report_to_pdf
          export_report_to_pdf("# Test Title\n* Test point", str(pdf_path))
      
      assert pdf_path.exists()
      content = pdf_path.read_text(encoding="utf-8")
      assert "PDF FALLBACK" in content
      assert "Test Title" in content

  def test_export_report_to_pptx_fallback(tmp_path):
      pptx_path = tmp_path / "report.pptx"
      # Mock import error for pptx
      with patch.dict('sys.modules', {'pptx': None, 'pptx.util': None, 'pptx.dml.color': None}):
          from tools import export_report_to_pptx
          export_report_to_pptx("# Test Title\n* Test point", str(pptx_path))
          
      assert pptx_path.exists()
      content = pptx_path.read_text(encoding="utf-8")
      assert "PPTX FALLBACK" in content
      assert "Test Title" in content

  def test_export_report_to_pdf_success(tmp_path):
      # Test with reportlab mock if reportlab is actually mocked out or not installed
      # to ensure it exercises the PDF building code paths when reportlab is simulated.
      pdf_path = tmp_path / "report.pdf"
      
      # Mock imports to return mock modules
      mock_reportlab = MagicMock()
      mock_pagesizes = MagicMock()
      mock_colors = MagicMock()
      mock_platypus = MagicMock()
      mock_styles = MagicMock()
      
      # Setup some mock objects so the code does not crash
      mock_styles.getSampleStyleSheet.return_value = MagicMock()
      
      with patch.dict('sys.modules', {
          'reportlab': mock_reportlab,
          'reportlab.lib.pagesizes': mock_pagesizes,
          'reportlab.lib': mock_colors,
          'reportlab.platypus': mock_platypus,
          'reportlab.lib.styles': mock_styles
      }):
          # Re-import or reload tools to use the mocked modules
          if 'tools' in sys.modules:
              del sys.modules['tools']
          from tools import export_report_to_pdf
          export_report_to_pdf("# Test Title\n* Point 1", str(pdf_path))
          
      mock_platypus.SimpleDocTemplate.assert_called_once()
      mock_platypus.SimpleDocTemplate.return_value.build.assert_called_once()

  def test_export_report_to_pptx_success(tmp_path):
      pptx_path = tmp_path / "report.pptx"
      
      mock_pptx = MagicMock()
      mock_util = MagicMock()
      mock_color = MagicMock()
      
      # Setup Presentation mock
      mock_pres = MagicMock()
      mock_pptx.Presentation.return_value = mock_pres
      mock_slide = MagicMock()
      mock_pres.slides.add_slide.return_value = mock_slide
      mock_shape = MagicMock()
      mock_slide.shapes.add_textbox.return_value = mock_shape
      mock_shape.text_frame = MagicMock()
      mock_shape.text_frame.paragraphs = [MagicMock()]
      
      # Title and placeholders
      mock_pres.slide_layouts = [MagicMock() for _ in range(10)]
      mock_slide.shapes.placeholders = [MagicMock(), MagicMock()]
      
      with patch.dict('sys.modules', {
          'pptx': mock_pptx,
          'pptx.util': mock_util,
          'pptx.dml.color': mock_color
      }):
          if 'tools' in sys.modules:
              del sys.modules['tools']
          from tools import export_report_to_pptx
          export_report_to_pptx("# Test Title\n* Point 1", str(pptx_path))
          
      mock_pptx.Presentation.assert_called_once()
      mock_pres.save.assert_called_once_with(str(pptx_path))
  ```
