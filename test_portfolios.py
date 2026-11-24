"""Synthetic fixtures for calculations only. These are not investment observations."""
import unittest

from compliance import largest_issuer, mandate_checks, one_way, rebalance, verdict
from strategies import BASELINES, risk_aware


class MandateTests(unittest.TestCase):
    def test_limits_include_boundaries(self):
        rules = mandate_checks((.50, .47, 0, .03), 100, (45, 42, 0), .08, .25)
        self.assertEqual(verdict(rules), "PASS")

    def test_failures_and_missing_evidence(self):
        rules = mandate_checks((.65, .39, 0, -.02), 100, (30, 30, 30), .081, .251)
        self.assertEqual({rule.name for rule in rules if rule.status == "FAIL"},
                         {"Weight sum", "Long-only", "Qualifying reserve", "Five-day liquidity",
                          "Single-company issuer", "Annual turnover"})
        self.assertEqual(verdict(rules), "FAIL")
        baseline_a, baseline_b = list(BASELINES.values())[:2]
        self.assertEqual(verdict(mandate_checks(baseline_a, 100)), "FAIL")
        self.assertEqual(verdict(mandate_checks(baseline_b, 100)), "UNVERIFIED")

    def test_issuer_aggregates_across_funds(self):
        weights = (.5, .47, 0, .03)
        rows = {"VT": {"Shared": .10}, "BND": {"Shared": .07, "Another": .05}}
        self.assertAlmostEqual(largest_issuer(weights, rows), .0829)
        self.assertIsNone(largest_issuer(weights, {"VT": rows["VT"]}))

    def test_cost_charged_on_buys_and_sales(self):
        values = (60., 30., 0., 10.)
        target = (.50, .47, 0., .03)
        post, cost, traded = rebalance(values, target, .001)
        self.assertAlmostEqual(sum(post) + cost, 100.)
        self.assertAlmostEqual(cost, traded * .001)
        self.assertAlmostEqual(post[3] / sum(post), .03)
        self.assertAlmostEqual(one_way((.60, .30, 0, .10), target), .17)

    def test_optimizer_and_independent_check(self):
        covariance = ((.004, .0001), (.0001, .001))
        weights, _ = risk_aware({"VT": .12, "BND": .01}, covariance, None, 100,
                                (100, 100, 0), .25)
        self.assertAlmostEqual(weights[0], .582)
        self.assertEqual(verdict(mandate_checks(weights, 100, (100, 100, 0), 0, 0)), "PASS")

    def test_optimizer_reports_binding_band_and_blocked_reason(self):
        momentum = {"VT": .18, "BND": .06}
        covariance = ((.004, .0001), (.0001, .001))
        diagnostics = {}
        result = risk_aware(momentum, covariance, None, 100, (100, 100, 0), .25,
                            diagnostics=diagnostics)
        self.assertEqual(result, risk_aware(momentum, covariance, None, 100, (100, 100, 0), .25))
        self.assertAlmostEqual(diagnostics["bounds"]["Momentum band"][0], .582)
        self.assertAlmostEqual(diagnostics["bounds"]["Momentum band"][1], .679)
        self.assertEqual(diagnostics["binding"], ["Momentum band lower bound"])

        blocked = {}
        target, reason = risk_aware(momentum, covariance, None, 100, (30, 30, 0), .25,
                                    diagnostics=blocked)
        self.assertIsNone(target)
        self.assertIn("Five-day liquidity", reason)
        self.assertIn("Momentum band", blocked["bounds"])
        self.assertNotIn("binding", blocked)

    def test_optimizer_rejects_infeasible_limits(self):
        momentum = {"VT": .12, "BND": .01}
        covariance = ((.004, .0001), (.0001, .001))
        self.assertIsNone(risk_aware(momentum, covariance, (.95, .02, 0, .03),
                                     100, (100, 100, 0), .15)[0])
        self.assertIsNone(risk_aware(momentum, covariance, None, 100, (30, 30, 0), .25)[0])
        self.assertIsNone(risk_aware(momentum, covariance, None, 100, (100, 100, 0), .25,
                                     {"VT": {"Shared": .10}, "BND": {"Shared": .10}})[0])


if __name__ == "__main__":
    unittest.main()
