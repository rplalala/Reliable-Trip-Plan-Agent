"""One authorized Melbourne V3 revalidation, separate from the exhausted pilot."""

from tools.validation import landmark_pilot as pilot


def main():
    pilot.CASES = ("focus_melbourne_v3",)
    pilot.OUTPUT = pilot.ROOT / "logs/focus_revalidation_20260928"
    pilot.CHILD_MODULE = "tools.validation.focus_revalidation"
    return pilot.main()


if __name__ == "__main__":
    raise SystemExit(main())
