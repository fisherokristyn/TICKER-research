# AI use and independent validation

Stage 1 revision: archived existing Edition B in `archive/pre-stage-1/`; preserved all 30 prior tests byte for byte; added source-policy tests. Changed Treasury input from 4.79% to prior-day 4.75%, reducing the derived borrowing cost by 4 basis points. Added explicit source-timing qualifications and strict refusal of unsupported certification. No Apple regression estimate was invented when a complete eligible series could not be obtained.

Stage 2 revision: preserved the original terminal valuation as a named comparison case; added annualized FY2031-to-terminal reconciliation, ROIC/growth grid, and a separate five-year gradual transition. Added terminal identity, sensitivity direction, transition path and parameter-validation tests. The transition is a judgment case and does not alter the base recommendation field, which remains null.

Stage 3 revision: implemented the separate `peer_valuation.py` comparable-company engine for Microsoft, Alphabet, HP and Dell. It preserves the current base DCF of $126.34/share and the separate transition comparison of $124.01/share. It reports peer-by-peer EV/EBITDA, EV/EBIT and reported/normalized P/E results, group ranges and leave-one-peer-out results without averaging unlike methods. Dell's cutoff-uncertain Q2 release is excluded. The latest complete run passed 57 tests.

This document records AI-assisted Edition B work; it is not a human prediction, partner challenge, committee decision or precommit receipt.

| AI-proposed change | Independent evidence needed to accept or reject |
| --- | --- |
| Preserve Edition A and archive the existing model | SHA-256 checks against original manifest; actual Week 2 receipt still needed from student |
| Update FY2025 base to LTM using eligible June statements | Open the cited SEC statements and verify every transcribed field and filing date |
| CAPM WACC with industry beta and AA debt proxy | Treasury/FRED/NYU source definitions; archived ERP; Apple bond quotes/regression to improve proxy |
| Normalize future compensation to cash and dilute legacy awards | Award count, recognition cost and vesting footnotes; independently reconcile share dates |
| Separate segment growth, explicit cost recast and linked statements | Recalculate statement identities and challenge operating assumptions using company evidence |
| Terminal reinvestment from ROIC and growth | Independent perpetuity arithmetic and sustainable return evidence |
| Low/base/high, sensitivity and conditional reverse DCF | Causal business evidence and independent changed-input reasoning |
| Automated corruption and instructor tests | Known answers from instructor fixtures, not the Apple model's saved outputs |

The new engine was implemented after approval, reusing original balance-sheet definitions and checks. Original regression tests remain unchanged. Actual automated run details and failures, if any, appear in `outputs/validation.txt`; execution timestamp and exact source SHA-256 appear in `outputs/edition_b_results.json`. Test passing is not evidence that a proxy assumption is financially correct.

Two official synthetic fixtures were available and used: Week 2 mini-case (FCFF 77.5, equity 820, per share 8.20) and Week 3 worked DCF (approximately 1,624.87 EV and 27.50 per share). They are separate from the student's Locked Changed-Input Record. Deliberate failures test source totals, accounting identities and invalid terminal conditions. Directional tests hold operations fixed when changing WACC.

No final investment recommendation was chosen. No AI-off prediction, precommit timestamp, partner challenge, committee decision or GitHub upload was fabricated. Student-only deliverables and source gaps remain visible in the README and methodology.
# Stage 3 comparable-company work

- Proposed and implemented a separate `peer_valuation.py` engine for Microsoft, Alphabet, HP and Dell.
- Independent evidence required: verify every source URL, cutoff timing, share basis, investment classification, and normalization adjustment against the cited filing before submission.
- The engine reports mechanical calculations and limitations; it does not select a recommendation or average methods.
