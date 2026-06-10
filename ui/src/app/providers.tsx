"use client";

import { CopilotKit } from "@copilotkit/react-core/v2";
import "@copilotkit/react-core/v2/styles.css";
import "@copilotkit/react-ui/styles.css";
import { resolveRuntimeUrl } from "@/lib/runtime-config";

export function Providers({ children }: { children: React.ReactNode }) {
  const runtimeUrl = resolveRuntimeUrl(
    process.env.NEXT_PUBLIC_COPILOTKIT_RUNTIME_URL,
  );

  return <CopilotKit runtimeUrl={runtimeUrl}>{children}</CopilotKit>;
}
