import type { Activity, Itinerary } from "../types";

function formatTime(value: string): string {
  const match = value.match(/T(\d{2}):(\d{2})/);
  return match ? `${match[1]}:${match[2]}` : value;
}

function ActivityCard({ activity }: { activity: Activity }) {
  return (
    <article className="activity-card">
      <div className="activity-time">
        {formatTime(activity.start_time)}–{formatTime(activity.end_time)}
      </div>
      <div className="activity-content">
        <h4>{activity.title}</h4>
        {activity.place_name && <p className="activity-place">{activity.place_name}</p>}
        {activity.location && <p>{activity.location}</p>}
        {activity.notes && <p>{activity.notes}</p>}
        {activity.estimated_cost && (
          <p className="cost">
            Estimated cost: {activity.estimated_cost.currency} {activity.estimated_cost.amount}
          </p>
        )}
      </div>
    </article>
  );
}

export function ItineraryView({ itinerary }: { itinerary: Itinerary }) {
  return (
    <section className="itinerary" aria-labelledby="itinerary-title">
      <header className="itinerary-header">
        <div>
          <p className="eyebrow">Your itinerary</p>
          <h2 id="itinerary-title">{itinerary.destination}</h2>
        </div>
        <p>
          {itinerary.start_date} to {itinerary.end_date}
        </p>
      </header>
      <div className="itinerary-days">
        {itinerary.days.map((day, index) => (
          <section className="itinerary-day" key={day.date}>
            <div className="day-heading">
              <span>Day {index + 1}</span>
              <h3>{day.date}</h3>
            </div>
            <div className="activity-list">
              {day.activities.length > 0 ? (
                day.activities.map((activity) => (
                  <ActivityCard activity={activity} key={activity.activity_id} />
                ))
              ) : (
                <p className="empty-day">No scheduled activities.</p>
              )}
            </div>
          </section>
        ))}
      </div>
      {!!itinerary.reference_recommendations?.length && (
        <section aria-label="Optional reference recommendations">
          <h3>Optional references — not scheduled</h3>
          <p>Additional options to consider independently. No bookings have been made.</p>
          {itinerary.reference_recommendations.map((reference, index) => (
            <article className="activity-card" key={reference.source_place_id ?? index}>
              <div className="activity-content">
                <h4>{reference.place_name}</h4>
                <p>{reference.reason}</p>
                {reference.associated_day && <p>Suggested day: {reference.associated_day}</p>}
                {reference.area && <p>{reference.area}</p>}
                <p>{reference.source_ref
                  ? "Linked to supplied place information; current details may be uncertain."
                  : "Model-generated suggestion; not live-verified."}</p>
                {reference.uncertainty && <p>{reference.uncertainty}</p>}
              </div>
            </article>
          ))}
        </section>
      )}
      <p className="field-help">
        Weather forecasts, when used, are provided by <a href="https://open-meteo.com/">Open-Meteo</a>
        {" "}under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.
        Forecasts may be incomplete and are not guarantees.
      </p>
    </section>
  );
}
