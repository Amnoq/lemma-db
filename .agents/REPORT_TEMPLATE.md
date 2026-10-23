# Report template

File: `reports/inbox/<issue>-<acct>-<agent>.md` on the agent's branch.
One report per agent per issue. The aggregator reads this and nothing
else from you — make it complete.

---

# Report — issue #`<N>` — `<acct>/<agent-id>` — `<YYYY-MM-DD>`

## Verdict

`<One paragraph: the answer, with its epistemic label.>`

## Claims

Each claim on its own line, labeled, with its evidence pointer:

- `[exact theorem]` ...
- `[computationally verified]` ... — script `<path>`, output `<path>`
- `[conjectural]` ...
- `[heuristic]` ...

## Evidence

- Scripts: `<paths in your workdir>`
- Captured outputs: `<paths>`
- Commands / environment notes needed to re-run: `<...>`

## Method notes

`<Forks run (claim / polar / null), controls used, what was observed in
the work's own forms. Anything the aggregator needs to judge the
verdict's weight.>`

## Dead ends

`<What was tried, why it was tried, exactly how it failed. Do not
soften these — they are first-class results.>`

## Proposed tree nodes

Provisional IDs only; the aggregator assigns canonical numbers.

- `[<acct>-<agent>-1]` `<node text: question, options, decision,
  evidence, proposed status>`
- `[<acct>-<agent>-2]` ...

## Open questions

`<What this leaves unresolved, and what would discriminate it next.>`
