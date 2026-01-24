"""
Indian Mutual Funds Analysis Dashboard
Complete Production-Ready Application
Author: Financial Analytics Team
Version: 1.0.0
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import requests
from typing import Dict, List, Optional

# Page Configuration
st.set_page_config(
    page_title="Indian MF Dashboard",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    font-weight: bold;
    background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 1rem;
}
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 10px;
    color: white;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# API Functions


@st.cache_data(ttl=3600)
def get_all_funds():
    try:
        response = requests.get("https://api.mfapi.in/mf", timeout=15)
        return response.json() if response.status_code == 200 else []
    except:
        return []


@st.cache_data(ttl=1800)
def get_fund_data(code):
    try:
        response = requests.get(f"https://api.mfapi.in/mf/{code}", timeout=15)
        return response.json() if response.status_code == 200 else None
    except:
        return None


def parse_nav(data):
    if not data or 'data' not in data:
        return None
    df = pd.DataFrame(data['data'])
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
    df = df.dropna().sort_values('date').set_index('date')
    return df

# Calculation Functions


def calc_returns(nav):
    if len(nav) < 2:
        return {}
    curr = nav.iloc[-1]
    ret = {}
    periods = {'1W': 7, '1M': 30, '3M': 90,
               '6M': 180, '1Y': 365, '3Y': 1095, '5Y': 1825}

    for name, days in periods.items():
        if len(nav) >= days:
            old = nav.iloc[-days]
            ret[name] = ((curr - old) / old) * 100 if old > 0 else 0
            if 'Y' in name and days >= 365:
                years = days / 365
                ret[f'{name}_CAGR'] = (
                    ((curr / old) ** (1/years)) - 1) * 100 if old > 0 else 0

    # Inception
    first = nav.iloc[0]
    years = (nav.index[-1] - nav.index[0]).days / 365.25
    if years > 0 and first > 0:
        ret['Inception'] = (((curr / first) ** (1/years)) - 1) * 100

    return ret


def calc_risk(nav):
    dr = nav.pct_change().dropna()
    if len(dr) == 0:
        return {}

    cum = (1 + dr).cumprod()
    rm = cum.expanding().max()
    dd = (cum - rm) / rm

    return {
        'volatility': dr.std() * np.sqrt(252) * 100,
        'max_dd': dd.min() * 100,
        'sharpe': (dr.mean() * 252 - 0.065) / (dr.std() * np.sqrt(252)) if dr.std() > 0 else 0,
        'best_day': dr.max() * 100,
        'worst_day': dr.min() * 100
    }

# Chart Functions


def chart_nav(df, name, show_ma=True):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=df['nav'], name='NAV',
        line=dict(color='#667eea', width=2),
        fill='tozeroy', fillcolor='rgba(102,126,234,0.1)'
    ))

    if show_ma and len(df) >= 50:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['nav'].rolling(50).mean(),
            name='50-Day MA', line=dict(color='orange', width=1.5, dash='dash')
        ))
    if show_ma and len(df) >= 200:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['nav'].rolling(200).mean(),
            name='200-Day MA', line=dict(color='red', width=1.5, dash='dash')
        ))

    fig.update_layout(
        title=f'{name} - NAV Chart',
        xaxis_title='Date', yaxis_title='NAV (₹)',
        template='plotly_dark', hovermode='x unified', height=500
    )
    return fig


def chart_returns(ret_dict):
    labels = []
    values = []
    mapping = {'1W': '1 Week', '1M': '1 Month', '3M': '3 Months', '6M': '6 Months',
               '1Y': '1 Year', '3Y_CAGR': '3Y CAGR', '5Y_CAGR': '5Y CAGR', 'Inception': 'Inception'}

    for k, v in mapping.items():
        if k in ret_dict:
            labels.append(v)
            values.append(ret_dict[k])

    if not labels:
        return None

    colors = ['green' if v >= 0 else 'red' for v in values]
    fig = go.Figure(go.Bar(
        x=labels, y=values, marker_color=colors,
        text=[f'{v:.2f}%' for v in values], textposition='outside'
    ))
    fig.update_layout(
        title='Returns Across Periods', xaxis_title='Period',
        yaxis_title='Return (%)', template='plotly_dark',
        height=400, showlegend=False
    )
    return fig


def chart_sip(monthly, rate, years):
    months = int(years * 12)
    mr = rate / 12 / 100
    data = []
    inv = val = 0

    for m in range(1, months + 1):
        inv += monthly
        val = (val + monthly) * (1 + mr)
        data.append({'Year': m/12, 'Invested': inv,
                    'Value': val, 'Gain': val - inv})

    df = pd.DataFrame(data)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Year'], y=df['Invested'],
                  name='Invested', line=dict(color='orange', width=2)))
    fig.add_trace(go.Scatter(x=df['Year'], y=df['Value'], name='Portfolio Value',
                             line=dict(color='green', width=3), fill='tonexty'))

    fig.update_layout(
        title=f'SIP Growth - ₹{monthly:,.0f}/month @ {rate:.1f}% p.a.',
        xaxis_title='Years', yaxis_title='Amount (₹)',
        template='plotly_dark', height=450
    )
    return fig, df

# Main App


def main():
    st.markdown('<p class="main-header">🇮🇳 Indian Mutual Funds Dashboard</p>',
                unsafe_allow_html=True)
    st.caption(
        "Real-time NAV tracking, returns analysis, risk metrics, and SIP planning for Indian mutual funds")

    # Sidebar
    with st.sidebar:
        st.header("🎯 Fund Selection")

        with st.spinner("Loading funds..."):
            funds = get_all_funds()

        if not funds:
            st.error("Failed to load funds")
            st.stop()

        st.success(f"✅ {len(funds):,} funds loaded")

        search = st.text_input("🔍 Search", placeholder="HDFC, SBI, Axis...")

        filtered = [f for f in funds if search.lower(
        ) in f['schemeName'].lower()] if search else funds[:100]

        if not filtered:
            st.warning("No funds found")
            selected_code = None
        else:
            fund_map = {f['schemeName']: f['schemeCode']
                        for f in filtered[:50]}
            selected_name = st.selectbox("Select Fund", list(fund_map.keys()))
            selected_code = fund_map[selected_name]

        st.divider()

        st.subheader("📅 Analysis Period")
        period_map = {'1M': 30, '3M': 90, '6M': 180,
                      '1Y': 365, '3Y': 1095, '5Y': 1825, 'All': None}
        period_sel = st.selectbox("Period", list(period_map.keys()), index=3)
        period_days = period_map[period_sel]

        show_ma = st.checkbox("Show Moving Averages", value=True)

        st.divider()
        st.markdown("### 💡 Resources")
        st.markdown("- [AMFI](https://www.amfiindia.com/)")
        st.markdown("- [Value Research](https://www.valueresearchonline.com/)")

    # Main Content
    if not selected_code:
        st.info("👈 Select a fund from sidebar to begin analysis")

        st.markdown("### 🔥 Popular Categories")
        cats = ['Large Cap', 'Mid Cap', 'Small Cap',
                'Flexi Cap', 'ELSS', 'Debt', 'Hybrid', 'Index']
        cols = st.columns(4)
        for idx, cat in enumerate(cats):
            with cols[idx % 4]:
                st.button(cat, key=cat, use_container_width=True)

        st.markdown("### 📊 Features")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            **📈 Price Analysis**
            - Real-time NAV tracking
            - Historical trends
            - Moving averages
            """)
        with col2:
            st.markdown("""
            **💰 Returns & Risk**
            - Multi-period returns
            - CAGR calculations
            - Risk metrics
            """)
        with col3:
            st.markdown("""
            **🧮 Planning Tools**
            - SIP calculator
            - Wealth projections
            - Goal planning
            """)

        st.stop()

    # Fetch Fund Data
    with st.spinner("Fetching fund data..."):
        fund_data = get_fund_data(selected_code)

    if not fund_data:
        st.error("Failed to fetch fund data")
        st.stop()

    df = parse_nav(fund_data)
    if df is None or df.empty:
        st.error("No NAV data available")
        st.stop()

    # Filter by period
    if period_days:
        cutoff = df.index[-1] - timedelta(days=period_days)
        df = df[df.index >= cutoff]

    # Calculate metrics
    returns = calc_returns(df['nav'])
    risk = calc_risk(df['nav'])

    # Fund Info
    st.markdown("### 📊 Fund Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Name:** {fund_data['meta']['scheme_name']}")
    with col2:
        st.info(
            f"**Category:** {fund_data['meta'].get('scheme_category', 'N/A')}")
    with col3:
        st.info(f"**Type:** {fund_data['meta'].get('scheme_type', 'N/A')}")

    st.divider()

    # Key Metrics
    curr_nav = df['nav'].iloc[-1]
    prev_nav = df['nav'].iloc[-2] if len(df) > 1 else curr_nav
    chg = curr_nav - prev_nav
    chg_pct = (chg / prev_nav) * 100 if prev_nav > 0 else 0

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Current NAV", f"₹{curr_nav:.4f}", f"{chg_pct:+.2f}%")
    col2.metric("1M Return", f"{returns.get('1M', 0):.2f}%")
    col3.metric("1Y Return", f"{returns.get('1Y', 0):.2f}%")
    col4.metric("3Y CAGR", f"{returns.get('3Y_CAGR', 0):.2f}%")
    col5.metric("Volatility", f"{risk.get('volatility', 0):.2f}%")

    st.divider()

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📈 Charts", "💰 Returns", "⚠️ Risk", "🧮 SIP", "📊 Stats"])

    with tab1:
        st.plotly_chart(chart_nav(
            df, fund_data['meta']['scheme_name'], show_ma), use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📊 NAV Statistics**")
            stats = pd.DataFrame({
                'Metric': ['Current', 'High', 'Low', 'Average', 'Median'],
                'Value': [f"₹{curr_nav:.4f}", f"₹{df['nav'].max():.4f}",
                          f"₹{df['nav'].min():.4f}", f"₹{df['nav'].mean():.4f}",
                          f"₹{df['nav'].median():.4f}"]
            })
            st.dataframe(stats, hide_index=True, use_container_width=True)

        with col2:
            st.markdown("**📅 Date Info**")
            info = pd.DataFrame({
                'Metric': ['Latest Date', 'First Date', 'Data Points', 'Fund Age (Years)'],
                'Value': [df.index[-1].strftime('%d-%b-%Y'), df.index[0].strftime('%d-%b-%Y'),
                          f"{len(df):,}", f"{(df.index[-1] - df.index[0]).days / 365.25:.2f}"]
            })
            st.dataframe(info, hide_index=True, use_container_width=True)

    with tab2:
        fig_ret = chart_returns(returns)
        if fig_ret:
            st.plotly_chart(fig_ret, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Absolute Returns**")
            abs_ret = pd.DataFrame({
                'Period': ['1 Week', '1 Month', '3 Months', '6 Months', '1 Year'],
                'Return': [f"{returns.get('1W', 0):.2f}%", f"{returns.get('1M', 0):.2f}%",
                           f"{returns.get('3M', 0):.2f}%", f"{returns.get('6M', 0):.2f}%",
                           f"{returns.get('1Y', 0):.2f}%"]
            })
            st.dataframe(abs_ret, hide_index=True, use_container_width=True)

        with col2:
            st.markdown("**Annualized Returns (CAGR)**")
            cagr = pd.DataFrame({
                'Period': ['3 Years', '5 Years', 'Inception'],
                'CAGR': [f"{returns.get('3Y_CAGR', 0):.2f}%",
                         f"{returns.get('5Y_CAGR', 0):.2f}%",
                         f"{returns.get('Inception', 0):.2f}%"]
            })
            st.dataframe(cagr, hide_index=True, use_container_width=True)

    with tab3:
        col1, col2, col3 = st.columns(3)
        col1.metric("Volatility", f"{risk.get('volatility', 0):.2f}%")
        col2.metric("Max Drawdown", f"{risk.get('max_dd', 0):.2f}%")
        col3.metric("Sharpe Ratio", f"{risk.get('sharpe', 0):.2f}")

        col1.metric("Best Day", f"{risk.get('best_day', 0):.2f}%")
        col2.metric("Worst Day", f"{risk.get('worst_day', 0):.2f}%")

        st.markdown("**📉 Risk Interpretation**")
        vol = risk.get('volatility', 0)
        if vol < 10:
            st.success("🟢 Low Risk - Suitable for conservative investors")
        elif vol < 20:
            st.info("🟡 Moderate Risk - Balanced risk-reward")
        else:
            st.warning("🔴 High Risk - For aggressive investors")

    with tab4:
        st.markdown("### 💰 SIP Investment Calculator")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("**Investment Parameters**")
            sip_amt = st.number_input(
                "Monthly SIP (₹)", 500, 1000000, 5000, 500)
            sip_years = st.slider("Duration (Years)", 1, 30, 10)

            exp_ret = returns.get(
                'Inception', 12.0) if 'Inception' in returns else 12.0
            st.info(f"📊 Historical Return: {exp_ret:.2f}% p.a.")

            use_custom = st.checkbox("Use Custom Return")
            if use_custom:
                exp_ret = st.slider("Expected Return (%)",
                                    0.0, 30.0, exp_ret, 0.5)

        with col2:
            fig_sip, sip_df = chart_sip(sip_amt, exp_ret, sip_years)
            st.plotly_chart(fig_sip, use_container_width=True)

            final = sip_df.iloc[-1]
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Total Invested", f"₹{final['Invested']:,.0f}")
            col_b.metric("Expected Value", f"₹{final['Value']:,.0f}")
            col_c.metric("Wealth Gained", f"₹{final['Gain']:,.0f}")

    with tab5:
        dr = df['nav'].pct_change().dropna()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📈 Performance Stats**")
            perf = pd.DataFrame({
                'Metric': ['Best Day', 'Worst Day', 'Avg Change', 'Positive Days', 'Win Rate'],
                'Value': [f"{dr.max()*100:.2f}%", f"{dr.min()*100:.2f}%",
                          f"{dr.mean()*100:.4f}%", f"{(dr>0).sum()}",
                          f"{(dr>0).sum()/len(dr)*100:.1f}%"]
            })
            st.dataframe(perf, hide_index=True, use_container_width=True)

        with col2:
            st.markdown("**📊 Distribution**")
            dist = pd.DataFrame({
                'Metric': ['Mean', 'Median', 'Std Dev', 'Skewness', 'Kurtosis'],
                'Value': [f"{dr.mean()*100:.4f}%", f"{dr.median()*100:.4f}%",
                          f"{dr.std()*100:.4f}%", f"{dr.skew():.2f}", f"{dr.kurtosis():.2f}"]
            })
            st.dataframe(dist, hide_index=True, use_container_width=True)

    # Footer
    st.divider()
    st.caption(
        "📊 Indian MF Dashboard | Data: MFAPI.in | For educational purposes only")
    st.caption(
        f"⚠️ Past performance is not indicative of future results | Updated: {datetime.now().strftime('%d-%b-%Y %H:%M')}")


if __name__ == "__main__":
    main()
