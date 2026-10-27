import { useEffect, useState } from "react";
import { getHealth } from "../api/health";

export default function Dashboard() {
  const [backendStatus, setBackendStatus] = useState("checking...");

  useEffect(() => {
    async function checkHealth() {
      try {
        const data = await getHealth();
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

