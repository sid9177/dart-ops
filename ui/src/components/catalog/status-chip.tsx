import type { RendererProps } from "@copilotkit/a2ui-renderer";

interface StatusChipProps {
  label: string;
  state: "queued" | "running" | "complete" | "error";
}

export function StatusChip({ props }: RendererProps<StatusChipProps>) {
  return (
    <div className="status-chip">
      <span className={`status-chip-dot ${props.state}`} />
      <span>{props.label}</span>
    </div>
  );
}