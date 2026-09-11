import { NavLink, Outlet } from "react-router-dom";

export function ProductLayout() {
  return (
    <div className="app-shell product-shell">
      <header className="site-header">
        <NavLink className="brand" to="/" aria-label="Reliable Trip Planner home">
          <span className="brand-mark" aria-hidden="true">
            R
          </span>
          <span>Reliable Trip Planner</span>
        </NavLink>
        <nav className="primary-nav" aria-label="Main navigation">
          <NavLink to="/" end>
            Home
          </NavLink>
          <NavLink to="/plan">Plan a trip</NavLink>
        </nav>
      </header>
      <main>
        <Outlet />
      </main>
      <footer className="site-footer">
        <p>Thoughtful itineraries, structured around your trip.</p>
      </footer>
    </div>
  );
}
