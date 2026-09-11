export function RawJsonView({ value }: { value: unknown }) {
  return (
    <section className="json-panel" aria-labelledby="raw-json-title">
      <div className="json-panel-header">
        <h2 id="raw-json-title">Raw response</h2>
        <span>JSON</span>
      </div>
      <pre>{JSON.stringify(value, null, 2)}</pre>
    </section>
  );
}
