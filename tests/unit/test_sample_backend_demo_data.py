from sample_backend.demo_data import build_demo_artifacts, build_demo_statuses


def test_build_demo_statuses_returns_reporting_trace():
    statuses = build_demo_statuses()

    assert statuses == [
        {"label": "Querying sample operational risk data", "state": "running"},
        {"label": "Drafting executive reporting summary", "state": "running"},
        {"label": "Preparing report artifacts", "state": "complete"},
    ]


def test_build_demo_artifacts_returns_all_template_artifact_types():
    artifacts = build_demo_artifacts()

    assert [artifact["type"] for artifact in artifacts] == [
        "markdown",
        "data-table",
        "chart",
        "report",
        "file-link",
    ]
    assert artifacts[0]["title"] == "Executive Summary"
    assert artifacts[1]["rows"][0]["riskId"] == "RSK-001"
    assert artifacts[2]["series"][0]["label"] == "Payments"
    assert artifacts[3]["reportTitle"] == "Operational Risk Brief"
    assert artifacts[4]["files"][0]["label"] == "Sample report link"
