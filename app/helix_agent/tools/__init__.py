from .duckdb_tool import execute_duckdb_query
from .report_tool import generate_pdf_report, generate_ppt_report

REGISTRY = {
    "execute_duckdb_query": execute_duckdb_query,
    "generate_pdf_report": generate_pdf_report,
    "generate_ppt_report": generate_ppt_report,
}
