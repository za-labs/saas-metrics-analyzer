import os
import streamlit as st
from dotenv import load_dotenv
from benchmarks import benchmarks, calculate_derived_metrics
from analysis import get_analysis

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from benchmarks import benchmarks, calculate_derived_metrics
st.title("Saas Metrics Analyzer")
st.markdown("Get an AI-powered health assessment of your SaaS metrics, like a 15 minute review from an experienced investor.")
st.header("Company Info")
stage = st.selectbox("Company Stage", ["Pre-seed", "Seed", "Series A", "Series B+"])
st.header("Growth Metrics")
mrr = st.number_input("MRR - Monthly Recurring Revenue (€)", min_value=0, value=0)
mom_growth = st.number_input("MoM MRR Growth Rate (%)", min_value=0.0, max_value=1000.0, value=0.0, format="%.1f")
st.header("Unit Economics")
gross_margin = st.number_input("Gross Margin (%)", min_value=-100.0, max_value=100.0, value=0.0, format="%.1f")
nrr = st.number_input("Net Revenue Retention / NRR (%)", min_value=0.0, max_value=300.0, value=0.0, format="%.1f")
monthly_churn = st.number_input("Monthly Gross Churn (%)", min_value=0.0, max_value=100.0, value=0.0, format="%.1f")
cac = st.number_input("CAC - Customer Acquisition Cost (€)", min_value=0, value=0)
arpa = st.number_input("ARPA - Average Revenue Per Account (€/month)", min_value=0, value=0)
num_customers = st.number_input("Number of Customers", min_value=0, value=0)
st.header("Cash Position")
burn_rate = st.number_input("Monthly Burn Rate (€)", min_value=0, value=0)
cash = st.number_input("Cash in Bank (€)", min_value=0, value=0)
run = st.button("Run Analysis")

if run:
    inputs = {
        "stage": stage,
        "mrr": mrr,
        "mom_growth": mom_growth,
        "gross_margin": gross_margin,
        "nrr": nrr,
        "monthly_churn": monthly_churn,
        "cac": cac,
        "arpa": arpa,
        "num_customers": num_customers,
        "burn_rate": burn_rate,
        "cash": cash,
    }

    derived = calculate_derived_metrics(inputs)

    st.header("Derived Metrics")

    if derived["cac_payback"] is not None:
        st.write(f"CAC Payback Period: {derived['cac_payback']:.1f} months")

    if derived["ltv"] is not None:
        st.write(f"Customer LTV: €{derived['ltv']:,.0f}")

    if derived["ltv_cac_ratio"] is not None:
        st.write(f"LTV:CAC Ratio: {derived['ltv_cac_ratio']:.1f}")

    if derived["runway_months"] is not None:
        st.write(f"Implied Runway: {derived['runway_months']:.1f} months")
    
    with st.spinner("Generating analysis..."):
        analysis = get_analysis(inputs, derived, benchmarks[stage])

    st.markdown(analysis)