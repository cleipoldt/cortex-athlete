import { apiGet } from "./client";

export type HealthResponse = {
  status: "ok";
};

export function getHealth(): Promise<HealthResponse> {
  return apiGet<HealthResponse>("/health");
}