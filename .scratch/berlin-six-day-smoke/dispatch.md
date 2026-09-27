# Berlin execution dispatch

Archived dispatch: all four attempts have been consumed. Do not execute these commands
again. The record below preserves the original instructions; assessment.md records
the outcomes and subsequent user decisions.

Read `plan.md` first. Preparation is already complete; do not run prepare again or
delete evidence/locks. Run from `D:\Workspace\Capstone\Reliable-Trip-Plan-Agent`,
with required network permission, sequentially and inspect evidence between cases:

```powershell
.venv\Scripts\python.exe .scratch\berlin-six-day-smoke\run_one.py v0
.venv\Scripts\python.exe .scratch\berlin-six-day-smoke\run_one.py v1
.venv\Scripts\python.exe .scratch\berlin-six-day-smoke\run_one.py v2
.venv\Scripts\python.exe .scratch\berlin-six-day-smoke\run_one.py v3
```

Do not combine these into an unconditional shell chain. A launcher returning normally
does not imply application success: inspect its printed status and the manifest.
Any `stopped_*` batch state blocks further cases. A crash while a case is marked
running also blocks progression; report instead of clearing its marker.

Evidence root: `logs/berlin_six_day_20260928/`. Preserve all outputs and write
`report.md` there. No fixes/retries are authorized. Report completion or blockers
to Iteration 2. Perform the single isolated blind review only under the gate and
anonymization rules in `plan.md`; report any missing evidence instead of weakening
the gate. Do not expose credentials or raw provider envelopes in messages.
