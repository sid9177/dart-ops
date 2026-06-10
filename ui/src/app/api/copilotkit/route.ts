import {
  CopilotRuntime,
  EmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { HttpAgent } from "@ag-ui/client";
import type { NextRequest } from "next/server";
import { DEFAULT_AGENT_ID, resolveAgentUrl } from "@/lib/runtime-config";

const serviceAdapter = new EmptyAdapter();

const runtime = new CopilotRuntime({
  agents: {
    [DEFAULT_AGENT_ID]: new HttpAgent({
      url: resolveAgentUrl(process.env.COPILOTKIT_AGENT_URL),
    }),
  },
});

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
