import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { submitDeveloperPlanningRequest } from "../../features/developer-planning/api";
import { HttpError } from "../../shared/api/http";
import { DeveloperPlannerPage } from "./DeveloperPlannerPage";

vi.mock("../../features/developer-planning/api", () => ({
  submitDeveloperPlanningRequest: vi.fn(),
}));

const submitDeveloperMock = vi.mocked(submitDeveloperPlanningRequest);

describe("DeveloperPlannerPage", () => {
  beforeEach(() => {
    submitDeveloperMock.mockReset();
  });

  it("offers only V0 and sends an explicit version", async () => {
    submitDeveloperMock.mockResolvedValue({
      system_version: "v0",
      requirements: {},
      itinerary: {},
    });
    const user = userEvent.setup();
    render(<DeveloperPlannerPage />);

    const versionSelector = screen.getByRole("combobox", { name: "Research version" });
    expect(screen.getAllByRole("option")).toHaveLength(1);
    expect(versionSelector).toHaveValue("v0");

    await user.type(screen.getByLabelText("Travel request"), "Plan one day in Kyoto.");
    await user.click(screen.getByRole("button", { name: "Run V0" }));

    expect(submitDeveloperMock).toHaveBeenCalledWith(
      expect.objectContaining({
        version: "v0",
        request_text: "Plan one day in Kyoto.",
      }),
    );
    expect(await screen.findByText(/"system_version": "v0"/)).toBeInTheDocument();
  });

  it("shows the raw developer error response", async () => {
    submitDeveloperMock.mockRejectedValue(
      new HttpError(502, {
        detail: {
          code: "v0_stage_failed",
          stage: "extract_requirements",
        },
      }),
    );
    const user = userEvent.setup();
    render(<DeveloperPlannerPage />);

    await user.type(screen.getByLabelText("Travel request"), "Plan one day in Kyoto.");
    await user.click(screen.getByRole("button", { name: "Run V0" }));

    expect(await screen.findByText(/"http_status": 502/)).toBeInTheDocument();
    expect(screen.getByText(/"stage": "extract_requirements"/)).toBeInTheDocument();
  });
});

vi.mock("../../features/planning/api", () => ({
  getTripDateWindow: vi.fn().mockResolvedValue({allowedStart:"2026-09-11", allowedEnd:"2026-09-24", maxTripDays:10}),
}));
