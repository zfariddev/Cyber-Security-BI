import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

# --- PAGE SETTINGS ---
st.set_page_config(page_title="Cyber Security Mega Panel", layout="wide", initial_sidebar_state="collapsed")
pio.templates.default = "plotly_dark"

# --- PREMIUM COMPACT CSS ---
st.markdown("""
<style>
    /* Completely remove Streamlit padding, header, and footer */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Make metric cards chic and compact (Glassmorphism) */
    div[data-testid="metric-container"] {
        background: rgba(30, 30, 47, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 5px 10px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    /* Metric label font size */
    div[data-testid="metric-container"] > div:nth-child(1) {
        font-size: 0.8rem !important;
        color: #a0a0b0;
    }
    /* Metric value font size */
    div[data-testid="metric-container"] > div:nth-child(2) {
        font-size: 1.5rem !important;
        font-weight: 800;
        color: #e0e0e0;
    }
    
    /* Title and Filter styling */
    .dashboard-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #4a90e2, #50e3c2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-top: 10px;
    }
    
    /* Reduce gap between columns */
    div[data-testid="column"] {
        padding: 0 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv("kurumsal_siber_veri.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Date'] = df['Timestamp'].dt.date
    return df

df_raw = load_data()

# --- TOP BAR: TITLE + FILTERS ---
# We put title and filters on the same row to save massive vertical space
t_col, f1, f2, f3, f4 = st.columns([1.5, 1, 1, 1, 1])

with t_col:
    st.markdown('<p class="dashboard-title">🛡️ Cyber Breaches</p>', unsafe_allow_html=True)

with f1:
    countries = ["All"] + sorted(df_raw['Source_Country'].dropna().unique().tolist())
    selected_country = st.selectbox("Country", countries, index=0, label_visibility="collapsed")

with f2:
    departments = ["All"] + sorted(df_raw['Department'].dropna().unique().tolist())
    selected_department = st.selectbox("Department", departments, index=0, label_visibility="collapsed")

with f3:
    os_list = ["All"] + sorted(df_raw['Device_OS'].dropna().unique().tolist())
    selected_os = st.selectbox("Device OS", os_list, index=0, label_visibility="collapsed")

with f4:
    users = ["All"] + sorted(df_raw['User'].dropna().unique().tolist())
    selected_user = st.selectbox("User", users, index=0, label_visibility="collapsed")

# Apply filters
df = df_raw.copy()
if selected_country != "All": df = df[df['Source_Country'] == selected_country]
if selected_department != "All": df = df[df['Department'] == selected_department]
if selected_os != "All": df = df[df['Device_OS'] == selected_os]
if selected_user != "All": df = df[df['User'] == selected_user]
df_breached = df[df['Action_Taken'].isin(['Allowed', 'Alerted Only'])]

# --- KPI METRICS ---
st.write("") # Tiny spacer
col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
with col_m1: st.metric("Total Events", f"{len(df):,}")
with col_m2: st.metric("Critical Breaches", f"{len(df_breached):,}", "-Action", delta_color="inverse")
with col_m3: st.metric("Financial Impact", f"${df['Financial_Impact_USD'].sum():,.0f}")
with col_m4: st.metric("Exfiltrated (GB)", f"{df['Data_Exfiltrated_MB'].sum() / 1024:,.1f} GB")
with col_m5: st.metric("Avg Resolve Time", f"{df['Time_to_Resolve_Mins'].mean() if len(df)>0 else 0:.1f} m")

# --- COMPACT CHARTS GRID (3 Columns) ---
# Chart Height heavily reduced to fit on one screen
CHART_HEIGHT = 220
MARGIN = dict(l=10, r=10, t=30, b=10)

c1, c2, c3 = st.columns(3)

with c1:
    if not df_breached.empty:
        fig1 = px.bar(df_breached.groupby('Department')['Financial_Impact_USD'].sum().reset_index(), 
                      x='Department', y='Financial_Impact_USD', color='Department', text_auto='.2s', title="Financial Impact")
        fig1.update_layout(margin=MARGIN, height=CHART_HEIGHT, showlegend=False, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig1, use_container_width=True)

    if not df.empty:
        iso_map = {
            'Russia': 'RUS', 'China': 'CHN', 'USA': 'USA', 
            'Germany': 'DEU', 'Brazil': 'BRA', 'North Korea': 'PRK', 'Seychelles': 'SYC'
        }
        country_counts = df['Source_Country'].value_counts().reset_index()
        country_counts['iso_alpha'] = country_counts['Source_Country'].map(iso_map)
        fig4 = px.choropleth(country_counts, locations="iso_alpha", locationmode='ISO-3', 
                             color="count", hover_name="Source_Country",
                             color_continuous_scale='Plasma', title="Global Threats")
        fig4.update_layout(margin=MARGIN, height=CHART_HEIGHT, coloraxis_showscale=False)
        st.plotly_chart(fig4, use_container_width=True)

    if not df.empty:
        fig7 = px.histogram(df, x='Time_to_Resolve_Mins', nbins=30, color_discrete_sequence=['cyan'], title="Resolution Time")
        fig7.update_layout(margin=MARGIN, height=CHART_HEIGHT, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig7, use_container_width=True)

    if not df.empty:
        fig10 = px.funnel(df['Action_Taken'].value_counts().reset_index(), x='count', y='Action_Taken', title="Firewall Rate")
        fig10.update_layout(margin=MARGIN, height=CHART_HEIGHT, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig10, use_container_width=True)


with c2:
    if not df_breached.empty:
        fig2 = px.pie(df_breached, values='Financial_Impact_USD', names='Attack_Type', hole=0.5, title="Top Attacks")
        fig2.update_layout(margin=MARGIN, height=CHART_HEIGHT, showlegend=False)
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig2, use_container_width=True)

    if not df.empty:
        fig5 = px.histogram(df, y='Target_Asset', color='Severity', barmode='group', orientation='h', title="Targeted Assets")
        fig5.update_layout(margin=MARGIN, height=CHART_HEIGHT, showlegend=False, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig5, use_container_width=True)

    if not df.empty:
        fig8 = px.pie(df, names='Device_OS', hole=0.5, title="Vulnerable OS")
        fig8.update_layout(margin=MARGIN, height=CHART_HEIGHT, showlegend=False)
        fig8.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig8, use_container_width=True)

    if not df.empty:
        trend = df.groupby('Date').size().reset_index(name='Count')
        fig11 = px.line(trend, x='Date', y='Count', line_shape='spline', title="Time Trend")
        fig11.update_layout(margin=MARGIN, height=CHART_HEIGHT, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig11, use_container_width=True)


with c3:
    if not df.empty:
        treemap_data = df.groupby(['Department', 'Attack_Type']).size().reset_index(name='Count')
        fig3 = px.treemap(treemap_data, path=[px.Constant("Comp"), 'Department', 'Attack_Type'], values='Count', color='Count', color_continuous_scale='Reds', title="Dept Radar")
        fig3.update_layout(margin=MARGIN, height=CHART_HEIGHT)
        st.plotly_chart(fig3, use_container_width=True)

    if not df_breached.empty:
        fig6 = px.box(df_breached, x='Attack_Type', y='Data_Exfiltrated_MB', color='Attack_Type', title="DLP Exfiltration")
        fig6.update_layout(margin=MARGIN, height=CHART_HEIGHT, showlegend=False, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig6, use_container_width=True)

    if not df.empty:
        fig9 = px.bar(df['Attack_Type'].value_counts().reset_index(), x='Attack_Type', y='count', color='Attack_Type', title="Vectors")
        fig9.update_layout(margin=MARGIN, height=CHART_HEIGHT, showlegend=False, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig9, use_container_width=True)

