import { Link } from "react-router-dom";

export function NotFoundPage() {
  return (
    <main className="page-width not-found">
      <p className="eyebrow">404</p>
      <h1>That route is not on the itinerary.</h1>
      <Link className="text-link" to="/">
        Return home
      </Link>
    </main>
  );
}
