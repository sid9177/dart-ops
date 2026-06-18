import type { RendererProps } from "@copilotkit/a2ui-renderer";

interface MarkdownSummaryProps {
  title: string;
  content: string;
}

export function MarkdownSummary({
  props,
}: RendererProps<MarkdownSummaryProps>) {
  return (
    <div className="markdown-summary">
      <h3>{props.title}</h3>
      <p>{props.content}</p>
    </div>
  );
}