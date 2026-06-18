import type { RendererProps } from "@copilotkit/a2ui-renderer";

interface ChartBarProps {
  title: string;
  series: { label: string; value: number }[];
}

export function ChartBar({ props }: RendererProps<ChartBarProps>) {
  const max = Math.max(...props.series.map((s) => s.value), 1);
  return (
    <div className="chart-card">
      <h3>{props.title}</h3>
      {props.series.map((point) => {
        const widthPct = (point.value / max) * 100;
        return (
          <div className="chart-bar-row" key={point.label}>
            <span>{point.label}</span>
            <div className="chart-bar-track">
              <span
                className="chart-bar-fill"
                style={{ width: `${widthPct}%` }}
              />
            </div>
            <strong>{point.value}</strong>
          </div>
        );
      })}
    </div>
  );
}