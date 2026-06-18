import type { RendererProps } from "@copilotkit/a2ui-renderer";

interface ChartDonutProps {
  title: string;
  segments: { label: string; value: number }[];
}

const DONUT_COLORS = [
  "#002D72",
  "#0041A5",
  "#005FF1",
  "#0076D4",
  "#00BDF2",
  "#219DFF",
];

export function ChartDonut({ props }: RendererProps<ChartDonutProps>) {
  const total = props.segments.reduce((sum, s) => sum + s.value, 0) || 1;
  const radius = 70;
  const cx = 80;
  const cy = 80;
  const strokeWidth = 20;

  const arcs = props.segments.reduce<
    { path: string; color: string; label: string; value: number }[]
  >((acc, segment, i) => {
    const prevEnd = acc.length > 0
      ? props.segments.slice(0, i).reduce((sum, s) => sum + s.value, 0)
      : 0;
    const startAngle = (prevEnd / total) * 2 * Math.PI;
    const endAngle = ((prevEnd + segment.value) / total) * 2 * Math.PI;

    const x1 = cx + radius * Math.sin(startAngle);
    const y1 = cy - radius * Math.cos(startAngle);
    const x2 = cx + radius * Math.sin(endAngle);
    const y2 = cy - radius * Math.cos(endAngle);
    const largeArc = endAngle - startAngle > Math.PI ? 1 : 0;

    const path = `M ${x1} ${y1} A ${radius} ${radius} 0 ${largeArc} 1 ${x2} ${y2}`;
    const color = DONUT_COLORS[i % DONUT_COLORS.length];
    return [...acc, { path, color, label: segment.label, value: segment.value }];
  }, []);

  return (
    <div className="chart-card">
      <h3>{props.title}</h3>
      <div style={{ display: "flex", gap: "20px", alignItems: "center" }}>
        <svg viewBox="0 0 160 160" style={{ width: "160px", height: "160px" }}>
          {arcs.map((arc, i) => (
            <path
              key={i}
              d={arc.path}
              fill="none"
              stroke={arc.color}
              strokeWidth={strokeWidth}
            />
          ))}
        </svg>
        <div>
          {arcs.map((arc, i) => (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: "6px", marginBottom: "4px" }}>
              <span style={{ width: "12px", height: "12px", background: arc.color, borderRadius: "2px" }} />
              <span style={{ fontSize: "var(--comp-font-size)", color: "var(--text-primary)" }}>
                {arc.label}: {arc.value}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}