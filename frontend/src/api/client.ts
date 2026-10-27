const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
if (!API_BASE_URL) {
    throw new Error("VITE_API_BASE_URL is not set. Add it to frontend/.env.development.");
}

export class ApiError extends Error {
    status: number;

    constructor(status: number, message: string){
        super(message);
        this.name = "ApiError";
        this.status = status;
    }
}

export async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);

  if (!response.ok) {
    throw new ApiError(response.status, `GET ${path} failed with status ${response.status}`);
  }

  return (await response.json()) as T;
}