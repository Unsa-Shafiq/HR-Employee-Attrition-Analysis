import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HR Attrition — Data Analytics Project",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── PALETTE ──────────────────────────────────────────────────────────────────
C = {
    "bg":       "#EDE8E0",   
    "bgL":      "#F5F1EC",   
    "bgD":      "#E0D9CE",   
    "navy":     "#1B2A4A",   
    "navyM":    "#243556",   
    "teal":     "#0D7377",   
    "tealL":    "#14BDBE",   
    "brown":    "#3B2F1E",   
    "brownM":   "#5C4A32",   
    "red":      "#C0392B",   
    "blue":     "#2E86AB",   
    "pink":     "#E8858B",   
    "orange":   "#E67E22",   
    "purple":   "#7B2D8B",   
    "gold":     "#F0A500",   
    "cream":    "#FEFAF4",   
    "border":   "#D4CABC",   
    "gray":     "#8B7D6B",   
    "grayL":    "#E8E0D5",   
}

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
    background-color: {C['bg']} !important;
    color: {C['brown']};
}}
.main {{ background-color: {C['bg']} !important; }}
.main .block-container {{
    padding: 1rem 1.8rem 2rem 1.8rem;
    max-width: 100%;
}}

#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stDecoration"] {{ display: none; }}

[data-testid="stSidebar"] {{
    background: {C['navy']} !important;
    border-right: 3px solid {C['teal']};
}}
[data-testid="stSidebar"] * {{ color: #D4E0F0 !important; }}

.ppt-header {{
    background: linear-gradient(135deg, {C['navy']} 0%, {C['navyM']} 100%);
    border-radius: 10px;
    padding: 1.2rem 1.8rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 24px rgba(27,42,74,0.18);
    border-bottom: 4px solid {C['teal']};
}}
.ppt-header-left h1 {{
    color: white;
    font-family: 'EB Garamond', serif;
    font-size: 1.7rem;
    font-weight: 700;
    margin: 0;
}}
.ppt-header-left p {{ color: {C['tealL']}; font-size: 0.78rem; margin: 0.2rem 0 0 0; font-style: italic; }}

.kpi-card {{
    background: {C['cream']};
    border-radius: 8px;
    padding: 1rem 1.1rem;
    border: 1px solid {C['border']};
    border-left: 5px solid;
    box-shadow: 0 2px 10px rgba(59,47,30,0.07);
    margin-bottom: 1rem;
}}
.kpi-lbl {{ font-size: 0.65rem; font-weight: 700; text-transform: uppercase; color: {C['gray']}; margin-bottom: 0.3rem; }}
.kpi-val {{ font-size: 1.9rem; font-weight: 700; font-family: 'EB Garamond', serif; line-height: 1; }}
.kpi-sub {{ font-size: 0.68rem; color: {C['gray']}; }}

.sec-pill {{
    display: inline-block;
    background: {C['teal']};
    color: white !important;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    padding: 0.22rem 0.75rem;
    border-radius: 4px;
    margin-bottom: 0.55rem;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 0.25rem;
    background: {C['bgD']};
    border-radius: 8px;
    padding: 0.28rem;
    border: 1px solid {C['border']};
    margin-bottom: 1rem;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 6px;
    padding: 0.38rem 1.1rem;
    font-size: 0.76rem;
    font-weight: 600;
    color: {C['brownM']};
}}
.stTabs [aria-selected="true"] {{ background: {C['navy']} !important; color: white !important; }}
</style>
""", unsafe_allow_html=True)

# ── DATA GENERATION ───────────────────────────────────────────────────────────
@st.cache_data
def generate_data():
    np.random.seed(42)
    n = 1470
    attrition = np.random.choice([0,1], n, p=[0.839, 0.161])
    age = np.clip(np.random.normal(37,9,n).astype(int), 18, 60)
    dept = np.random.choice(['Sales','Research & Development','Human Resources'], n, p=[0.30,0.65,0.05])
    gender = np.random.choice(['Male','Female'], n, p=[0.60,0.40])
    overtime = np.where(np.random.rand(n) < np.where(attrition==1,0.54,0.23),'Yes','No')
    jobrole = np.random.choice(['Sales Executive','Research Scientist','Laboratory Technician','Manufacturing Director','Healthcare Representative','Manager','Sales Representative','Research Director','Human Resources'], n)
    monthly_income = np.where(attrition==1, np.random.normal(4500,2000,n), np.random.normal(7000,3000,n)).astype(int)
    years_company = np.where(attrition==1, np.random.exponential(3,n), np.random.exponential(8,n)).astype(int)
    marital = np.random.choice(['Single','Married','Divorced'], n)
    job_sat = np.random.choice([1,2,3,4], n)
    env_sat = np.random.choice([1,2,3,4], n)

    return pd.DataFrame({
        'Attrition': attrition, 'Age': age, 'Department': dept, 'Gender': gender,
        'OverTime': overtime, 'JobRole': jobrole, 'MonthlyIncome': monthly_income,
        'YearsAtCompany': years_company, 'MaritalStatus': marital,
        'JobSatisfaction': job_sat, 'EnvironmentSatisfaction': env_sat
    })

df_raw = generate_data()

# ── PLOTLY THEME ──────────────────────────────────────────────────────────────
def theme(fig, title="", h=320, bg=None):
    fig.update_layout(
        paper_bgcolor=C["cream"],
        plot_bgcolor=bg if bg else C["bgL"],
        font=dict(family="DM Sans, sans-serif", color=C["brown"], size=11),
        title_text=title,
        title=dict(font=dict(color=C["navy"], size=13, family="EB Garamond, serif"), x=0.01),
        margin=dict(l=8, r=8, t=38, b=8),
        height=h,
    )
    return fig

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"<div style='text-align:center;'><h2 style='color:{C['gold']};'>Data Analytics</h2><p style='color:{C['tealL']};'>HR ATTRITION PROJECT</p></div><hr/>", unsafe_allow_html=True)
    sel_dept = st.selectbox("Department", ["All"] + sorted(df_raw["Department"].unique().tolist()))
    sel_gender = st.selectbox("Gender", ["All","Male","Female"])
    sel_ot = st.selectbox("Overtime", ["All","Yes","No"])
    sel_age = st.slider("Age Range", int(df_raw.Age.min()), int(df_raw.Age.max()), (18, 60))

# ── FILTER DATA ───────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_dept != "All": df = df[df.Department == sel_dept]
if sel_gender != "All": df = df[df.Gender == sel_gender]
if sel_ot != "All": df = df[df.OverTime == sel_ot]
df = df[(df.Age >= sel_age[0]) & (df.Age <= sel_age[1])]

n_total = len(df)
n_left = int(df.Attrition.sum())
attr_rate = n_left / n_total * 100 if n_total else 0

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="ppt-header">
  <div class="ppt-header-left">
    <h1>HR Employee Attrition Dashboard</h1>
    <p>Data Analytics Project · Visual Analytics Overview</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI ROW ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
metrics = [
    (k1, "Total Employees", f"{n_total:,}", C["navy"]),
    (k2, "Attrition Count", f"{n_left:,}", C["red"]),
    (k3, "Attrition Rate", f"{attr_rate:.1f}%", C["teal"]),
    (k4, "Avg Monthly Income", f"${df.MonthlyIncome.mean():,.0f}", C["brownM"]),
]
for col, lbl, val, color in metrics:
    with col:
        st.markdown(f"""<div class="kpi-card" style="border-left-color:{color};"><div class="kpi-lbl">{lbl}</div><div class="kpi-val" style="color:{color};">{val}</div></div>""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📊 Demographic Analysis", "📈 Workplace Factors"])

with tab1:
    c1, c2 = st.columns([1, 1.7])
    with c1:
        st.markdown('<span class="sec-pill">Attrition Distribution</span>', unsafe_allow_html=True)
        counts = df.Attrition.value_counts().sort_index()
        fig = go.Figure(go.Bar(x=["No","Yes"], y=counts.values, marker_color=[C["blue"], C["red"]]))
        theme(fig, "Total Count", h=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.markdown('<span class="sec-pill">By Department</span>', unsafe_allow_html=True)
        dg = df.groupby(["Department","Attrition"]).size().unstack(fill_value=0)
        fig = go.Figure()
        fig.add_trace(go.Bar(name="No Attrition", x=dg.index, y=dg[0], marker_color=C["blue"]))
        fig.add_trace(go.Bar(name="Attrition", x=dg.index, y=dg[1], marker_color=C["red"]))
        theme(fig, "Department Comparison", h=300)
        fig.update_layout(barmode="group")
        st.plotly_chart(fig, use_container_width=True)

    c3, c4, c5 = st.columns(3)
    with c3:
        st.markdown('<span class="sec-pill">Gender Split</span>', unsafe_allow_html=True)
        gen = df.groupby("Gender")["Attrition"].mean().mul(100)
        fig = go.Figure(go.Bar(x=gen.index, y=gen.values, marker_color=[C["blue"], C["pink"]]))
        theme(fig, "Attrition Rate (%)", h=250)
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        st.markdown('<span class="sec-pill">Marital Status</span>', unsafe_allow_html=True)
        ms = df.groupby("MaritalStatus")["Attrition"].mean().mul(100)
        fig = go.Figure(go.Bar(x=ms.index, y=ms.values, marker_color=C["teal"]))
        theme(fig, "Attrition Rate (%)", h=250)
        st.plotly_chart(fig, use_container_width=True)

    with c5:
        st.markdown('<span class="sec-pill">Overtime Impact</span>', unsafe_allow_html=True)
        ot = df.groupby("OverTime")["Attrition"].mean().mul(100)
        fig = go.Figure(go.Bar(x=ot.index, y=ot.values, marker_color=[C["blue"], C["red"]]))
        theme(fig, "Attrition Rate (%)", h=250)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown('<span class="sec-pill">Correlation Heatmap</span>', unsafe_allow_html=True)
    corr = df.select_dtypes(include=[np.number]).corr().round(2)
    fig = go.Figure(go.Heatmap(z=corr.values, x=corr.columns, y=corr.columns, colorscale=[[0,C["blue"]],[0.5,C["bgL"]],[1,C["red"]]]))
    theme(fig, "Numeric Correlation Matrix", h=450)
    st.plotly_chart(fig, use_container_width=True)

    c6, c7 = st.columns(2)
    with c6:
        st.markdown('<span class="sec-pill">Job Satisfaction</span>', unsafe_allow_html=True)
        js = df.groupby("JobSatisfaction")["Attrition"].mean().mul(100)
        fig = go.Figure(go.Scatter(x=js.index, y=js.values, mode='lines+markers', line=dict(color=C["red"])))
        theme(fig, "Satisfaction Level vs Attrition", h=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with c7:
        st.markdown('<span class="sec-pill">Income vs Age</span>', unsafe_allow_html=True)
        fig = go.Figure(go.Box(y=df["MonthlyIncome"], x=df["Attrition"], marker_color=C["navy"]))
        theme(fig, "Monthly Income Distribution", h=300)
        st.plotly_chart(fig, use_container_width=True)
