import { useEffect, useRef, useState } from "react";

import {
  postPreferencePolish,
  type PreferencePolishContext,
  type PreferencePolishResponse,
} from "../api";

interface PreferencePolisherProps {
  text: string;
  context: PreferencePolishContext;
  onApply: (text: string) => void;
  disabled: boolean;
}

const MAX_ATTEMPTS = 3;

export function PreferencePolisher({ text, context, onApply, disabled }: PreferencePolisherProps) {
  const [response, setResponse] = useState<PreferencePolishResponse | null>(null);
  const [error, setError] = useState(false);
  const [busy, setBusy] = useState(false);
  const [attempts, setAttempts] = useState(0);
  const [undo, setUndo] = useState<{ before: string; after: string } | null>(null);
  const revision = useRef(0);
  const controller = useRef<AbortController | null>(null);
  const signature = JSON.stringify([text, context]);
  const currentSignature = useRef(signature);
  currentSignature.current = signature;

  useEffect(() => {
    revision.current += 1;
    controller.current?.abort();
    controller.current = null;
    setBusy(false);
    setResponse(null);
    setError(false);
  }, [signature]);

  useEffect(() => () => controller.current?.abort(), []);

  async function polish() {
    if (disabled || busy || !text.trim() || text.length > 4000 || attempts >= MAX_ATTEMPTS) return;
    const sourceSignature = signature;
    const sourceRevision = String(++revision.current);
    const requestController = new AbortController();
    controller.current = requestController;
    setAttempts(value => value + 1);
    setBusy(true);
    setResponse(null);
    setError(false);
    setUndo(null);
    try {
      const result = await postPreferencePolish({
        original_text: text,
        context,
        client_revision: sourceRevision,
      }, requestController.signal);
      if (requestController.signal.aborted || revision.current !== Number(sourceRevision) ||
        currentSignature.current !== sourceSignature) return;
      if (result.client_revision !== sourceRevision || result.original_text !== text) {
        setError(true);
        return;
      }
      setResponse(result);
    } catch {
      if (!requestController.signal.aborted && currentSignature.current === sourceSignature) setError(true);
    } finally {
      if (controller.current === requestController) {
        controller.current = null;
        setBusy(false);
      }
    }
  }

  function apply() {
    if (!response || response.status !== "suggested" || !response.suggested_text ||
      response.original_text !== text) return;
    const candidate = response.suggested_text;
    setUndo({ before: text, after: candidate });
    setResponse(null);
    onApply(candidate);
  }

  function undoRewrite() {
    if (!undo || text !== undo.after) return;
    onApply(undo.before);
    setUndo(null);
  }

  const available = attempts < MAX_ATTEMPTS;
  return <div className="preference-assistance">
    <div className="preference-assistance-actions">
      <button className="button button-secondary" type="button" onClick={polish}
        disabled={disabled || busy || !text.trim() || text.length > 4000 || !available}>
        {busy ? "Polishing…" : "Polish preferences"}
      </button>
      {undo && text === undo.after && <button className="button button-secondary" type="button"
        onClick={undoRewrite} disabled={disabled}>Undo rewrite</button>}
      <small>{attempts}/{MAX_ATTEMPTS} attempts used</small>
    </div>
    <p className="field-help">Review any suggestion before applying it. Your original meaning and normal planning checks still matter.</p>
    {text.length > 4000 && <p className="field-error">Polishing accepts at most 4,000 characters.</p>}
    {!available && <p className="field-help">The polish limit for this form has been reached.</p>}
    {error && <p role="alert">Polishing is unavailable. Your preferences were not changed.</p>}
    {response && <div className="preference-preview" aria-live="polite">
      {response.status === "suggested" && response.suggested_text && <>
        <div className="preference-compare">
          <section><h3>Original</h3><p>{response.original_text}</p></section>
          <section><h3>Suggested rewrite</h3><p>{response.suggested_text}</p></section>
        </div>
        <p>{response.explanation}</p>
        <div className="preference-assistance-actions">
          <button className="button button-primary" type="button" onClick={apply} disabled={disabled}>Apply rewrite</button>
          <button className="button button-secondary" type="button" onClick={() => setResponse(null)}>Dismiss</button>
        </div>
      </>}
      {response.status !== "suggested" && <>
        <p>{response.explanation}</p>
        {response.questions.map(question => <p key={question}>{question}</p>)}
        <button className="button button-secondary" type="button" onClick={() => setResponse(null)}>Dismiss</button>
      </>}
    </div>}
  </div>;
}
