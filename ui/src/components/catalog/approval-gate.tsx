import type { RendererProps } from "@copilotkit/a2ui-renderer";

interface ApprovalGateProps {
  question: string;
  draftSummary: string;
}

export function ApprovalGate({
  props,
  dispatch,
}: RendererProps<ApprovalGateProps>) {
  return (
    <div className="approval-gate">
      <h4>{props.question}</h4>
      <p>{props.draftSummary}</p>
      <div className="approval-gate-actions">
        <button
          type="button"
          className="approve"
          onClick={() => dispatch?.({ type: "approve", value: true })}
        >
          Approve
        </button>
        <button
          type="button"
          className="decline"
          onClick={() => dispatch?.({ type: "approve", value: false })}
        >
          Decline
        </button>
      </div>
    </div>
  );
}