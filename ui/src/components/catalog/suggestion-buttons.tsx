import type { RendererProps } from "@copilotkit/a2ui-renderer";

interface SuggestionButtonsProps {
  prompts: string[];
}

export function SuggestionButtons({
  props,
  dispatch,
}: RendererProps<SuggestionButtonsProps>) {
  return (
    <div className="suggestion-buttons">
      {props.prompts.map((prompt, i) => (
        <button
          key={i}
          type="button"
          className="suggestion-button"
          onClick={() => dispatch?.({ type: "submitMessage", message: prompt })}
        >
          {prompt}
        </button>
      ))}
    </div>
  );
}