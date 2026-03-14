import textwrap
"""
Economy Dashboard - Professional Financial Analytics
K-line charts, depth visualization, sentiment heatmaps, order flow
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.demo_data import WORLD_OVERVIEW, METRIC_DATA, AGENTS, LAYER_NAMES
from core.ui_utils import (
    load_css, pro_header, section_header, status_bar,
    stat_card, gauge_chart, heatmap_cell, status_dot,
    hex_to_rgba_str, LAYER_COLORS, ACTION_COLORS,
    apply_dark_theme
)

st.set_page_config(page_title="Economy", page_icon="◈", layout="wide")
load_css()

# ===== HEADER =====
st.markdown(pro_header("◈ ECONOMY DASHBOARD", "Real-Time World Analytics & Order Flow"), unsafe_allow_html=True)

# ===== STATUS BAR =====
world_status = "online" if WORLD_OVERVIEW['world_condition'] in ['牛市', '反彈'] else "warning"
st.markdown(status_bar([
    {"label": "MARKET", "value": WORLD_OVERVIEW['world_condition'], "status": world_status},
    {"label": "SPX", "value": f"{WORLD_OVERVIEW['global_score']:,.0f}", "status": "online"},
    {"label": "NDX", "value": f"{WORLD_OVERVIEW['nasdaq']:,.0f}", "status": "online"},
    {"label": "VIX", "value": f"{WORLD_OVERVIEW['vix']:.1f}", "status": "warning" if WORLD_OVERVIEW['vix'] > 20 else "online"},
    {"label": "SESSION", "value": "LIVE", "status": "processing"},
]), unsafe_allow_html=True)

# ===== KPI ROW =====
kpi_cols = st.columns(5)
kpi_data = [
    {"label": "S&P 500", "value": f"{WORLD_OVERVIEW['global_score']:,.2f}", "color": "#00ff88", "delta": "+1.23%"},
    {"label": "NASDAQ", "value": f"{WORLD_OVERVIEW['nasdaq']:,.2f}", "color": "#00d4ff", "delta": "+0.87%"},
    {"label": "VIX", "value": f"{WORLD_OVERVIEW['vix']:.2f}", "color": "#ffcc00", "delta": "-5.3%"},
    {"label": "Fear & Greed", "value": str(WORLD_OVERVIEW['system_tension']), "color": "#b400ff", "delta": "+12"},
    {"label": "World", "value": WORLD_OVERVIEW['world_condition'], "color": "#ff8800", "delta": None},
]
for idx, kpi in enumerate(kpi_data):
    with kpi_cols[idx]:
        st.markdown(stat_card(kpi["label"], kpi["value"], kpi["color"], kpi.get("delta")), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===== PRICE CHART (K-LINE STYLE) & VOLUME =====
price_col, volume_col = st.columns([2.5, 1])

with price_col:
    st.markdown(section_header("📈", "PRICE ACTION (30 DAYS)"), unsafe_allow_html=True)
    
    fig = go.Figure()
    
    # Area fill with gradient effect
    fig.add_trace(go.Scatter(
        x=METRIC_DATA['date'],
        y=METRIC_DATA['price'],
        mode='lines',
        name='Price',
        line=dict(color='#00ff88', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 136, 0.05)',
        hovertemplate='<b>%{x|%b %d}</b><br>Price: $%{y:.2f}<extra></extra>'
    ))
    
    # 7-day MA
    ma_7 = METRIC_DATA['price'].rolling(window=7).mean()
    fig.add_trace(go.Scatter(
        x=METRIC_DATA['date'],
        y=ma_7,
        mode='lines',
        name='7D MA',
        line=dict(color='#00d4ff', width=1.5, dash='dot'),
        hovertemplate='7D MA: $%{y:.2f}<extra></extra>'
    ))
    
    # 20-day MA
    ma_20 = METRIC_DATA['price'].rolling(window=20).mean()
    fig.add_trace(go.Scatter(
        x=METRIC_DATA['date'],
        y=ma_20,
        mode='lines',
        name='20D MA',
        line=dict(color='#b400ff', width=1, dash='dash'),
        hovertemplate='20D MA: $%{y:.2f}<extra></extra>'
    ))
    
    fig = apply_dark_theme(fig, height=380, showlegend=True)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)

with volume_col:
    st.markdown(section_header("📊", "VOLUME"), unsafe_allow_html=True)
    
    fig = go.Figure()
    
    colors = ['#00ff88' if r >= 0 else '#ff0055' for r in METRIC_DATA['return']]
    fig.add_trace(go.Bar(
        x=METRIC_DATA['date'],
        y=METRIC_DATA['volume'],
        marker_color=colors,
        opacity=0.7,
        hovertemplate='<b>%{x|%b %d}</b><br>Vol: %{y:,.0f}<extra></extra>'
    ))
    
    # Volume MA
    vol_ma = METRIC_DATA['volume'].rolling(window=7).mean()
    fig.add_trace(go.Scatter(
        x=METRIC_DATA['date'],
        y=vol_ma,
        mode='lines',
        name='Vol MA',
        line=dict(color='#ffcc00', width=1.5)
    ))
    
    fig = apply_dark_theme(fig, height=380, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ===== MARKET DEPTH & SENTIMENT GAUGES =====
left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown(section_header("📉", "ORDER BOOK DEPTH"), unsafe_allow_html=True)
    
    # Simulated order book
    np.random.seed(42)
    mid_price = 100.0
    bid_prices = [mid_price - i*0.1 for i in range(1, 21)]
    ask_prices = [mid_price + i*0.1 for i in range(1, 21)]
    bid_volumes = np.random.exponential(500, 20).cumsum()[::-1]
    ask_volumes = np.random.exponential(500, 20).cumsum()
    
    fig = go.Figure()
    
    # Bids (green)
    fig.add_trace(go.Scatter(
        x=bid_volumes, y=bid_prices,
        fill='tozeroy', fillcolor='rgba(0,255,136,0.15)',
        line=dict(color='#00ff88', width=2),
        name='Bids',
        hovertemplate='Price: $%{y:.2f}<br>Vol: %{x:,.0f}<extra></extra>'
    ))
    
    # Asks (red)
    fig.add_trace(go.Scatter(
        x=ask_volumes, y=ask_prices,
        fill='tozeroy', fillcolor='rgba(255,0,85,0.15)',
        line=dict(color='#ff0055', width=2),
        name='Asks',
        hovertemplate='Price: $%{y:.2f}<br>Vol: %{x:,.0f}<extra></extra>'
    ))
    
    fig.add_hline(y=mid_price, line_dash="dash", line_color="#ffcc00", annotation_text="Mid", annotation_font_color="#ffcc00")
    
    fig = apply_dark_theme(fig, height=350)
    fig.update_layout(xaxis_title="Cumulative Volume", yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.markdown(section_header("🎯", "SENTIMENT GAUGES"), unsafe_allow_html=True)
    
    gauge_cols = st.columns(2)
    with gauge_cols[0]:
        st.plotly_chart(
            gauge_chart(WORLD_OVERVIEW['system_tension'], "Fear & Greed", 100, size=220),
            use_container_width=True
        )
    with gauge_cols[1]:
        bullish = sum(1 for a in AGENTS if a['mood'] in ['bullish', 'greedy'])
        bearish = sum(1 for a in AGENTS if a['mood'] in ['bearish', 'fearful'])
        total = len(AGENTS)
        bull_pct = bullish / total * 100 if total > 0 else 50
        st.plotly_chart(
            gauge_chart(bull_pct, "Bull/Bear Ratio", 100, "%", size=220),
            use_container_width=True
        )
    
    # World pressure indicator
    pressure = (bullish - bearish) / max(total, 1) * 100
    pressure_color = "#00ff88" if pressure > 0 else "#ff0055"
    arrow = "▲" if pressure > 0 else "▼"
    
    st.markdown(f"""
<div class='stat-card' style='text-align:center;margin-top:1rem;'>
<div style='color:#6b7a90;font-size:0.7rem;letter-spacing:2px;font-family:Orbitron,sans-serif;'>MARKET PRESSURE</div>
<div style='font-size:2.5rem;font-weight:bold;color:{pressure_color};margin:0.5rem 0;font-family:Orbitron,sans-serif;'>
{arrow} {pressure:+.1f}%
</div>
<div style='display:flex;justify-content:space-around;'>
<div>
<div style='color:#00ff88;font-size:1.3rem;font-weight:bold;'>{bullish}</div>
<div style='color:#6b7a90;font-size:0.7rem;'>BULLISH</div>
</div>
<div>
<div style='color:#ff0055;font-size:1.3rem;font-weight:bold;'>{bearish}</div>
<div style='color:#6b7a90;font-size:0.7rem;'>BEARISH</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===== TRADING ACTIVITY HEATMAP =====
st.markdown(section_header("🔥", "TRADING ACTIVITY HEATMAP"), unsafe_allow_html=True)

heatmap_col1, heatmap_col2 = st.columns([1.5, 1])

with heatmap_col1:
    # Layer x Action heatmap
    layer_action_data = []
    for agent in AGENTS:
        layer_action_data.append({
            "Layer": f"L{agent['layer']}",
            "Action": agent['action'],
            "Count": 1
        })
    
    df_heat = pd.DataFrame(layer_action_data)
    pivot = df_heat.pivot_table(index='Layer', columns='Action', values='Count', aggfunc='sum', fill_value=0)
    
    # Reorder columns
    action_order = ['ACT', 'OBSERVE', 'HOLD', 'WAIT', 'RESEARCH']
    pivot = pivot.reindex(columns=[c for c in action_order if c in pivot.columns], fill_value=0)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale=[
            [0, '#0d1117'],
            [0.3, '#1a2332'],
            [0.6, '#00d4ff33'],
            [1, '#00ff88']
        ],
        text=pivot.values,
        texttemplate="%{text}",
        textfont=dict(size=14, color='#e8edf4', family='Orbitron'),
        hovertemplate='Layer: %{y}<br>Action: %{x}<br>Count: %{z}<extra></extra>',
        showscale=False
    ))
    
    fig = apply_dark_theme(fig, height=280)
    fig.update_layout(title=dict(text='Layer vs Action Distribution', font=dict(size=12, color='#6b7a90')))
    st.plotly_chart(fig, use_container_width=True)

with heatmap_col2:
    st.markdown(section_header("⚡", "ACTION DISTRIBUTION"), unsafe_allow_html=True)
    
    action_counts = {}
    for agent in AGENTS:
        action_counts[agent['action']] = action_counts.get(agent['action'], 0) + 1
    
    fig = go.Figure(data=[go.Pie(
        labels=list(action_counts.keys()),
        values=list(action_counts.values()),
        hole=0.6,
        marker=dict(colors=[ACTION_COLORS.get(k, '#8892a4') for k in action_counts.keys()]),
        textinfo='label+percent',
        textfont=dict(size=10, color='#e8edf4'),
        hovertemplate='%{label}<br>Count: %{value}<br>%{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=280,
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        annotations=[dict(
            text=f'<b>{len(AGENTS)}</b><br>AGENTS',
            x=0.5, y=0.5, font_size=14, font_color='#e8edf4', showarrow=False
        )]
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ===== LAYER CONFIDENCE & TOP INFLUENCERS =====
conf_col, influencer_col = st.columns([1, 1])

with conf_col:
    st.markdown(section_header("📐", "CONFIDENCE BY LAYER"), unsafe_allow_html=True)
    
    fig = go.Figure()
    
    for layer_id, layer_info in LAYER_NAMES.items():
        layer_agents = [a for a in AGENTS if a['layer'] == layer_id]
        confidences = sorted([a['confidence'] for a in layer_agents])
        
        fig.add_trace(go.Box(
            y=confidences,
            name=f"L{layer_id}",
            marker_color=LAYER_COLORS[layer_id],
            boxmean='sd',
            line=dict(width=1.5),
            hovertemplate='L' + str(layer_id) + '<br>Conf: %{y:.2f}<extra></extra>'
        ))
    
    fig = apply_dark_theme(fig, height=300)
    fig.update_layout(yaxis_title="Confidence", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with influencer_col:
    st.markdown(section_header("🏆", "TOP INFLUENCERS"), unsafe_allow_html=True)
    
    top_agents = sorted(AGENTS, key=lambda x: x['influence'], reverse=True)[:8]
    
    for i, agent in enumerate(top_agents[:5], 1):
        layer_info = LAYER_NAMES[agent['layer']]
        layer_color = LAYER_COLORS[agent['layer']]
        bar_width = agent['influence'] * 100
        
        st.markdown(f"""
<div style='display:flex;align-items:center;gap:0.75rem;padding:0.5rem;margin-bottom:0.35rem;background:rgba(255,255,255,0.02);border-radius:8px;'>
<span style='color:#6b7a90;font-size:0.75rem;font-family:Orbitron,sans-serif;width:20px;'>#{i}</span>
<span style='font-size:1rem;'>{layer_info['icon']}</span>
<div style='flex:1;'>
<div style='display:flex;justify-content:space-between;'>
<span style='color:#e8edf4;font-size:0.85rem;font-weight:bold;'>{agent['name']}</span>
<span style='color:{layer_color};font-size:0.75rem;font-family:JetBrains Mono,monospace;'>{agent['influence']:.2f}</span>
</div>
<div class='stat-bar' style='margin-top:4px;'>
<div class='stat-bar-fill' style='width:{bar_width}%;background:{layer_color};'></div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# ===== CANDLESTICK CHART (simulated) =====
st.markdown("---")
st.markdown(section_header("🕯️", "CANDLESTICK CHART (SIMULATED)"), unsafe_allow_html=True)

# Generate OHLC data from price series
np.random.seed(42)
ohlc_data = []
for i, row in METRIC_DATA.iterrows():
    base = row['price']
    o = base * (1 + np.random.uniform(-0.01, 0.01))
    h = max(o, base) * (1 + abs(np.random.uniform(0, 0.015)))
    l = min(o, base) * (1 - abs(np.random.uniform(0, 0.015)))
    c = base
    ohlc_data.append({'date': row['date'], 'open': o, 'high': h, 'low': l, 'close': c, 'volume': row['volume']})

df_ohlc = pd.DataFrame(ohlc_data)

candle_col, info_col = st.columns([3, 1])

with candle_col:
    fig = go.Figure()
    
    fig.add_trace(go.Candlestick(
        x=df_ohlc['date'],
        open=df_ohlc['open'],
        high=df_ohlc['high'],
        low=df_ohlc['low'],
        close=df_ohlc['close'],
        increasing_line_color='#00ff88',
        decreasing_line_color='#ff0055',
        increasing_fillcolor='rgba(0,255,136,0.7)',
        decreasing_fillcolor='rgba(255,0,85,0.7)',
        name='OHLC'
    ))
    
    fig = apply_dark_theme(fig, height=350)
    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with info_col:
    latest = df_ohlc.iloc[-1]
    prev = df_ohlc.iloc[-2]
    change = (latest['close'] - prev['close']) / prev['close'] * 100
    change_color = "#00ff88" if change >= 0 else "#ff0055"
    
    st.markdown(f"""
<div class='stat-card' style='margin-bottom:1rem;'>
<div style='color:#6b7a90;font-size:0.7rem;letter-spacing:2px;font-family:Orbitron,sans-serif;'>LATEST OHLC</div>
<div style='margin-top:0.75rem;font-family:JetBrains Mono,monospace;font-size:0.8rem;'>
<div style='display:flex;justify-content:space-between;margin-bottom:0.25rem;'>
<span style='color:#6b7a90;'>Open</span><span style='color:#e8edf4;'>${latest['open']:.2f}</span>
</div>
<div style='display:flex;justify-content:space-between;margin-bottom:0.25rem;'>
<span style='color:#6b7a90;'>High</span><span style='color:#00ff88;'>${latest['high']:.2f}</span>
</div>
<div style='display:flex;justify-content:space-between;margin-bottom:0.25rem;'>
<span style='color:#6b7a90;'>Low</span><span style='color:#ff0055;'>${latest['low']:.2f}</span>
</div>
<div style='display:flex;justify-content:space-between;margin-bottom:0.25rem;'>
<span style='color:#6b7a90;'>Close</span><span style='color:#e8edf4;font-weight:bold;'>${latest['close']:.2f}</span>
</div>
<div style='display:flex;justify-content:space-between;'>
<span style='color:#6b7a90;'>Change</span><span style='color:{change_color};font-weight:bold;'>{change:+.2f}%</span>
</div>
</div>
</div>
""", unsafe_allow_html=True)
    
    # RSI indicator (simulated)
    rsi = 45 + np.random.uniform(-10, 20)
    rsi_color = "#00ff88" if rsi < 70 else ("#ff0055" if rsi > 30 else "#ffcc00")
    st.markdown(f"""
<div class='stat-card' style='margin-bottom:1rem;'>
<div style='color:#6b7a90;font-size:0.7rem;letter-spacing:2px;font-family:Orbitron,sans-serif;'>INDICATORS</div>
<div style='margin-top:0.75rem;font-family:JetBrains Mono,monospace;font-size:0.8rem;'>
<div style='display:flex;justify-content:space-between;margin-bottom:0.25rem;'>
<span style='color:#6b7a90;'>RSI (14)</span><span style='color:{rsi_color};font-weight:bold;'>{rsi:.1f}</span>
</div>
<div style='display:flex;justify-content:space-between;margin-bottom:0.25rem;'>
<span style='color:#6b7a90;'>MACD</span><span style='color:#00d4ff;font-weight:bold;'>+0.42</span>
</div>
<div style='display:flex;justify-content:space-between;margin-bottom:0.25rem;'>
<span style='color:#6b7a90;'>BB Width</span><span style='color:#ffcc00;font-weight:bold;'>3.2%</span>
</div>
<div style='display:flex;justify-content:space-between;'>
<span style='color:#6b7a90;'>ATR</span><span style='color:#b400ff;font-weight:bold;'>1.85</span>
</div>
</div>
</div>
""", unsafe_allow_html=True)
    
    # Volume summary
    total_vol = df_ohlc['volume'].sum()
    avg_vol = df_ohlc['volume'].mean()
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#6b7a90;font-size:0.7rem;letter-spacing:2px;font-family:Orbitron,sans-serif;'>VOLUME SUMMARY</div>
<div style='margin-top:0.75rem;font-family:JetBrains Mono,monospace;font-size:0.8rem;'>
<div style='display:flex;justify-content:space-between;margin-bottom:0.25rem;'>
<span style='color:#6b7a90;'>Total</span><span style='color:#e8edf4;'>{total_vol:,.0f}</span>
</div>
<div style='display:flex;justify-content:space-between;margin-bottom:0.25rem;'>
<span style='color:#6b7a90;'>Avg/Day</span><span style='color:#e8edf4;'>{avg_vol:,.0f}</span>
</div>
<div style='display:flex;justify-content:space-between;'>
<span style='color:#6b7a90;'>Last</span><span style='color:#00d4ff;font-weight:bold;'>{latest['volume']:,.0f}</span>
</div>
</div>
</div>
""", unsafe_allow_html=True)