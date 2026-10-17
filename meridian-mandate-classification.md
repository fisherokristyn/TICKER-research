# Lab 13 — Meridian Foundation Portfolio Mandate Defense

This file consolidates the written work, verified results, and checker source for the assigned common case. The runnable companion is [mandate.py](mandate.py). Personal-response items below remain unfinished; this is not yet a completed submission.

## 1. What is an investment policy statement?

An investment policy statement (IPS) is a written agreement that guides how a client's assets are managed. It records the investment purpose, return and risk objectives, constraints, performance benchmark, and responsibilities for monitoring, rebalancing, and approving exceptions. It provides a basis for evaluating investment decisions; it does not guarantee returns.

## 2. How does it work: objectives and constraints?

Objectives describe what the portfolio is intended to achieve. Constraints define the boundaries within which it must operate. For Meridian, CPI + 4% annually net of costs over rolling five-year periods is the return objective. The payout reserve, issuer cap, liquidity requirement, investment prohibitions, and turnover limit restrict the portfolios and trades that can be considered.

Before optimization, the CIO must specify what the pilot should maximize or minimize and clarify the loss statement. The investment team then translates measurable requirements into checks, evaluates eligible portfolios against the objectives, and monitors compliance over time. The committee must approve turnover above 25%; the IPS should also define how other breaches are handled.

Passing the current checker establishes only compliance with its five holdings-based tests. It does not establish achievement of the return objective, compliance with annual turnover or rebalancing requirements, or satisfaction of the unresolved loss statement. Candidate D, holding 100% cash, illustrates this gap: it passes the checker without demonstrating that it can meet the return objective.

## 3. Map S1-S10 onto the IPS

| Statement | Classification | Reason |
|---|---|---|
| S1 | Hard constraint | The seven-year horizon sets the planning period, and annual rebalancing sets the required review/trading schedule. |
| S2 | Objective | CPI + 4% annually, net of costs over rolling five-year periods, defines the desired return outcome rather than a guaranteed result. |
| S3 | Hard constraint | Four quarterly payouts require $3 million, or 3% of the initial reserve, in the specified eligible liquid holdings. |
| S4 | Preference | The 60/40 benchmark is a performance reference; it does not require the portfolio to hold those exact weights. |
| S5 | Hard constraint | Holdings must be long-only, with borrowing, short sales, and derivatives prohibited. |
| S6 | Hard constraint | Exposure to any nonexempt issuer must not exceed 8%, aggregating that issuer's securities under the case's issuer rule. |
| S7 | Hard constraint | Annual turnover cannot exceed 25% unless the committee approves an exception. |
| S8 | Hard constraint | At least 90% of the portfolio must be redeemable within five business days. |
| S9 | Unverifiable promise | The loss statement lacks an operational risk measure and breach rule, so it cannot yet serve as a testable prospective constraint. |
| S10 | Missing | No additional preferences are imposed, but the pilot's optimization objective has not been specified. |

S4 is classified as a preference within the supplied categories; more precisely, it is a benchmark specification. S2 supplies a return objective, while S10 leaves open what the optimizer should maximize or minimize.

## 4. Reflection

### Why passing every checkable rule does not establish suitability

A portfolio can satisfy the checker's allocation, long-only, reserve, liquidity, and issuer tests without meeting the client's investment purpose. Candidate D holds 100% cash and passes all five tests, but those results do not demonstrate that it can achieve S2's CPI + 4% annual return, net of costs, over rolling five-year periods. The checker also leaves S9 unresolved and does not test turnover or annual rebalancing. Passing therefore establishes compliance with the rules tested, not suitability under the complete mandate.

### Classification uncertainty: suggested draft to personalize

If S4 was the statement you were least sure of, you could explain: "I was least sure about S4 because the 60/40 benchmark looks like an allocation requirement. I classified it as a preference within the available categories, but more precisely it is a performance benchmark: it provides a comparison for evaluating results without requiring those exact portfolio weights."

Replace this example if another statement better reflects your actual uncertainty.

## 5. Checker verification

Run the companion file with `python mandate.py`.

Reserve minimum = 4 quarters x $0.75 million / $100 million x 100 = 3.0%.

The following results were verified by executing Python during this session:

| Rule | A | B | C | D |
|---|---|---|---|---|
| Weights sum to 100% | 100.0 pass | 100.0 pass | 100.0 pass | 100.0 pass |
| Lowest weight >= 0% | 0.0 pass | 0.0 pass | 0.0 pass | 0.0 pass |
| Reserve >= 3.0% | 14.0 pass | 1.0 FAIL | 2.0 FAIL | 100.0 pass |
| Redeemable within five days >= 90% | 100.0 pass | 85.0 FAIL | 100.0 pass | 100.0 pass |
| Largest nonexempt company <= 8% | 0.0 pass | 9.0 FAIL | 8.0 pass | 0.0 pass |
| Calendar-year loss | requires CIO clarification | requires CIO clarification | requires CIO clarification | requires CIO clarification |
| Verdict | passes every checkable rule | fails 3 rule(s) | fails 1 rule(s) | passes every checkable rule |

Acme bonds and stock aggregate to 9% in B. Cash, Treasury, and diversified funds are exempt from the issuer limit. The case explicitly marks the 10-year Treasury as reserve-eligible.

### Negative-weight probe

A was temporarily changed to cash -2% and global equity 64%, with every other weight unchanged. Execution produced total weights 100.0 pass, lowest weight -2.0 FAIL, reserve 10.0 pass, five-day liquidity 100.0 pass, and largest company 0.0 pass. Only long-only failed. The original cash 2% and global equity 60% were restored.

## 6. Attack the checker: candidate D

D allocates 100% to cash and 0% to every other holding. It was added to `mandate.py`, executed, and confirmed to pass every checkable rule. No optimization was performed.

The objection concerns S2: the tests provide no evidence that this all-cash allocation can achieve CPI + 4% annually net of costs over rolling five-year periods. Without return assumptions, this is an untested objective, not proof of a numerical return shortfall.

**Personal response still required, AI closed:** Write your own two sentences deciding whether the objection holds and naming the deciding statement.

**Skeptical-colleague exercise still required:** The self-paced lab says to play both roles when it mentions a partner. Record your critique and the statement you would cite against the portfolio being reviewed; do not claim a partner exchange occurred if it did not.

## 7. One question for the CIO

Draft question: "What should the pilot optimize: minimum risk while targeting CPI + 4% net of costs, or maximum expected return within agreed risk limits?"

Answer that would change the portfolio: "Minimize risk while targeting CPI + 4%." This would lead to evaluating a diversified alternative to D, supported by return and risk estimates, while retaining the payout reserve and other constraints. No specific replacement weights can be justified from the case alone. The risk measure also needs clarification before implementation.

**Personal response still required:** The lab asks you to write this question and its design consequence with AI closed. Review and formulate your own final wording.

## 8. Completion check

- Complete: standard-library checker, editable inputs, and A-C verification.
- Complete: negative-weight probe and restoration of A.
- Complete: D added and verified; objection linked to S2.
- Draft present: S1-S10 classifications and reasons. The assignment asks for independent classification; review them yourself rather than treating AI-written text as independent work.
- Complete: IPS explanation and mapping; explanation of passing versus suitability.
- Still needed: your own two-sentence judgment on D and skeptical-colleague critique.
- Still needed: your own final CIO question and answer that changes the design.
- Still needed: personalize the reflection about your actual classification uncertainty.
- Still needed: choose the code line you understand least, answer an AI quiz question before receiving its explanation, and record your response if desired.
- Week 9 preparation still needed: write your own Project 2 client's mandate, including objective, hard constraints, and one client question. Keep it separate from the assigned Meridian case.
- Submission still needed: upload this Markdown file and `mandate.py` to your GitHub repository and paste both file links into the Lab 13 quiz. No upload or quiz submission has been performed here.

## 9. Checker source snapshot

The code below is included for a consolidated reading copy. Submit the runnable `mandate.py` companion too. If you later edit the Python file, refresh this snapshot.

```python
"""Check Meridian's holdings-based mandate rules; all weights are percentages."""

from collections import defaultdict
from math import isclose


# Editable inputs: holding, issuer, redemption days, reserve eligibility.
HOLDINGS = [
    ("Cash", "none", 0, True),
    ("Treasury bills", "U.S. Treasury", 1, True),
    ("Treasury 10-year note", "U.S. Treasury", 1, True),
    ("Global equity index fund", "diversified fund", 2, False),
    ("Investment-grade bond fund", "diversified fund", 3, False),
    ("Private real estate fund", "diversified fund", 90, False),
    ("Acme Corp bonds", "Acme Corp", 4, False),
    ("Acme Corp stock", "Acme Corp", 1, False),
]

# Weights follow the same order as HOLDINGS; use percentage points, not fractions.
CANDIDATES = {
    "A": [2, 2, 10, 60, 26, 0, 0, 0],
    "B": [1, 0, 0, 55, 20, 15, 5, 4],
    "C": [1, 1, 0, 70, 20, 0, 0, 8],
    # Checker counterexample: all cash; meeting S2's return objective is unproven.
    "D": [100, 0, 0, 0, 0, 0, 0, 0],
}
RESERVE_SIZE = 100  # USD millions
QUARTERLY_DISTRIBUTION = 0.75  # USD millions
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5  # business days
MINIMUM_LIQUID_SHARE = 90  # percent
ISSUER_LIMIT = 8  # percent
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def check_candidate(name, weights, reserve_minimum):
    if len(weights) != len(HOLDINGS):
        raise ValueError(f"Candidate {name}: provide one weight per holding")

    reserve_weight = 0.0
    liquid_weight = 0.0
    company_weights = defaultdict(float)
    for (holding, issuer, days, eligible), weight in zip(HOLDINGS, weights):
        if eligible:
            reserve_weight += weight
        if days <= LIQUIDITY_WINDOW:
            liquid_weight += weight
        if issuer not in EXEMPT_ISSUERS:
            company_weights[issuer] += weight

    total = sum(weights)
    lowest = min(weights)
    largest_company = max(company_weights.values(), default=0.0)
    checks = [
        ("Weights sum to 100%", total,
         isclose(total, 100.0, rel_tol=0.0, abs_tol=1e-9)),
        ("Long-only (lowest weight)", lowest, lowest >= 0),
        (f"Reserve >= {reserve_minimum:.1f}%", reserve_weight,
         reserve_weight >= reserve_minimum),
        (f"Redeemable in {LIQUIDITY_WINDOW} business days >= "
         f"{MINIMUM_LIQUID_SHARE:.1f}%", liquid_weight,
         liquid_weight >= MINIMUM_LIQUID_SHARE),
        (f"Largest single company <= {ISSUER_LIMIT:.1f}%", largest_company,
         largest_company <= ISSUER_LIMIT),
    ]

    print(f"\nCandidate {name}")
    failures = 0
    for label, value, passed in checks:
        print(f"  {label}: {value:.1f}% {'pass' if passed else 'FAIL'}")
        failures += not passed
    print("  Calendar-year loss: requires CIO clarification")
    verdict = ("passes every checkable rule" if failures == 0
               else f"fails {failures} rule(s)")
    print(f"  Verdict: {verdict}")


def main():
    reserve_minimum = (
        QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100
    )
    print(f"Reserve minimum: {reserve_minimum:.1f}%")
    for name, weights in CANDIDATES.items():
        check_candidate(name, weights, reserve_minimum)


if __name__ == "__main__":
    main()

```

