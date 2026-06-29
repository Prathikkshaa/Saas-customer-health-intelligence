import json

with open("kpis.json") as f:
    K = json.load(f)
with open("scored_customers.json") as f:
    customers_json = f.read()

kpis_json = json.dumps(K)

html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SaaS Customer Health · A Portfolio Analysis</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
:root{
  --paper:#FAF8F3;
  --surface:#FFFFFF;
  --ink:#1A1A1F;
  --muted:#6B6862;
  --rule:#E2DED1;
  --rule-strong:#C9C3B2;
  --neg:#B23A2F;
  --pos:#2E5D4E;
  --neutral:#8B8478;
  --warm:#C9844A;
}
*{box-sizing:border-box;margin:0;padding:0;}
html,body{background:var(--paper);color:var(--ink);font-family:'IBM Plex Sans',sans-serif;font-size:14px;line-height:1.55;}
.page{max-width:1180px;margin:0 auto;padding:48px 44px 60px;}

/* Masthead */
.masthead{border-top:3px solid var(--ink);padding-top:18px;display:flex;justify-content:space-between;align-items:flex-end;gap:24px;margin-bottom:36px;flex-wrap:wrap;}
.kicker{font-family:'IBM Plex Mono',monospace;font-size:10.5px;text-transform:uppercase;letter-spacing:.22em;color:var(--muted);margin-bottom:8px;}
.masthead h1{font-family:'IBM Plex Serif',serif;font-weight:500;font-size:38px;line-height:1.05;letter-spacing:-.5px;max-width:720px;}
.masthead h1 em{font-style:italic;color:var(--neg);font-weight:500;}
.byline{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--muted);text-align:right;line-height:1.7;letter-spacing:.02em;}
.byline strong{color:var(--ink);font-weight:500;}

/* KPI strip */
.kpi-strip{display:grid;grid-template-columns:repeat(6,1fr);border-top:1px solid var(--rule-strong);border-bottom:1px solid var(--rule-strong);margin-bottom:36px;}
.kpi{padding:18px 18px;border-right:1px solid var(--rule);position:relative;}
.kpi:last-child{border-right:none;}
.kpi-label{font-family:'IBM Plex Mono',monospace;font-size:9.5px;text-transform:uppercase;letter-spacing:.18em;color:var(--muted);margin-bottom:10px;}
.kpi-value{font-family:'IBM Plex Serif',serif;font-size:28px;font-weight:500;line-height:1;letter-spacing:-.3px;}
.kpi-value .unit{font-family:'IBM Plex Mono',monospace;font-size:13px;color:var(--muted);font-weight:400;margin-left:3px;}
.kpi-meta{font-family:'IBM Plex Mono',monospace;font-size:10.5px;color:var(--muted);margin-top:8px;}
.kpi-meta.pos{color:var(--pos);}
.kpi-meta.neg{color:var(--neg);}

/* Tabs */
.tab-row{display:flex;gap:0;border-bottom:1px solid var(--rule-strong);margin-bottom:28px;}
.tab{font-family:'IBM Plex Mono',monospace;font-size:11px;text-transform:uppercase;letter-spacing:.16em;padding:14px 22px 12px;color:var(--muted);cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-1px;transition:all .12s;}
.tab:first-child{padding-left:0;}
.tab:hover{color:var(--ink);}
.tab.active{color:var(--ink);border-bottom-color:var(--ink);}

/* Sections */
.section{display:none;}
.section.active{display:block;}
.section-head{display:flex;align-items:baseline;gap:14px;margin-bottom:22px;}
.section-num{font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--muted);letter-spacing:.05em;}
.section-title{font-family:'IBM Plex Serif',serif;font-size:22px;font-weight:500;letter-spacing:-.2px;}
.section-desc{font-family:'IBM Plex Serif',serif;font-style:italic;font-size:14.5px;color:var(--muted);max-width:680px;margin-bottom:24px;line-height:1.6;}

/* Charts */
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:24px;}
.grid-2-wide{display:grid;grid-template-columns:1.4fr 1fr;gap:24px;margin-bottom:24px;}
.grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px;margin-bottom:24px;}
.card{background:var(--surface);border:1px solid var(--rule);padding:22px 22px 18px;}
.card-label{font-family:'IBM Plex Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.16em;color:var(--muted);margin-bottom:6px;}
.card-title{font-family:'IBM Plex Serif',serif;font-size:16px;font-weight:500;margin-bottom:4px;}
.card-sub{font-size:12px;color:var(--muted);margin-bottom:16px;line-height:1.5;}
canvas{max-height:260px;}

/* Prose blocks */
.prose{font-family:'IBM Plex Serif',serif;font-size:14.5px;line-height:1.7;max-width:720px;color:var(--ink);}
.prose p{margin-bottom:12px;}
.prose .pullquote{border-left:2px solid var(--neg);padding-left:18px;margin:18px 0;font-style:italic;color:var(--muted);font-size:14px;}

/* Tables */
.data-table{width:100%;border-collapse:collapse;font-size:13px;}
.data-table th{text-align:left;font-family:'IBM Plex Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.14em;color:var(--muted);padding:10px 12px;border-bottom:1px solid var(--rule-strong);font-weight:500;}
.data-table th.num,.data-table td.num{text-align:right;font-family:'IBM Plex Mono',monospace;font-variant-numeric:tabular-nums;}
.data-table td{padding:9px 12px;border-bottom:1px solid var(--rule);}
.data-table tr:last-child td{border-bottom:none;}
.data-table tr:hover td{background:#F4F0E5;}

/* Risk chips */
.chip{font-family:'IBM Plex Mono',monospace;font-size:10.5px;padding:2px 8px;border:1px solid;display:inline-block;letter-spacing:.04em;}
.chip-high{color:var(--neg);border-color:var(--neg);}
.chip-med{color:var(--warm);border-color:var(--warm);}
.chip-low{color:var(--pos);border-color:var(--pos);}

/* Filters */
.filter-row{display:flex;gap:12px;margin-bottom:18px;flex-wrap:wrap;align-items:center;}
.filter-row label{font-family:'IBM Plex Mono',monospace;font-size:10.5px;text-transform:uppercase;letter-spacing:.14em;color:var(--muted);}
.filter-row select,.filter-row input{background:var(--surface);color:var(--ink);border:1px solid var(--rule-strong);padding:7px 12px;font-family:'IBM Plex Sans',sans-serif;font-size:12.5px;}
.filter-row select:focus,.filter-row input:focus{outline:none;border-color:var(--ink);}
.row-count{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--muted);margin-left:auto;}
.table-scroll{max-height:520px;overflow:auto;border:1px solid var(--rule);background:var(--surface);}

/* Benchmark */
.bench-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border:1px solid var(--rule);}
.bench-cell{padding:22px;border-right:1px solid var(--rule);background:var(--surface);}
.bench-cell:last-child{border-right:none;}
.bench-cell.us{background:#F4F0E5;}
.bench-name{font-family:'IBM Plex Serif',serif;font-size:18px;font-weight:500;margin-bottom:2px;}
.bench-model{font-family:'IBM Plex Mono',monospace;font-size:10.5px;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);margin-bottom:18px;}
.bench-stat{display:flex;justify-content:space-between;padding:8px 0;border-top:1px solid var(--rule);font-size:12.5px;}
.bench-stat .v{font-family:'IBM Plex Mono',monospace;font-variant-numeric:tabular-nums;font-weight:500;}

/* Caveat panel */
.caveat{background:#F4F0E5;border-left:3px solid var(--warm);padding:18px 22px;margin:20px 0;max-width:780px;}
.caveat-label{font-family:'IBM Plex Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.18em;color:var(--warm);margin-bottom:6px;font-weight:500;}
.caveat p{font-family:'IBM Plex Serif',serif;font-size:13.5px;line-height:1.65;color:var(--ink);}

/* Footer */
.colophon{margin-top:48px;padding-top:24px;border-top:1px solid var(--rule-strong);font-family:'IBM Plex Serif',serif;font-style:italic;font-size:12px;color:var(--muted);line-height:1.7;max-width:780px;}

@media(max-width:1000px){
  .kpi-strip{grid-template-columns:repeat(2,1fr);}
  .kpi{border-bottom:1px solid var(--rule);}
  .grid-2,.grid-2-wide,.grid-3{grid-template-columns:1fr;}
  .bench-grid{grid-template-columns:1fr;}
  .bench-cell{border-right:none;border-bottom:1px solid var(--rule);}
  .masthead h1{font-size:30px;}
}
</style>
</head>
<body>
<div class="page">

<div class="masthead">
  <div>
    <div class="kicker">Portfolio Analysis · Issue 01 · June 2026</div>
    <h1>The arithmetic of <em>retention</em>: a SaaS customer-health study.</h1>
  </div>
  <div class="byline">
    <div><strong>Methods</strong> · descriptive, diagnostic, predictive</div>
    <div><strong>Dataset</strong> · 1,800 customers / 24 months</div>
    <div><strong>Benchmarks</strong> · Datadog, HubSpot (SEC 8-K)</div>
  </div>
</div>

<div class="kpi-strip" id="kpiStrip"></div>

<div class="tab-row">
  <div class="tab active" data-tab="descriptive">Descriptive</div>
  <div class="tab" data-tab="diagnostic">Diagnostic</div>
  <div class="tab" data-tab="predictive">Customer Drill-Through</div>
  <div class="tab" data-tab="benchmark">Real-World Benchmark</div>
  <div class="tab" data-tab="notes">Methodology &amp; Caveats</div>
</div>

<!-- DESCRIPTIVE -->
<div class="section active" id="descriptive">
  <div class="section-head"><div class="section-num">01.</div><div class="section-title">Revenue trajectory and the retention floor</div></div>
  <div class="section-desc">Twenty-four months of ARR accumulation against a trailing-twelve-month NRR series that has yet to lift above 110%. The book is growing, but not the way a consumption-pricing business grows.</div>

  <div class="grid-2-wide">
    <div class="card">
      <div class="card-label">Section 01 · Figure A</div>
      <div class="card-title">Annual Recurring Revenue</div>
      <div class="card-sub">Sum of active-customer MRR &times; 12, by month index. Steady accumulation, no inflection.</div>
      <canvas id="arrChart"></canvas>
    </div>
    <div class="card">
      <div class="card-label">Section 01 · Figure B</div>
      <div class="card-title">Net Revenue Retention (TTM)</div>
      <div class="card-sub">100% line marks the break-even between expansion and contraction within the existing cohort.</div>
      <canvas id="nrrChart"></canvas>
    </div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-label">Section 01 · Figure C</div>
      <div class="card-title">Churn by plan tier</div>
      <div class="card-sub">Starter churn runs roughly five times Enterprise.</div>
      <canvas id="planChurnChart"></canvas>
    </div>
    <div class="card">
      <div class="card-label">Section 01 · Figure D</div>
      <div class="card-title">Churn by region</div>
      <div class="card-sub">Distribution is relatively flat &mdash; not the lever.</div>
      <canvas id="regionChurnChart"></canvas>
    </div>
    <div class="card">
      <div class="card-label">Section 01 · Figure E</div>
      <div class="card-title">Churn by acquisition channel</div>
      <div class="card-sub">Product-led trial signups carry the highest baseline risk.</div>
      <canvas id="channelChurnChart"></canvas>
    </div>
  </div>
</div>

<!-- DIAGNOSTIC -->
<div class="section" id="diagnostic">
  <div class="section-head"><div class="section-num">02.</div><div class="section-title">What actually drives churn and expansion</div></div>
  <div class="section-desc">Two models, reported side by side, no cherry-picking. Logistic regression supplies interpretable coefficients; XGBoost handles non-linear interaction effects for the expansion side.</div>

  <div class="grid-2">
    <div class="card">
      <div class="card-label">Section 02 · Figure A</div>
      <div class="card-title">Churn drivers, standardised</div>
      <div class="card-sub">Negative bars push churn odds down. Tenure and CSM coverage dominate; usage and NPS contribute at the margin.</div>
      <canvas id="driverChart"></canvas>
    </div>
    <div class="card">
      <div class="card-label">Section 02 · Figure B</div>
      <div class="card-title">Model comparison · AUC</div>
      <div class="card-sub">Comparable AUCs indicate the signal here is largely linear and additive.</div>
      <canvas id="modelCompareChart"></canvas>
    </div>
  </div>

  <div class="card" style="margin-bottom:24px;">
    <div class="card-label">Section 02 · Figure C</div>
    <div class="card-title">Plan tier economics</div>
    <div class="card-sub">The Starter tier carries most of the churn risk and the least of the revenue.</div>
    <table class="data-table" id="planTable"></table>
  </div>

  <div class="caveat">
    <div class="caveat-label">Methodological honesty</div>
    <p>Tenure is the strongest churn coefficient by a wide margin &mdash; but tenure-at-observation-end is partly downstream of the outcome (a customer who churned in month 4 has tenure 4 regardless of behaviour). In a production setting the right model uses snapshot features at month <em>T</em> to predict churn over months <em>T+1</em>&nbsp;&hellip;&nbsp;<em>T+k</em>. This is called out here rather than hidden in a footnote.</p>
  </div>
</div>

<!-- PREDICTIVE -->
<div class="section" id="predictive">
  <div class="section-head"><div class="section-num">03.</div><div class="section-title">Customer-level health score</div></div>
  <div class="section-desc">A multi-class XGBoost model classifies each customer as Churned, Stable/At-risk, or Healthy/Expanding. The drill-through below scores all 1,800 customers; filter to find the high-risk cohort a CSM team would prioritise.</div>

  <div class="card">
    <div class="filter-row">
      <label>Risk</label>
      <select id="filterRisk"><option value="">All</option><option value="high">High</option><option value="med">Medium</option><option value="low">Low</option></select>
      <label>Plan</label>
      <select id="filterPlan"><option value="">All</option></select>
      <label>Region</label>
      <select id="filterRegion"><option value="">All</option></select>
      <input id="searchBox" placeholder="Customer ID&hellip;">
      <span class="row-count" id="rowCount"></span>
    </div>
    <div class="table-scroll">
      <table class="data-table" id="custTable">
        <thead><tr>
          <th>Customer</th><th>Plan</th><th>Region</th>
          <th class="num">Tenure</th><th class="num">MRR</th><th class="num">Logins/mo</th>
          <th class="num">Tickets/mo</th><th class="num">NPS</th>
          <th>Predicted status</th><th class="num">Risk</th>
        </tr></thead>
        <tbody></tbody>
      </table>
    </div>
  </div>
</div>

<!-- BENCHMARK -->
<div class="section" id="benchmark">
  <div class="section-head"><div class="section-num">04.</div><div class="section-title">Where this book sits against the real world</div></div>
  <div class="section-desc">Two reference points, pulled from SEC 8-K filings and investor materials in June 2026. The gap is real and tells you something about pricing-model architecture, not just retention discipline.</div>

  <div class="bench-grid" id="benchGrid"></div>

  <div class="prose" style="margin-top:24px;">
    <p>Datadog reports trailing NRR in the 110&ndash;130% range because its pricing is consumption-based: a customer's bill grows when their data volumes grow, with no renewal conversation required. HubSpot, on a seat-and-tier model closer to this synthetic book's structure, currently runs around 103%.</p>
    <p>That means the relevant near-term comparison is HubSpot, not Datadog. Closing the gap to Datadog would require a pricing-model change, not a retention initiative. Closing the gap to HubSpot is a CSM-coverage and product-adoption story &mdash; precisely the levers Section 02 identified.</p>
  </div>
</div>

<!-- METHODOLOGY -->
<div class="section" id="notes">
  <div class="section-head"><div class="section-num">05.</div><div class="section-title">Methodology, caveats, and what would change in production</div></div>
  <div class="prose">
    <p><strong>Data.</strong> The customer-level data is synthetic, generated to mirror the schema and behavioural patterns of published SaaS churn datasets (tenure, MRR, login frequency, support tickets, NPS, plan tier, acquisition channel, CSM coverage). It is not real customer data, and is labelled as such throughout. The benchmark figures in Section 04 are real, pulled from Datadog and HubSpot SEC 8-K filings.</p>
    <p><strong>Modelling choices.</strong> Logistic regression and XGBoost AUCs are reported as observed (<span id="aucPair"></span>) rather than after threshold-tuning to favour one. Comparable performance indicates the signal is largely linear and additive in this dataset.</p>
    <p class="pullquote">Tenure-at-observation-end is partly downstream of churn outcome. A forward-looking production model would replace it with a snapshot of usage features at month <em>T</em>.</p>
    <p><strong>NRR computation.</strong> Trailing 12-month, cohort-based: for each month <em>m</em>, the ratio of active-customer MRR at <em>m</em> to that same cohort's MRR at <em>m-12</em>. Customers who joined within the trailing window are excluded from the denominator (otherwise NRR inflates artificially).</p>
    <p><strong>What would change in production.</strong> Live data feeds rather than a snapshot; survival-analysis (Kaplan-Meier, Cox) for time-to-churn rather than binary classification; cohort-specific NRR rather than aggregate; calibration plots and decision curves alongside AUC.</p>
  </div>
</div>

<div class="colophon">
  Synthetic dataset of 1,800 customers across 24 months · Real benchmarks from Datadog and HubSpot SEC 8-K filings and investor materials, accessed June 2026 · Built with Python (pandas, scikit-learn, XGBoost, SHAP) for modelling; Chart.js for in-browser charts; ReportLab for the companion PDF.
</div>

</div>

<script>
const KPIS = __KPIS_JSON__;
const CUSTOMERS = __CUSTOMERS_JSON__;

const INK="#1A1A1F", NEG="#B23A2F", POS="#2E5D4E", NEUTRAL="#8B8478", WARM="#C9844A", RULE="#E2DED1";
const fmtM = n => (n/1e6).toFixed(2);

// Build KPI strip
const nrrDelta = (KPIS.latest_nrr_pct - 100).toFixed(1);
const nrrDeltaText = (nrrDelta >= 0 ? "+" : "") + nrrDelta + " pts vs flat";
const nrrDeltaClass = nrrDelta >= 0 ? "pos" : "neg";
document.getElementById("kpiStrip").innerHTML = `
  <div class="kpi"><div class="kpi-label">Current ARR</div><div class="kpi-value">$${fmtM(KPIS.current_arr)}<span class="unit">M</span></div></div>
  <div class="kpi"><div class="kpi-label">Active customers</div><div class="kpi-value">${KPIS.active_customers.toLocaleString()}</div></div>
  <div class="kpi"><div class="kpi-label">Churn rate</div><div class="kpi-value">${KPIS.overall_churn_rate_pct}<span class="unit">%</span></div></div>
  <div class="kpi"><div class="kpi-label">Trailing NRR</div><div class="kpi-value">${KPIS.latest_nrr_pct}<span class="unit">%</span></div><div class="kpi-meta ${nrrDeltaClass}">${nrrDeltaText}</div></div>
  <div class="kpi"><div class="kpi-label">Expansion rate</div><div class="kpi-value">${KPIS.expansion_rate_pct}<span class="unit">%</span></div></div>
  <div class="kpi"><div class="kpi-label">Avg NRR (window)</div><div class="kpi-value">${KPIS.avg_nrr_pct}<span class="unit">%</span></div></div>
`;

document.getElementById("aucPair").textContent = `LogReg AUC ${KPIS.logreg_churn_auc} for churn, XGBoost AUC ${KPIS.xgb_expansion_auc} for expansion`;

// Chart.js global styling
Chart.defaults.color = "#6B6862";
Chart.defaults.borderColor = RULE;
Chart.defaults.font.family = "'IBM Plex Sans', sans-serif";
Chart.defaults.font.size = 11;

// ARR
new Chart(document.getElementById("arrChart"), {
  type:"line",
  data:{ labels:Object.keys(KPIS.arr_series), datasets:[{
    data:Object.values(KPIS.arr_series),
    borderColor:INK, backgroundColor:"rgba(26,26,31,0.06)",
    fill:true, tension:.25, pointRadius:0, borderWidth:1.5
  }]},
  options:{plugins:{legend:{display:false}}, scales:{
    x:{grid:{display:false}, ticks:{maxRotation:0,autoSkipPadding:12}},
    y:{ticks:{callback:v=>"$"+(v/1e6).toFixed(1)+"M"}, grid:{color:RULE, drawBorder:false}}
  }}
});
// NRR
new Chart(document.getElementById("nrrChart"), {
  type:"line",
  data:{ labels:Object.keys(KPIS.nrr_series), datasets:[{
    data:Object.values(KPIS.nrr_series),
    borderColor:NEG, backgroundColor:"rgba(178,58,47,0.07)",
    fill:true, tension:.25, pointRadius:0, borderWidth:1.5
  }]},
  options:{
    plugins:{legend:{display:false},
      annotation:{annotations:{line1:{type:"line", yMin:100, yMax:100, borderColor:NEUTRAL, borderDash:[3,3], borderWidth:1}}}},
    scales:{
      x:{grid:{display:false}, ticks:{maxRotation:0,autoSkipPadding:12}},
      y:{suggestedMin:95,suggestedMax:115, grid:{color:RULE, drawBorder:false}, ticks:{callback:v=>v+"%"}}
    }
  }
});
// Plan churn
new Chart(document.getElementById("planChurnChart"), {
  type:"bar",
  data:{labels:KPIS.plan_breakdown.map(p=>p.plan_tier),
    datasets:[{data:KPIS.plan_breakdown.map(p=>p.churn_rate), backgroundColor:NEG, borderWidth:0}]},
  options:{plugins:{legend:{display:false}},
    scales:{x:{grid:{display:false}}, y:{grid:{color:RULE, drawBorder:false}, ticks:{callback:v=>v+"%"}}}}
});
// Region churn
new Chart(document.getElementById("regionChurnChart"), {
  type:"bar",
  data:{labels:Object.keys(KPIS.churn_by_region), datasets:[{data:Object.values(KPIS.churn_by_region), backgroundColor:INK, borderWidth:0}]},
  options:{indexAxis:"y", plugins:{legend:{display:false}},
    scales:{y:{grid:{display:false}}, x:{grid:{color:RULE, drawBorder:false}, ticks:{callback:v=>v+"%"}}}}
});
// Channel churn
new Chart(document.getElementById("channelChurnChart"), {
  type:"bar",
  data:{labels:Object.keys(KPIS.churn_by_channel), datasets:[{data:Object.values(KPIS.churn_by_channel), backgroundColor:NEUTRAL, borderWidth:0}]},
  options:{indexAxis:"y", plugins:{legend:{display:false}},
    scales:{y:{grid:{display:false}}, x:{grid:{color:RULE, drawBorder:false}, ticks:{callback:v=>v+"%"}}}}
});

// Driver chart from REAL coefficients
const coefs = KPIS.churn_driver_coefs;
const driverEntries = Object.entries(coefs).sort((a,b)=>a[1]-b[1]);
new Chart(document.getElementById("driverChart"), {
  type:"bar",
  data:{labels:driverEntries.map(d=>d[0]),
    datasets:[{data:driverEntries.map(d=>d[1]),
      backgroundColor:driverEntries.map(d=>d[1]>0?NEG:POS), borderWidth:0}]},
  options:{indexAxis:"y", plugins:{legend:{display:false}},
    scales:{y:{grid:{display:false}}, x:{grid:{color:RULE, drawBorder:false}}}}
});

// Model compare
new Chart(document.getElementById("modelCompareChart"), {
  type:"bar",
  data:{labels:["LogReg · churn", "XGBoost · expansion"],
    datasets:[{data:[KPIS.logreg_churn_auc, KPIS.xgb_expansion_auc],
      backgroundColor:[INK, WARM], borderWidth:0}]},
  options:{plugins:{legend:{display:false}},
    scales:{x:{grid:{display:false}}, y:{min:0.5,max:1, grid:{color:RULE, drawBorder:false}}}}
});

// Plan table
const planTable = document.getElementById("planTable");
planTable.innerHTML = `<thead><tr>
  <th>Plan</th><th class="num">Customers</th><th class="num">Churn rate</th><th class="num">Avg MRR</th><th class="num">Avg NPS</th>
</tr></thead><tbody>` + KPIS.plan_breakdown.map(p=>`
  <tr><td>${p.plan_tier}</td><td class="num">${p.customers}</td>
  <td class="num">${p.churn_rate}%</td><td class="num">$${p.avg_mrr.toFixed(0)}</td>
  <td class="num">${p.avg_nps.toFixed(1)}</td></tr>`).join("") + "</tbody>";

// Benchmark grid
const bench = KPIS.real_benchmarks;
let benchHTML = "";
for (const [name, b] of Object.entries(bench)) {
  benchHTML += `
    <div class="bench-cell">
      <div class="bench-name">${name}</div>
      <div class="bench-model">${b.model}</div>
      <div class="bench-stat"><span>NRR</span><span class="v">${b.nrr_pct}%</span></div>
      <div class="bench-stat"><span>ARR</span><span class="v">$${b.arr_usd_b}B</span></div>
    </div>`;
}
benchHTML += `
  <div class="bench-cell us">
    <div class="bench-name">This book</div>
    <div class="bench-model">Synthetic · mixed model</div>
    <div class="bench-stat"><span>NRR</span><span class="v">${KPIS.latest_nrr_pct}%</span></div>
    <div class="bench-stat"><span>ARR</span><span class="v">$${fmtM(KPIS.current_arr)}M</span></div>
  </div>`;
document.getElementById("benchGrid").innerHTML = benchHTML;

// Tabs
document.querySelectorAll(".tab").forEach(t => {
  t.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(x=>x.classList.remove("active"));
    document.querySelectorAll(".section").forEach(x=>x.classList.remove("active"));
    t.classList.add("active");
    document.getElementById(t.dataset.tab).classList.add("active");
  });
});

// Customer table
const plans = [...new Set(CUSTOMERS.map(c=>c.plan_tier))];
const regions = [...new Set(CUSTOMERS.map(c=>c.region))];
plans.forEach(p => document.getElementById("filterPlan").innerHTML += `<option value="${p}">${p}</option>`);
regions.forEach(r => document.getElementById("filterRegion").innerHTML += `<option value="${r}">${r}</option>`);

function riskBucket(s){ return s>=60?"high":s>=30?"med":"low"; }
function statusLabel(p){ return p===0?"Churned":p===2?"Healthy / expanding":"Stable / at-risk"; }

function renderTable(){
  const riskF = document.getElementById("filterRisk").value;
  const planF = document.getElementById("filterPlan").value;
  const regionF = document.getElementById("filterRegion").value;
  const q = document.getElementById("searchBox").value.toLowerCase();
  const rows = CUSTOMERS.filter(c=>{
    if(riskF && riskBucket(c.risk_score_0_100)!==riskF) return false;
    if(planF && c.plan_tier!==planF) return false;
    if(regionF && c.region!==regionF) return false;
    if(q && !c.customer_id.toLowerCase().includes(q)) return false;
    return true;
  });
  const shown = rows.slice(0, 500);
  document.getElementById("rowCount").textContent =
    `Showing ${shown.length.toLocaleString()} of ${rows.length.toLocaleString()} matching · ${CUSTOMERS.length.toLocaleString()} total`;
  document.querySelector("#custTable tbody").innerHTML = shown.map(c=>{
    const rb = riskBucket(c.risk_score_0_100);
    return `<tr>
      <td>${c.customer_id}</td><td>${c.plan_tier}</td><td>${c.region}</td>
      <td class="num">${c.tenure_months}</td>
      <td class="num">$${c.current_mrr.toFixed(0)}</td>
      <td class="num">${c.avg_logins.toFixed(1)}</td>
      <td class="num">${c.avg_support_tickets.toFixed(1)}</td>
      <td class="num">${c.avg_nps.toFixed(0)}</td>
      <td>${statusLabel(c.health_score_pred)}</td>
      <td class="num"><span class="chip chip-${rb}">${c.risk_score_0_100}</span></td>
    </tr>`;
  }).join("");
}
["filterRisk","filterPlan","filterRegion","searchBox"].forEach(id =>
  document.getElementById(id).addEventListener("input", renderTable));
renderTable();
</script>
</body>
</html>
"""

html = html.replace("__KPIS_JSON__", kpis_json).replace("__CUSTOMERS_JSON__", customers_json)
with open("saas_health_dashboard.html","w") as f:
    f.write(html)
print("Dashboard rebuilt:", len(html), "bytes")
