import type { RendererProps } from "@copilotkit/a2ui-renderer";

interface ChartColumnProps {
  title: string;
  series: { label: string; value: number }[];
}

export function ChartColumn({ props }: RendererProps<ChartColumnProps>) {
  const max = Math.max(...props.series.map((s) => s.value), 1);
  const chartHeight = 200;
  return (
    <div className="chart-card">
      <h3>{props.title}</h3>
      <svg
        viewBox={`0 0 ${props.series.length * 60 + 40} ${chartHeight + 30}`}
        style={{ width: "100%", maxWidth: "600px" }}
      >
        {props.series.map((point, i) => {
          const barHeight = (point.value / max) * chartHeight;
          const x = i * 60 + 20;
          const y = chartHeight - barHeight;
          return (
            <g key={point.label}>
              <rect
                x={x}
                y={y}
                width={40}
                height={barHeight}
                fill="var(--citi-action)"
              />
              <text
                x={x + 20}
                y={chartHeight + 15}
                textAnchor="middle"
                fontSize="11"
                fill="var(--text-muted)"
              >
                {point.label.length > 8
                  ? point.label.substring(0, 7) + "\u2026"
                  : point.label}
              </text>
              <text
                x={x + 20}
                y={y - 5}
                textAnchor="middle"
                fontSize="11"
                fill="var(--text-primary)"
                fontWeight="700"
              >
                {point.value}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}