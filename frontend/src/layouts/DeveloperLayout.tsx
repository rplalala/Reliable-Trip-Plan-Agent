import { NavLink, Outlet } from "react-router-dom";

export function DeveloperLayout() {
  return (
    <div className="app-shell developer-shell">
      <header className="developer-header">
        <div>
          <p className="eyebrow">Local development and research</p>
          <h1>Planner workbench</h1>
        </div>
        <nav aria-label="Developer navigation">
          <NavLink to="/dev/planner">Planner</NavLink>
          <NavLink to="/">Return to product</NavLink>
        </nav>
      </header>
      <div className="developer-warning" role="note">
        This interface exposes internal planner output. Protect or disable it before any public
        production deployment.
      </div>
      <main className="developer-main">
        <Outlet />
      </main>
    </div>
  );
}
