from __future__ import annotations


def build_demo_statuses() -> list[dict[str, str]]:
    return [
        {"label": "Querying sample operational risk data", "state": "running"},
        {"label": "Drafting executive reporting summary", "state": "running"},
        {"label": "Preparing report artifacts", "state": "complete"},
    ]


def build_demo_artifacts() -> list[dict[str, object]]:
    return [
        {
            "type": "markdown",
            "title": "Executive Summary",
            "content": (
                "Payment operations and third-party controls show the highest "
                "sample residual risk. The recommended next step is an executive "
                "brief focused on remediation ownership and aging exceptions."
            ),
        },
        {
            "type": "data-table",
            "rows": [
                {
                    "riskId": "RSK-001",
                    "businessUnit": "Payments",
                    "severity": "High",
                    "status": "Open",
                },
                {
                    "riskId": "RSK-002",
                    "businessUnit": "Markets",
                    "severity": "Medium",
                    "status": "Review",
                },
                {
                    "riskId": "RSK-003",
                    "businessUnit": "Treasury",
                    "severity": "Medium",
                    "status": "Mitigating",
                },
            ],
        },
        {
            "type": "chart",
            "series": [
                {"label": "Payments", "value": 18},
                {"label": "Markets", "value": 11},
                {"label": "Treasury", "value": 9},
            ],
        },
        {
            "type": "report",
            "reportTitle": "Operational Risk Brief",
            "sections": [
                {
                    "heading": "Top Findings",
                    "body": (
                        "Sample analysis indicates concentrated exposure in "
                        "payment operations."
                    ),
                },
                {
                    "heading": "Recommended Actions",
                    "body": (
                        "Prioritize remediation ownership, aging exceptions, "
                        "and executive review cadence."
                    ),
                },
            ],
            "files": [{"label": "Sample report link", "href": "/files/sample-report.pdf"}],
        },
        {
            "type": "file-link",
            "files": [{"label": "Sample report link", "href": "/files/sample-report.pdf"}],
        },
    ]
