"use client";

import { useState } from "react";
import Image from "next/image";
import { CopilotSidebar } from "@copilotkit/react-core/v2";
import { CanvasPane } from "@/components/canvas-pane";
import { SurfaceBridge } from "@/components/surface-bridge";
import {
  createInitialCanvasState,
  applySurfaceRegistration,
  type SurfaceSpec,
} from "@/lib/surface-types";
import { DEFAULT_AGENT_ID } from "@/lib/runtime-config";

export default function Page() {
  const [canvasState, setCanvasState] = useState(createInitialCanvasState);

  const handleSurface = (surface: SurfaceSpec) => {
    setCanvasState((state) => applySurfaceRegistration(state, surface));
  };

  const handleApproval = (_approved: boolean) => {
    // Approval is handled by the respond() callback in the render function
  };

  return (
    <>
      <SurfaceBridge onSurface={handleSurface} onApproval={handleApproval} />
      <main className="app-shell">
        <header className="app-header">
          <div className="brand-lockup">
            <div className="brand-logo-frame">
              <Image
                src="/brand/citi-logo.svg"
                alt="Citi"
                width={72}
                height={42}
                className="brand-logo"
                unoptimized
              />
            </div>
            <div>
              <p className="eyebrow">Analytics and reporting</p>
              <h1>Ops Risk Reporting Workspace</h1>
            </div>
          </div>
          <div className="runtime-pill" aria-label="Runtime connection">
            <span className="runtime-dot" />
            Local ADK runtime
          </div>
        </header>
        <section className="workspace-layout">
          <aside className="chat-column">
            <CopilotSidebar
              agentId={DEFAULT_AGENT_ID}
              defaultOpen={true}
              labels={{
                welcomeMessageText:
                  "Ask for analysis, report drafts, data tables, charts, or file links.",
              }}
            />
          </aside>
          <section className="canvas-column">
            <CanvasPane state={canvasState} />
          </section>
        </section>
      </main>
    </>
  );
}