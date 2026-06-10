"use client";

import { useFrontendTool } from "@copilotkit/react-core/v2";
import { z } from "zod";
import type { ArtifactEvent, StatusEvent } from "@/lib/artifacts";

interface CopilotAgentBridgeProps {
  onArtifact: (event: ArtifactEvent) => void;
  onStatus: (event: StatusEvent) => void;
}

const artifactRowSchema = z.record(
  z.union([z.string(), z.number(), z.boolean(), z.null()]),
);

const fileLinkSchema = z.object({
  label: z.string(),
  href: z.string(),
});

const artifactSchema = z.discriminatedUnion("type", [
  z.object({
    type: z.literal("markdown"),
    title: z.string(),
    content: z.string(),
  }),
  z.object({
    type: z.literal("data-table"),
    rows: z.array(artifactRowSchema),
  }),
  z.object({
    type: z.literal("chart"),
    series: z.array(
      z.object({
        label: z.string(),
        value: z.number(),
      }),
    ),
  }),
  z.object({
    type: z.literal("report"),
    reportTitle: z.string(),
    sections: z.array(
      z.object({
        heading: z.string(),
        body: z.string(),
      }),
    ),
    files: z.array(fileLinkSchema).optional(),
  }),
  z.object({
    type: z.literal("file-link"),
    files: z.array(fileLinkSchema),
  }),
]);

const statusSchema = z.object({
  label: z.string(),
  state: z.enum(["queued", "running", "complete", "error"]),
});

export function CopilotAgentBridge({
  onArtifact,
  onStatus,
}: CopilotAgentBridgeProps) {
  useFrontendTool({
    name: "render_artifact",
    description:
      "Render generated analytics or reporting output in the main artifact canvas.",
    parameters: z.object({ artifact: artifactSchema }),
    handler: async ({ artifact }: { artifact: ArtifactEvent }) => {
      onArtifact(artifact);
      return "Artifact rendered in the reporting workspace.";
    },
  });

  useFrontendTool({
    name: "append_status",
    description:
      "Append a concise agent progress event to the activity trace rail.",
    parameters: z.object({ status: statusSchema }),
    handler: async ({ status }: { status: StatusEvent }) => {
      onStatus(status);
      return "Status appended to the activity rail.";
    },
  });

  return null;
}
