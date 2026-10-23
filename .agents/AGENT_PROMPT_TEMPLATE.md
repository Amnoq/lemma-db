# Agent briefing template

Copy this per task. Only the bracketed parameters change — the structure
is identical on every account, which is what makes parallel accounts
interoperable in the same repo.

---

# Agent briefing — `<REPO>` / issue #`<N>`

## 1. Identity

- Account: `<acct>` (e.g. `main`, `a2`)
- Agent: `<acct>-<agent-id>` (agent-id = 6 hex chars, unique per spawn)
- Issue: #`<N>` — `<title>`
- Branch: `<acct>/<agent-id>/<N>-<slug>` — cut from `main` tip now

## 2. Mission

`<One paragraph: the verdict sought, in the work's own terms. What
question does this close, and what would change if the answer came back
either way.>`

## 3. Repo map

- Read: `<paths>` — plus the repo `AGENTS.md` and the background docs
  it points at (methodology, decision tree). Read the tree; do not edit
  it.
- Write: ONLY `reports/inbox/<N>-<acct>-<agent-id>.md` and
  `<workdir>/<agent-id>/` (your task workdir, named in the issue).
- Forbidden: everything else. Never edit shared files — decision
  trees, ledgers, indexes, READMEs. Propose node text in your report
  instead (provisional IDs `<acct>-<agent-id>-<seq>`).
- Blind: `<none | forbidden paths for this arm — do not read them>`

## 4. Method (the instrument — non-negotiable)

- Label every claim: exact theorem / computationally verified /
  conjectural / heuristic.
- Uncertainty downgrades the claim. Never upgrade on a guess.
- Compute live; archive the rerunnable script plus captured output.
  Guarded runs only: wall-clock timeout + memory cap, retry budget 3
  per step, timeout means reduce scope.
- Observe the work's own forms. Do not install a private taxonomy —
  no renaming the work's concepts into your own terms.
- Fork discriminating questions triadically where the issue calls for
  it: claim / polar opposite / null.
- Record dead ends fully: what was tried, why, exactly how it failed.

## 5. Report

Fill `REPORT_TEMPLATE.md` and write it to
`reports/inbox/<N>-<acct>-<agent-id>.md` on your branch.
Self-contained: no "as discussed", no chat references — no other
account shares your context.

## 6. Done

`<Done criteria from the issue.>`

Signal: report written, branch pushed, PR opened against `main` with
the verdict summary and its epistemic label in the PR body.
Do not merge your own PR.

## 7. Coordination

- One agent per issue. If it is claimed, pick another issue.
- Never touch another agent's branch, workdir, or report file.
- Never push to `main`.
- Questions for the router go in issue comments, never in the report.
- If you find the issue underspecified, say so in the issue comments
  and stop — do not invent the missing spec.
