# Spec 04 — Stable ability estimate and correct before/after P(pass)

## Problem (found in the smoke test)
1. One 10-item run of random answers moved P(pass) from 0.82 to 0.49. The online Elo update with k_sec=0.3 is far too volatile for a learner whose confidence matters; a single bad session must not halve the number.
2. `/api/finish` returns `p_pass_before == p_pass_after`: "before" is computed after the run's attempts were appended.
3. The initial `trend` is "down" with no history; it must be "flat" until there are ≥4 runs.

## Change `engine/model.py` (section abilities used by simulate.py)
Replace the online section update with a **Bayesian logistic (Rasch) posterior per section**, recomputed from all attempts each time (order-independent):
- θ_sec prior N(0.5, 1.0²) (listening N(0.4, 1.0²)). Likelihood Σ w_i·log σ(±(θ − b_i)), with item difficulty b_i = the tier/level prior (easy −1.5, medium 0, hard +1.5; N5 −0.5, N4-hard +0.5) plus the item's learned offset, clipped to ±1.
- **Recency weights** w_i = 0.5^(age_days/14), so improvement shows up while old mistakes fade. `guess` flag → w×0.5. Timed-out = wrong.
- MAP by Newton's method (numpy, ≤20 iterations); sd = 1/sqrt(posterior precision) (Laplace).
- **Evidence cap:** the effective sample size of the last 24 hours counts at most 40 items per section (scale those weights down if over), so one long bad session can't dominate.
- Keep the per-tag Elo skills as they are (they drive selection, not P(pass)).
- Item offsets: keep the existing slow update (0.15) but only from attempts older than the current run, so a run doesn't explain itself away.

## Change `server.py` / `engine/simulate.py`
- `p_pass_before` = the `p_pass` in model_state.json read **before** appending the run; `p_pass_after` = recomputed afterwards.
- Trend rule: "flat" until there are ≥4 runs, then compare the EMA with the EMA 3 runs earlier (±0.01).

## Tests to add
- Stability: with the placement prior plus 200 attempts at ~80% on medium items, one extra run of 10 random answers moves P(pass) by **less than 0.08**.
- Responsiveness: 100 consistent attempts at 95% on medium items raise θ_sec by ≥0.5 over the prior state.
- Before/after: in the server test, `p_pass_before` equals the status value from before the run.
All existing tests must still pass.
