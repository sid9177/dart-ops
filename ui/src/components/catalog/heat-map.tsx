import type { RendererProps } from "@copilotkit/a2ui-renderer";

interface HeatMapProps {
  title: string;
  rows: { label: string; cells: { label: string; value: number }[] }[];
}

function heatColor(value: number): string {
  if (value >= 75) return "#B60000";
  if (value >= 50) return "#ED8B00";
  if (value >= 25) return "#FFCD00";
  return "#00B755";
}

export function HeatMap({ props }: RendererProps<HeatMapProps>) {
  const cellSize = 50;
  const labelWidth = 100;
  const headerHeight = 30;

  return (
    <div className="chart-card">
      <h3>{props.title}</h3>
      <div style={{ overflowX: "auto" }}>
        <svg
          viewBox={`0 0 ${labelWidth + (props.rows[0]?.cells.length ?? 0) * cellSize} ${headerHeight + props.rows.length * cellSize}`}
          style={{ width: "100%", maxWidth: "600px" }}
        >
          {props.rows[0]?.cells.map((cell, colIdx) => (
            <text
              key={colIdx}
              x={labelWidth + colIdx * cellSize + cellSize / 2}
              y={20}
              textAnchor="middle"
              fontSize="11"
              fill="var(--text-muted)"
            >
              {cell.label}
            </text>
          ))}
          {props.rows.map((row, rowIdx) => (
            <g key={rowIdx}>
              <text
                x={labelWidth - 8}
                y={headerHeight + rowIdx * cellSize + cellSize / 2 + 4}
                textAnchor="end"
                fontSize="11"
                fill="var(--text-muted)"
              >
                {row.label}
              </text>
              {row.cells.map((cell, colIdx) => (
                <g key={colIdx}>
                  <rect
                    x={labelWidth + colIdx * cellSize}
                    y={headerHeight + rowIdx * cellSize}
                    width={cellSize - 2}
                    height={cellSize - 2}
                    rx="2"
                    fill={heatColor(cell.value)}
                  />
                  <text
                    x={labelWidth + colIdx * cellSize + cellSize / 2}
                    y={headerHeight + rowIdx * cellSize + cellSize / 2 + 4}
                    textAnchor="middle"
                    fontSize="12"
                    fontWeight="700"
                    fill="var(--white)"
                  >
                    {cell.value}
                  </text>
                </g>
              ))}
            </g>
          ))}
        </svg>
      </div>
    </div>
  );
}