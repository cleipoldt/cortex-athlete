import { NavLink, Route, Routes } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import CognitiveTest from "./pages/CognitiveTest";
import LogSession from "./pages/LogSession";

export default function App() {
  return (
    <div className="app">
      <header>
        <h1>Cortex Athlete</h1>
        <nav>
          <NavLink to="/">Dashboard</NavLink>
          <NavLink to="/test">Cognitive Test</NavLink>
          <NavLink to="/log">Log Session</NavLink>
        </nav>
      </header>

      <main>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/test" element={<CognitiveTest />} />
          <Route path="/log" element={<LogSession />} />
          <Route path="*" element={<p>Page not found.</p>} />
        </Routes>
      </main>
    </div>
  );
}