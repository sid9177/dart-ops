import Image from "next/image";
import type { ReactNode } from "react";

interface AppShellProps {
  runtimeLabel: string;
  chat: ReactNode;
  canvas: ReactNode;
  status: ReactNode;
}

export function AppShell({ runtimeLabel, chat, canvas, status }: AppShellProps) {
  return (
    <main className="app-shell">
      <header className="app-header">
        <div className="brand-lockup">
          <div className="brand-logo-frame">
            <Image
              src="/brand/citi-logo.svg"
              alt=""
              width={72}
              height={28}
              className="brand-logo"
              unoptimized
            />
            <span className="brand-fallback">Citi | Ops Risk</span>
          </div>
          <div>
            <p className="eyebrow">Analytics and reporting</p>
            <h1>Reporting Analyst Workspace</h1>
          </div>
        </div>
        <div className="runtime-pill" aria-label="Runtime connection">
          <span className="runtime-dot" />
          {runtimeLabel}
        </div>
      </header>

      <section className="workspace-layout">
        <aside className="chat-column" aria-label="Copilot chat panel">
          {chat}
        </aside>
        <section className="canvas-column" aria-label="Artifact workspace">
          {canvas}
        </section>
        <aside className="status-column" aria-label="Agent activity rail">
          {status}
        </aside>
      </section>
    </main>
  );
}
