import { useEffect, useState } from "react";

export default function Dashboard() {
  const [backendStatus, setBackendStatus] = useState("checking...");

  useEffect(() => {
    async function checkHealth() {
      try {
        const response = await fetch("http://127.0.0.1:8000/health");
        const data = await response.json();
        setBackendStatus(data.status);
      } catch (error) {
        console.error("Health check failed:", error);
        setBackendStatus("unreachable");
      }
    }

    checkHealth();
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Backend status: {backendStatus}</p>
    </div>
  );
}

