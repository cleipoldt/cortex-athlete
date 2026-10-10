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