"""Reproducible offline report; validation runs before results are written."""
import csv
import hashlib
import io
import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
import apple_edition_b as m


def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                     ['| ' + ' | '.join(str(v) for v in row) + ' |' for row in rows])


def validate():
    stream = io.StringIO()
    loader = unittest.TestLoader()
    suite = unittest.TestSuite([loader.discover(str(m.ROOT / 'tests'), pattern='test_*.py'),
                               loader.loadTestsFromName('test_apple_proforma')])
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise RuntimeError('VALIDATION FAILED; results not refreshed.\n' + stream.getvalue())
    return result.testsRun, stream.getvalue()


def render(result, data, count):
    w = result['wacc']
    base = result['cases']['base']['valuation']
    lines = ['# Apple Edition B — model and validation',
             f"Valuation: {data['valuation_date']} close. Cutoff: {data['information_cutoff']}. USD millions and shares millions, except per-share values. {count} automated tests passed.",
             '**Provisional valuation: calculated proxy WACC and estimated diluted shares. No investment recommendation selected.**',
             '## Calculated WACC', w['status'],
             'Ke = Rf + beta × ERP. WACC = E/(D+E) × Ke + D/(D+E) × Kd × (1−tax).',
             table(['Input/output', 'Value'], [
                 ['Risk-free Treasury yield', f"{w['risk_free']:.3%}"], ['Equity risk premium', f"{w['erp']:.3%}"],
                 ['Relevered industry beta proxy', f"{w['beta']:.6f}"], ['Borrowing cost proxy', f"{w['borrowing_cost']:.3%}"],
                 ['Interest tax shield', f"{w['shield_tax']:.1%}"], ['Market equity', f"{w['equity_market']:,.2f}"],
                 ['Market debt proxy', f"{w['debt_market']:,.2f}"], ['Equity / debt weights', f"{w['equity_weight']:.4%} / {w['debt_weight']:.4%}"],
                 ['Cost of equity', f"{w['cost_of_equity']:.4%}"], ['After-tax cost of debt', f"{w['after_tax_cost_of_debt']:.4%}"],
                 ['Calculated WACC', f"{w['wacc']:.4%}"], ['Difference from old 9%', f"{10000 * w['difference_from_9pct']:.2f} basis points"]]),
             f"With identical Edition B operations, 9% gives ${result['at_9pct_same_operations']['per_share']:.2f}; calculated WACC gives ${base['per_share']:.2f}. Higher WACC lowers discounted cash flows and terminal value. This isolates WACC; it is not the total change from the archived model.",
             '## Scenarios and valuation',
             table(['Case', 'EV', 'Equity value', 'Shares proxy', '$/share', 'TV / EV'],
                   [[c['name'], f"{c['valuation']['enterprise']:,.1f}", f"{c['valuation']['equity']:,.1f}",
                     f"{c['valuation']['diluted_shares_proxy']:,.3f}", f"{c['valuation']['per_share']:.2f}",
                     f"{c['valuation']['terminal_fraction']:.1%}"] for c in result['cases'].values()]),
             'Low case: slower Services growth, weaker Products margins, greater R&D intensity and inventory requirements. High case: stronger product adoption and Services mix. These are conditional judgments, not probabilities. Compare the cases with your own decision threshold; the program does not assign Buy/Hold/Sell.',
             f"Decision relevance: at an entry price between ${result['cases']['low']['valuation']['per_share']:.2f} and ${base['per_share']:.2f}, the named downside switches base-case positive modeled upside to negative modeled upside. At the recorded ${data['market']['price']:.2f} market price, all three cases are below price; this downside does not itself reverse that comparison. A different recommendation would require your explicit decision rule or better-supported assumptions.",
             '## Base enterprise-to-equity bridge',
             table(['Component', 'USD millions'], [[k, f'{base[k]:,.3f}'] for k in
                   ('enterprise', 'cash', 'securities', 'operating_reserve', 'debt_market_proxy', 'other_claims', 'equity')]),
             'Equity = EV + cash + securities − operating reserve − debt − other claims. Operating cash is excluded from excess cash; future increases are deducted in FCFF. Other claims are zero only under the documented claim-review assumption.',
             '## Historical reconciliation (facts, not forecasts)',
             'LTM through June 27, 2026 = FY2025 + nine months FY2026 − nine months FY2025. No historical fact is replaced with a normalized forecast assumption.',
             table(['Metric', 'FY2025', '+ 9m2026', '− 9m2025', '= LTM'],
                   [[k, data['fy2025'][k], data['nine_months_2026'][k], data['nine_months_2025'][k], result['trailing_base'][k]]
                    for k in ('revenue', 'products', 'services', 'ebit', 'tax', 'net_income', 'da', 'sbc', 'capex')]),
             f"June reported balance-sheet assets: {data['q3_balance']['assets']:,}; liabilities: {data['q3_balance']['liabilities']:,}; equity: {data['q3_balance']['equity']:,}. The June-to-September bridge is an estimate, shown separately in JSON. The FY2026 remaining stub is discounted separately, followed by five fiscal years FY2027–FY2031.",
             '## Historical-to-forecast normalization',
             'No one-off dollar adjustment is silently applied to LTM history. Instead these explicit prospective policy assumptions replace historical ratios. Margin references are then recast for separately modeled D&A and compensation.',
             table(['Metric', 'LTM fact / calculated ratio', 'Base forecast assumption'], [
                 ['Products gross margin', f"{1-result['trailing_base']['product_cogs']/result['trailing_base']['products']:.2%}", f"{m.BASE['product_margin']:.2%}"],
                 ['Services gross margin', f"{1-result['trailing_base']['service_cogs']/result['trailing_base']['services']:.2%}", f"{m.BASE['service_margin']:.2%}"],
                 ['R&D / sales', f"{result['trailing_base']['rd']/result['trailing_base']['revenue']:.2%}", f"{m.BASE['rd_ratio']:.2%}"],
                 ['SG&A / sales', f"{result['trailing_base']['sga']/result['trailing_base']['revenue']:.2%}", f"{m.BASE['sga_ratio']:.2%}"],
                 ['Provision / pretax earnings', f"{result['trailing_base']['tax']/result['trailing_base']['pretax']:.2%}", f"{m.BASE['tax_rate']:.2%}"],
                 ['Capex / sales', f"{result['trailing_base']['capex']/result['trailing_base']['revenue']:.2%}", f"{m.BASE['capex_ratio']:.2%}"],
                 ['SBC / sales', f"{result['trailing_base']['sbc']/result['trailing_base']['revenue']:.2%}", f"{m.BASE['compensation_ratio']:.2%} total budget; legacy noncash/new cash"]]),
             '## Linked base pro-forma',
             table(['Metric'] + [r['name'] for r in result['cases']['base']['rows']],
                   [[k] + [f'{r[k]:,.1f}' for r in result['cases']['base']['rows']]
                    for k in ('revenue', 'operating_income', 'interest', 'tax', 'net_income', 'cash', 'ppe', 'assets', 'liabilities', 'equity', 'cfo', 'cfi', 'cff', 'capex', 'working_capital_change', 'fcff')]),
             'Full line items for all cases are in forecast.csv and results.json. D&A and compensation cost recasts are shown explicitly; see methodology before treating these as GAAP segment forecasts.',
             '## Terminal economics',
             f"Terminal NOPAT {base['terminal_nopat']:,.1f}; ROIC {base['terminal_roic']:.1%}; growth {base['terminal_growth']:.1%}; reinvestment {base['terminal_reinvestment']:,.1f}; terminal FCFF {base['terminal_fcff']:,.1f}. Reinvestment = NOPAT × growth / ROIC. Growth is a judgment: approximately 2% long-run inflation plus 0.5% real growth, challenged in the grid. Neither ROIC nor growth is company guidance.",
             '## WACC × terminal growth ($/share)',
             table(['WACC', 'g=2.0%', 'g=2.5%', 'g=3.0%'],
                   [[f"{result['sensitivity'][i]['wacc']:.3%}"] + [f"{x['per_share']:.2f}" for x in result['sensitivity'][i:i+3]]
                    for i in range(0, len(result['sensitivity']), 3)]),
             '## Reverse DCF (conditional market expectation)',
             '```json\n' + json.dumps(result['reverse_dcf'], indent=2) + '\n```',
             '## Driver sensitivity',
             'One variable at a time, all other base assumptions fixed. Ranking depends on the chosen shock sizes; half-width checks are included in JSON.',
             table(['Driver', 'Lower input', 'Upper input', '$/share at lower', '$/share at upper', 'Price span'],
                   [[x['driver'], f"{x['low_input']['input']:.4f}", f"{x['high_input']['input']:.4f}", f"{x['low_input']['per_share']:.2f}",
                     f"{x['high_input']['per_share']:.2f}", f"{x['price_span']:.2f}"] for x in result['driver_sensitivity'] if x['range_scale'] == 1]),
             '## Remaining limits and student decisions',
             '\n'.join('- ' + x for x in result['limitations']),
             '- ERP historical archive and exact intraday availability remain unverified. Source arithmetic and hashes do not establish authenticity.',
             '- Human AI-off prediction, precommit receipt, locked-test execution, partner challenge and final recommendation remain uncompleted student work.',
             '## Sources',
             '\n'.join(f"- **{k}**: [{s.get('definition', s.get('basis', k))}]({s['url']}); available {s.get('available_on', 'teaching fixture')}; {s.get('locator', '')}" for k, s in data['sources'].items())]
    return '\n\n'.join(lines) + '\n'


def main():
    count, log = validate()
    data = m.load_sources()
    result = m.calculate_all(data)
    result['validation'] = {'tests_passed': count, 'executed_at_utc': datetime.now(timezone.utc).isoformat(),
                            'source_sha256': hashlib.sha256(m.SOURCE_PATH.read_bytes()).hexdigest(),
                            'scope': 'AI-assisted automated checks; NOT the student Locked Changed-Input Record'}
    out = m.ROOT / 'outputs'
    out.mkdir(exist_ok=True)
    (out / 'edition_b_results.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    report = render(result, data, count)
    (out / 'edition_b_report.md').write_text(report, encoding='utf-8')
    (out / 'validation.txt').write_text(log, encoding='utf-8')
    rows = [dict(case=k, **r) for k, c in result['cases'].items() for r in c['rows']]
    with (out / 'forecast.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f'{count} tests passed. Proxy WACC: {result["wacc"]["wacc"]:.4%}')
    for k, c in result['cases'].items():
        print(f'{k}: ${c["valuation"]["per_share"]:.2f}/share')
    print('Report: ' + str(out / 'edition_b_report.md'))
    return result


if __name__ == '__main__':
    main()
