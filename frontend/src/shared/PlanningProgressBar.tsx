interface Props { label: string; value: number; state: string; message?: string }

export function PlanningProgressBar({ label, value, state, message }: Props) {
  return <div className="planning-progress" data-state={state}>
    <div className="planning-progress-track" role="progressbar" aria-label={label}
      aria-valuemin={0} aria-valuemax={1} aria-valuenow={value}
      aria-valuetext={message || state}>
      <div className="planning-progress-fill" style={{ width: `${value * 100}%` }} />
    </div>
    <small>Approximate workflow progress, not a time estimate.</small>
  </div>;
}
