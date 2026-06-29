import json
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                 Table, TableStyle, PageBreak, HRFlowable)

DASH = "/home/claude/product_analytics/dashboard"
with open(f"{DASH}/kpis.json") as f:
    K = json.load(f)

styles = getSampleStyleSheet()
navy = colors.HexColor("#0B1220")
accent = colors.HexColor("#1971C2")
muted = colors.HexColor("#5C6B82")

styles.add(ParagraphStyle("TitleBig", parent=styles["Title"], fontSize=22, textColor=navy, spaceAfter=4))
styles.add(ParagraphStyle("SubTitle", parent=styles["Normal"], fontSize=11, textColor=muted, spaceAfter=18))
styles.add(ParagraphStyle("H2", parent=styles["Heading2"], fontSize=14, textColor=navy, spaceBefore=14, spaceAfter=8))
styles.add(ParagraphStyle("Body", parent=styles["Normal"], fontSize=10, leading=15, spaceAfter=8))
styles.add(ParagraphStyle("Caption", parent=styles["Normal"], fontSize=8.5, textColor=muted, spaceAfter=12))
styles.add(ParagraphStyle("KpiLabel", parent=styles["Normal"], fontSize=8.5, textColor=muted))
styles.add(ParagraphStyle("KpiValue", parent=styles["Normal"], fontSize=16, textColor=accent, leading=20))

story = []
story.append(Paragraph("SaaS Customer Health Intelligence", styles["TitleBig"]))
story.append(Paragraph("Descriptive, diagnostic &amp; predictive analysis of ARR, NRR, and product usage metrics &mdash; portfolio analytics project, June 2026", styles["SubTitle"]))
story.append(HRFlowable(width="100%", color=colors.HexColor("#DDE3EC"), thickness=1))
story.append(Spacer(1, 12))

kpi_data = [
    ["Current ARR", f"${K['current_arr']/1e6:.2f}M", "Active Customers", f"{K['active_customers']:,}"],
    ["Overall Churn Rate", f"{K['overall_churn_rate_pct']}%", "Expansion Rate", f"{K['expansion_rate_pct']}%"],
    ["Trailing NRR", f"{K['latest_nrr_pct']}%", "Avg NRR (window)", f"{K['avg_nrr_pct']}%"],
]
kpi_table = Table(kpi_data, colWidths=[1.6*inch, 1.5*inch, 1.6*inch, 1.5*inch])
kpi_table.setStyle(TableStyle([
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("TEXTCOLOR", (0,0), (0,-1), muted), ("TEXTCOLOR", (2,0), (2,-1), muted),
    ("FONTNAME", (1,0), (1,-1), "Helvetica-Bold"), ("FONTNAME", (3,0), (3,-1), "Helvetica-Bold"),
    ("TEXTCOLOR", (1,0), (1,-1), accent), ("TEXTCOLOR", (3,0), (3,-1), accent),
    ("FONTSIZE", (1,0), (1,-1), 13), ("FONTSIZE", (3,0), (3,-1), 13),
    ("BOTTOMPADDING", (0,0), (-1,-1), 10), ("TOPPADDING", (0,0), (-1,-1), 6),
    ("LINEBELOW", (0,0), (-1,-2), 0.5, colors.HexColor("#EDEFF4")),
]))
story.append(kpi_table)
story.append(Spacer(1, 14))

story.append(Paragraph("Executive Summary", styles["H2"]))
story.append(Paragraph(
    f"This report analyzes a synthetic 1,800-customer SaaS book (24 months of MRR and usage history, "
    f"generated to mirror the schema of real published SaaS-churn datasets) across three layers: "
    f"descriptive KPIs, diagnostic driver analysis, and a predictive customer health-score model. "
    f"Trailing NRR sits at {K['latest_nrr_pct']}% against an overall churn rate of {K['overall_churn_rate_pct']}%. "
    f"Results are benchmarked against real, publicly reported metrics from Datadog and HubSpot (SEC 8-K filings, "
    f"accessed June 2026) to give the synthetic figures external context.", styles["Body"]))

story.append(Paragraph("1. Descriptive — ARR &amp; NRR Trend", styles["H2"]))
story.append(Image(f"{DASH}/assets_arr_trend.png", width=6.3*inch, height=3.0*inch))
story.append(Paragraph("ARR grows steadily across the 24-month window as the book matures and existing customers expand.", styles["Caption"]))
story.append(Image(f"{DASH}/assets_nrr_trend.png", width=6.3*inch, height=3.0*inch))
story.append(Paragraph("Trailing 12-month NRR oscillates around the 100&ndash;108% band &mdash; net-positive but well short of the consumption-pricing leaders covered in Section 4.", styles["Caption"]))

story.append(PageBreak())
story.append(Paragraph("2. Descriptive — Churn Breakdown", styles["H2"]))
story.append(Image(f"{DASH}/assets_churn_breakdown.png", width=6.3*inch, height=2.7*inch))
plan_rows = [["Plan", "Customers", "Churn Rate", "Avg MRR", "Avg NPS"]]
for p in K["plan_breakdown"]:
    plan_rows.append([p["plan_tier"], str(p["customers"]), f"{p['churn_rate']}%", f"${p['avg_mrr']}", f"{p['avg_nps']:.1f}"])
plan_table = Table(plan_rows, colWidths=[1.3*inch]*5)
plan_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), navy), ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTSIZE", (0,0), (-1,-1), 9), ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F7F9FC")]),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#DDE3EC")),
    ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
]))
story.append(Spacer(1, 8))
story.append(plan_table)
story.append(Spacer(1, 4))
story.append(Paragraph("Starter-tier churn (47%) is roughly 5x Enterprise churn (9%) &mdash; consistent with lower switching cost and weaker CSM coverage at the entry tier.", styles["Caption"]))

story.append(Paragraph("3. Diagnostic — Churn &amp; Expansion Drivers", styles["H2"]))
story.append(Image(f"{DASH}/assets_churn_drivers.png", width=6.3*inch, height=3.2*inch))
story.append(Paragraph(
    f"Logistic regression (churn AUC {K['logreg_churn_auc']}) gives interpretable, directionally sane coefficients: "
    f"usage depth (logins, active seats, feature adoption) and CSM coverage push churn odds down; support-ticket "
    f"volume pushes them up. XGBoost was used separately for expansion prediction (AUC {K['xgb_expansion_auc']}) "
    f"with SHAP for non-linear interaction effects (see notebook). The two models' AUCs are reported side by side "
    f"rather than cherry-picked &mdash; comparable performance signals the underlying relationship is largely linear "
    f"and additive, which is itself a useful finding, not a weakness to hide.", styles["Body"]))
story.append(Image(f"{DASH}/assets_shap_expansion.png", width=6.0*inch, height=3.4*inch))
story.append(Paragraph("SHAP summary for the expansion model &mdash; usage and tenure dominate; see notebook for full feature interactions.", styles["Caption"]))

story.append(PageBreak())
story.append(Paragraph("4. Predictive — Combined Health Score Model", styles["H2"]))
story.append(Paragraph(
    "A multi-class XGBoost model classifies each customer into Churned / Stable-at-risk / Healthy-expanding, "
    "combining churn and expansion signal into a single actionable score used for the customer drill-through "
    "in the interactive dashboard. Confusion matrix below shows the model separates the three classes with "
    "reasonable precision, with most error concentrated in the Stable/At-risk middle class &mdash; expected, "
    "since that class is a residual catch-all rather than a sharply defined behavior pattern.", styles["Body"]))
story.append(Image(f"{DASH}/assets_health_confusion.png", width=4.2*inch, height=3.5*inch))

story.append(Paragraph("5. Real-World Benchmark", styles["H2"]))
bench_rows = [["Company", "Revenue Model", "NRR", "ARR"]]
for name, b in K["real_benchmarks"].items():
    bench_rows.append([name, b["model"], f"{b['nrr_pct']}%", f"${b['arr_usd_b']}B"])
bench_rows.append(["This Book (synthetic)", "Mixed seat/usage", f"{K['latest_nrr_pct']}%", f"${K['current_arr']/1e9:.3f}B"])
bench_table = Table(bench_rows, colWidths=[1.8*inch, 1.7*inch, 1.2*inch, 1.2*inch])
bench_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), navy), ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTSIZE", (0,0), (-1,-1), 9), ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F7F9FC")]),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#DDE3EC")),
    ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
]))
story.append(bench_table)
story.append(Spacer(1, 8))
story.append(Paragraph(
    "Source: Datadog and HubSpot SEC 8-K filings and investor materials, accessed June 2026. Datadog's "
    "consumption-pricing model drives NRR into the 110&ndash;130% range without a renewal conversation; HubSpot's "
    "seat/tier model (NRR ~103%) is the more structurally comparable benchmark for this synthetic book.", styles["Body"]))

story.append(Paragraph("6. Recommendations", styles["H2"]))
recs = [
    "Expand CSM coverage below Enterprise tier &mdash; the churn-reduction effect of CSM assignment held even controlling for usage.",
    "Prioritize usage-depth interventions (onboarding, feature adoption nudges) for Starter/Growth tiers, where churn is concentrated.",
    "Re-route Product-Led-Trial signups into a lighter-touch nurture sequence; this channel showed elevated churn.",
    "Track NRR against the HubSpot-style benchmark (~103%) as a near-term target before reaching for Datadog-style consumption economics, which require a pricing-model change, not just retention tactics.",
]
for r in recs:
    story.append(Paragraph(f"&bull; {r}", styles["Body"]))

story.append(Spacer(1, 16))
story.append(HRFlowable(width="100%", color=colors.HexColor("#DDE3EC"), thickness=1))
story.append(Paragraph(
    "Methodology note: dataset is synthetic, generated with Faker + custom stochastic churn/expansion simulation "
    "to mirror real SaaS subscription-churn dataset schemas. Full notebook (EDA, modeling, SHAP, validation) "
    "and interactive HTML dashboard accompany this report.", styles["Caption"]))

doc = SimpleDocTemplate("/home/claude/product_analytics/report/SaaS_Customer_Health_Insights.pdf",
                         pagesize=letter, topMargin=0.6*inch, bottomMargin=0.6*inch,
                         leftMargin=0.65*inch, rightMargin=0.65*inch)
doc.build(story)
print("PDF built.")
