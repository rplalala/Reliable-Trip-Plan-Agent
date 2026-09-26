import { act, fireEvent, render, screen } from "@testing-library/react";
import { useState } from "react";
import { afterEach, expect, it, vi } from "vitest";
import { getDestinationSuggestions } from "../api";
import { DestinationCombobox } from "./DestinationCombobox";

vi.mock("../api", () => ({ getDestinationSuggestions: vi.fn() }));
const suggestions = vi.mocked(getDestinationSuggestions);
const london = { id: "1", city: "London", region: "England", country: "United Kingdom",
  country_code: "GB", label: "London, England, United Kingdom" };

function ControlledDestination() {
  const [value, setValue] = useState("");
  return <DestinationCombobox value={value} onChange={setValue} disabled={false} />;
}

afterEach(() => { vi.useRealTimers(); suggestions.mockReset(); });

it("debounces prefix search and selects a labeled city without submitting", async () => {
  vi.useFakeTimers();
  suggestions.mockResolvedValue({ source: "geodb", suggestions: [london] });
  render(<form onSubmit={event => event.preventDefault()}><ControlledDestination /></form>);
  fireEvent.change(screen.getByRole("combobox", { name: "Destination" }), { target: { value: "L" } });
  await act(async () => { vi.advanceTimersByTime(600); });
  expect(suggestions).not.toHaveBeenCalled();
  fireEvent.change(screen.getByRole("combobox", { name: "Destination" }), { target: { value: "Lon" } });
  await act(async () => { vi.advanceTimersByTime(500); });
  expect(suggestions).toHaveBeenCalledOnce();
  fireEvent.keyDown(screen.getByRole("combobox", { name: "Destination" }), { key: "ArrowDown" });
  fireEvent.keyDown(screen.getByRole("combobox", { name: "Destination" }), { key: "Enter" });
  expect(screen.getByRole("combobox", { name: "Destination" })).toHaveValue(london.label);
});

it("keeps manual entry on provider failure and ignores stale answers", async () => {
  vi.useFakeTimers();
  let finish!: (value: { source: "geodb"; suggestions: typeof london[] }) => void;
  suggestions.mockImplementationOnce(() => new Promise(resolve => { finish = resolve; }))
    .mockRejectedValueOnce(new Error("offline"));
  render(<ControlledDestination />);
  const input = screen.getByRole("combobox", { name: "Destination" });
  fireEvent.change(input, { target: { value: "Lon" } });
  await act(async () => { vi.advanceTimersByTime(500); });
  fireEvent.change(input, { target: { value: "Londonderry" } });
  await act(async () => { vi.advanceTimersByTime(1100); });
  await act(async () => finish({ source: "geodb", suggestions: [london] }));
  expect(input).toHaveValue("Londonderry");
  expect(screen.queryByRole("option", { name: london.label })).toBeNull();
  expect(screen.getByText(/You can enter a destination manually/)).toBeInTheDocument();
});

it("does not search during IME composition", async () => {
  vi.useFakeTimers();
  suggestions.mockResolvedValue({ source: "geodb", suggestions: [] });
  render(<ControlledDestination />);
  const input = screen.getByRole("combobox", { name: "Destination" });
  fireEvent.compositionStart(input);
  fireEvent.change(input, { target: { value: "Lo" } });
  await act(async () => { vi.advanceTimersByTime(600); });
  expect(suggestions).not.toHaveBeenCalled();
  fireEvent.compositionEnd(input);
  await act(async () => { vi.advanceTimersByTime(500); });
  expect(suggestions).toHaveBeenCalledOnce();
});

it("closes on Escape and searches again only after a selected label is edited", async () => {
  vi.useFakeTimers();
  suggestions.mockResolvedValue({ source: "geodb", suggestions: [london] });
  render(<ControlledDestination />);
  const input = screen.getByRole("combobox", { name: "Destination" });
  fireEvent.change(input, { target: { value: "Lon" } });
  await act(async () => { vi.advanceTimersByTime(500); });
  expect(screen.getByRole("option", { name: london.label })).toBeInTheDocument();
  fireEvent.keyDown(input, { key: "Escape" });
  expect(screen.queryByRole("option", { name: london.label })).toBeNull();
  await act(async () => { vi.advanceTimersByTime(1100); });
  fireEvent.change(input, { target: { value: "Lond" } });
  await act(async () => { vi.advanceTimersByTime(500); });
  fireEvent.click(screen.getByRole("option", { name: london.label }));
  expect(input).toHaveValue(london.label);
  await act(async () => { vi.advanceTimersByTime(2000); });
  expect(suggestions).toHaveBeenCalledTimes(2);
  fireEvent.change(input, { target: { value: "London manual" } });
  await act(async () => { vi.advanceTimersByTime(500); });
  expect(suggestions).toHaveBeenCalledTimes(3);
  expect(input).toHaveValue("London manual");
});
