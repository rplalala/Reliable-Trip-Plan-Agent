import type { DeveloperVersion } from "../types";

interface DeveloperPlanningFormProps {
  version: DeveloperVersion;
  requestText: string;
  referenceDate: string;
  isSubmitting: boolean;
  onRequestTextChange: (value: string) => void;
  onReferenceDateChange: (value: string) => void;
  onSubmit: () => void;
}

export function DeveloperPlanningForm({
  version,
  requestText,
  referenceDate,
  isSubmitting,
  onRequestTextChange,
  onReferenceDateChange,
  onSubmit,
}: DeveloperPlanningFormProps) {
  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onSubmit();
  }

  return (
    <form className="developer-form" onSubmit={handleSubmit}>
      <div className="developer-fields">
        <label>
          Research version
          <select value={version} disabled={isSubmitting} onChange={() => undefined}>
            <option value="v0">V0 — Plain LLM</option>
          </select>
        </label>
        <label>
          Reference date
          <input
            type="date"
            value={referenceDate}
            required
            disabled={isSubmitting}
            onChange={(event) => onReferenceDateChange(event.target.value)}
          />
        </label>
      </div>
      <label htmlFor="developer-request">Travel request</label>
      <textarea
        id="developer-request"
        value={requestText}
        rows={7}
        required
        disabled={isSubmitting}
        onChange={(event) => onRequestTextChange(event.target.value)}
        placeholder="Enter a request to inspect the V0 result."
      />
      <button
        className="button button-developer"
        type="submit"
        disabled={isSubmitting || requestText.trim().length === 0}
      >
        {isSubmitting ? "Running V0…" : "Run V0"}
      </button>
    </form>
  );
}
