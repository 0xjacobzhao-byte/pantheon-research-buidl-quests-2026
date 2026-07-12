// Shared verdict → color mapping for the five-model LLM views.

const VERDICT_COLORS: Record<string, string> = {
  excellent: "#16a34a",
  strong: "#16a34a",
  positive: "#16a34a",
  wide: "#16a34a",
  high: "#16a34a",
  good: "#22c55e",
  moderate: "#f59e0b",
  neutral: "#f59e0b",
  fair: "#f59e0b",
  narrow: "#f59e0b",
  mixed: "#f59e0b",
  weak: "#dc2626",
  poor: "#dc2626",
  negative: "#dc2626",
  none: "#6b7280",
  unknown: "#6b7280",
  not_assessed: "#6b7280",
};

export function verdictColor(verdict: string | null | undefined): string {
  if (!verdict) return "#6b7280";
  const key = verdict.toLowerCase().replace(/\s+/g, "_");
  return VERDICT_COLORS[key] ?? "#3b82f6";
}
