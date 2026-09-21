import { render, screen } from "@testing-library/react";
import { RouterProvider, createMemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

import { routes } from "./router";

describe("application route boundaries", () => {
  it("renders the product layout for the planner", () => {
    const testRouter = createMemoryRouter(routes, { initialEntries: ["/plan"] });
    render(<RouterProvider router={testRouter} />);

    expect(screen.getByLabelText("Main navigation")).toBeInTheDocument();
    expect(screen.getByText("Reliable Trip Planner")).toBeInTheDocument();
    expect(screen.queryByText("Local development and research")).not.toBeInTheDocument();
  });

  it("renders the isolated developer layout and deployment warning", () => {
    const testRouter = createMemoryRouter(routes, { initialEntries: ["/dev/planner"] });
    render(<RouterProvider router={testRouter} />);

    expect(screen.getByText("Local development and research")).toBeInTheDocument();
    expect(
      screen.getByText(/Protect or disable it before any public production deployment/),
    ).toBeInTheDocument();
    expect(screen.queryByLabelText("Main navigation")).not.toBeInTheDocument();
  });
});

vi.mock("../features/planning/api", () => ({
  getTripDateWindow: vi.fn().mockResolvedValue({allowedStart:"2026-09-11", allowedEnd:"2026-09-24", maxTripDays:10}),
}));
