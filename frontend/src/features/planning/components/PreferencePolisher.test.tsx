import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { useState } from "react";
import { afterEach, expect, it, vi } from "vitest";
import { postPreferencePolish } from "../api";
import { PreferencePolisher } from "./PreferencePolisher";

vi.mock("../api", () => ({ postPreferencePolish: vi.fn() }));
const polish = vi.mocked(postPreferencePolish);

function ControlledPolisher() {
  const [text, setText] = useState("I like climbing mountain, visiting a zoo, and a rich trip.");
  const [destination, setDestination] = useState("London");
  return <>
    <textarea aria-label="Preferences" value={text} onChange={event => setText(event.target.value)} />
    <button onClick={() => setDestination("Paris")}>Change destination</button>
    <PreferencePolisher text={text} context={{ destination }} onApply={setText} disabled={false} />
  </>;
}

afterEach(() => polish.mockReset());

it("previews a reviewed rewrite and applies or undoes it only by explicit action", async () => {
  polish.mockImplementation(async request => ({ status: "suggested", original_text: request.original_text,
    suggested_text: "I enjoy mountain climbing, would like to visit a zoo, and prefer a varied trip.",
    explanation: "Clarified the wishes.", questions: [], client_revision: request.client_revision }));
  render(<ControlledPolisher />);
  expect(polish).not.toHaveBeenCalled();
  fireEvent.click(screen.getByRole("button", { name: "Polish preferences" }));
  expect(await screen.findByText("Clarified the wishes.")).toBeInTheDocument();
  expect(screen.getByLabelText("Preferences")).toHaveValue("I like climbing mountain, visiting a zoo, and a rich trip.");
  fireEvent.click(screen.getByRole("button", { name: "Apply rewrite" }));
  expect(screen.getByLabelText("Preferences")).toHaveValue("I enjoy mountain climbing, would like to visit a zoo, and prefer a varied trip.");
  fireEvent.click(screen.getByRole("button", { name: "Undo rewrite" }));
  expect(screen.getByLabelText("Preferences")).toHaveValue("I like climbing mountain, visiting a zoo, and a rich trip.");
  expect(polish).toHaveBeenCalledOnce();
});

it("drops a late suggestion after the trip context changes", async () => {
  let finish!: (value: Awaited<ReturnType<typeof postPreferencePolish>>) => void;
  polish.mockImplementation(() => new Promise(resolve => { finish = resolve; }));
  render(<ControlledPolisher />);
  fireEvent.click(screen.getByRole("button", { name: "Polish preferences" }));
  const request = polish.mock.calls[0][0];
  fireEvent.click(screen.getByRole("button", { name: "Change destination" }));
  finish({ status: "suggested", original_text: request.original_text,
    suggested_text: "Unwanted stale rewrite", explanation: "Stale", questions: [],
    client_revision: request.client_revision });
  await waitFor(() => expect(screen.queryByText("Unwanted stale rewrite")).toBeNull());
  expect(screen.queryByRole("button", { name: "Apply rewrite" })).toBeNull();
});

it("leaves original text intact for uncertainty and provider failure", async () => {
  polish.mockResolvedValueOnce({ status: "needs_input", original_text: "I like climbing mountain, visiting a zoo, and a rich trip.",
    suggested_text: null, explanation: "Please clarify the pace.", questions: ["What pace do you prefer?"], client_revision: "2" })
    .mockRejectedValueOnce(new Error("raw provider secret"));
  render(<ControlledPolisher />);
  fireEvent.click(screen.getByRole("button", { name: "Polish preferences" }));
  expect(await screen.findByText("What pace do you prefer?")).toBeInTheDocument();
  expect(screen.queryByRole("button", { name: "Apply rewrite" })).toBeNull();
  fireEvent.click(screen.getByRole("button", { name: "Polish preferences" }));
  expect(await screen.findByRole("alert")).toHaveTextContent("preferences were not changed");
  expect(screen.queryByText("raw provider secret")).toBeNull();
  expect(screen.getByLabelText("Preferences")).toHaveValue("I like climbing mountain, visiting a zoo, and a rich trip.");
});

it("invalidates a preview after editing and caps manual attempts", async () => {
  polish.mockImplementation(async request => ({ status: "suggested", original_text: request.original_text,
    suggested_text: "A safe rewrite.", explanation: "Clearer.", questions: [], client_revision: request.client_revision }));
  render(<ControlledPolisher />);
  fireEvent.click(screen.getByRole("button", { name: "Polish preferences" }));
  expect(await screen.findByText("A safe rewrite.")).toBeInTheDocument();
  fireEvent.change(screen.getByLabelText("Preferences"), { target: { value: "New preference" } });
  expect(screen.queryByRole("button", { name: "Apply rewrite" })).toBeNull();
  for (let index = 0; index < 2; index += 1) {
    fireEvent.click(screen.getByRole("button", { name: "Polish preferences" }));
    expect(await screen.findByText("A safe rewrite.")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Dismiss" }));
  }
  expect(screen.getByRole("button", { name: "Polish preferences" })).toBeDisabled();
  expect(polish).toHaveBeenCalledTimes(3);
});
