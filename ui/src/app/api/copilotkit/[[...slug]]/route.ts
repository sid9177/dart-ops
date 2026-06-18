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
  a2ui: {},
});

const runtimeInfoBody = JSON.stringify({
  version: "1.55.2-next.1",
  agents: {
    [DEFAULT_AGENT_ID]: {
      name: DEFAULT_AGENT_ID,
      description: "",
    },
  },
  audioFileTranscriptionEnabled: false,
  mode: "sse",
  a2uiEnabled: true,
  openGenerativeUIEnabled: false,
});

export const GET = async () => {
  return new Response(runtimeInfoBody, {
    headers: { "Content-Type": "application/json" },
  });
};

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });
  return handleRequest(req);
};