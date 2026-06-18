import { describe, expect, it } from "vitest";
import { catalogDefinitions, citiTheme } from "./catalog-definitions";

describe("catalog definitions", () => {
  it("defines all 14 components", () => {
    const names = Object.keys(catalogDefinitions);
    expect(names).toContain("StatusChip");
    expect(names).toContain("SuggestionButtons");
    expect(names).toContain("ApprovalGate");
    expect(names).toContain("MarkdownSummary");
    expect(names).toContain("DataTable");
    expect(names).toContain("ChartBar");
    expect(names).toContain("ChartColumn");
    expect(names).toContain("ChartLine");
    expect(names).toContain("ChartDonut");
    expect(names).toContain("KpiCard");
    expect(names).toContain("HeatMap");
    expect(names).toContain("ReportSection");
    expect(names).toContain("FileLink");
    expect(names).toHaveLength(13);
  });

  it("StatusChip schema validates a running state", () => {
    const result = catalogDefinitions.StatusChip.props.safeParse({
      label: "Querying data",
      state: "running",
    });
    expect(result.success).toBe(true);
  });

  it("StatusChip schema rejects invalid state", () => {
    const result = catalogDefinitions.StatusChip.props.safeParse({
      label: "Test",
      state: "invalid",
    });
    expect(result.success).toBe(false);
  });

  it("DataTable schema validates rows array", () => {
    const result = catalogDefinitions.DataTable.props.safeParse({
      rows: [{ id: 1, name: "A" }],
    });
    expect(result.success).toBe(true);
  });

  it("ChartBar schema validates series", () => {
    const result = catalogDefinitions.ChartBar.props.safeParse({
      title: "Risk by Unit",
      series: [{ label: "Payments", value: 18 }],
    });
    expect(result.success).toBe(true);
  });

  it("citiTheme has primary color matching Citi action blue", () => {
    expect(citiTheme.colors?.primary).toBe("#255BE3");
  });
});