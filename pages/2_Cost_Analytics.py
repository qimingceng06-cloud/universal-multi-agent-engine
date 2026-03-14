import textwrap
"""
Cost Analytics Page - Token usage tracking and optimization
Monitor costs, savings, and efficiency across all layers
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.demo_data import AGENTS, COST_DATA, LAYER_NAMES

st.set_page_config(page_title="Cost Analytics", page_icon="💵", layout="wide")

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("# 💵 Cost Analytics & Token Management")
st.markdown("*Track token usage, costs, and optimization savings*")
st.markdown("---")

# ===== DAILY OVERVIEW =====
overview_cols = st.columns(5)

daily = COST_DATA['daily']

with overview_cols[0]:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>TOTAL TOKENS TODAY</div>
<div style='font-size:1.8rem;font-weight:bold;color:#00ff88;'>{daily['total_tokens']:,}</div>
</div>
""", unsafe_allow_html=True)

with overview_cols[1]:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>INPUT TOKENS</div>
<div style='font-size:1.8rem;font-weight:bold;color:#00d4ff;'>{daily['input_tokens']:,}</div>
</div>
""", unsafe_allow_html=True)

with overview_cols[2]:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>OUTPUT TOKENS</div>
<div style='font-size:1.8rem;font-weight:bold;color:#ffcc00;'>{daily['output_tokens']:,}</div>
</div>
""", unsafe_allow_html=True)

with overview_cols[3]:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>TODAY'S COST</div>
<div style='font-size:1.8rem;font-weight:bold;color:#ff8800;'>${daily['cost_usd']:.2f}</div>
</div>
""", unsafe_allow_html=True)

with overview_cols[4]:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>API CALLS</div>
<div style='font-size:1.8rem;font-weight:bold;color:#b400ff;'>{daily['api_calls']:,}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===== COST BY LAYER =====
st.markdown("### 🏛️ Cost Distribution by Layer")

layer_cost_col1, layer_cost_col2 = st.columns([2, 1])

with layer_cost_col1:
    # Layer cost breakdown
    layer_costs = COST_DATA['by_layer']
    
    cost_df = pd.DataFrame({
        'Layer': [f"L{i}: {LAYER_NAMES[i]['name_en']}" for i in range(1, 5)],
        'Tokens': [layer_costs[i]['tokens'] for i in range(1, 5)],
        'Cost (USD)': [layer_costs[i]['cost'] for i in range(1, 5)],
        'Color': [LAYER_NAMES[i]['color'] for i in range(1, 5)]
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=cost_df['Layer'],
        y=cost_df['Tokens'],
        marker_color=cost_df['Color'],
        name='Tokens',
        text=cost_df['Tokens'].apply(lambda x: f"{x:,}"),
        textposition='auto'
    ))
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(10, 14, 23, 1)',
        plot_bgcolor='rgba(10, 14, 23, 1)',
        height=350,
        title='Token Usage by Layer',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
    )
    
    st.plotly_chart(fig, use_container_width=True)

with layer_cost_col2:
    st.markdown("### 💰 Cost Breakdown")
    
    for layer_id in range(1, 5):
        layer_info = LAYER_NAMES[layer_id]
        cost = layer_costs[layer_id]['cost']
        tokens = layer_costs[layer_id]['tokens']
        
        st.markdown(f"""
<div style='display:flex;align-items:center;justify-content:space-between;padding:0.75rem;margin:0.5rem 0;background:#151a27;border-radius:8px;border-left:3px solid {layer_info['color']};'>
<div>
<span style='font-size:1.2rem;'>{layer_info['icon']}</span>
<span style='color:#e0e6ed;font-weight:bold;margin-left:0.5rem;'>L{layer_id}</span>
</div>
<div style='text-align:right;'>
<div style='color:#ff8800;font-weight:bold;'>${cost:.2f}</div>
<div style='color:#8892a4;font-size:0.75rem;'>{tokens:,} tokens</div>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===== OPTIMIZATION SAVINGS =====
st.markdown("### ⚡ Token Optimization Savings")

savings = COST_DATA['savings']

savings_cols = st.columns(4)

with savings_cols[0]:
    st.markdown(f"""
<div class='stat-card' style='border-top:3px solid #00ff88;'>
<div style='color:#8892a4;font-size:0.8rem;'>HASH CACHE HITS</div>
<div style='font-size:2rem;font-weight:bold;color:#00ff88;'>{savings['hash_cache_hits']}</div>
<div style='font-size:0.8rem;color:#8892a4;margin-top:0.5rem;'>Duplicate requests avoided</div>
</div>
""", unsafe_allow_html=True)

with savings_cols[1]:
    st.markdown(f"""
<div class='stat-card' style='border-top:3px solid #00d4ff;'>
<div style='color:#8892a4;font-size:0.8rem;'>GROUP DELEGATION</div>
<div style='font-size:2rem;font-weight:bold;color:#00d4ff;'>{savings['group_delegation_saves']}</div>
<div style='font-size:0.8rem;color:#8892a4;margin-top:0.5rem;'>Batch operations saved</div>
</div>
""", unsafe_allow_html=True)

with savings_cols[2]:
    st.markdown(f"""
<div class='stat-card' style='border-top:3px solid #ffcc00;'>
<div style='color:#8892a4;font-size:0.8rem;'>TEMPLATE REUSE</div>
<div style='font-size:2rem;font-weight:bold;color:#ffcc00;'>{savings['template_reuse_saves']}</div>
<div style='font-size:0.8rem;color:#8892a4;margin-top:0.5rem;'>Prompt templates cached</div>
</div>
""", unsafe_allow_html=True)

with savings_cols[3]:
    st.markdown(f"""
<div class='stat-card' style='border-top:3px solid #b400ff;'>
<div style='color:#8892a4;font-size:0.8rem;'>TOTAL SAVED</div>
<div style='font-size:2rem;font-weight:bold;color:#b400ff;'>{savings['total_saved_tokens']:,}</div>
<div style='font-size:1rem;color:#ff8800;margin-top:0.5rem;'>≈ ${savings['total_saved_usd']:.2f} USD</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===== OPTIMIZATION RATE GAUGE =====
st.markdown("### 🎯 Optimization Efficiency")

gauge_col1, gauge_col2, gauge_col3 = st.columns([1, 2, 1])

with gauge_col2:
    opt_rate = COST_DATA['optimization_rate']
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=opt_rate * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Token Optimization Rate", 'font': {'size': 24, 'color': '#e0e6ed'}},
        delta={'reference': 50, 'increasing': {'color': "#00ff88"}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#8892a4'},
            'bar': {'color': "#00ff88"},
            'bgcolor': "rgba(26, 31, 46, 0.8)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 30], 'color': 'rgba(255, 0, 85, 0.2)'},
                {'range': [30, 60], 'color': 'rgba(255, 204, 0, 0.2)'},
                {'range': [60, 100], 'color': 'rgba(0, 255, 136, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': opt_rate * 100
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(10, 14, 23, 1)',
        height=300,
        font={'color': '#e0e6ed'}
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ===== 7 MAJOR TOKEN SAVING TECHNIQUES =====
st.markdown("### 🔧 7 Major Token Saving Techniques")

tech_cols = st.columns(4)

techniques = [
    {"name": "Hash Cache", "desc": "Cache API responses by content hash", "saving": f"{random.randint(15, 35)}%", "icon": "🔑", "color": "#00ff88"},
    {"name": "Group Delegation", "desc": "Batch similar agents into single call", "saving": f"{random.randint(20, 40)}%", "icon": "👥", "color": "#00d4ff"},
    {"name": "Template Reuse", "desc": "Cache and reuse prompt templates", "saving": f"{random.randint(10, 25)}%", "icon": "📝", "color": "#ffcc00"},
    {"name": "Layer Filtering", "desc": "Only process relevant layer data", "saving": f"{random.randint(8, 20)}%", "icon": "🔍", "color": "#b400ff"},
    {"name": "Memory Share", "desc": "Share memories across similar agents", "saving": f"{random.randint(12, 28)}%", "icon": "🧠", "color": "#ff8800"},
    {"name": "Incremental Update", "desc": "Only process changed data", "saving": f"{random.randint(15, 30)}%", "icon": "⚡", "color": "#ff0055"},
    {"name": "Smart Batching", "desc": "Optimize API call batching", "saving": f"{random.randint(10, 22)}%", "icon": "📦", "color": "#8892a4"},
]

for idx, tech in enumerate(techniques[:4]):
    with tech_cols[idx]:
        st.markdown(f"""
<div class='stat-card' style='border-top:3px solid {tech['color']};'>
<div style='font-size:2rem;text-align:center;margin-bottom:0.5rem;'>{tech['icon']}</div>
<div style='font-weight:bold;color:{tech['color']};text-align:center;'>{tech['name']}</div>
<div style='font-size:0.8rem;color:#8892a4;text-align:center;margin:0.5rem 0;'>{tech['desc']}</div>
<div style='text-align:center;margin-top:0.75rem;'>
<span style='font-size:1.5rem;font-weight:bold;color:#00ff88;'>{tech['saving']}</span>
<span style='color:#8892a4;font-size:0.8rem;'> saved</span>
</div>
</div>
""", unsafe_allow_html=True)

tech_cols2 = st.columns(3)
for idx, tech in enumerate(techniques[4:]):
    with tech_cols2[idx]:
        st.markdown(f"""
<div class='stat-card' style='border-top:3px solid {tech['color']};'>
<div style='font-size:2rem;text-align:center;margin-bottom:0.5rem;'>{tech['icon']}</div>
<div style='font-weight:bold;color:{tech['color']};text-align:center;'>{tech['name']}</div>
<div style='font-size:0.8rem;color:#8892a4;text-align:center;margin:0.5rem 0;'>{tech['desc']}</div>
<div style='text-align:center;margin-top:0.75rem;'>
<span style='font-size:1.5rem;font-weight:bold;color:#00ff88;'>{tech['saving']}</span>
<span style='color:#8892a4;font-size:0.8rem;'> saved</span>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===== DAILY COST TREND =====
st.markdown("### 📈 7-Day Cost Trend")

# Generate 7-day trend data
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
costs = [round(random.uniform(15, 45), 2) for _ in days]
tokens = [random.randint(100000, 400000) for _ in days]

trend_df = pd.DataFrame({
    'Day': days,
    'Cost': costs,
    'Tokens': tokens
})

fig = go.Figure()

fig.add_trace(go.Bar(
    x=trend_df['Day'],
    y=trend_df['Cost'],
    name='Cost (USD)',
    marker_color='#00ff88',
    yaxis='y'
))

fig.add_trace(go.Scatter(
    x=trend_df['Day'],
    y=trend_df['Tokens'],
    name='Tokens',
    line=dict(color='#00d4ff', width=3),
    yaxis='y2'
))

fig.update_layout(
    template='plotly_dark',
    paper_bgcolor='rgba(10, 14, 23, 1)',
    plot_bgcolor='rgba(10, 14, 23, 1)',
    height=350,
    yaxis=dict(
        title='Cost (USD)',
        showgrid=True,
        gridcolor='rgba(255,255,255,0.05)'
    ),
    yaxis2=dict(
        title='Tokens',
        overlaying='y',
        side='right',
        showgrid=False
    ),
    xaxis=dict(showgrid=False),
    legend=dict(bgcolor='rgba(26, 31, 46, 0.8)')
)

st.plotly_chart(fig, use_container_width=True)