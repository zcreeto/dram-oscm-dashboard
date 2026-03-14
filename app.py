# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║   DRAM SUPPLY CHAIN — OSCM OPERATIONS DASHBOARD                            ║
# ║   FORE School of Management  |  Instructor: Nandan Kumar Singh             ║
# ║   Group: Aman, Ashwin, Khushbu, Kritika, Rishika, Shubhojeet              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
#
# ── GOOGLE COLAB ──────────────────────────────────────────────────────────────
# Cell 1:  !pip install -q streamlit plotly pandas numpy pyngrok
# Cell 2:  Upload this file → app.py
# Cell 3:  from pyngrok import ngrok; ngrok.set_auth_token("TOKEN")
# Cell 4:  import subprocess, time
#          subprocess.Popen(["streamlit","run","app.py","--server.port","8501",
#                            "--server.headless","true"])
#          time.sleep(4)
#          tunnel = ngrok.connect(8501)
#          print(tunnel.public_url)
#
# ── STREAMLIT CLOUD ───────────────────────────────────────────────────────────
# Push app.py + requirements.txt to GitHub → share.streamlit.io → Deploy
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import math

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DRAM Supply Chain — OSCM Dashboard",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── GLOBAL STYLES ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

.stApp { background:#0A0E1A; color:#D1DCE8; }
.main .block-container { padding:1rem 2rem 3rem; max-width:100%; }
#MainMenu,footer,header,.stDeployButton { visibility:hidden; display:none; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  background:#0D1525; border-bottom:2px solid #1E293B; gap:2px; padding:0;
}
.stTabs [data-baseweb="tab"] {
  background:transparent; color:rgba(180,200,220,0.5);
  border:none; border-bottom:3px solid transparent;
  font-family:'Inter',sans-serif; font-size:12px; font-weight:600;
  letter-spacing:.8px; padding:12px 20px; text-transform:uppercase;
}
.stTabs [aria-selected="true"] {
  background:transparent !important; color:#38BDF8 !important;
  border-bottom:3px solid #38BDF8 !important;
}

/* Cards */
.metric-card {
  background:#111827; border:1px solid #1E293B; border-radius:8px;
  padding:14px 16px; font-family:'Inter',sans-serif;
}
.metric-label { font-size:10px; color:rgba(180,200,220,0.45); letter-spacing:1.5px; text-transform:uppercase; margin-bottom:5px; }
.metric-value { font-size:22px; font-weight:700; }
.metric-sub   { font-size:10px; color:rgba(180,200,220,0.4); margin-top:3px; }

/* Stage card */
.stage-card {
  background:#0F172A; border:1px solid #1E293B;
  border-radius:8px; padding:16px; font-family:'Inter',sans-serif; height:100%;
}
.stage-title  { font-size:13px; font-weight:700; color:#E2E8F0; margin-bottom:3px; }
.stage-sub    { font-size:10px; color:rgba(180,200,220,0.45); margin-bottom:12px; }

/* Formula box */
.formula-box {
  background:#070B14; border:1px solid #1E3A5F; border-left:3px solid #38BDF8;
  border-radius:6px; padding:12px 16px; font-family:'JetBrains Mono',monospace;
  font-size:11px; color:#93C5FD; line-height:1.9; margin:8px 0;
}
/* Result highlight */
.result-box {
  background:rgba(56,189,248,0.07); border:1px solid rgba(56,189,248,0.25);
  border-radius:6px; padding:10px 14px; font-family:'JetBrains Mono',monospace;
  font-size:12px; color:#38BDF8; font-weight:600; margin:6px 0;
}
/* Strategy card */
.strat-card {
  background:#0F172A; border:1px solid #1E293B;
  border-radius:8px; padding:16px 18px; font-family:'Inter',sans-serif; margin-bottom:12px;
}
.strat-title  { font-size:13px; font-weight:700; color:#E2E8F0; margin-bottom:6px; }
.strat-body   { font-size:11px; color:rgba(180,200,220,0.7); line-height:1.7; }

/* Section heading */
.sec-head {
  font-family:'Inter',sans-serif; font-size:11px; font-weight:600;
  letter-spacing:2px; text-transform:uppercase; color:rgba(56,189,248,0.7);
  border-bottom:1px solid #1E293B; padding-bottom:6px; margin:18px 0 12px;
}
/* Warning / info banners */
.banner-red  { background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.3);
               border-left:4px solid #EF4444; border-radius:6px; padding:10px 14px;
               font-family:'Inter',sans-serif; font-size:11px; color:#FCA5A5; margin:8px 0; }
.banner-grn  { background:rgba(34,197,94,0.08); border:1px solid rgba(34,197,94,0.25);
               border-left:4px solid #22C55E; border-radius:6px; padding:10px 14px;
               font-family:'Inter',sans-serif; font-size:11px; color:#86EFAC; margin:8px 0; }
.banner-amb  { background:rgba(251,191,36,0.08); border:1px solid rgba(251,191,36,0.25);
               border-left:4px solid #FBBF24; border-radius:6px; padding:10px 14px;
               font-family:'Inter',sans-serif; font-size:11px; color:#FDE68A; margin:8px 0; }

/* Expander */
.streamlit-expanderHeader {
  font-family:'Inter',sans-serif !important; font-size:12px !important;
  color:#94A3B8 !important; background:#0F172A !important;
}

/* Tag pill */
.pill {
  display:inline-block; font-size:9px; font-weight:600; padding:2px 8px;
  border-radius:99px; letter-spacing:.8px; font-family:'Inter',sans-serif;
  text-transform:uppercase; margin-right:4px;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CORE DATA  (4-stage model from report)
# ═══════════════════════════════════════════════════════════════════════════════
STAGES = [
    {"id":1,"name":"Wafer Fabrication","at":60.0,  "ac":1000,"util":98.7,"color":"#EF4444","bottleneck":True,  "companies":"Samsung, SK Hynix, Micron"},
    {"id":2,"name":"Wafer Dicing",      "at":21.4,  "ac":2804,"util":35.2,"color":"#3B82F6","bottleneck":False, "companies":"ASE Technology, Amkor"},
    {"id":3,"name":"Testing & Burn-in", "at":27.3,  "ac":2198,"util":44.9,"color":"#8B5CF6","bottleneck":False, "companies":"ASE Technology, Amkor"},
    {"id":4,"name":"Packaging & Assy.", "at":17.1,  "ac":3509,"util":28.1,"color":"#10B981","bottleneck":False, "companies":"Kingston, Corsair, ADATA"},
]
DEMAND      = 987
FLOW_TIME   = 125.8   # minutes
PC          = 1000    # process capacity = min AC
THROUGHPUT  = 987     # min(demand, PC)

# EOQ base parameters (aligned with report Section 9)
EOQ_D_HR    = 987         # units/hour demand
EOQ_HOURS   = 24*365      # annual operating hours
EOQ_D_ANN   = EOQ_D_HR * EOQ_HOURS
EOQ_UNIT_C  = 183.0       # $/unit (crisis price from OSCM report)
EOQ_HOLD_R  = 0.20        # 20% annual holding rate (standard semiconductor)
EOQ_H       = EOQ_UNIT_C * EOQ_HOLD_R
EOQ_S_BASE  = 50_000.0    # $ setup/order cost

# ─── PLOTLY THEME ─────────────────────────────────────────────────────────────
PLT = dict(
    paper_bgcolor="#0A0E1A", plot_bgcolor="#0D1525",
    font=dict(family="Inter", color="#94A3B8", size=11),
    margin=dict(l=10,r=10,t=40,b=10),
)
GRID = dict(gridcolor="#1E293B", zerolinecolor="#1E293B")

def pltcfg(**kw): return dict(**PLT, **kw)
def ax(**kw):     return dict(**GRID, **kw)

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def hex_rgba(h, a=1.0):
    h=h.lstrip("#"); r,g,b=int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return f"rgba({r},{g},{b},{a})"

def kpi(label, value, color="#38BDF8", sub=""):
    return f"""<div class="metric-card" style="border-top:3px solid {color}">
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color:{color}">{value}</div>
        {'<div class="metric-sub">'+sub+'</div>' if sub else ''}
    </div>"""

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="background:linear-gradient(135deg,#0D1525,#0F1F3D);border-bottom:2px solid #1E293B;
            padding:20px 0 16px;margin:-1rem -2rem 0;padding-left:2rem;padding-right:2rem;">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;flex-wrap:wrap;">
    <span style="background:#EF4444;color:#fff;font-size:9px;font-weight:700;padding:3px 9px;
                 border-radius:4px;font-family:Inter,sans-serif;letter-spacing:1.5px;">
      ● BOTTLENECK — WAFER FAB 98.7%
    </span>
    <span style="font-size:9px;color:rgba(148,163,184,0.6);font-family:Inter,sans-serif;letter-spacing:1px;">
      FORE SCHOOL OF MANAGEMENT &nbsp;|&nbsp; INSTRUCTOR: NANDAN KUMAR SINGH
    </span>
  </div>
  <h1 style="margin:0 0 4px;font-size:22px;color:#E2E8F0;font-family:Inter,sans-serif;font-weight:700;">
    DRAM Supply Chain — Operations & Supply Chain Management Dashboard
  </h1>
  <p style="margin:0;font-size:11px;color:rgba(148,163,184,0.65);font-family:Inter,sans-serif;">
    4-Stage Process Analysis &nbsp;·&nbsp; Bottleneck Identification &nbsp;·&nbsp;
    Alternative Strategies &nbsp;·&nbsp; EOQ / UTC / LTC Analysis &nbsp;·&nbsp;
    Sensitivity Simulation &nbsp;·&nbsp; Break-Even Calculator
  </p>
</div>
""", unsafe_allow_html=True)

# KPI strip
k1,k2,k3,k4,k5,k6 = st.columns(6)
kpis = [
    (k1,"Demand Rate","987 u/hr","#EF4444","Crisis scenario"),
    (k2,"Process Capacity","1,000 u/hr","#EF4444","min{ACᵢ} — Bottleneck"),
    (k3,"Throughput","987 u/hr","#38BDF8","min(D, PC)"),
    (k4,"BN Utilization","98.7%","#F59E0B","Near saturation"),
    (k5,"Flow Time","125.8 min","#8B5CF6","End-to-end"),
    (k6,"Queue Wait","4.55 min","#10B981","M/M/1 model"),
]
for col, label, val, c, sub in kpis:
    col.markdown(kpi(label, val, c, sub), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════════
t1,t2,t3,t4,t5 = st.tabs([
    "⬡  Process & Bottleneck",
    "⚙  Alternative Strategies",
    "📦  EOQ · UTC · LTC",
    "📊  Sensitivity & Simulation",
    "💰  Break-Even Analysis",
])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — PROCESS & BOTTLENECK
# ════════════════════════════════════════════════════════════════════════════════
with t1:
    st.markdown('<div class="sec-head">3.1 — FOUR-STAGE PRODUCTION PROCESS</div>', unsafe_allow_html=True)

    # Stage cards
    cols = st.columns(4)
    for col, s in zip(cols, STAGES):
        with col:
            bn_badge = f'<span class="pill" style="background:{hex_rgba(s["color"],0.2)};color:{s["color"]};border:1px solid {hex_rgba(s["color"],0.4)};">{"● BOTTLENECK" if s["bottleneck"] else "✓ OK"}</span>'
            st.markdown(f"""
            <div class="stage-card" style="border-top:3px solid {s['color']}">
              <div style="font-size:9px;color:rgba(148,163,184,0.45);letter-spacing:2px;margin-bottom:4px;">STAGE {s['id']}</div>
              <div class="stage-title">{s['name']}</div>
              <div class="stage-sub">{s['companies']}</div>
              {bn_badge}
              <div style="margin-top:12px;">
                <div style="display:flex;justify-content:space-between;font-size:10px;padding:4px 0;border-bottom:1px solid #1E293B;">
                  <span style="color:rgba(148,163,184,0.5)">Activity Time</span>
                  <span style="color:#E2E8F0;font-weight:600;font-family:JetBrains Mono">{s['at']} min</span>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:10px;padding:4px 0;border-bottom:1px solid #1E293B;">
                  <span style="color:rgba(148,163,184,0.5)">Capacity AC</span>
                  <span style="color:#E2E8F0;font-weight:600;font-family:JetBrains Mono">{s['ac']:,} u/hr</span>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:10px;padding:4px 0;">
                  <span style="color:rgba(148,163,184,0.5)">Utilization</span>
                  <span style="color:{s['color']};font-weight:700;font-family:JetBrains Mono">{s['util']}%</span>
                </div>
              </div>
              <div style="margin-top:10px;height:4px;background:#1E293B;border-radius:2px;">
                <div style="height:100%;width:{s['util']}%;background:{s['color']};border-radius:2px;"></div>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row ──────────────────────────────────────────────────────────
    ch1, ch2 = st.columns(2)

    with ch1:
        st.markdown('<div class="sec-head">3.3 — Capacity Analysis (PC = min{ACᵢ})</div>', unsafe_allow_html=True)
        fig = go.Figure()
        colors = [s["color"] for s in STAGES]
        fig.add_trace(go.Bar(
            y=[s["name"] for s in STAGES],
            x=[s["ac"] for s in STAGES],
            orientation="h",
            marker=dict(color=[hex_rgba(c,0.75) for c in colors],
                        line=dict(color=colors, width=2)),
            text=[f"{s['ac']:,}" for s in STAGES],
            textposition="inside",
            textfont=dict(color="white", size=11, family="JetBrains Mono"),
            showlegend=False,
        ))
        fig.add_vline(x=DEMAND, line_dash="dot", line_color="#F59E0B", line_width=2,
                      annotation_text=f"Demand {DEMAND}", annotation_font_color="#F59E0B")
        fig.add_vline(x=PC, line_dash="dash", line_color="#EF4444", line_width=2,
                      annotation_text=f"PC = {PC}", annotation_font_color="#EF4444")
        fig.update_layout(
            **pltcfg(title=dict(text="Stage Capacity (u/hr)", font=dict(color="#38BDF8",size=12))),
            xaxis=ax(title=dict(text="units/hour",font=dict(color="#94A3B8")),
                     tickfont=dict(family="JetBrains Mono",size=10)),
            yaxis=dict(tickfont=dict(size=10), gridcolor="#1E293B"),
            height=280,
        )
        st.plotly_chart(fig, use_container_width=True)

    with ch2:
        st.markdown('<div class="sec-head">3.4 — Utilization per Stage</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        util_colors = [s["color"] for s in STAGES]
        fig2.add_trace(go.Bar(
            x=[s["name"] for s in STAGES],
            y=[s["util"] for s in STAGES],
            marker=dict(color=[hex_rgba(c,0.75) for c in util_colors],
                        line=dict(color=util_colors,width=2)),
            text=[f"{s['util']}%" for s in STAGES],
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=11),
            showlegend=False,
        ))
        fig2.add_hline(y=90, line_dash="dash", line_color="#F59E0B", line_width=1,
                       annotation_text="90% Warning", annotation_font_color="#F59E0B")
        fig2.add_hline(y=100, line_dash="dot", line_color="#EF4444", line_width=1)
        fig2.update_layout(
            **pltcfg(title=dict(text="Stage Utilization U = FR/AC", font=dict(color="#38BDF8",size=12))),
            yaxis=ax(title=dict(text="%",font=dict(color="#94A3B8")), range=[0,115],
                     tickfont=dict(family="JetBrains Mono",size=10)),
            xaxis=ax(tickfont=dict(size=10)),
            height=280,
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Math formulas ────────────────────────────────────────────────────────
    st.markdown('<div class="sec-head">3.2 — Activity Cycle Time  &  3.4 — Utilization Calculations</div>',
                unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("""<div class="formula-box">
ACT = AT / N  (N = number of resources)
<br>
ACT₁ = 60.0 / 1 = 60.0 min/unit  ← Bottleneck
ACT₂ = 21.4 / 1 = 21.4 min/unit
ACT₃ = 27.3 / 1 = 27.3 min/unit
ACT₄ = 17.1 / 1 = 17.1 min/unit
<br>
Flow Time FT = 60.0 + 21.4 + 27.3 + 17.1 = 125.8 min
</div>""", unsafe_allow_html=True)
    with m2:
        st.markdown("""<div class="formula-box">
PC = min{AC₁, AC₂, AC₃, AC₄}
   = min{1000, 2804, 2198, 3509} = <b>1000 u/hr</b>
<br>
TH = min{Demand, PC} = min{987, 1000} = <b>987 u/hr</b>
<br>
U₁ = 987/1000 = <b>98.7%</b>  ← Stage 1 is the bottleneck
U₂ = 987/2804 = 35.2%
U₃ = 987/2198 = 44.9%
U₄ = 987/3509 = 28.1%
</div>""", unsafe_allow_html=True)

    # ── Queueing ─────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-head">3.5 — M/M/1 Queueing Analysis — Waiting Time at Bottleneck</div>',
                unsafe_allow_html=True)
    q1, q2, q3 = st.columns(3)
    with q1:
        st.markdown("""<div class="formula-box">
M/M/1 Queue Model
λ = 987 units/hour (arrival rate)
μ = 1000 units/hour (service rate)
ρ = λ/μ = 987/1000 = 0.987
</div>""", unsafe_allow_html=True)
    with q2:
        st.markdown("""<div class="formula-box">
Average waiting time in queue:
Wq = ρ / (μ − λ)
   = 0.987 / (1000 − 987)
   = 0.987 / 13
   = 0.0759 hr = <b>4.55 min</b>
</div>""", unsafe_allow_html=True)
    with q3:
        st.markdown("""<div class="formula-box">
Total time in system:
W = Wq + (1/μ)
  = 0.0759 + 0.001
  = 0.0769 hr = <b>4.6 min</b>

Queue length Lq = λ × Wq = 987 × 0.0759
               = <b>74.9 units</b>
</div>""", unsafe_allow_html=True)

    # Wq vs utilization curve
    st.markdown('<div class="sec-head">INSIGHT — Waiting Time Explodes as Utilization Approaches 100%</div>',
                unsafe_allow_html=True)
    rho_arr = np.linspace(0.01, 0.998, 300)
    mu_val  = 1000
    lam_arr = rho_arr * mu_val
    wq_arr  = rho_arr / (mu_val - lam_arr)          # hours
    wq_min  = wq_arr * 60                            # minutes

    fig_q = go.Figure()
    fig_q.add_trace(go.Scatter(
        x=rho_arr*100, y=wq_min, mode="lines", name="Wq (min)",
        line=dict(color="#38BDF8", width=2),
        fill="tozeroy", fillcolor=hex_rgba("#38BDF8",0.05),
    ))
    fig_q.add_vline(x=98.7, line_dash="dot", line_color="#EF4444", line_width=2,
                    annotation_text="Current 98.7%", annotation_font_color="#EF4444",
                    annotation_position="top left")
    fig_q.add_vline(x=90, line_dash="dash", line_color="#F59E0B", line_width=1.5,
                    annotation_text="Safe zone ≤90%", annotation_font_color="#F59E0B")
    fig_q.add_hrect(y0=0, y1=5, fillcolor=hex_rgba("#22C55E",0.06), line_width=0, annotation_text="Acceptable")
    fig_q.add_hrect(y0=5, y1=20, fillcolor=hex_rgba("#F59E0B",0.06), line_width=0, annotation_text="Warning")
    fig_q.add_hrect(y0=20, y1=200, fillcolor=hex_rgba("#EF4444",0.05), line_width=0, annotation_text="Critical")
    fig_q.update_layout(
        **pltcfg(title=dict(text="Average Queue Waiting Time Wq vs Utilization ρ (M/M/1)", font=dict(color="#38BDF8",size=12))),
        xaxis=ax(title=dict(text="Utilization ρ (%)", font=dict(color="#94A3B8")),
                 range=[0,100], tickfont=dict(family="JetBrains Mono",size=10)),
        yaxis=ax(title=dict(text="Waiting Time (minutes)", font=dict(color="#94A3B8")),
                 range=[0,80], tickfont=dict(family="JetBrains Mono",size=10)),
        height=320, showlegend=False,
    )
    st.plotly_chart(fig_q, use_container_width=True)
    st.markdown("""<div class="banner-red">
    <b>Key Insight:</b> At 98.7% utilization, the average queue wait is 4.55 minutes.
    If utilization reaches 99.5%, waiting time jumps to ~20 minutes. The non-linear relationship
    means small demand increases cause disproportionately large queues — confirming the urgency of
    reducing Wafer Fab utilization to ≤90%.
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — ALTERNATIVE STRATEGIES
# ════════════════════════════════════════════════════════════════════════════════
with t2:
    st.markdown("""<div class="banner-amb">
    <b>Section 4 — Beyond Capacity Expansion:</b> Four alternative operational strategies are
    analysed below, each with interactive calculations showing their quantified impact on
    Activity Cycle Time, system throughput, and the process capacity chart.
    </div>""", unsafe_allow_html=True)

    strat = st.radio("Select Strategy to Analyse:",
                     ["4.2 Inventory Buffering",
                      "4.3 Supplier Diversification",
                      "4.4 Process Redesign (Lean)",
                      "4.5 Task Parallelization & Automation"],
                     horizontal=True, label_visibility="collapsed")

    st.markdown("---")

    # ──────────────────────────────────────────────────────────────────────────
    # 4.2 INVENTORY BUFFERING
    # ──────────────────────────────────────────────────────────────────────────
    if "4.2" in strat:
        st.markdown("### 4.2 — Inventory Buffering Between Production Stages")
        st.markdown("""<div class="strat-card">
        <div class="strat-title">Concept</div>
        <div class="strat-body">
        Placing controlled WIP (Work-In-Process) buffers between stages decouples upstream and
        downstream operations. When the Wafer Fab stalls due to equipment downtime or process variation,
        the downstream Dicing, Testing, and Packaging stages can continue processing from the buffer,
        preventing idle time and preserving system throughput.<br><br>
        However, semiconductor inventory carries <b>high holding costs (~20% of unit cost/year)</b>
        and faces obsolescence risk. The optimal buffer must balance protection against downtime versus cost.
        </div></div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-head">INTERACTIVE — Buffer Sizing Calculator</div>', unsafe_allow_html=True)
        bc1, bc2 = st.columns(2)
        with bc1:
            buf_hours = st.slider("Buffer coverage (hours of demand)", 1, 72, 8,
                                  help="How many hours of demand the buffer should cover")
            downtime_pct = st.slider("Expected Fab downtime (%)", 0.5, 10.0, 2.0, step=0.5)
        with bc2:
            unit_cost = st.number_input("Unit cost ($)", 50.0, 500.0, 183.0, step=5.0)
            hold_rate = st.slider("Annual holding cost rate (%)", 10, 30, 20)

        buf_units     = DEMAND * buf_hours
        hold_cost_hr  = (unit_cost * (hold_rate/100)) / (365*24)
        hold_cost_yr  = unit_cost * (hold_rate/100) * buf_units
        downtime_loss = DEMAND * (downtime_pct/100) * 8760 * unit_cost  # annual cost of lost prod
        net_benefit   = downtime_loss - hold_cost_yr

        st.markdown(f"""<div class="formula-box">
Buffer Units = Demand × Coverage Hours = {DEMAND} × {buf_hours} = <b>{buf_units:,.0f} units</b>
<br>
Annual Holding Cost = Units × Unit Cost × Hold Rate
                    = {buf_units:,.0f} × ${unit_cost:.0f} × {hold_rate}%
                    = <b>${hold_cost_yr:,.0f}</b>
<br>
Annual Production Loss from {downtime_pct}% downtime (without buffer)
= {DEMAND} u/hr × {downtime_pct}% × 8,760 hrs × ${unit_cost:.0f}
= <b>${downtime_loss:,.0f}</b>
<br>
Net Annual Benefit of Buffer = Loss Avoided − Holding Cost
                             = ${downtime_loss:,.0f} − ${hold_cost_yr:,.0f}
                             = <b style="color:{'#22C55E' if net_benefit>0 else '#EF4444'}">${net_benefit:,.0f}</b>
</div>""", unsafe_allow_html=True)

        # Buffer impact chart: throughput with/without buffer under downtime
        downtime_vals = np.linspace(0, 10, 50)
        th_no_buffer  = THROUGHPUT * (1 - downtime_vals/100)
        th_with_buf   = np.minimum(THROUGHPUT * (1 - np.maximum(downtime_vals - buf_hours/(8760/100),0)/100),
                                   THROUGHPUT)

        fig_buf = go.Figure()
        fig_buf.add_trace(go.Scatter(x=downtime_vals, y=th_no_buffer, mode="lines", name="No Buffer",
            line=dict(color="#EF4444", width=2.5, dash="dot")))
        fig_buf.add_trace(go.Scatter(x=downtime_vals, y=th_with_buf, mode="lines",
            name=f"{buf_hours}-hr Buffer",
            line=dict(color="#22C55E", width=2.5),
            fill="tonexty", fillcolor=hex_rgba("#22C55E",0.07)))
        fig_buf.add_vline(x=downtime_pct, line_dash="dot", line_color="#F59E0B",
                          annotation_text=f"Current: {downtime_pct}%",
                          annotation_font_color="#F59E0B")
        fig_buf.update_layout(
            **pltcfg(title=dict(text="Throughput Protection: Buffer vs No-Buffer Under Downtime",
                                font=dict(color="#38BDF8",size=12))),
            xaxis=ax(title=dict(text="Fab Downtime (%)",font=dict(color="#94A3B8")),
                     tickfont=dict(family="JetBrains Mono",size=10)),
            yaxis=ax(title=dict(text="Effective Throughput (u/hr)",font=dict(color="#94A3B8")),
                     tickfont=dict(family="JetBrains Mono",size=10)),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
            height=320,
        )
        st.plotly_chart(fig_buf, use_container_width=True)

        r1,r2,r3 = st.columns(3)
        r1.markdown(kpi("Buffer Size",f"{buf_units:,.0f} units","#38BDF8",f"{buf_hours}-hr coverage"), unsafe_allow_html=True)
        r2.markdown(kpi("Annual Holding Cost",f"${hold_cost_yr:,.0f}","#F59E0B","at 20% hold rate"), unsafe_allow_html=True)
        r3.markdown(kpi("Net Benefit",f"${net_benefit:,.0f}","#22C55E" if net_benefit>0 else "#EF4444","per year"), unsafe_allow_html=True)

    # ──────────────────────────────────────────────────────────────────────────
    # 4.3 SUPPLIER DIVERSIFICATION
    # ──────────────────────────────────────────────────────────────────────────
    elif "4.3" in strat:
        st.markdown("### 4.3 — Supplier Diversification & Risk Pooling")
        st.markdown("""<div class="strat-card">
        <div class="strat-title">Concept</div>
        <div class="strat-body">
        The DRAM industry relies on a few critical suppliers for photolithography machines (ASML),
        specialty chemicals (JSR, Tokyo Ohka), and silicon wafers (Shin-Etsu, SUMCO). A disruption
        at any single supplier can halt production. Diversifying suppliers applies
        <b>portfolio theory (risk pooling)</b>: spreading demand across independent suppliers
        reduces effective supply variance — the same principle as financial portfolio diversification.
        </div></div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-head">INTERACTIVE — Risk Pooling Calculator</div>', unsafe_allow_html=True)
        sc1, sc2 = st.columns(2)
        with sc1:
            sigma_a    = st.slider("Supplier A supply σ (units/week)", 200, 1500, 800)
            sigma_b    = st.slider("Supplier B supply σ (units/week)", 200, 1500, 700)
            rho_ab     = st.slider("Correlation ρ between suppliers", -1.0, 1.0, 0.25, step=0.05,
                                   help="Lower correlation = greater diversification benefit")
        with sc2:
            alpha      = st.slider("% from Supplier A", 10, 90, 50, step=5)
            beta       = 100 - alpha
            z_95       = 1.645   # 95% service level z-score

        var_p = (alpha/100)**2 * sigma_a**2 + (beta/100)**2 * sigma_b**2 \
                + 2*(alpha/100)*(beta/100)*rho_ab*sigma_a*sigma_b
        sigma_p    = math.sqrt(max(var_p, 0))
        risk_redn  = (1 - sigma_p / sigma_a) * 100
        ss_single  = z_95 * sigma_a
        ss_dual    = z_95 * sigma_p
        ss_saving  = ss_single - ss_dual
        unit_c     = 183.0
        annual_sav = ss_saving * unit_c * 0.20   # holding cost saving

        st.markdown(f"""<div class="formula-box">
Portfolio Variance Formula:
σ²_p = α²σ²_A + β²σ²_B + 2αβ·ρ_AB·σ_A·σ_B
     = ({alpha/100:.2f})²×{sigma_a}² + ({beta/100:.2f})²×{sigma_b}²
       + 2×{alpha/100:.2f}×{beta/100:.2f}×{rho_ab:.2f}×{sigma_a}×{sigma_b}
     = {(alpha/100)**2*sigma_a**2:,.0f} + {(beta/100)**2*sigma_b**2:,.0f} + {2*(alpha/100)*(beta/100)*rho_ab*sigma_a*sigma_b:,.0f}
     = {var_p:,.0f}  →  σ_p = <b>{sigma_p:,.0f} units/week</b>
<br>
Risk Reduction = (1 − {sigma_p:.0f}/{sigma_a}) × 100 = <b>{risk_redn:.1f}%</b>
<br>
Safety Stock (single) = z × σ_A = 1.645 × {sigma_a} = <b>{ss_single:,.0f} units</b>
Safety Stock (dual)   = z × σ_p = 1.645 × {sigma_p:.0f} = <b>{ss_dual:,.0f} units</b>
SS Saving = <b>{ss_saving:,.0f} units/week</b>
Annual Holding Cost Saving ≈ <b>${annual_sav:,.0f}</b>
</div>""", unsafe_allow_html=True)

        # Correlation vs risk reduction chart
        rho_vals  = np.linspace(-1, 1, 100)
        rr_vals   = []
        for r in rho_vals:
            vp = (alpha/100)**2*sigma_a**2 + (beta/100)**2*sigma_b**2 + \
                 2*(alpha/100)*(beta/100)*r*sigma_a*sigma_b
            rr_vals.append((1 - math.sqrt(max(vp,0))/sigma_a)*100)

        fig_rp = go.Figure()
        fig_rp.add_trace(go.Scatter(x=rho_vals, y=rr_vals, mode="lines", name="Risk Reduction",
            line=dict(color="#38BDF8",width=2.5),
            fill="tozeroy", fillcolor=hex_rgba("#38BDF8",0.06)))
        fig_rp.add_vline(x=rho_ab, line_dash="dot", line_color="#F59E0B",
                         annotation_text=f"Current ρ={rho_ab}", annotation_font_color="#F59E0B")
        fig_rp.add_hline(y=risk_redn, line_dash="dot", line_color="#22C55E",
                         annotation_text=f"RR={risk_redn:.1f}%", annotation_font_color="#22C55E")
        fig_rp.update_layout(
            **pltcfg(title=dict(text="Supply Risk Reduction vs Supplier Correlation ρ",
                                font=dict(color="#38BDF8",size=12))),
            xaxis=ax(title=dict(text="Correlation ρ",font=dict(color="#94A3B8")),
                     tickfont=dict(family="JetBrains Mono",size=10)),
            yaxis=ax(title=dict(text="Risk Reduction (%)",font=dict(color="#94A3B8")),
                     tickfont=dict(family="JetBrains Mono",size=10)),
            height=300, showlegend=False,
        )
        st.plotly_chart(fig_rp, use_container_width=True)

        r1,r2,r3 = st.columns(3)
        r1.markdown(kpi("Portfolio σ",f"{sigma_p:,.0f} u/wk","#38BDF8",f"vs single {sigma_a:,}"), unsafe_allow_html=True)
        r2.markdown(kpi("Risk Reduction",f"{risk_redn:.1f}%","#22C55E","via diversification"), unsafe_allow_html=True)
        r3.markdown(kpi("SS Saving",f"{ss_saving:,.0f} units","#F59E0B","= ${:,.0f}/yr".format(annual_sav)), unsafe_allow_html=True)

    # ──────────────────────────────────────────────────────────────────────────
    # 4.4 PROCESS REDESIGN (LEAN)
    # ──────────────────────────────────────────────────────────────────────────
    elif "4.4" in strat:
        st.markdown("### 4.4 — Process Redesign (Lean Optimization)")
        st.markdown("""<div class="strat-card">
        <div class="strat-title">Concept</div>
        <div class="strat-body">
        Lean optimization reconfigures production flow to eliminate waste (<i>muda</i>) without adding
        capital. Techniques include reducing lot sizes, rearranging tool sequences, one-piece flow,
        and deploying AI-driven digital twins to simulate and optimise wafer movement.
        Intel's digital twin implementation reduced WIP variability by ~40%.
        Industry data shows 10–30% throughput improvement and 30–50% labour productivity gains.
        </div></div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-head">INTERACTIVE — Lean Improvement Slider</div>', unsafe_allow_html=True)
        lean_pct = st.slider("Lean improvement applied to Wafer Fab ACT (%)", 0, 30, 15,
                             help="Percentage reduction in Wafer Fab Activity Time via lean practices")
        lot_reduction = st.slider("Lot size reduction (%)", 0, 50, 20,
                                  help="Smaller lots reduce WIP and queueing delay")

        new_at1  = 60.0 * (1 - lean_pct/100)
        new_ac1  = (60 / new_at1) * 1000  # scaled
        new_pc   = min(new_ac1, 2804, 2198, 3509)
        new_th   = min(DEMAND, new_pc)
        new_u1   = DEMAND / new_ac1 * 100
        new_lq_time = (DEMAND / new_ac1) / (new_ac1/60 - DEMAND/60) * 60 if new_ac1/60 > DEMAND/60 else 999
        lot_wip_reduction = lot_reduction  # percentage WIP reduction

        st.markdown(f"""<div class="formula-box">
Lean improvement of {lean_pct}% on Wafer Fab:
<br>
New ACT₁ = {60.0} × (1 − {lean_pct}%) = <b>{new_at1:.1f} min/unit</b>
New AC₁  = 1000 × (60/{new_at1:.1f})   = <b>{new_ac1:,.0f} u/hr</b>
<br>
New PC   = min({new_ac1:,.0f}, 2804, 2198, 3509) = <b>{new_pc:,.0f} u/hr</b>
New TH   = min({DEMAND}, {new_pc:,.0f}) = <b>{new_th:,.0f} u/hr</b>
New U₁   = {DEMAND}/{new_ac1:.0f} = <b>{new_u1:.1f}%</b>  (was 98.7%)
<br>
WIP Reduction from Lot-Size cut: <b>−{lot_wip_reduction}%</b>
Wait Time Wq → {min(new_lq_time, 99.0):.1f} min  (was 4.55 min)
</div>""", unsafe_allow_html=True)

        # Side-by-side capacity chart: baseline vs lean
        fig_lean = go.Figure()
        stage_names = [s["name"] for s in STAGES]
        base_caps   = [s["ac"] for s in STAGES]
        lean_caps   = [new_ac1, 2804, 2198, 3509]

        fig_lean.add_trace(go.Bar(name="Baseline", x=stage_names, y=base_caps,
            marker=dict(color=[hex_rgba(s["color"],0.45) for s in STAGES],
                        line=dict(color=[s["color"] for s in STAGES],width=1.5)),
            text=[f"{v:,}" for v in base_caps], textposition="outside",
            textfont=dict(size=10,family="JetBrains Mono")))
        fig_lean.add_trace(go.Bar(name=f"After {lean_pct}% Lean", x=stage_names, y=lean_caps,
            marker=dict(color=[hex_rgba("#22C55E" if i==0 else s["color"],0.75) for i,s in enumerate(STAGES)],
                        line=dict(color=["#22C55E" if i==0 else s["color"] for i,s in enumerate(STAGES)],width=2)),
            text=[f"{v:,.0f}" for v in lean_caps], textposition="outside",
            textfont=dict(size=10,family="JetBrains Mono")))
        fig_lean.add_hline(y=DEMAND, line_dash="dot", line_color="#F59E0B", line_width=2,
                           annotation_text=f"Demand {DEMAND}", annotation_font_color="#F59E0B")
        fig_lean.update_layout(
            **pltcfg(title=dict(text="Capacity: Baseline vs Post-Lean Optimization",
                                font=dict(color="#38BDF8",size=12))),
            yaxis=ax(title=dict(text="Capacity (u/hr)",font=dict(color="#94A3B8")),
                     tickfont=dict(family="JetBrains Mono",size=10)),
            xaxis=ax(tickfont=dict(size=10)), barmode="group",
            legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(size=11)),
            height=320,
        )
        st.plotly_chart(fig_lean, use_container_width=True)

        r1,r2,r3,r4 = st.columns(4)
        r1.markdown(kpi("New ACT₁",f"{new_at1:.1f} min","#22C55E",f"−{lean_pct}% improvement"), unsafe_allow_html=True)
        r2.markdown(kpi("New AC₁",f"{new_ac1:,.0f} u/hr","#22C55E","Fab capacity"), unsafe_allow_html=True)
        r3.markdown(kpi("New Util₁",f"{new_u1:.1f}%","#38BDF8" if new_u1<90 else "#F59E0B","was 98.7%"), unsafe_allow_html=True)
        r4.markdown(kpi("TH Change",f"+{new_th - THROUGHPUT:.0f} u/hr","#22C55E","incremental gain"), unsafe_allow_html=True)

        if lean_pct >= 20:
            st.markdown("""<div class="banner-grn">
            <b>Breakthrough Zone:</b> At ≥20% lean improvement, Wafer Fab is no longer the binding
            constraint — the bottleneck shifts to Testing & Burn-in (2,198 u/hr). This validates
            the OSCM principle: eliminating waste at the bottleneck can shift system constraints
            without capital expenditure.
            </div>""", unsafe_allow_html=True)

    # ──────────────────────────────────────────────────────────────────────────
    # 4.5 TASK PARALLELIZATION
    # ──────────────────────────────────────────────────────────────────────────
    elif "4.5" in strat:
        st.markdown("### 4.5 — Task Parallelization & Automation")
        st.markdown("""<div class="strat-card">
        <div class="strat-title">Concept</div>
        <div class="strat-body">
        Adding parallel processing resources (N machines) at the bottleneck stage directly reduces
        Activity Cycle Time: <b>ACT = AT / N</b>. Intel reported 25% reduction in wafer transport time
        after optimizing Automated Material Handling Systems (AMHS). Parallel testing lanes and
        multiple tools for identical process steps can yield 5–15% overall throughput improvement.
        This is more targeted than full fab expansion — adding 1–2 machines at the bottleneck is
        far cheaper than a new facility.
        </div></div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-head">INTERACTIVE — Parallel Machines at Wafer Fab</div>', unsafe_allow_html=True)
        n_machines = st.slider("Number of parallel Wafer Fab machines (N)", 1, 6, 1,
                               help="N=1 is baseline; N=2 means two machines running simultaneously")
        amhs_gain  = st.slider("AMHS transport time reduction (%)", 0, 30, 25,
                               help="Intel achieved 25% with optimized AMHS routing")

        new_act_par = 60.0 / n_machines
        new_ac_par  = (60 / new_act_par) * 1000
        amhs_boost  = new_ac_par * (1 + amhs_gain/200)  # partial AMHS benefit
        new_pc_par  = min(amhs_boost, 2804, 2198, 3509)
        new_th_par  = min(DEMAND, new_pc_par)
        new_u_par   = DEMAND / amhs_boost * 100

        st.markdown(f"""<div class="formula-box">
Parallelization with N = {n_machines} machine(s):
<br>
ACT₁ = AT / N = 60 / {n_machines} = <b>{new_act_par:.1f} min/unit</b>
AC₁  = 1000 × (60/{new_act_par:.1f}) = <b>{new_ac_par:,.0f} u/hr</b>
<br>
AMHS boost ({amhs_gain}%): effective AC₁ ≈ <b>{amhs_boost:,.0f} u/hr</b>
<br>
New PC  = min({amhs_boost:,.0f}, 2804, 2198, 3509) = <b>{new_pc_par:,.0f} u/hr</b>
New TH  = min({DEMAND}, {new_pc_par:,.0f}) = <b>{new_th_par:,.0f} u/hr</b>
New U₁  = {DEMAND}/{amhs_boost:.0f} = <b>{new_u_par:.1f}%</b>
</div>""", unsafe_allow_html=True)

        # N machines vs capacity/utilization chart
        n_range  = np.arange(1, 8)
        ac_range = [(60/n_machines_i)*1000 for n_machines_i in n_range]
        u_range  = [min(DEMAND/ac*100, 100) for ac in ac_range]
        wq_range = []
        for ac in ac_range:
            mu_i = ac; lam_i = DEMAND
            wq_range.append(min((lam_i/mu_i)/(mu_i-lam_i)*60, 200) if mu_i > lam_i else 200)

        fig_par = make_subplots(specs=[[{"secondary_y":True}]])
        fig_par.add_trace(go.Bar(x=n_range, y=ac_range, name="Fab Capacity (u/hr)",
            marker=dict(color=[hex_rgba("#38BDF8" if n==n_machines else "#1E3A5F",0.8) for n in n_range],
                        line=dict(color="#38BDF8",width=1)),
            text=[f"{int(v):,}" for v in ac_range], textposition="outside",
            textfont=dict(size=10,family="JetBrains Mono")), secondary_y=False)
        fig_par.add_trace(go.Scatter(x=n_range, y=u_range, mode="lines+markers",
            name="Utilization (%)", line=dict(color="#EF4444",width=2.5),
            marker=dict(size=8,color="#EF4444")), secondary_y=True)
        fig_par.add_hline(y=DEMAND, line_dash="dot", line_color="#F59E0B",
                          annotation_text="Demand 987", annotation_font_color="#F59E0B",
                          secondary_y=False)
        fig_par.update_layout(
            **pltcfg(title=dict(text="Capacity & Utilization vs Number of Parallel Fab Machines",
                                font=dict(color="#38BDF8",size=12))),
            xaxis=ax(title=dict(text="N Machines",font=dict(color="#94A3B8")),
                     tickfont=dict(family="JetBrains Mono",size=10), dtick=1),
            legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(size=11)),
            height=320, barmode="group",
        )
        fig_par.update_yaxes(title_text="Capacity (u/hr)",   secondary_y=False,
                             **ax(tickfont=dict(family="JetBrains Mono",size=10)))
        fig_par.update_yaxes(title_text="Utilization (%)",    secondary_y=True,
                             range=[0,110], gridcolor="transparent",
                             tickfont=dict(family="JetBrains Mono",size=10))
        st.plotly_chart(fig_par, use_container_width=True)

        r1,r2,r3,r4 = st.columns(4)
        r1.markdown(kpi("New ACT₁",f"{new_act_par:.1f} min","#22C55E",f"AT/N = 60/{n_machines}"), unsafe_allow_html=True)
        r2.markdown(kpi("Fab Capacity",f"{amhs_boost:,.0f} u/hr","#38BDF8","incl. AMHS boost"), unsafe_allow_html=True)
        r3.markdown(kpi("Utilization",f"{new_u_par:.1f}%","#22C55E" if new_u_par<90 else "#F59E0B","new level"), unsafe_allow_html=True)
        r4.markdown(kpi("Add. Throughput",f"+{new_th_par - THROUGHPUT:.0f} u/hr","#22C55E","vs baseline"), unsafe_allow_html=True)

        if n_machines >= 3:
            st.markdown("""<div class="banner-grn">
            <b>Bottleneck Shift:</b> With 3+ parallel fab machines, the Wafer Fab capacity
            exceeds Testing (2,198 u/hr) and the system bottleneck shifts downstream —
            consistent with Section 3.6 of the report. Capital investment is now justified only
            for the testing stage.
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — EOQ / UTC / LTC
# ════════════════════════════════════════════════════════════════════════════════
with t3:
    st.markdown('<div class="sec-head">EOQ — ECONOMIC ORDER QUANTITY ANALYSIS WITH UTC & LTC CURVES</div>',
                unsafe_allow_html=True)
    st.markdown("""<div class="banner-amb">
    The EOQ model finds the order quantity Q* that minimises total annual inventory cost.
    The <b>UTC (Unit Total Cost)</b> and <b>LTC (Lot Total Cost)</b> curves show how cost components
    behave as Q changes. The <b>slider</b> lets you explore what happens when Q deviates from EOQ —
    showing the zone where the inventory policy is no longer optimal.
    </div>""", unsafe_allow_html=True)

    # ── EOQ Inputs ────────────────────────────────────────────────────────────
    ec1, ec2, ec3 = st.columns(3)
    with ec1:
        st.markdown("**Demand Parameters**")
        eoq_d_hr  = st.number_input("Demand rate (u/hr)", 500, 2000, 987, step=10)
        eoq_d_ann = eoq_d_hr * 24 * 365
        st.caption(f"Annual demand = {eoq_d_ann:,.0f} units")
    with ec2:
        st.markdown("**Cost Parameters**")
        eoq_s  = st.number_input("Setup/Order cost S ($)", 1000, 200000, 50000, step=1000)
        eoq_c  = st.number_input("Unit purchase cost c ($)", 10.0, 500.0, 183.0, step=5.0)
        eoq_hr = st.slider("Annual holding rate (%)", 10, 35, 20)
        eoq_h  = eoq_c * (eoq_hr/100)
    with ec3:
        st.markdown("**Derived Values**")
        eoq_star = math.sqrt(2 * eoq_d_ann * eoq_s / eoq_h)
        tc_star  = math.sqrt(2 * eoq_d_ann * eoq_s * eoq_h)  # annual ordering+holding
        n_orders = eoq_d_ann / eoq_star
        cycle_hr = (eoq_star / eoq_d_hr)  # hours per cycle
        st.markdown(f"""<div class="result-box">
EOQ  = √(2DS/H) = <b>{eoq_star:,.0f} units</b>
TC*  = √(2DSH)  = <b>${tc_star:,.0f}/yr</b>
Orders/yr = D/Q* = {n_orders:.1f}
Cycle time = {cycle_hr:.1f} hours
</div>""", unsafe_allow_html=True)

    # ── EOQ Formula ──────────────────────────────────────────────────────────
    st.markdown('<div class="sec-head">FORMULA DERIVATION</div>', unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    with f1:
        st.markdown(f"""<div class="formula-box">
Total Cost TC(Q) = Ordering Cost + Holding Cost + Purchase Cost
<br>
TC(Q) = (D/Q)·S + (Q/2)·H + D·c
<br>
where:
  D = {eoq_d_ann:,.0f} units/year (annual demand)
  S = ${eoq_s:,.0f} (setup/order cost)
  H = c × r = ${eoq_c:.0f} × {eoq_hr}% = ${eoq_h:.2f}/unit/year
  c = ${eoq_c:.0f}/unit (purchase cost)
<br>
dTC/dQ = 0  →  Q* = √(2DS/H)
       = √(2 × {eoq_d_ann:,.0f} × {eoq_s:,} / {eoq_h:.2f})
       = <b>{eoq_star:,.0f} units</b>
</div>""", unsafe_allow_html=True)
    with f2:
        st.markdown(f"""<div class="formula-box">
LTC (Lot Total Cost) per order cycle:
  LTC(Q) = S + H·(Q/2)
  LTC(Q*) = ${eoq_s:,.0f} + ${eoq_h:.2f}×{eoq_star/2:,.0f}
           = <b>${eoq_s + eoq_h*(eoq_star/2):,.0f}</b>
<br>
UTC (Unit Total Cost) per unit ordered:
  UTC(Q) = S/Q + H/2 + c
  UTC(Q*)= ${eoq_s:,.0f}/{eoq_star:.0f} + ${eoq_h:.2f}/2 + ${eoq_c:.0f}
         = <b>${eoq_s/eoq_star + eoq_h/2 + eoq_c:,.2f}/unit</b>
<br>
At Q = EOQ: Ordering Cost = Holding Cost = ${tc_star/2:,.0f}/yr ✓
</div>""", unsafe_allow_html=True)

    # ── SLIDER — Explore Q vs EOQ ────────────────────────────────────────────
    st.markdown('<div class="sec-head">INTERACTIVE SLIDER — How Q Deviates from EOQ Affects Total Cost</div>',
                unsafe_allow_html=True)
    st.markdown("""<span style="font-size:11px;color:rgba(148,163,184,0.7);font-family:Inter,sans-serif;">
    Move the slider to see real-time cost changes. The <b style="color:#22C55E">green zone</b> is within 10% of EOQ optimal.
    Outside this zone, the policy is <b style="color:#EF4444">no longer in EOQ</b>.</span>""",
                unsafe_allow_html=True)

    q_factor = st.slider("Order quantity Q as multiple of EOQ",
                         min_value=0.10, max_value=3.0, value=1.0, step=0.05,
                         format="%.2f × EOQ")
    q_chosen = q_factor * eoq_star

    # Costs at chosen Q
    ord_cost_q  = (eoq_d_ann / q_chosen) * eoq_s
    hold_cost_q = (q_chosen / 2) * eoq_h
    purch_cost  = eoq_d_ann * eoq_c
    tc_q        = ord_cost_q + hold_cost_q + purch_cost
    tc_eoq_full = tc_star + purch_cost
    pct_above   = (tc_q - tc_eoq_full) / tc_eoq_full * 100
    ltc_q       = eoq_s + eoq_h * (q_chosen/2)
    utc_q       = eoq_s/q_chosen + eoq_h/2 + eoq_c
    in_eoq      = abs(pct_above) <= 10

    # Status banner
    if in_eoq:
        st.markdown(f"""<div class="banner-grn">
        ✓ Q = {q_chosen:,.0f} units ({q_factor:.2f}×EOQ) — <b>WITHIN EOQ ZONE</b> (cost is {pct_above:+.1f}% vs optimal).
        This order quantity is acceptably close to the economic optimum.
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="banner-red">
        ✗ Q = {q_chosen:,.0f} units ({q_factor:.2f}×EOQ) — <b>OUTSIDE EOQ ZONE</b> (cost is {pct_above:+.1f}% above optimal = ${tc_q - tc_eoq_full:,.0f}/yr excess).
        At this quantity, the inventory policy is sub-optimal. Return Q toward {eoq_star:,.0f} units.
        </div>""", unsafe_allow_html=True)

    # ── UTC / LTC / TC Curves ─────────────────────────────────────────────────
    q_vals    = np.linspace(eoq_star*0.05, eoq_star*3.5, 300)
    ord_vals  = (eoq_d_ann / q_vals) * eoq_s
    hold_vals = (q_vals / 2) * eoq_h
    tc_vals   = ord_vals + hold_vals + purch_cost
    ltc_vals  = eoq_s + eoq_h*(q_vals/2)
    utc_vals  = eoq_s/q_vals + eoq_h/2 + eoq_c
    eoq_opt   = eoq_star

    # Green zone band: within ±10% of EOQ
    q_lo = eoq_opt * 0.70
    q_hi = eoq_opt * 1.40

    fig_eoq = make_subplots(rows=1, cols=2,
                             subplot_titles=["Total Cost TC(Q) — EOQ Optimum",
                                             "UTC and LTC Curves"])

    # Left: TC with components
    fig_eoq.add_trace(go.Scatter(x=q_vals, y=tc_vals, mode="lines", name="Total Cost TC(Q)",
        line=dict(color="#38BDF8",width=2.5)), row=1, col=1)
    fig_eoq.add_trace(go.Scatter(x=q_vals, y=ord_vals+purch_cost, mode="lines", name="Ordering Cost",
        line=dict(color="#EF4444",width=1.5,dash="dot")), row=1, col=1)
    fig_eoq.add_trace(go.Scatter(x=q_vals, y=hold_vals+purch_cost, mode="lines", name="Holding Cost",
        line=dict(color="#F59E0B",width=1.5,dash="dot")), row=1, col=1)
    # EOQ vertical
    fig_eoq.add_vline(x=eoq_opt, line_dash="solid", line_color="#22C55E", line_width=2,
                      annotation_text=f"EOQ={eoq_opt:,.0f}", annotation_font_color="#22C55E",
                      row=1, col=1)
    # Green zone band
    fig_eoq.add_vrect(x0=q_lo, x1=q_hi, fillcolor=hex_rgba("#22C55E",0.07),
                      line_width=0, annotation_text="±10% optimal zone", row=1, col=1)
    # Chosen Q marker
    tc_at_q = (eoq_d_ann/q_chosen)*eoq_s + (q_chosen/2)*eoq_h + purch_cost
    fig_eoq.add_trace(go.Scatter(x=[q_chosen], y=[tc_at_q], mode="markers", name="Your Q",
        marker=dict(size=12, color="#EF4444" if not in_eoq else "#22C55E",
                    symbol="diamond", line=dict(color="white",width=2))), row=1, col=1)

    # Right: UTC and LTC
    fig_eoq.add_trace(go.Scatter(x=q_vals, y=utc_vals, mode="lines", name="UTC",
        line=dict(color="#8B5CF6",width=2.5)), row=1, col=2)
    fig_eoq.add_trace(go.Scatter(x=q_vals, y=ltc_vals, mode="lines", name="LTC",
        line=dict(color="#F59E0B",width=2.5)), row=1, col=2)
    fig_eoq.add_vline(x=eoq_opt, line_dash="dash", line_color="#22C55E", line_width=1.5,
                      annotation_text="EOQ", annotation_font_color="#22C55E",
                      row=1, col=2)
    fig_eoq.add_vrect(x0=q_lo, x1=q_hi, fillcolor=hex_rgba("#22C55E",0.07),
                      line_width=0, row=1, col=2)
    # Chosen Q markers
    utc_at_q = eoq_s/q_chosen + eoq_h/2 + eoq_c
    ltc_at_q = eoq_s + eoq_h*(q_chosen/2)
    fig_eoq.add_trace(go.Scatter(x=[q_chosen,q_chosen], y=[utc_at_q, ltc_at_q],
        mode="markers", name="Your Q",
        marker=dict(size=10, color="#EF4444" if not in_eoq else "#22C55E",
                    symbol="diamond", line=dict(color="white",width=1.5)),
        showlegend=False), row=1, col=2)

    fig_eoq.update_layout(
        **pltcfg(height=380),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
    )
    for i in range(1,3):
        fig_eoq.update_xaxes(title_text="Order Quantity Q (units)", **GRID,
                              tickfont=dict(family="JetBrains Mono",size=9), row=1, col=i)
    fig_eoq.update_yaxes(title_text="Annual Cost ($)", **GRID,
                         tickfont=dict(family="JetBrains Mono",size=9), row=1, col=1)
    fig_eoq.update_yaxes(title_text="Cost ($)", **GRID,
                         tickfont=dict(family="JetBrains Mono",size=9), row=1, col=2)
    st.plotly_chart(fig_eoq, use_container_width=True)

    # ── Cost breakdown at chosen Q ────────────────────────────────────────────
    st.markdown('<div class="sec-head">COST BREAKDOWN AT SELECTED Q</div>', unsafe_allow_html=True)
    r1,r2,r3,r4,r5 = st.columns(5)
    r1.markdown(kpi("Order Qty Q",   f"{q_chosen:,.0f}",  "#38BDF8",  f"{q_factor:.2f}×EOQ"), unsafe_allow_html=True)
    r2.markdown(kpi("LTC / Cycle",   f"${ltc_q:,.0f}",   "#F59E0B",  "Lot Total Cost"), unsafe_allow_html=True)
    r3.markdown(kpi("UTC / Unit",    f"${utc_q:,.2f}",   "#8B5CF6",  "Unit Total Cost"), unsafe_allow_html=True)
    r4.markdown(kpi("Annual TC",     f"${tc_q:,.0f}",    "#EF4444" if not in_eoq else "#22C55E", f"{pct_above:+.1f}% vs EOQ"), unsafe_allow_html=True)
    r5.markdown(kpi("EOQ Zone",      "✓ YES" if in_eoq else "✗ NO", "#22C55E" if in_eoq else "#EF4444", "within 10%"), unsafe_allow_html=True)

    # ── Sensitivity: EOQ change with holding cost ─────────────────────────────
    st.markdown('<div class="sec-head">EOQ SENSITIVITY — How EOQ Shifts with Holding Cost Rate</div>',
                unsafe_allow_html=True)
    hr_vals  = np.linspace(5, 40, 100)
    eoq_line = np.sqrt(2 * eoq_d_ann * eoq_s / (eoq_c * hr_vals/100))
    fig_sens = go.Figure()
    fig_sens.add_trace(go.Scatter(x=hr_vals, y=eoq_line, mode="lines",
        line=dict(color="#38BDF8",width=2.5),
        fill="tozeroy", fillcolor=hex_rgba("#38BDF8",0.05)))
    fig_sens.add_vline(x=eoq_hr, line_dash="dot", line_color="#F59E0B",
                       annotation_text=f"Current {eoq_hr}%→EOQ={eoq_star:,.0f}",
                       annotation_font_color="#F59E0B")
    fig_sens.update_layout(
        **pltcfg(title=dict(text="EOQ vs Annual Holding Cost Rate",font=dict(color="#38BDF8",size=12))),
        xaxis=ax(title=dict(text="Holding Rate (%)",font=dict(color="#94A3B8")),
                 tickfont=dict(family="JetBrains Mono",size=10)),
        yaxis=ax(title=dict(text="EOQ (units)",font=dict(color="#94A3B8")),
                 tickfont=dict(family="JetBrains Mono",size=10)),
        height=260, showlegend=False,
    )
    st.plotly_chart(fig_sens, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — SENSITIVITY & SIMULATION
# ════════════════════════════════════════════════════════════════════════════════
with t4:
    st.markdown('<div class="sec-head">7 — SENSITIVITY ANALYSIS & SIMULATION</div>', unsafe_allow_html=True)

    sim_type = st.radio("Analysis type:", ["7.1 Demand Variation", "7.2 Processing Time", "7.3 Utilization Sensitivity"],
                        horizontal=True, label_visibility="collapsed")

    if "7.1" in sim_type:
        st.markdown("#### 7.1 — Demand Variation Scenario Analysis")
        demand_sim = st.slider("Simulated demand rate (u/hr)", 400, 1500, DEMAND, step=10)
        th_sim  = min(demand_sim, PC)
        u_sim   = demand_sim / PC * 100
        unmet   = max(demand_sim - PC, 0)
        rho_sim = min(demand_sim / PC, 0.999)
        wq_sim  = (rho_sim / (PC - demand_sim)) * 60 if demand_sim < PC else 999

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""<div class="formula-box">
TH = min(D, PC) = min({demand_sim}, {PC}) = <b>{th_sim:,} u/hr</b>
U₁ = {demand_sim}/{PC} = <b>{u_sim:.1f}%</b>
Unmet demand = max({demand_sim}−{PC}, 0) = <b>{unmet} u/hr</b>
Wq = {wq_sim:.1f if wq_sim < 900 else '∞'} min
</div>""", unsafe_allow_html=True)

            if demand_sim > PC:
                st.markdown(f"""<div class="banner-red">
                Demand ({demand_sim:,}) exceeds capacity ({PC:,}).
                Unmet demand = <b>{unmet:,} u/hr</b>. Capacity expansion required.
                </div>""", unsafe_allow_html=True)
            elif demand_sim < PC * 0.85:
                st.markdown("""<div class="banner-grn">
                Utilization below 85% — system is operating in a healthy zone with adequate buffer
                for variability absorption.
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class="banner-amb">
                Utilization in 85–100% warning zone. Minor demand spikes may cause queueing.
                </div>""", unsafe_allow_html=True)

        with col_b:
            # Demand sweep chart
            d_vals   = np.arange(400, 1600, 10)
            th_vals  = [min(d, PC) for d in d_vals]
            u_vals   = [min(d/PC*100, 100) for d in d_vals]
            fig_d = go.Figure()
            fig_d.add_trace(go.Scatter(x=d_vals, y=th_vals, mode="lines", name="Throughput",
                line=dict(color="#38BDF8",width=2)))
            fig_d.add_trace(go.Scatter(x=d_vals, y=u_vals, mode="lines", name="Utilization %",
                line=dict(color="#F59E0B",width=2,dash="dot"), yaxis="y2"))
            fig_d.add_vline(x=demand_sim, line_dash="dot", line_color="#EF4444",
                            annotation_text=f"D={demand_sim}", annotation_font_color="#EF4444")
            fig_d.add_vline(x=PC, line_dash="dash", line_color="#22C55E",
                            annotation_text=f"PC={PC}", annotation_font_color="#22C55E")
            fig_d.update_layout(
                **pltcfg(title=dict(text="TH & Utilization vs Demand",font=dict(color="#38BDF8",size=11))),
                xaxis=ax(title=dict(text="Demand (u/hr)"), tickfont=dict(family="JetBrains Mono",size=9)),
                yaxis=ax(title=dict(text="TH (u/hr)"), tickfont=dict(family="JetBrains Mono",size=9)),
                yaxis2=dict(title=dict(text="Utilization (%)"), overlaying="y", side="right",
                            range=[0,120], gridcolor="transparent",
                            tickfont=dict(family="JetBrains Mono",size=9)),
                legend=dict(bgcolor="rgba(0,0,0,0)"), height=300,
            )
            st.plotly_chart(fig_d, use_container_width=True)

        r1,r2,r3,r4 = st.columns(4)
        r1.markdown(kpi("Demand",f"{demand_sim:,} u/hr","#38BDF8","simulation"), unsafe_allow_html=True)
        r2.markdown(kpi("Throughput",f"{th_sim:,} u/hr","#22C55E" if th_sim==demand_sim else "#EF4444","actual"), unsafe_allow_html=True)
        r3.markdown(kpi("Utilization",f"{u_sim:.1f}%","#EF4444" if u_sim>90 else "#22C55E","S1 Wafer Fab"), unsafe_allow_html=True)
        r4.markdown(kpi("Unmet Demand",f"{unmet:,} u/hr","#EF4444" if unmet>0 else "#22C55E","capacity gap"), unsafe_allow_html=True)

    elif "7.2" in sim_type:
        st.markdown("#### 7.2 — Processing Time Sensitivity")
        at1_new = st.slider("Wafer Fab activity time AT₁ (minutes)", 30, 90, 60,
                            help="Reduce via lean/tech improvement; increase via complexity")
        at_others = [21.4, 27.3, 17.1]
        new_ac1_pt = (60 / at1_new) * 1000
        new_pc_pt  = min(new_ac1_pt, 2804, 2198, 3509)
        new_u1_pt  = DEMAND / new_ac1_pt * 100

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""<div class="formula-box">
New ACT₁ = {at1_new} / 1 = {at1_new} min/unit
New AC₁  = (60/{at1_new}) × 1000 = <b>{new_ac1_pt:,.0f} u/hr</b>
New PC   = min({new_ac1_pt:,.0f}, 2804, 2198, 3509) = <b>{new_pc_pt:,.0f} u/hr</b>
New U₁   = {DEMAND}/{new_ac1_pt:.0f} = <b>{new_u1_pt:.1f}%</b>
New FT   = {at1_new}+21.4+27.3+17.1 = <b>{at1_new+21.4+27.3+17.1:.1f} min</b>
</div>""", unsafe_allow_html=True)

        with col2:
            # AT sweep
            at_range = np.linspace(20, 100, 200)
            ac_range_pt = (60/at_range)*1000
            u_range_pt  = np.minimum(DEMAND/ac_range_pt*100, 100)
            fig_at = go.Figure()
            fig_at.add_trace(go.Scatter(x=at_range, y=u_range_pt, mode="lines", name="Utilization",
                line=dict(color="#EF4444",width=2.5)))
            fig_at.add_hline(y=90, line_dash="dash", line_color="#F59E0B",
                             annotation_text="90% target", annotation_font_color="#F59E0B")
            fig_at.add_hline(y=100, line_dash="dot", line_color="#EF4444")
            fig_at.add_vline(x=at1_new, line_dash="dot", line_color="#38BDF8",
                             annotation_text=f"AT={at1_new}min", annotation_font_color="#38BDF8")
            fig_at.update_layout(
                **pltcfg(title=dict(text="Utilization vs Wafer Fab AT₁",font=dict(color="#38BDF8",size=11))),
                xaxis=ax(title=dict(text="Activity Time AT₁ (min)"),tickfont=dict(family="JetBrains Mono",size=9)),
                yaxis=ax(title=dict(text="Utilization (%)"),range=[0,115],tickfont=dict(family="JetBrains Mono",size=9)),
                height=280, showlegend=False,
            )
            st.plotly_chart(fig_at, use_container_width=True)

        # Find break-even AT (where util = 90%)
        at_90 = (DEMAND / (PC * 0.90)) * 60
        st.markdown(f"""<div class="result-box">
To achieve 90% target utilization: AT₁ must drop below <b>{at_90:.1f} min</b>
(requires {(60-at_90)/60*100:.1f}% reduction in Wafer Fab processing time)
</div>""", unsafe_allow_html=True)

    else:  # 7.3
        st.markdown("#### 7.3 — Utilization Sensitivity to Wq (Queue Length)")
        st.markdown("""Shows non-linear relationship between utilization and waiting time —
        justifying the need to maintain ≤90% utilization at the bottleneck stage.""")

        # Wq surface: varying both demand and capacity
        u_range_s = np.linspace(0.5, 99.5, 200)
        wq_range_s = []
        for u in u_range_s:
            rho_val = u/100
            mu_val_s = PC
            lam_val_s = rho_val * mu_val_s
            wq_val = (rho_val / (mu_val_s - lam_val_s)) * 60
            wq_range_s.append(min(wq_val, 150))

        fig_util = go.Figure()
        fig_util.add_trace(go.Scatter(x=u_range_s, y=wq_range_s, mode="lines",
            line=dict(color="#38BDF8",width=2.5),
            fill="tozeroy", fillcolor=hex_rgba("#38BDF8",0.05)))
        fig_util.add_vrect(x0=0, x1=85, fillcolor=hex_rgba("#22C55E",0.06), line_width=0,
                           annotation_text="Safe Zone (≤85%)")
        fig_util.add_vrect(x0=85, x1=95, fillcolor=hex_rgba("#F59E0B",0.06), line_width=0,
                           annotation_text="Warning (85–95%)")
        fig_util.add_vrect(x0=95, x1=100, fillcolor=hex_rgba("#EF4444",0.07), line_width=0,
                           annotation_text="Critical (>95%)")
        fig_util.add_vline(x=98.7, line_color="#EF4444", line_width=2, line_dash="dot",
                           annotation_text="Current 98.7%", annotation_font_color="#EF4444")
        fig_util.update_layout(
            **pltcfg(title=dict(text="Queue Waiting Time Wq vs Utilization — Non-Linear Relationship",
                                font=dict(color="#38BDF8",size=12))),
            xaxis=ax(title=dict(text="Utilization (%)",font=dict(color="#94A3B8")),
                     range=[0,100],tickfont=dict(family="JetBrains Mono",size=10)),
            yaxis=ax(title=dict(text="Wq (minutes)",font=dict(color="#94A3B8")),
                     range=[0,80],tickfont=dict(family="JetBrains Mono",size=10)),
            height=340, showlegend=False,
        )
        st.plotly_chart(fig_util, use_container_width=True)

        # Sensitivity table
        util_pts = [70, 75, 80, 85, 90, 95, 98, 98.7, 99, 99.5]
        rows = []
        for u in util_pts:
            rho = u/100
            lam = rho * PC
            wq  = (rho / (PC - lam)) * 60 if lam < PC else math.inf
            rows.append({"Utilization (%)": u,
                         "λ (u/hr)": int(lam),
                         "Wq (min)": f"{wq:.2f}" if wq < 9999 else "∞",
                         "Zone": "✓ Safe" if u<=85 else ("⚠ Warning" if u<=95 else "✗ Critical")})
        df_util = pd.DataFrame(rows)
        st.dataframe(df_util, hide_index=True, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 5 — BREAK-EVEN ANALYSIS
# ════════════════════════════════════════════════════════════════════════════════
with t5:
    st.markdown('<div class="sec-head">9 — INVESTMENT & BREAK-EVEN ANALYSIS (SECTION 9 OF REPORT)</div>',
                unsafe_allow_html=True)
    st.markdown("""<div class="strat-card">
    <div class="strat-title">Context</div>
    <div class="strat-body">
    Installing an additional wafer fabrication machine increases capacity and revenue.
    The break-even point is when cumulative additional profit equals the investment cost.
    This analysis dynamically evaluates whether the strategy is financially justified.
    </div></div>""", unsafe_allow_html=True)

    bc1, bc2, bc3 = st.columns(3)
    with bc1:
        invest = st.number_input("Investment Cost ($M)", 1.0, 50.0, 10.0, step=0.5) * 1_000_000
    with bc2:
        profit_per_unit = st.number_input("Profit per unit ($)", 1.0, 20.0, 5.0, step=0.5)
        extra_units     = st.number_input("Additional units / hour", 100, 2000, 500, step=50)
    with bc3:
        ops_hours = st.number_input("Operating hours / day", 8, 24, 24)
        ramp_wks  = st.slider("Ramp-up period (weeks)", 0, 12, 4)

    add_profit_hr  = extra_units * profit_per_unit
    add_profit_day = add_profit_hr * ops_hours
    be_hours       = invest / add_profit_hr
    be_days        = invest / add_profit_day
    be_days_ramp   = be_days + ramp_wks * 7
    roi_yr         = (add_profit_day * 365 - invest) / invest * 100 if invest > 0 else 0

    st.markdown(f"""<div class="formula-box">
Additional Profit/hr = extra units × profit/unit = {extra_units} × ${profit_per_unit:.2f} = <b>${add_profit_hr:,.0f}/hr</b>
Additional Profit/day = ${add_profit_hr:,.0f} × {ops_hours} hrs = <b>${add_profit_day:,.0f}/day</b>
<br>
Break-even Hours = Investment / Profit per hour
                 = ${invest:,.0f} / ${add_profit_hr:,.0f}
                 = <b>{be_hours:,.0f} hours</b>
<br>
Break-even Days  = ${invest:,.0f} / ${add_profit_day:,.0f}/day
                 = <b>{be_days:.0f} days</b>  (+{ramp_wks}-wk ramp-up = <b>{be_days_ramp:.0f} days</b>)
<br>
First-Year ROI   = (Annual Profit − Investment) / Investment
                 = (${add_profit_day*365:,.0f} − ${invest:,.0f}) / ${invest:,.0f}
                 = <b>{roi_yr:.1f}%</b>
</div>""", unsafe_allow_html=True)

    # Break-even chart
    hours_range   = np.linspace(0, max(be_hours*2, 8000), 500)
    cumul_profit  = add_profit_hr * hours_range
    invest_line   = np.full_like(hours_range, invest)

    fig_be = go.Figure()
    fig_be.add_trace(go.Scatter(x=hours_range/24, y=cumul_profit, mode="lines", name="Cumulative Revenue",
        line=dict(color="#22C55E",width=2.5),
        fill="tozeroy", fillcolor=hex_rgba("#22C55E",0.05)))
    fig_be.add_trace(go.Scatter(x=hours_range/24, y=invest_line, mode="lines", name="Investment Cost",
        line=dict(color="#EF4444",width=2.5,dash="dot")))
    fig_be.add_vline(x=be_days, line_dash="dash", line_color="#F59E0B", line_width=2,
                     annotation_text=f"Break-even: Day {be_days:.0f}", annotation_font_color="#F59E0B",
                     annotation_position="top left")
    if ramp_wks > 0:
        fig_be.add_vrect(x0=0, x1=ramp_wks*7, fillcolor=hex_rgba("#F59E0B",0.05), line_width=0,
                         annotation_text=f"{ramp_wks}-wk ramp-up", annotation_position="top left")
    fig_be.update_layout(
        **pltcfg(title=dict(text="Break-Even Analysis: Cumulative Profit vs Investment",
                            font=dict(color="#38BDF8",size=12))),
        xaxis=ax(title=dict(text="Days",font=dict(color="#94A3B8")),
                 tickfont=dict(family="JetBrains Mono",size=10)),
        yaxis=ax(title=dict(text="Cumulative $ Profit / Cost",font=dict(color="#94A3B8")),
                 tickfont=dict(family="JetBrains Mono",size=10)),
        legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(size=11)),
        height=340,
    )
    st.plotly_chart(fig_be, use_container_width=True)

    r1,r2,r3,r4 = st.columns(4)
    r1.markdown(kpi("Investment",   f"${invest/1e6:.1f}M", "#EF4444", "capital outlay"), unsafe_allow_html=True)
    r2.markdown(kpi("Break-even",   f"{be_days:.0f} days", "#F59E0B",  f"≈{be_days/30:.1f} months"), unsafe_allow_html=True)
    r3.markdown(kpi("With Ramp-up", f"{be_days_ramp:.0f} days","#F59E0B",f"{ramp_wks}-wk delay"), unsafe_allow_html=True)
    r4.markdown(kpi("First-Year ROI",f"{roi_yr:.0f}%","#22C55E" if roi_yr>0 else "#EF4444","net return"), unsafe_allow_html=True)

    # Strategy comparison table
    st.markdown('<div class="sec-head">STRATEGY COMPARISON — ALL ALTERNATIVES</div>', unsafe_allow_html=True)
    comp_data = {
        "Strategy": ["Capacity Expansion (New Machine)","Inventory Buffering","Supplier Diversification",
                     "Process Redesign (Lean)","Task Parallelization (AMHS)"],
        "Throughput Gain": ["+100–120% if BN shifts","Protects existing TH","No direct TH gain",
                            "+10–30%","+5–15%"],
        "Capital Required": ["High ($10M+)","Low ($1–5M stock)","Low (contracts)",
                             "Minimal (software)","Moderate ($2–10M)"],
        "Lead Time": ["18–36 months","Immediate","1–3 months","3–6 months","3–9 months"],
        "Risk Level":  ["Very High","Low","Low","Low","Medium"],
        "Best For":    ["Long-term demand surge","Downtime protection","Geopolitical/supply risk",
                        "Efficiency & flow","Reducing ACT without full fab"],
    }
    comp_df = pd.DataFrame(comp_data)
    st.dataframe(comp_df, hide_index=True, use_container_width=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="border-top:1px solid #1E293B;padding-top:14px;margin-top:24px;
            font-family:Inter,sans-serif;font-size:9px;color:rgba(148,163,184,0.35);line-height:1.9;">
  <b style="color:rgba(148,163,184,0.5)">OSCM FRAMEWORKS:</b>
  Sessions 2–4 (Process Analysis, Bottleneck, Little's Law) &nbsp;|&nbsp;
  Sessions 5–6 (Forecasting) &nbsp;|&nbsp;
  Sessions 7–9 (Inventory Management, EOQ, Safety Stock, Newsvendor Model) &nbsp;|&nbsp;
  Session 10 (Facility Layout) &nbsp;|&nbsp;
  <b style="color:rgba(148,163,184,0.5)">FORE School of Management</b> &nbsp;|&nbsp;
  Instructor: Nandan Kumar Singh &nbsp;|&nbsp;
  Group: Aman Verma · Ashwin Soni · Khushbu Teotia · Kritika Bhachawat · Rishika Soni · Shubhojeet Mondal &nbsp;|&nbsp;
  Data: SoftwareSeni (2025), ASML, Micron 10-K, SK Hynix, Samsung, McKinsey Semiconductor Report
</div>
""", unsafe_allow_html=True)
