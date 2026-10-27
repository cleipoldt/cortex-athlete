import { afterEach, expect, test, vi } from "vitest";
import { ApiError, apiGet } from "./client";

afterEach(() => {
  vi.unstubAllGlobals();
});

test("apiGet returns the JSON body when the response is ok", async () => {
  const fakeFetch = vi.fn().mockResolvedValue(
    new Response(JSON.stringify({ status: "ok" }), { status: 200 })
  );
  vi.stubGlobal("fetch", fakeFetch);

  const result = await apiGet<{ status: string }>("/health");

  expect(result).toEqual({ status: "ok" });
  expect(fakeFetch).toHaveBeenCalledWith("http://127.0.0.1:8000/health");
});

test("apiGet throws an ApiError with the status code when the response is not ok", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: "Not Found" }), { status: 404 }))
  );

  const error = await apiGet("/missing").catch((e) => e);

  expect(error).toBeInstanceOf(ApiError);
  expect((error as ApiError).status).toBe(404);
});

test("apiGet passes network failures through without wrapping them", async () => {
  vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));

  const error = await apiGet("/health").catch((e) => e);

  expect(error).toBeInstanceOf(TypeError);
  expect(error).not.toBeInstanceOf(ApiError);
});
