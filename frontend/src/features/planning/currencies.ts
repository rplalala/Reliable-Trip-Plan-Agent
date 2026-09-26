export const currencies = [
  { code: "AUD", name: "Australian dollar" },
  { code: "USD", name: "US dollar" },
  { code: "EUR", name: "Euro" },
  { code: "GBP", name: "British pound" },
  { code: "CNY", name: "Chinese yuan" },
  { code: "JPY", name: "Japanese yen" },
  { code: "CAD", name: "Canadian dollar" },
  { code: "NZD", name: "New Zealand dollar" },
  { code: "SGD", name: "Singapore dollar" },
  { code: "HKD", name: "Hong Kong dollar" },
  { code: "CHF", name: "Swiss franc" },
  { code: "KRW", name: "South Korean won" },
  { code: "INR", name: "Indian rupee" },
  { code: "THB", name: "Thai baht" },
  { code: "MYR", name: "Malaysian ringgit" },
  { code: "IDR", name: "Indonesian rupiah" },
  { code: "VND", name: "Vietnamese dong" },
  { code: "PHP", name: "Philippine peso" },
  { code: "AED", name: "UAE dirham" },
  { code: "ZAR", name: "South African rand" },
] as const;

export function isListedCurrency(value: string): boolean {
  return currencies.some(currency => currency.code === value);
}
