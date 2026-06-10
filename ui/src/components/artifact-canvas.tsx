"use client";

import { useMemo, useState } from "react";
import type { ArtifactState, ArtifactTab } from "@/lib/artifacts";

const tabs: { id: ArtifactTab; label: string }[] = [
  { id: "summary", label: "Summary" },
  { id: "data", label: "Data" },
  { id: "charts", label: "Charts" },
  { id: "report", label: "Report" },
  { id: "files", label: "Files" },
];

export function ArtifactCanvas({ state }: { state: ArtifactState }) {
  const [manualTab, setManualTab] = useState<ArtifactTab | null>(null);
  const activeTab = manualTab ?? state.activeTab;
  const headers = useMemo(
    () => Array.from(new Set(state.rows.flatMap((row) => Object.keys(row)))),
    [state.rows],
  );

  return (
    <div className="artifact-canvas">
      <div className="artifact-toolbar">
        <div>
          <p className="eyebrow dark">Generated output</p>
          <h2>Reporting Workspace</h2>
        </div>
        <div className="artifact-tabs" role="toolbar" aria-label="Artifact tabs">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              type="button"
              aria-pressed={activeTab === tab.id}
              onClick={() => setManualTab(tab.id)}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      <div className="artifact-body">
        {activeTab === "summary" && (
          <section>
            <h3>{state.summaryTitle}</h3>
            {state.summary ? (
              <p className="report-copy">{state.summary}</p>
            ) : (
              <p className="empty-copy">
                Ask Copilot to generate analysis, tables, charts, reports, or
                file links.
              </p>
            )}
          </section>
        )}

        {activeTab === "data" && (
          <section className="table-shell">
            {state.rows.length === 0 ? (
              <p className="empty-copy">No data table has been generated.</p>
            ) : (
              <table>
                <thead>
                  <tr>
                    {headers.map((header) => (
                      <th key={header}>{header}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {state.rows.map((row, index) => (
                    <tr key={`row-${index}`}>
                      {headers.map((header) => (
                        <td key={header}>{String(row[header] ?? "")}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </section>
        )}

        {activeTab === "charts" && (
          <section className="chart-list">
            {state.chartSeries.length === 0 ? (
              <p className="empty-copy">No chart data has been generated.</p>
            ) : (
              state.chartSeries.map((point) => (
                <div className="chart-row" key={point.label}>
                  <span>{point.label}</span>
                  <div className="chart-track">
                    <span style={{ width: `${Math.min(point.value * 3, 100)}%` }} />
                  </div>
                  <strong>{point.value}</strong>
                </div>
              ))
            )}
          </section>
        )}

        {activeTab === "report" && (
          <section className="report-preview">
            <h3>{state.reportTitle || "Report Preview"}</h3>
            {state.reportSections.length === 0 ? (
              <p className="empty-copy">No report preview has been generated.</p>
            ) : (
              state.reportSections.map((section) => (
                <article key={section.heading}>
                  <h4>{section.heading}</h4>
                  <p>{section.body}</p>
                </article>
              ))
            )}
          </section>
        )}

        {activeTab === "files" && (
          <section className="file-list">
            {state.files.length === 0 ? (
              <p className="empty-copy">No file links have been generated.</p>
            ) : (
              state.files.map((file) => (
                <a href={file.href} key={file.href}>
                  {file.label}
                </a>
              ))
            )}
          </section>
        )}
      </div>
    </div>
  );
}
