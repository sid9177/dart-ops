import type { RendererProps } from "@copilotkit/a2ui-renderer";

interface ChartLineProps {
  title: string;
  points: { x: string; y: number }[];
}

export function ChartLine({ props }: RendererProps<ChartLineProps>) {
  const width = 500;
  const height = 200;
  const padding = 30;
  const maxY = Math.max(...props.points.map((p) => p.y), 1);
  const minY = Math.min(...props.points.map((p) => p.y), 0);
  const rangeY = maxY - minY || 1;
  const stepX = (width - padding * 2) / Math.max(props.points.length - 1, 1);

  const coords = props.points.map((p, i) => {
    const x = padding + i * stepX;
    const y = height - padding - ((p.y - minY) / rangeY) * (height - padding * 2);
    return { x, y, label: p.x, value: p.y };
  });

  const polyline = coords.map((c) => `${c.x},${c.y}`).join(" ");

  return (
    <div className="chart-card">
      <h3>{props.title}</h3>
      <svg viewBox={`0 0 ${width} ${height}`} style={{ width: "100%", maxWidth: "600px" }}>
        <polyline
          points={polyline}
          fill="none"
          stroke="var(--citi-action)"
          strokeWidth="2"
        />
        {coords.map((c, i) => (
          <g key={i}>
            <circle cx={c.x} cy={c.y} r="4" fill="var(--citi-action)" />
            <text
              x={c.x}
              y={height - 10}
              textAnchor="middle"
              fontSize="10"
              fill="var(--text-muted)"
            >
              {c.label.length > 6 ? c.label.substring(0, 5) + "\u2026" : c.label}
            </text>
          </g>
        ))}
      </svg>
    </div>
  );
}