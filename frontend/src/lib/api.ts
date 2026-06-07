import type { CsvPreview, CsvResult, TextResult } from "../types";

const BASE = "/api";

export async function analyzeText(text: string): Promise<TextResult> {
  const res = await fetch(`${BASE}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: "Request failed" }));
    throw new Error((err as { error: string }).error ?? "Request failed");
  }
  return res.json() as Promise<TextResult>;
}

export async function previewCsv(file: File): Promise<CsvPreview> {
  const form = new FormData();
  form.append("csv_file", file);
  const res = await fetch(`${BASE}/csv/preview`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: "Request failed" }));
    throw new Error((err as { error: string }).error ?? "Request failed");
  }
  return res.json() as Promise<CsvPreview>;
}

export async function analyzeCsvStream(
  filename: string,
  column: string,
  onProgress: (percent: number, message: string) => void
): Promise<CsvResult> {
  const res = await fetch(`${BASE}/csv/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ filename, column }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: "Request failed" }));
    throw new Error((err as { error: string }).error ?? "Request failed");
  }
  if (!res.body) throw new Error("No response body");

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    // SSE events are separated by double newlines
    const parts = buffer.split("\n\n");
    buffer = parts.pop() ?? "";

    for (const part of parts) {
      for (const line of part.split("\n")) {
        if (!line.startsWith("data: ")) continue;
        const raw = line.slice(6).trim();
        if (!raw) continue;

        const event = JSON.parse(raw) as {
          type: string;
          percent?: number;
          message?: string;
          result?: CsvResult;
        };

        if (event.type === "progress" && event.percent != null && event.message) {
          onProgress(event.percent, event.message);
        } else if (event.type === "complete" && event.result) {
          return event.result;
        } else if (event.type === "error") {
          throw new Error(event.message ?? "Analysis failed");
        }
      }
    }
  }

  throw new Error("Stream ended unexpectedly — please try again");
}
