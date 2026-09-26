import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { useState } from "react";
import { expect, it, vi } from "vitest";
import { TripDateInput } from "./TripDateInput";

function ControlledDate({ onSelect = () => {} }: { onSelect?: () => void }) {
  const [date, setDate] = useState("");
  return <TripDateInput label="Start date" value={date} onChange={setDate}
    onSelect={onSelect} min="2026-09-11" max="2026-09-24" />;
}

it("keeps an English ISO date control under a Chinese document locale", () => {
  document.documentElement.lang = "zh-CN";
  render(<ControlledDate />);
  const input = screen.getByRole("textbox", { name: "Start date" });
  expect(input).toHaveAttribute("type", "text");
  fireEvent.change(input, { target: { value: "2026-09-12" } });
  expect(input).toHaveValue("2026-09-12");
  fireEvent.click(screen.getByRole("button", { name: "Choose Start date" }));
  expect(screen.getByText("September 2026")).toBeInTheDocument();
  document.documentElement.lang = "en";
});

it("supports calendar keyboard selection, Escape, and focus return", () => {
  const onSelect = vi.fn();
  render(<ControlledDate onSelect={onSelect} />);
  const trigger = screen.getByRole("button", { name: "Choose Start date" });
  fireEvent.click(trigger);
  const day = screen.getByRole("button", { name: "September 12, 2026" });
  day.focus();
  fireEvent.keyDown(day, { key: "ArrowRight" });
  expect(screen.getByRole("button", { name: "September 13, 2026" })).toHaveFocus();
  fireEvent.keyDown(document.activeElement!, { key: "Enter" });
  expect(screen.getByRole("textbox", { name: "Start date" })).toHaveValue("2026-09-13");
  expect(onSelect).toHaveBeenCalledOnce();
  expect(trigger).toHaveFocus();
  fireEvent.click(trigger);
  fireEvent.keyDown(trigger, { key: "Escape" });
  expect(screen.queryByRole("dialog", { name: "Start date calendar" })).toBeNull();
  expect(trigger).toHaveFocus();
});

it("disables dates outside the authoritative window", () => {
  render(<ControlledDate />);
  fireEvent.click(screen.getByRole("button", { name: "Choose Start date" }));
  expect(screen.getByRole("button", { name: "September 10, 2026" })).toBeDisabled();
  expect(screen.getByRole("button", { name: "September 24, 2026" })).toBeEnabled();
  expect(screen.getByRole("button", { name: "September 25, 2026" })).toBeDisabled();
});

it("aligns English weekday headings with real calendar weekdays", () => {
  render(<ControlledDate />);
  fireEvent.click(screen.getByRole("button", { name: "Choose Start date" }));
  expect(screen.getByText("Tue")).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "September 1, 2026" })).toHaveStyle({ gridColumnStart: "3" });
});

it("moves keyboard focus across a month boundary within the allowed window", async () => {
  render(<TripDateInput label="Start date" value="2026-09-30" onChange={() => {}}
    min="2026-09-20" max="2026-10-05" />);
  fireEvent.click(screen.getByRole("button", { name: "Choose Start date" }));
  const lastSeptemberDay = screen.getByRole("button", { name: "September 30, 2026" });
  lastSeptemberDay.focus();
  fireEvent.keyDown(lastSeptemberDay, { key: "ArrowRight" });
  await waitFor(() => expect(screen.getByRole("button", { name: "October 1, 2026" })).toHaveFocus());
});
