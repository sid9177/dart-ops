import { AppShell } from "@/components/app-shell";

export default function Page() {
  return (
    <AppShell
      runtimeLabel="Local sample runtime"
      chat={<div className="panel-placeholder">Copilot chat loading</div>}
      canvas={<div className="panel-placeholder">Artifact workspace</div>}
      status={<div className="panel-placeholder">Agent activity</div>}
    />
  );
}
