"""
Synthetic SaaS customer dataset generator.
Produces customer-level + monthly MRR/usage history realistic enough for
churn, expansion, and combined health-score modeling.
"""
import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

np.random.seed(42)
fake = Faker()
Faker.seed(42)

N_CUSTOMERS = 1800
START_DATE = datetime(2023, 7, 1)
N_MONTHS = 24  # through June 2025

PLANS = {
    "Starter": {"base_mrr": (49, 199), "weight": 0.45},
    "Growth":  {"base_mrr": (200, 999), "weight": 0.35},
    "Enterprise": {"base_mrr": (1000, 8000), "weight": 0.20},
}
INDUSTRIES = ["SaaS/Tech", "E-commerce", "Healthcare", "FinTech", "Education",
              "Manufacturing", "Professional Services", "Media"]
REGIONS = ["North America", "Europe", "APAC", "LATAM", "MEA"]
ACQ_CHANNELS = ["Inbound/Organic", "Paid Search", "Outbound Sales", "Partner/Referral", "Product-Led Trial"]

plan_names = list(PLANS.keys())
plan_weights = [PLANS[p]["weight"] for p in plan_names]

customers = []
for i in range(N_CUSTOMERS):
    cust_id = f"CUST-{10000+i}"
    plan = np.random.choice(plan_names, p=plan_weights)
    lo, hi = PLANS[plan]["base_mrr"]
    base_mrr = round(np.random.uniform(lo, hi), 2)
    signup_offset = np.random.randint(0, N_MONTHS - 1)  # month index they joined
    industry = np.random.choice(INDUSTRIES)
    region = np.random.choice(REGIONS, p=[0.40, 0.28, 0.18, 0.09, 0.05])
    channel = np.random.choice(ACQ_CHANNELS)
    company_size = int(np.random.lognormal(mean=3.2, sigma=1.1))
    company_size = max(2, min(company_size, 5000))
    csm_assigned = "Enterprise" == plan or np.random.rand() < 0.15

    customers.append(dict(
        customer_id=cust_id, plan_tier=plan, base_mrr=base_mrr,
        signup_month_idx=signup_offset, industry=industry, region=region,
        acquisition_channel=channel, company_size_employees=company_size,
        has_csm=csm_assigned
    ))

cust_df = pd.DataFrame(customers)

# ---- Monthly history simulation ----
records = []
rng = np.random.default_rng(42)

for _, c in cust_df.iterrows():
    cust_id = c.customer_id
    mrr = c.base_mrr
    plan = c.plan_tier
    has_csm = c.has_csm
    status = "active"
    months_active = 0
    churned_month = None

    # baseline propensity to churn/expand depends on plan + csm + channel
    monthly_churn_base = {"Starter": 0.045, "Growth": 0.022, "Enterprise": 0.010}[plan]
    if has_csm:
        monthly_churn_base *= 0.55
    if c.acquisition_channel == "Outbound Sales":
        monthly_churn_base *= 0.85
    if c.acquisition_channel == "Product-Led Trial":
        monthly_churn_base *= 1.25

    monthly_expansion_base = {"Starter": 0.03, "Growth": 0.06, "Enterprise": 0.08}[plan]
    if has_csm:
        monthly_expansion_base *= 1.6

    # usage baseline correlates inversely with churn risk
    usage_level = rng.normal(0.65, 0.18)
    usage_level = np.clip(usage_level, 0.05, 1.0)

    support_ticket_rate = rng.gamma(2.0, 1.0)  # tickets/month baseline

    for m in range(c.signup_month_idx, N_MONTHS):
        if status == "churned":
            break
        months_active += 1
        tenure = months_active

        # usage drifts; declining usage raises churn risk, predicts contraction
        usage_drift = rng.normal(0, 0.04)
        usage_level = np.clip(usage_level + usage_drift, 0.02, 1.0)

        logins = max(0, int(rng.normal(usage_level * 40, 8)))
        active_seats_pct = np.clip(usage_level + rng.normal(0, 0.1), 0.05, 1.0)
        features_adopted = max(1, int(rng.normal(usage_level * 12, 2)))
        support_tickets = max(0, int(rng.poisson(support_ticket_rate * (1.3 - usage_level))))
        nps = int(np.clip(rng.normal(usage_level * 80 + 10, 15), -100, 100))

        # dynamic churn probability: low usage + high tickets + low tenure = higher risk
        churn_risk = monthly_churn_base
        churn_risk *= (1.8 - usage_level)               # low usage -> higher
        churn_risk *= (1 + 0.08 * min(support_tickets, 6))
        churn_risk *= (1.4 if tenure <= 3 else (0.8 if tenure > 12 else 1.0))
        churn_risk = np.clip(churn_risk, 0.001, 0.5)

        expand_prob = monthly_expansion_base * usage_level * (1.3 if tenure > 6 else 0.7)
        expand_prob = np.clip(expand_prob, 0.001, 0.4)
        contract_prob = np.clip(0.02 * (1.6 - usage_level) * (1 + 0.05 * support_tickets), 0.001, 0.3)

        roll = rng.random()
        event = "none"
        if roll < churn_risk:
            status = "churned"
            event = "churned"
            mrr_this_month = mrr
            mrr = 0.0
        else:
            roll2 = rng.random()
            if roll2 < expand_prob:
                bump = rng.uniform(0.05, 0.35)
                mrr *= (1 + bump)
                event = "expansion"
            elif roll2 < expand_prob + contract_prob:
                cut = rng.uniform(0.05, 0.30)
                mrr *= (1 - cut)
                event = "contraction"
            mrr_this_month = mrr

        records.append(dict(
            customer_id=cust_id, month_idx=m, tenure_months=tenure,
            mrr=round(mrr_this_month, 2), status=status, event=event,
            logins_per_month=logins, active_seats_pct=round(active_seats_pct, 3),
            features_adopted=features_adopted, support_tickets=support_tickets,
            nps_score=nps
        ))

monthly_df = pd.DataFrame(records)

# ---- Build customer-level summary (for churn/health modeling) ----
last_rows = monthly_df.sort_values("month_idx").groupby("customer_id").tail(1)
first_rows = monthly_df.sort_values("month_idx").groupby("customer_id").head(1)

summary = cust_df.merge(
    last_rows[["customer_id", "month_idx", "tenure_months", "mrr", "status",
               "logins_per_month", "active_seats_pct", "features_adopted",
               "support_tickets", "nps_score"]].rename(columns={"mrr": "current_mrr"}),
    on="customer_id", how="left"
)

agg = monthly_df.groupby("customer_id").agg(
    avg_logins=("logins_per_month", "mean"),
    avg_support_tickets=("support_tickets", "mean"),
    avg_nps=("nps_score", "mean"),
    n_expansion_events=("event", lambda x: (x == "expansion").sum()),
    n_contraction_events=("event", lambda x: (x == "contraction").sum()),
    months_observed=("month_idx", "count"),
).reset_index()

summary = summary.merge(agg, on="customer_id", how="left")
summary["churned"] = (summary["status"] == "churned").astype(int)
summary["net_mrr_change_pct"] = np.where(
    summary["base_mrr"] > 0,
    (summary["current_mrr"] - summary["base_mrr"]) / summary["base_mrr"] * 100,
    0
)
summary["expanded"] = (summary["n_expansion_events"] > summary["n_contraction_events"]).astype(int)
# combined health label: 2=healthy/expanding, 1=stable/at-risk, 0=churned
summary["health_class"] = np.select_ = np.where(
    summary["churned"] == 1, 0,
    np.where(summary["expanded"] == 1, 2, 1)
)

cust_df.to_csv("/home/claude/product_analytics/data/customers.csv", index=False)
monthly_df.to_csv("/home/claude/product_analytics/data/monthly_history.csv", index=False)
summary.to_csv("/home/claude/product_analytics/data/customer_summary.csv", index=False)

print("Customers:", len(cust_df))
print("Monthly records:", len(monthly_df))
print("Summary shape:", summary.shape)
print(summary["health_class"].value_counts())
print(summary["churned"].mean(), "overall churn rate")
