# Video 1 — Thought process and system evolution

**Target** 2:40. **Maximum** 3:00. Read the paragraphs labeled **Say**. Screen cues are silent.

**Before recording:** Open the app at the baseline, pin `mandate.py` and the three documents in the sequence below, and make the commit and authorship checks in the [recording checklist](recording-checklist.md).

## 0:00–0:30 | Start with the client's problem

**Show** Streamlit, **Strategies**, with the Meridian header visible. Switch to [Proposed mandate](proposed-mandate.md), **Inherited requirements**.

**Say**

This project asks how a fictional foundation could invest a one hundred million dollar reserve over seven years while still paying out seven hundred fifty thousand dollars every quarter. Its objective is inflation plus four percentage points, net of costs, over rolling five-year periods. I started by asking which parts of that mandate I could test and which would still need evidence or a decision from the CIO.

## 0:30–1:00 | Turn policy into checks

**Show** VS Code, [mandate.py](../mandate.py), the editable inputs and checks. Then show [compliance.py](../compliance.py), `mandate_checks`.

**Say**

The Lab Thirteen checker gave me a starting point. For the application, I translated the mandate into checks for portfolio weights, long-only exposure, the three percent qualifying reserve, five-day liquidity, issuer concentration, and turnover. I kept failed checks separate from checks we can't verify. That's important because a missing issuer file and an observed reserve breach tell the committee two different things.

## 1:00–1:38 | Compare designs and build the replay

**Show** Streamlit, **Strategies → Strategy design**, then **Historical comparison** and **Stress tests**. Leave **Run stress scenarios** unchecked.

**Say**

I used equal weight as a simple reference, a cash-adjusted sixty-forty portfolio as a benchmark-oriented alternative, and a risk-aware strategy to test whether a lagged signal and variance estimates added anything. The project went from static checks to a walk-forward replay using a validated snapshot of real ETF prices. The dashboard then added rule-by-rule evidence, blocked trades, and stress controls. That made the committee decision depend on more than a return chart.

## 1:38–2:13 | Explain the locked test

**Show** [Validation and AI use](validation-and-ai-use.md), **Before and after** and **Prediction comparison**.

**Say**

The locked experiment changed one input, trading costs from ten to twenty-five basis points. Every strategy earned less after modeled fees. The targets, rule statuses, and blocked dates stayed the same. B had the biggest increase in total dollars paid, but A had the biggest decline in annualized return. I use the trade ledger to explain that distinction. Dollar fees, percentage turnover, and impact on compounded returns measure different things.

## 2:13–2:42 | Disclose assistance and close

**Show** [Recording checklist](recording-checklist.md#authorship-and-evidence-check), then [Decision memo](decision-memo.md), **Final committee recommendation**.

**Say**

I used ChatGPT and Codex for coding, testing, analysis, and drafting. I wrote the locked prediction entirely on my own, without AI. I committed it to GitHub before running the test and preserved the original text and commit ID so I could compare the results with what I had documented beforehand. My recommendation weighs the reserve failures and missing evidence alongside performance. It's a conditional, non-live pilot of Strategy B, with zero dollars approved for deployment.
