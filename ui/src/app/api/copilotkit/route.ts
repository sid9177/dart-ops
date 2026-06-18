import {
  CopilotRuntime,
  createCopilotHonoHandler,
  InMemoryAgentRunner,
} from "@copilotkit/runtime/v2";
import { HttpAgent } from "@ag-ui/client";
import { handle } from "hono/vercel";
import { DEFAULT_AGENT_ID, resolveAgentUrl } from "@/lib/runtime-config";

const runtime = new CopilotRuntime({
  agents: {
    [DEFAULT_AGENT_ID]: new HttpAgent({
      url: resolveAgentUrl(process.env.COPILOTKIT_AGENT_URL),
    }),
  },
  runner: new InMemoryAgentRunner(),
  a2ui: {},
});

const app = createCopilotHonoHandler({
  runtime,
  basePath: "/api/copilotkit",
});

export const GET = handle(app);
export const POST = handle(app);
export const PATCH = handle(app);
export const DELETE = handle(app);