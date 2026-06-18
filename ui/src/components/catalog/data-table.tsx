import { useMemo } from "react";
import type { RendererProps } from "@copilotkit/a2ui-renderer";

type Row = Record<string, string | number | boolean | null>;

interface DataTableProps {
  columns?: string[];
  rows: Row[];
}

export function DataTable({ props }: RendererProps<DataTableProps>) {
  const columns = useMemo(
    () =>
      props.columns ?? Array.from(
        new Set(props.rows.flatMap((row) => Object.keys(row))),
      ),
    [props.columns, props.rows],
  );

  return (
    <div className="data-table-shell">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {props.rows.map((row, i) => (
            <tr key={`row-${i}`}>
              {columns.map((col) => (
                <td key={col}>{String(row[col] ?? "")}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}