"use client";

import { useState } from "react";
import { AppShell } from "@/components/app-shell";
import { ArtifactCanvas } from "@/components/artifact-canvas";
import { ChatPanel } from "@/components/chat-panel";
import { CopilotAgentBridge } from "@/components/copilot-agent-bridge";
import { StatusRail } from "@/components/status-rail";
import {
  applyArtifactEvent,
  applyStatusEvent,
  createInitialArtifactState,
} from "@/lib/artifacts";

export default function Page() {
  const [artifactState, setArtifactState] = useState(createInitialArtifactState);

  return (
    <>
      <CopilotAgentBridge
        onArtifact={(event) =>
          setArtifactState((state) => applyArtifactEvent(state, event))
        }
        onStatus={(event) =>
          setArtifactState((state) => applyStatusEvent(state, event))
        }
      />
      <AppShell
        runtimeLabel="Local sample runtime"
        chat={<ChatPanel />}
        canvas={<ArtifactCanvas state={artifactState} />}
        status={<StatusRail statusItems={artifactState.statusItems} />}
      />
    </>
  );
}
