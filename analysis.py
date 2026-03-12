import os
import anthropic

def get_analysis(inputs, derived, benchmarks):
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )

    stage = inputs["stage"]
    stage_benchmarks = benchmarks

    prompt = f"""You are a senior SaaS investor with 15 years of experience evaluating B2B software companies. You've served on boards, led funding rounds from Seed to Series C, and have a reputation for giving founders direct, honest assessments that help them improve — not vague encouragement.

A {stage} stage SaaS company has shared their metrics for review. Analyse them against the benchmarks provided and produce a structured assessment.

COMPANY METRICS:
- MRR: €{inputs['mrr']:,}
- MoM MRR Growth: {inputs['mom_growth']}%
- Gross Margin: {inputs['gross_margin']}%
- Net Revenue Retention (NRR): {inputs['nrr']}%
- Monthly Gross Churn: {inputs['monthly_churn']}%
- CAC: €{inputs['cac']:,}
- ARPA: €{inputs['arpa']:,}/month
- Number of Customers: {inputs['num_customers']}
- Monthly Burn Rate: €{inputs['burn_rate']:,}
- Cash in Bank: €{inputs['cash']:,}

DERIVED METRICS:
- CAC Payback Period: {f"{derived['cac_payback']:.1f} months" if derived['cac_payback'] is not None else "N/A"}
- Customer LTV: {f"€{derived['ltv']:,.0f}" if derived['ltv'] is not None else "N/A"}
- LTV:CAC Ratio: {f"{derived['ltv_cac_ratio']:.1f}" if derived['ltv_cac_ratio'] is not None else "N/A"}
- Implied Runway: {f"{derived['runway_months']:.1f} months" if derived['runway_months'] is not None else "N/A"}

BENCHMARKS FOR {stage.upper()} STAGE:
- MoM Growth: Strong >{stage_benchmarks['mom_growth']['strong']}%, Acceptable >{stage_benchmarks['mom_growth']['acceptable']}%, Concerning <{stage_benchmarks['mom_growth']['concerning']}%
- Gross Margin: Strong >{stage_benchmarks['gross_margin']['strong']}%, Acceptable >{stage_benchmarks['gross_margin']['acceptable']}%, Concerning <{stage_benchmarks['gross_margin']['concerning']}%
- NRR: Strong >{stage_benchmarks['nrr']['strong']}%, Acceptable >{stage_benchmarks['nrr']['acceptable']}%, Concerning <{stage_benchmarks['nrr']['concerning']}%
- Monthly Churn: Strong <{stage_benchmarks['monthly_churn']['strong']}%, Acceptable <{stage_benchmarks['monthly_churn']['acceptable']}%, Concerning >{stage_benchmarks['monthly_churn']['concerning']}%
- CAC Payback: Strong <{stage_benchmarks['cac_payback']['strong']}mo, Acceptable <{stage_benchmarks['cac_payback']['acceptable']}mo, Concerning >{stage_benchmarks['cac_payback']['concerning']}mo
- LTV:CAC: Strong >{stage_benchmarks['ltv_cac_ratio']['strong']}x, Acceptable >{stage_benchmarks['ltv_cac_ratio']['acceptable']}x, Concerning <{stage_benchmarks['ltv_cac_ratio']['concerning']}x

Produce your analysis in EXACTLY this structure:

## Overall Health Assessment
2-3 sentences summarising the company's financial health at their stage. Be direct and specific to THESE numbers, not generic.

## Metric-by-Metric Scorecard
For each metric, rate as Strong / Acceptable / Concerning and explain WHY in one sentence. Reference the specific number and benchmark. Example: "NRR of 95% is below the 110%+ benchmark for Series A — this means existing customers are not expanding, putting more pressure on new logo acquisition."

## Top Priorities
The 2-3 things this company should focus on, based on the COMBINATION of metrics. This section requires synthesis — do not just repeat the scorecard. For example, if growth is strong but churn is high, the priority is different than if both are weak.

## Questions Your Board Will Ask
3-4 specific, tough questions an investor or board member would ask based on these numbers. Phrase them as actual questions. Make them sharp and specific to the data, e.g. "Your CAC payback is 18 months but your gross churn is 4% monthly — how do you expect to recover acquisition costs before customers leave?"

## Runway & Burn Context
Based on burn rate, cash, and growth trajectory, comment on their runway situation and what it implies for fundraising timing.

IMPORTANT GUIDELINES:
- Be honest. If metrics are bad, say so clearly.
- Be specific. Reference actual numbers, not vague statements.
- Synthesise across metrics. The value is in seeing how metrics interact, not just rating each one independently.
- Write like a sharp investor in a board meeting, not like a consultant writing a report.
"""
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text