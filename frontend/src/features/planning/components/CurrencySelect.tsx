import { useId, useState } from "react";
import { currencies } from "../currencies";

interface CurrencySelectProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
  describedBy?: string;
}

export function CurrencySelect({ value, onChange, disabled, describedBy }: CurrencySelectProps) {
  const [query, setQuery] = useState("");
  const searchId = useId();
  const choices = currencies.filter(currency =>
    currency.code === value || `${currency.code} ${currency.name}`.toLowerCase().includes(query.trim().toLowerCase()),
  );

  return <div className="currency-control">
    <label htmlFor={searchId} className="currency-search-label">Search currencies</label>
    <input id={searchId} type="search" value={query} disabled={disabled}
      onChange={event => { event.stopPropagation(); setQuery(event.target.value); }} />
    <label>Currency
      <select value={value} disabled={disabled} required aria-describedby={describedBy}
        onChange={event => onChange(event.target.value)}>
        {choices.map(currency => <option key={currency.code} value={currency.code}>
          {currency.code} — {currency.name}
        </option>)}
      </select>
    </label>
  </div>;
}
