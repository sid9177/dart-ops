import type { RendererProps } from "@copilotkit/a2ui-renderer";

interface KpiCardProps {
  label: string;
  value: string;
  delta?: string;
}

export function KpiCard({ props }: RendererProps<KpiCardProps>) {
  return (
    <div className="kpi-card">
      <p className="kpi-label">{props.label}</p>
      <p className="kpi-value">{props.value}</p>
      {props.delta && <p className="kpi-delta">{props.delta}</p>}
    </div>
  );
}