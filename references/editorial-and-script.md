# Editorial and script specification

## Relationship between facts and opinion

- Treat the user's prediction as the editorial thesis, not as verified truth.
- Use verified facts to support or challenge it.
- Label tactical and lineup forecasts as judgment, possibility, or expectation.
- If research materially contradicts the thesis, explain the evidence and let the user decide whether to keep or revise the viewpoint.

## Default script shape

Aim for 55–65 seconds and roughly 280–350 Chinese characters:

1. **Hook (0–6s):** one sharp match question or tension; no false certainty.
2. **Context (6–16s):** identify match and why it matters.
3. **Team A evidence (16–29s):** form/tactical strength and one vulnerability.
4. **Team B evidence (29–42s):** counter-path and one vulnerability.
5. **Decision (42–55s):** the two or three variables driving the pick.
6. **Prediction (55–62s):** result or score, followed by uncertainty/risk language.
7. **CTA (optional):** one short audience prompt, only when requested or already approved as a default.

Write for natural Mandarin speech, not a report. Use short sentences and pronounceable player/team names. Avoid stacking figures.

## Prohibited writing

- No guaranteed-win language such as “稳过”, “必胜”, or “稳赚”.
- No invented statistics, quotes, injuries, transfers, lineups, or odds.
- No claim that a likely lineup is official.
- No hidden change to the user's score prediction.
- No betting CTA unless the user explicitly requests it and applicable platform/legal requirements are addressed.

## Approval payload

Show the entire script, not an outline. Include:

- estimated duration;
- prediction/score extracted from the script;
- material caveats;
- a direct request for approval or changes.

Only an explicit approval of the displayed version satisfies the gate. Hash the exact UTF-8 script bytes. Any spoken-text change creates a new version and invalidates approval.
