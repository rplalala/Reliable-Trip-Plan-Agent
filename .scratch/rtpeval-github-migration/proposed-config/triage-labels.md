# Triage labels

Apply after the approved tracker activation. Keep the existing canonical roles.

| Role | GitHub label | Legacy local Status | Meaning |
| --- | --- | --- | --- |
| needs-triage | needs-triage | needs-triage | Incoming work awaiting triage |
| needs-info | needs-info | needs-info | Specification has a bounded information gap |
| ready-for-agent | ready-for-agent | ready-for-agent | Specification ready; dependencies and approval still checked |
| ready-for-human | ready-for-human | ready-for-human | Requires human implementation |
| wontfix | wontfix | wontfix | Work will not be actioned |

GitHub open/closed is lifecycle, not one of these five specification roles.
`resolved` maps to closed/completed for approved completed work; it needs no extra
resolved triage label. `claimed` is represented by assignment/current-scope comment
on an open issue, not a readiness label granting permission. A ready ticket with an
open blocker stays ready-for-agent and blocked; a needs-info ticket with no open blocker
still needs specification closure. `rtpeval` is a feature grouping label, not a sixth
triage role. Existing labels must be inspected before any approved creation/update.
