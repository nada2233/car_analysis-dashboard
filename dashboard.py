import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AutoPulse · Car Sales Intelligence",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #080810; color: #ddddf0; }
section[data-testid="stSidebar"] { background: #0c0c18 !important; border-right: 1px solid #1a1a30 !important; }
section[data-testid="stSidebar"] * { color: #b0b0d0 !important; }
.dash-header { background: linear-gradient(120deg,#0c0c1e 0%,#130d20 60%,#0c0c1e 100%); border:1px solid #1e1830; border-radius:18px; padding:36px 44px; margin-bottom:30px; position:relative; overflow:hidden; }
.dash-header::before { content:''; position:absolute; top:-80px; right:-60px; width:260px; height:260px; background:radial-gradient(circle,rgba(255,72,40,0.18) 0%,transparent 65%); border-radius:50%; }
.dash-title { font-family:'Bebas Neue',sans-serif; font-size:3.6rem; letter-spacing:6px; color:#fff; margin:0; line-height:1; }
.dash-title span { color:#ff4828; }
.dash-sub { font-size:0.78rem; color:#5a5a80; letter-spacing:4px; text-transform:uppercase; margin-top:8px; }
.dash-badge { display:inline-block; background:rgba(255,72,40,0.15); border:1px solid rgba(255,72,40,0.3); border-radius:20px; padding:3px 12px; font-size:0.7rem; color:#ff6848; letter-spacing:2px; text-transform:uppercase; margin-top:14px; }
.kpi-wrap { display:flex; gap:14px; margin-bottom:28px; }
.kpi-card { flex:1; background:#0c0c1e; border:1px solid #1a1a30; border-radius:14px; padding:22px 20px; position:relative; overflow:hidden; transition:all 0.25s; }
.kpi-card:hover { border-color:#ff4828; transform:translateY(-2px); box-shadow:0 8px 30px rgba(255,72,40,0.12); }
.kpi-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,#ff4828,#ff8040); }
.kpi-label { font-size:0.65rem; color:#505070; text-transform:uppercase; letter-spacing:2.5px; margin-bottom:10px; }
.kpi-value { font-family:'Bebas Neue',sans-serif; font-size:2.1rem; color:#fff; letter-spacing:1px; line-height:1; }
.kpi-sub { font-size:0.72rem; margin-top:6px; }
.kpi-sub.green { color:#40d090; }
.kpi-sub.red   { color:#ff4828; }
.kpi-sub.blue  { color:#40a0ff; }
.kpi-icon { position:absolute; top:18px; right:18px; font-size:1.4rem; opacity:0.25; }
.sec-title { font-family:'Bebas Neue',sans-serif; font-size:1.3rem; letter-spacing:4px; color:#ff4828; border-left:3px solid #ff4828; padding-left:12px; margin:8px 0 18px 0; }
.divider { height:1px; background:linear-gradient(90deg,#1a1a30 0%,transparent 100%); margin:20px 0; }
.stTabs [data-baseweb="tab-list"] { background:#0c0c1e !important; border:1px solid #1a1a30 !important; border-radius:12px; gap:3px; padding:5px; }
.stTabs [data-baseweb="tab"] { background:transparent !important; color:#5a5a80 !important; border-radius:9px; font-weight:500; font-size:0.83rem; }
.stTabs [aria-selected="true"] { background:#ff4828 !important; color:#fff !important; }
</style>
""", unsafe_allow_html=True)

# ─── PLOTLY THEME ─────────────────────────────────────────────────────────────
COLORS = ['#ff4828','#ff8040','#ffb840','#40c8ff','#40ff9f','#c040ff','#ff40b0','#40b0ff','#80ff40','#ff4080']

def apply_theme(fig, title=""):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', color='#8888b0', size=12),
        title=dict(text=title, font=dict(family='DM Sans', color='#e0e0f8', size=14)),
        xaxis=dict(gridcolor='#14142a', linecolor='#1a1a30', tickfont=dict(color='#606080')),
        yaxis=dict(gridcolor='#14142a', linecolor='#1a1a30', tickfont=dict(color='#606080')),
        legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='#1a1a30', font=dict(color='#8888b0')),
        colorway=COLORS,
        margin=dict(l=8, r=8, t=45, b=8),
        hoverlabel=dict(bgcolor='#0f0f20', bordercolor='#1a1a30', font=dict(color='#e0e0f8')),
    )
    return fig

# ─── LOAD DATA ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")
    df['Gross'] = df['SellingPrice'] - df['MMR']
    df['GrossMarginPct'] = ((df['Gross'] / df['MMR'].replace(0, np.nan)) * 100).round(2)
    df['Underpriced'] = df['SellingPrice'] < df['MMR']
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️  `cleaned_data.csv` not found — place it in the same directory as this script.")
    st.stop()

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;letter-spacing:4px;color:#ff4828;margin-bottom:2px'>AUTOPULSE</div>
    <div style='font-size:0.65rem;color:#303050;letter-spacing:3px;text-transform:uppercase;margin-bottom:22px;border-bottom:1px solid #1a1a30;padding-bottom:14px'>Filter Controls</div>
    """, unsafe_allow_html=True)

    sel_makes  = st.multiselect("🏷️ Make",         sorted(df['Make'].unique()),        default=df['Make'].value_counts().head(8).index.tolist())
    sel_bodies = st.multiselect("🚘 Body Type",     sorted(df['Body'].dropna().unique()), default=sorted(df['Body'].dropna().unique()))
    sel_trans  = st.multiselect("⚙️ Transmission",  sorted(df['Transmission'].dropna().unique()), default=sorted(df['Transmission'].dropna().unique()))

    p_min, p_max = int(df['SellingPrice'].min()), int(df['SellingPrice'].max())
    price_range  = st.slider("💰 Price Range ($)", p_min, p_max, (p_min, p_max), step=500, format="$%d")

    y_min, y_max = int(df['Year'].min()), int(df['Year'].max())
    year_range   = st.slider("📅 Mfg. Year", y_min, y_max, (y_min, y_max))

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.65rem;color:#252540;text-align:center'>AutoPulse v1.0</div>", unsafe_allow_html=True)

# ─── FILTER ───────────────────────────────────────────────────────────────────
fdf = df.copy()
if sel_makes:   fdf = fdf[fdf['Make'].isin(sel_makes)]
if sel_bodies:  fdf = fdf[fdf['Body'].isin(sel_bodies)]
if sel_trans:   fdf = fdf[fdf['Transmission'].isin(sel_trans)]
fdf = fdf[(fdf['SellingPrice'] >= price_range[0]) & (fdf['SellingPrice'] <= price_range[1]) &
          (fdf['Year'] >= year_range[0]) & (fdf['Year'] <= year_range[1])]

if len(fdf) == 0:
    st.warning("No data matches the selected filters.")
    st.stop()

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class='dash-header'>
  <div class='dash-title'>AUTO<span>PULSE</span></div>
  <div class='dash-sub'>Car Sales Intelligence Dashboard</div>
  <div class='dash-badge'>Live Filter Active</div>
</div>
""", unsafe_allow_html=True)

# ─── KPIs ─────────────────────────────────────────────────────────────────────
avg_gross  = fdf['Gross'].mean()
gross_cls  = "red" if avg_gross < 0 else "green"
gross_lbl  = "below market" if avg_gross < 0 else "above market"
top_make   = fdf['Make'].value_counts().index[0]

st.markdown(f"""
<div class='kpi-wrap'>
  <div class='kpi-card'><div class='kpi-icon'>💵</div><div class='kpi-label'>Total Revenue</div><div class='kpi-value'>${fdf['SellingPrice'].sum()/1e6:.1f}M</div><div class='kpi-sub blue'>{len(fdf):,} transactions</div></div>
  <div class='kpi-card'><div class='kpi-icon'>🏷️</div><div class='kpi-label'>Avg Selling Price</div><div class='kpi-value'>${fdf['SellingPrice'].mean():,.0f}</div><div class='kpi-sub green'>per vehicle</div></div>
  <div class='kpi-card'><div class='kpi-icon'>📊</div><div class='kpi-label'>Avg Gross vs MMR</div><div class='kpi-value'>${avg_gross:+,.0f}</div><div class='kpi-sub {gross_cls}'>{gross_lbl}</div></div>
  <div class='kpi-card'><div class='kpi-icon'>⚠️</div><div class='kpi-label'>Underpriced Cars</div><div class='kpi-value'>{fdf['Underpriced'].mean()*100:.1f}%</div><div class='kpi-sub red'>sold below MMR</div></div>
  <div class='kpi-card'><div class='kpi-icon'>🥇</div><div class='kpi-label'>Top Make</div><div class='kpi-value' style='font-size:1.6rem'>{top_make}</div><div class='kpi-sub blue'>{fdf['Make'].nunique()} makes · {fdf['Model'].nunique()} models</div></div>
</div>
""", unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
t1,t2,t3,t4,t5,t6,t7 = st.tabs(["📅 Time","🏷️ Brand & Market","🔩 Trim & Body","💰 Price & Value","🔧 Condition & Usage","🏪 Sellers","🌍 Geography"])

# ── TAB 1 — TIME ──────────────────────────────────────────────────────────────
with t1:
    st.markdown("<div class='sec-title'>Time-Based Analysis</div>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        mon = fdf.groupby('SaleMonth')['SellingPrice'].sum().reset_index()
        fig = px.bar(mon, x='SaleMonth', y='SellingPrice', text_auto='.2s')
        fig.update_traces(marker_color='#ff4828', textfont_color='white')
        st.plotly_chart(apply_theme(fig,"Total Revenue per Month"), use_container_width=True)
    with c2:
        avg_m = fdf.groupby('SaleMonth')['SellingPrice'].mean().round().reset_index()
        fig = px.line(avg_m, x='SaleMonth', y='SellingPrice', markers=True, text='SellingPrice')
        fig.update_traces(line_color='#ff8040', marker_color='#ff4828', textposition='top center')
        st.plotly_chart(apply_theme(fig,"Avg Selling Price per Month"), use_container_width=True)
    c3,c4 = st.columns(2)
    with c3:
        cnt = fdf.groupby('SaleMonth')['SellingPrice'].count().reset_index()
        cnt.columns = ['SaleMonth','Count']
        fig = px.line(cnt, x='SaleMonth', y='Count', markers=True, text='Count')
        fig.update_traces(line_color='#40c8ff', marker_color='#40c8ff', fill='tozeroy', fillcolor='rgba(64,200,255,0.07)', textposition='top center')
        st.plotly_chart(apply_theme(fig,"Number of Sales per Month"), use_container_width=True)
    with c4:
        yr_m = fdf.groupby(['Year','SaleMonth'])['SellingPrice'].sum().reset_index()
        fig = px.histogram(yr_m, x='SaleMonth', y='SellingPrice', color='Year', text_auto=True)
        st.plotly_chart(apply_theme(fig,"Revenue by Month across Years"), use_container_width=True)
    c5,c6 = st.columns(2)
    with c5:
        xcol = 'SaleYear' if 'SaleYear' in fdf.columns else 'Year'
        yr_r = fdf.groupby(xcol)['SellingPrice'].sum().reset_index()
        fig = px.bar(yr_r, x=xcol, y='SellingPrice', text_auto='.2s')
        fig.update_traces(marker_color='#c040ff')
        st.plotly_chart(apply_theme(fig,"Total Revenue per Sale Year"), use_container_width=True)
    with c6:
        yo = fdf.groupby('Year')['Odometer'].mean().round().reset_index()
        fig = px.bar(yo, x='Year', y='Odometer', text_auto=True)
        fig.update_traces(marker_color='#40ff9f')
        st.plotly_chart(apply_theme(fig,"Avg Odometer by Manufacturing Year"), use_container_width=True)

# ── TAB 2 — BRAND & MARKET ────────────────────────────────────────────────────
with t2:
    st.markdown("<div class='sec-title'>Brand & Market Analysis</div>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        bp = fdf.groupby('Make')['SellingPrice'].mean().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(bp, x='Make', y='SellingPrice', text_auto='.2s')
        fig.update_traces(marker_color='#ff4828')
        st.plotly_chart(apply_theme(fig,"Top 10 Expensive Makes (Avg Price)"), use_container_width=True)
    with c2:
        bc = fdf['Make'].value_counts().head(10).reset_index(); bc.columns=['Make','Count']
        fig = px.bar(bc, x='Make', y='Count', text='Count')
        fig.update_traces(marker_color='#40c8ff')
        st.plotly_chart(apply_theme(fig,"Top 10 Makes by Volume"), use_container_width=True)
    c3,c4 = st.columns(2)
    with c3:
        top_mk = fdf['Make'].value_counts().head(10).index
        top_mo = fdf['Model'].value_counts().head(12).index
        mm = fdf[fdf['Make'].isin(top_mk) & fdf['Model'].isin(top_mo)].groupby(['Make','Model']).size().reset_index(name='Count')
        pivot = mm.pivot(index='Make', columns='Model', values='Count').fillna(0)
        fig = px.imshow(pivot, text_auto=True, aspect='auto', color_continuous_scale='Reds')
        st.plotly_chart(apply_theme(fig,"Make vs Model — Sales Heatmap"), use_container_width=True)
    with c4:
        top_mo10 = fdf['Model'].value_counts().head(8).index
        myp = fdf[fdf['Model'].isin(top_mo10)].groupby(['Model','Year'])['SellingPrice'].mean().round().reset_index()
        fig = px.line(myp, x='Year', y='SellingPrice', color='Model', markers=True)
        st.plotly_chart(apply_theme(fig,"Avg Price by Model across Years"), use_container_width=True)
    c5,c6 = st.columns(2)
    with c5:
        top_mk15 = fdf['Make'].value_counts().head(12).index
        mc = fdf[fdf['Make'].isin(top_mk15)].groupby(['Make','Color']).size().reset_index(name='Count')
        best_c = mc.loc[mc.groupby('Make')['Count'].idxmax()].sort_values('Count',ascending=False)
        fig = px.bar(best_c, x='Make', y='Count', color='Color', text='Color')
        st.plotly_chart(apply_theme(fig,"Best-Selling Color per Make"), use_container_width=True)
    with c6:
        top_mk8 = fdf['Make'].value_counts().head(8).index
        tm = fdf[fdf['Make'].isin(top_mk8)].groupby(['Make','Transmission']).size().reset_index(name='Count')
        fig = px.bar(tm, x='Make', y='Count', color='Transmission', barmode='group', text='Count')
        st.plotly_chart(apply_theme(fig,"Transmission Type per Make"), use_container_width=True)

# ── TAB 3 — TRIM & BODY ───────────────────────────────────────────────────────
with t3:
    st.markdown("<div class='sec-title'>Trim & Body Analysis</div>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        tv = fdf['Trim'].value_counts().head(20).reset_index(); tv.columns=['Trim','Count']
        fig = px.bar(tv, x='Trim', y='Count', text='Count')
        fig.update_traces(marker_color='#ff8040')
        st.plotly_chart(apply_theme(fig,"Top 20 Trims by Volume"), use_container_width=True)
    with c2:
        bv = fdf['Body'].value_counts().reset_index(); bv.columns=['Body','Count']
        fig = px.pie(bv, names='Body', values='Count', hole=0.5)
        fig.update_traces(textfont_color='white', marker=dict(colors=COLORS))
        st.plotly_chart(apply_theme(fig,"Body Type Distribution"), use_container_width=True)
    c3,c4 = st.columns(2)
    with c3:
        top_tr = fdf['Trim'].value_counts().head(12).index
        tb = fdf[fdf['Trim'].isin(top_tr)].groupby(['Trim','Body']).size().reset_index(name='Count')
        fig = px.bar(tb, x='Trim', y='Count', color='Body', barmode='stack', text_auto=True)
        st.plotly_chart(apply_theme(fig,"Trim vs Body Type"), use_container_width=True)
    with c4:
        trbody = fdf.groupby(['Transmission','Body']).size().reset_index(name='Count')
        fig = px.bar(trbody, x='Body', y='Count', color='Transmission', barmode='group', text='Count')
        st.plotly_chart(apply_theme(fig,"Transmission vs Body Type"), use_container_width=True)
    c5,c6 = st.columns(2)
    with c5:
        top_tr2 = fdf['Trim'].value_counts().head(10).index
        trtrim = fdf[fdf['Trim'].isin(top_tr2)].groupby(['Transmission','Trim']).size().reset_index(name='Count')
        fig = px.bar(trtrim, x='Trim', y='Count', color='Transmission', barmode='group', text_auto=True)
        st.plotly_chart(apply_theme(fig,"Transmission vs Trim"), use_container_width=True)
    with c6:
        top_mo8 = fdf['Model'].value_counts().head(8).index
        trmod = fdf[fdf['Model'].isin(top_mo8)].groupby(['Model','Transmission']).size().reset_index(name='Count')
        fig = px.bar(trmod, x='Model', y='Count', color='Transmission', barmode='group', text='Count')
        st.plotly_chart(apply_theme(fig,"Transmission vs Model"), use_container_width=True)

# ── TAB 4 — PRICE & VALUE ─────────────────────────────────────────────────────
with t4:
    st.markdown("<div class='sec-title'>Price & Value Insights</div>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        fig = px.histogram(fdf, x='SellingPrice', nbins=60)
        fig.update_traces(marker_color='#ff4828', opacity=0.85)
        st.plotly_chart(apply_theme(fig,"Selling Price Distribution"), use_container_width=True)
    with c2:
        samp = fdf.sample(min(8000,len(fdf)), random_state=42)
        fig = px.scatter(samp, x='MMR', y='SellingPrice', opacity=0.25, trendline='ols')
        max_v = max(samp['MMR'].max(), samp['SellingPrice'].max())
        fig.add_trace(go.Scatter(x=[0,max_v], y=[0,max_v], mode='lines', name='Perfect Pricing', line=dict(color='#40ff9f',dash='dash',width=2)))
        st.plotly_chart(apply_theme(fig,"MMR vs Selling Price"), use_container_width=True)
    c3,c4 = st.columns(2)
    with c3:
        gy = fdf.groupby('Year').agg(AvgGross=('Gross','mean'),AvgMMR=('MMR','mean'),AvgSP=('SellingPrice','mean')).round(0).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(x=gy['Year'], y=gy['AvgMMR'], name='Avg MMR', marker_color='#40c8ff'))
        fig.add_trace(go.Bar(x=gy['Year'], y=gy['AvgSP'], name='Avg Selling Price', marker_color='#ff8040'))
        fig.add_trace(go.Scatter(x=gy['Year'], y=gy['AvgGross'], name='Avg Gross', mode='lines+markers', line=dict(color='#40ff9f',width=3)))
        fig.update_layout(barmode='group')
        st.plotly_chart(apply_theme(fig,"Gross vs MMR across Manufacturing Years"), use_container_width=True)
    with c4:
        udf = fdf[fdf['Underpriced']].copy()
        if len(udf) > 0:
            udf['Discount'] = udf['MMR'] - udf['SellingPrice']
            um = udf.groupby('Make').agg(Count=('Discount','count'),AvgDiscount=('Discount','mean')).round(0).sort_values('Count',ascending=False).head(12).reset_index()
            fig = px.bar(um, x='Make', y='Count', color='AvgDiscount', text='Count', color_continuous_scale='Reds')
            st.plotly_chart(apply_theme(fig,f"Underpriced Cars by Make ({len(udf)/len(fdf)*100:.1f}% of sales)"), use_container_width=True)
    c5,c6 = st.columns(2)
    with c5:
        yp = fdf.groupby('Year')['SellingPrice'].mean().reset_index()
        fig = px.line(yp, x='Year', y='SellingPrice', markers=True)
        fig.update_traces(line_color='#ff4828', marker_color='#ff8040', fill='tozeroy', fillcolor='rgba(255,72,40,0.06)')
        st.plotly_chart(apply_theme(fig,"Avg Selling Price by Manufacturing Year"), use_container_width=True)
    with c6:
        col_p = fdf.groupby('Color')['SellingPrice'].agg(['mean','count']).rename(columns={'mean':'AvgPrice','count':'Count'}).query('Count > 50').sort_values('AvgPrice',ascending=False).reset_index()
        fig = px.bar(col_p, x='Color', y='AvgPrice', text_auto='.2s', color='AvgPrice', color_continuous_scale='Reds')
        st.plotly_chart(apply_theme(fig,"Avg Selling Price by Color"), use_container_width=True)

# ── TAB 5 — CONDITION & USAGE ─────────────────────────────────────────────────
with t5:
    st.markdown("<div class='sec-title'>Condition & Usage Insights</div>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        cp = fdf.groupby('ConditionValue')['SellingPrice'].mean().reset_index()
        fig = px.bar(cp, x='ConditionValue', y='SellingPrice', text_auto='.2s')
        fig.update_traces(marker_color='#ff8040')
        st.plotly_chart(apply_theme(fig,"Avg Selling Price by Condition"), use_container_width=True)
    with c2:
        fig = px.histogram(fdf, x='Odometer', nbins=60)
        fig.update_traces(marker_color='#40c8ff', opacity=0.85)
        st.plotly_chart(apply_theme(fig,"Odometer Distribution"), use_container_width=True)
    c3,c4 = st.columns(2)
    with c3:
        s2 = fdf.sample(min(8000,len(fdf)), random_state=1)
        fig = px.scatter(s2, x='Odometer', y='SellingPrice', opacity=0.25, trendline='ols')
        st.plotly_chart(apply_theme(fig,"Odometer vs Selling Price"), use_container_width=True)
    with c4:
        top_mk6 = fdf['Make'].value_counts().head(6).index
        sm = fdf[fdf['Make'].isin(top_mk6)].sample(min(6000,len(fdf[fdf['Make'].isin(top_mk6)])), random_state=2)
        fig = px.scatter(sm, x='Odometer', y='SellingPrice', color='Make', opacity=0.35, trendline='ols')
        st.plotly_chart(apply_theme(fig,"Odometer vs Selling Price by Make"), use_container_width=True)

# ── TAB 6 — SELLERS ───────────────────────────────────────────────────────────
with t6:
    st.markdown("<div class='sec-title'>Seller Insights</div>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        ts = fdf['Seller'].value_counts().head(10).reset_index(); ts.columns=['Seller','Count']
        fig = px.bar(ts, x='Seller', y='Count', text='Count')
        fig.update_traces(marker_color='#ff4828')
        st.plotly_chart(apply_theme(fig,"Top Sellers by Volume"), use_container_width=True)
    with c2:
        sp2 = fdf.groupby('Seller')['SellingPrice'].mean().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(sp2, x='Seller', y='SellingPrice', text_auto='.2s')
        fig.update_traces(marker_color='#40c8ff')
        st.plotly_chart(apply_theme(fig,"Top Sellers by Avg Price"), use_container_width=True)
    c3,_ = st.columns([1,1])
    with c3:
        sg = fdf.groupby('Seller').agg(AvgGross=('Gross','mean'),Count=('Gross','count'),AvgPct=('GrossMarginPct','mean')).round(2).sort_values('AvgGross',ascending=False).head(15).reset_index()
        fig = px.bar(sg, x='Seller', y='AvgGross', color='AvgPct', text=sg['AvgGross'].round(0), color_continuous_scale='RdYlGn')
        st.plotly_chart(apply_theme(fig,"Top Sellers by Avg Gross (Price − MMR)"), use_container_width=True)

# ── TAB 7 — GEOGRAPHY ─────────────────────────────────────────────────────────
with t7:
    st.markdown("<div class='sec-title'>State-Level Analysis</div>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        ss = fdf['State'].value_counts().reset_index(); ss.columns=['State','Count']
        fig = px.choropleth(ss, locations='State', locationmode='USA-states', color='Count', scope='usa', color_continuous_scale='Reds')
        fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#080810', landcolor='#0f0f20', subunitcolor='#1a1a30'))
        st.plotly_chart(apply_theme(fig,"Sales Volume by State"), use_container_width=True)
    with c2:
        spr = fdf.groupby('State')['SellingPrice'].mean().round().reset_index()
        fig = px.choropleth(spr, locations='State', locationmode='USA-states', color='SellingPrice', scope='usa', color_continuous_scale='Oranges')
        fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#080810', landcolor='#0f0f20', subunitcolor='#1a1a30'))
        st.plotly_chart(apply_theme(fig,"Avg Selling Price by State"), use_container_width=True)
    c3,c4 = st.columns(2)
    with c3:
        top_st = fdf['State'].value_counts().head(10).reset_index(); top_st.columns=['State','Count']
        fig = px.bar(top_st, x='State', y='Count', text='Count')
        fig.update_traces(marker_color='#ff4828')
        st.plotly_chart(apply_theme(fig,"Top 10 States by Sales Volume"), use_container_width=True)
    with c4:
        int_p = fdf.groupby('Interior')['SellingPrice'].agg(['mean','count']).rename(columns={'mean':'AvgPrice','count':'Count'}).query('Count > 50').sort_values('AvgPrice',ascending=False).reset_index()
        fig = px.bar(int_p, x='Interior', y='AvgPrice', text_auto='.2s', color='AvgPrice', color_continuous_scale='Oranges')
        st.plotly_chart(apply_theme(fig,"Avg Selling Price by Interior Color"), use_container_width=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class='divider'></div>
<div style='text-align:center;font-size:0.7rem;color:#252540;padding:10px 0 20px'>
  AutoPulse · Car Sales Intelligence · Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
