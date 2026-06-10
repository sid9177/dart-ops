import { describe, expect, it } from "vitest";
import {
  DEFAULT_AGENT_ID,
  DEFAULT_AGENT_URL,
  DEFAULT_RUNTIME_URL,
  resolveAgentUrl,
  resolveRuntimeUrl,
} from "./runtime-config";

describe("runtime config", () => {
  it("uses stable defaults for local development", () => {
    expect(DEFAULT_RUNTIME_URL).toBe("/api/copilotkit");
    expect(DEFAULT_AGENT_URL).toBe("http://127.0.0.1:8000/");
    expect(DEFAULT_AGENT_ID).toBe("ops-risk-reporting");
  });

  it("resolves a public runtime URL with a fallback", () => {
    expect(resolveRuntimeUrl(undefined)).toBe("/api/copilotkit");
    expect(resolveRuntimeUrl("")).toBe("/api/copilotkit");
    expect(resolveRuntimeUrl("http://localhost:3000/api/copilotkit")).toBe(
      "http://localhost:3000/api/copilotkit",
    );
  });

  it("resolves the downstream AG-UI agent URL with a fallback", () => {
    expect(resolveAgentUrl(undefined)).toBe("http://127.0.0.1:8000/");
    expect(resolveAgentUrl("")).toBe("http://127.0.0.1:8000/");
    expect(resolveAgentUrl("http://localhost:8000/")).toBe(
      "http://localhost:8000/",
    );
  });
});
