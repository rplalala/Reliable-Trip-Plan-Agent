import { Fragment } from "react";
import type { Activity, Itinerary, Transfer, MinimumDailyCoverage } from "../types";

function TransferCard({ transfer }: { transfer: Transfer }) {
  const label = { WALK: "Walk", TRANSIT: "Public transport", DRIVE: "Car transport" }[transfer.mode];
  return (
    <aside className="activity-card" aria-label="Transfer">
      <p>{label}: {transfer.provider_duration_seconds === null ? "Time unknown" :
        `about ${Math.ceil(transfer.provider_duration_seconds / 60)} min`}
        {" · "}{transfer.distance_meters === null ? "Distance unknown" :
          `${(transfer.distance_meters / 1000).toFixed(1)} km`}</p>
      {transfer.reserve_seconds > 0 && <p>Allow an additional {Math.ceil(transfer.reserve_seconds / 60)} min {transfer.mode === "DRIVE" ? "for pickup/drop-off." : "as a conservative scheduling reserve; route unverified."}</p>}
      <p>{transfer.validation_state === "CONFIRMED" ? "Transfer conflict remains." :
        transfer.validation_state === "UNKNOWN" ? "Transfer feasibility is unverified." :
          "Based on the adopted route estimate; not a guarantee."}</p>
      {transfer.unknowns.map((value, index) => <p key={index}>{value}</p>)}
    </aside>
  );
}

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

export function ItineraryView({ itinerary, minimumCoverage = [] }: {
  itinerary: Itinerary; minimumCoverage?: MinimumDailyCoverage[];
}) {
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
      {minimumCoverage.filter(row => row.status !== "satisfied").map(row => (
        <p key={row.date} role={row.status === "missing" ? "status" : undefined}>
          {row.date}: {row.status === "missing"
            ? "Minimum daily coverage remains unmet: no countable main visit was arranged."
            : row.status === "exempt"
              ? "Exempt from minimum sightseeing coverage because of a fixed user commitment."
              : "Minimum daily coverage could not be fully assessed."}
        </p>
      ))}
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
                  <Fragment key={activity.activity_id}>
                    {(itinerary.transfers ?? []).filter(t => t.to_activity_id === activity.activity_id)
                      .map(t => <TransferCard key={`${t.from_activity_id}:${t.to_activity_id}`} transfer={t} />)}
                    <ActivityCard activity={activity} />
                  </Fragment>
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
