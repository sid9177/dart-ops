"use client";

import { useFrontendTool, useHumanInTheLoop } from "@copilotkit/react-core/v2";
import { z } from "zod";
import type { SurfaceSpec } from "@/lib/surface-types";

const surfaceSchema = z.object({
  surfaceId: z.string(),
  component: z.string(),
  props: z.record(z.unknown()),
});

const approvalSchema = z.object({
  question: z.string(),
  draftSummary: z.string(),
});

interface SurfaceBridgeProps {
  onSurface: (surface: SurfaceSpec) => void;
  onApproval: (approved: boolean) => void;
}

export function SurfaceBridge({ onSurface, onApproval }: SurfaceBridgeProps) {
  useFrontendTool({
    name: "register_surface",
    description:
      "Register a surface to be rendered in the canvas pane. Call once per surface emitted via A2UI.",
    parameters: z.object({ surface: surfaceSchema }),
    handler: async ({ surface }) => {
      onSurface(surface as unknown as SurfaceSpec);
      return "Surface registered in canvas.";
    },
  });

  useHumanInTheLoop({
    name: "approval_gate",
    description:
      "Ask the user for approval before concluding. Renders an approval card in chat with Approve/Decline buttons.",
    parameters: approvalSchema,
    render: ({ args, status, respond }) => {
      const { question, draftSummary } = args as z.infer<typeof approvalSchema>;
      if (status !== "executing" && status !== "inProgress") {
        return null;
      }
      return (
        <div className="approval-gate">
          <h4>{question}</h4>
          <p>{draftSummary}</p>
          <div className="approval-gate-actions">
            <button
              type="button"
              className="approve"
              onClick={() => {
                onApproval(true);
                respond?.({ approved: true });
              }}
            >
              Approve
            </button>
            <button
              type="button"
              className="decline"
              onClick={() => {
                onApproval(false);
                respond?.({ approved: false });
              }}
            >
              Decline
            </button>
          </div>
        </div>
      );
    },
  });

  return null;
}