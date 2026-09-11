import { Link } from "react-router-dom";

export function HomePage() {
  return (
    <section className="hero page-width">
      <div className="hero-copy">
        <p className="eyebrow">Plan with clarity</p>
        <h1>A trip plan that reads like a day you can actually enjoy.</h1>
        <p className="hero-summary">
          Describe where you want to go, when you are travelling, and what matters to you. We
          will turn it into a structured day-by-day itinerary.
        </p>
        <Link className="button button-primary" to="/plan">
          Start planning
        </Link>
      </div>
      <div className="hero-card" aria-label="Planning steps">
        <p className="card-kicker">Your idea, made practical</p>
        <ol>
          <li>Share your destination and dates</li>
          <li>Add interests, pace, and budget</li>
          <li>Review a clear daily itinerary</li>
        </ol>
      </div>
    </section>
  );
}
