import type { RendererProps } from "@copilotkit/a2ui-renderer";

interface ReportSectionProps {
  heading: string;
  body: string;
}

export function ReportSection({
  props,
}: RendererProps<ReportSectionProps>) {
  return (
    <article className="report-section">
      <h4>{props.heading}</h4>
      <p>{props.body}</p>
    </article>
  );
}