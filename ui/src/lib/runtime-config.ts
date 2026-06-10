export const DEFAULT_RUNTIME_URL = "/api/copilotkit";
export const DEFAULT_AGENT_URL = "http://127.0.0.1:8000/";
export const DEFAULT_AGENT_ID = "ops-risk-reporting";

export function resolveRuntimeUrl(value: string | undefined): string {
  return value && value.trim().length > 0 ? value : DEFAULT_RUNTIME_URL;
}

export function resolveAgentUrl(value: string | undefined): string {
  return value && value.trim().length > 0 ? value : DEFAULT_AGENT_URL;
}
