import textwrap
"""
Event Replay Page - Timeline visualization and simulation replay
View past events, analyze patterns, and replay simulation states
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.demo_data import EVENTS, AGENTS, LAYER_NAMES

st.set_page_config(page_title="Event Replay", page_icon="⏪", layout="wide")

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("# ⏪ Event Replay & Timeline")
st.markdown("*Browse simulation history and replay key moments*")
st.markdown("---")

# ===== REPLAY CONTROLS =====
control_col1, control_col2, control_col3, control_col4 = st.columns([2, 1, 1, 1])

with control_col1:
    btn1, btn2, btn3, btn4, btn5 = st.columns(5)
    with btn1:
        st.button("⏮️ FIRST", use_container_width=True, key="replay_first")
    with btn2:
        st.button("◀️ PREV", use_container_width=True, key="replay_prev")
    with btn3:
        st.button("▶️ PLAY", use_container_width=True, key="replay_play", type="primary")
    with btn4:
        st.button("NEXT ▶️", use_container_width=True, key="replay_next")
    with btn5:
        st.button("⏭️ LAST", use_container_width=True, key="replay_last")

with control_col2:
    event_index = st.number_input("Event #", min_value=1, max_value=len(EVENTS), value=1)

with control_col3:
    playback_speed = st.select_slider("Speed", options=["0.5x", "1x", "2x", "5x", "10x"], value="1x")

with control_col4:
    auto_refresh = st.toggle("Auto-play", value=False)

st.markdown("---")

# ===== EVENT TIMELINE =====
st.markdown("### 📅 Event Timeline")

event_types = list(set(e['type'] for e in EVENTS))
selected_types = st.multiselect("Filter by Event Type", event_types, default=event_types)

filtered_events = [e for e in EVENTS if e['type'] in selected_types]

timeline_data = []
for event in filtered_events:
    timeline_data.append({
        'Timestamp': event['timestamp'],
        'Type': event['type'],
        'Description': event['description'],
        'Impact': event['impact']
    })

df_timeline = pd.DataFrame(timeline_data)
df_timeline['Timestamp'] = pd.to_datetime(df_timeline['Timestamp'])

fig = go.Figure()

type_colors = {
    'action': '#00ff88',
    'thought': '#00d4ff',
    'interaction': '#b400ff',
    'world': '#ffcc00',
    'milestone': '#ff8800'
}

for event_type in selected_types:
    type_events = df_timeline[df_timeline['Type'] == event_type]
    fig.add_trace(go.Scatter(
        x=type_events['Timestamp'], y=type_events['Impact'],
        mode='markers', name=event_type.upper(),
        marker=dict(size=12, color=type_colors.get(event_type, '#8892a4'), line=dict(color='white', width=1)),
        text=type_events['Description'], hoverinfo='text+x+y'
    ))

fig.update_layout(
    template='plotly_dark', paper_bgcolor='rgba(10, 14, 23, 1)',
    plot_bgcolor='rgba(10, 14, 23, 1)', height=300,
    xaxis=dict(showgrid=False),
    yaxis=dict(title='Impact', showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[-1.2, 1.2]),
    legend=dict(bgcolor='rgba(26, 31, 46, 0.8)'), showlegend=True
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

# ===== EVENT LOG =====
st.markdown("### 📜 Event Log")

log_col1, log_col2 = st.columns([2, 1])

with log_col1:
    st.markdown("""
<div style='max-height:500px;overflow-y:auto;background:#0a0e17;border-radius:12px;padding:1rem;'>
""", unsafe_allow_html=True)
    
    for idx, event in enumerate(filtered_events[:30]):
        type_color = type_colors.get(event['type'], '#8892a4')
        impact_color = '#00ff88' if event['impact'] > 0 else '#ff0055' if event['impact'] < 0 else '#ffcc00'
        impact_icon = '📈' if event['impact'] > 0 else '📉' if event['impact'] < 0 else '➡️'
        is_selected = (idx + 1 == event_index)
        border_style = 'border:2px solid #00ff88;' if is_selected else ''
        st.markdown(f"""
<div style='background:#151a27;border-radius:8px;padding:0.75rem;margin:0.5rem 0;{border_style}'>
<div style='display:flex;justify-content:space-between;align-items:center;'>
<div style='display:flex;align-items:center;gap:0.5rem;'>
<span style='color:#8892a4;font-size:0.75rem;'>#{event['id']}</span>
<span style='background:{type_color};color:#0a0e17;padding:2px 8px;border-radius:4px;font-size:0.7rem;font-weight:bold;'>{event['type'].upper()}</span>
</div>
<span style='color:#8892a4;font-size:0.75rem;'>{event['timestamp']}</span>
</div>
<div style='margin-top:0.5rem;color:#e0e6ed;font-size:0.9rem;'>{event['description']}</div>
<div style='margin-top:0.5rem;display:flex;align-items:center;gap:0.5rem;'>
<span>{impact_icon}</span>
<span style='color:{impact_color};font-weight:bold;'>{event['impact']:+.2f}</span>
<span style='color:#8892a4;font-size:0.75rem;'>impact</span>
</div>
</div>
""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with log_col2:
    st.markdown("### 📊 Event Statistics")
    event_counts = {}
    for event in filtered_events:
        event_counts[event['type']] = event_counts.get(event['type'], 0) + 1
    for event_type, count in sorted(event_counts.items(), key=lambda x: x[1], reverse=True):
        color = type_colors.get(event_type, '#8892a4')
        st.markdown(f"""
<div style='display:flex;align-items:center;justify-content:space-between;padding:0.75rem;background:#151a27;border-radius:8px;margin:0.5rem 0;border-left:3px solid {color};'>
<span style='color:{color};font-weight:bold;'>{event_type.upper()}</span>
<span style='color:#e0e6ed;font-size:1.2rem;font-weight:bold;'>{count}</span>
</div>
""", unsafe_allow_html=True)
    avg_impact = sum(e['impact'] for e in filtered_events) / len(filtered_events) if filtered_events else 0
    st.markdown(f"""
<div class='stat-card' style='margin-top:1rem;'>
<div style='color:#8892a4;font-size:0.8rem;'>AVERAGE IMPACT</div>
<div style='font-size:2rem;font-weight:bold;color:{"#00ff88" if avg_impact > 0 else "#ff0055" if avg_impact < 0 else "#ffcc00"};'>
{avg_impact:+.3f}
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===== AGENT ACTIVITY TIMELINE =====
st.markdown("### 👤 Agent Activity Timeline")

agent_names = [a['name'] for a in AGENTS]
selected_agent_name = st.selectbox("Select Agent", agent_names, key="replay_agent_select")
selected_agent = next(a for a in AGENTS if a['name'] == selected_agent_name)
layer_info = LAYER_NAMES[selected_agent['layer']]

agent_col1, agent_col2 = st.columns([1, 2])

with agent_col1:
    st.markdown(f"""
<div class='agent-card layer-{selected_agent['layer']}'>
<div style='text-align:center;'>
<div style='font-size:3rem;'>{layer_info['icon']}</div>
<div style='font-size:1.5rem;font-weight:bold;color:#e0e6ed;margin:0.5rem 0;'>{selected_agent['name']}</div>
<span class='layer-badge l{selected_agent['layer']}'>L{selected_agent['layer']}</span>
</div>
<div style='margin-top:1rem;display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;font-size:0.8rem;'>
<div style='text-align:center;padding:0.5rem;background:rgba(255,255,255,0.03);border-radius:4px;'>
<div style='color:#8892a4;'>Influence</div>
<div style='color:#b400ff;font-weight:bold;'>{selected_agent['influence']:.2f}</div>
</div>
<div style='text-align:center;padding:0.5rem;background:rgba(255,255,255,0.03);border-radius:4px;'>
<div style='color:#8892a4;'>Confidence</div>
<div style='color:#00d4ff;font-weight:bold;'>{selected_agent['confidence']:.0%}</div>
</div>
<div style='text-align:center;padding:0.5rem;background:rgba(255,255,255,0.03);border-radius:4px;'>
<div style='color:#8892a4;'>Trades</div>
<div style='color:#00ff88;font-weight:bold;'>{selected_agent['total_actions']}</div>
</div>
<div style='text-align:center;padding:0.5rem;background:rgba(255,255,255,0.03);border-radius:4px;'>
<div style='color:#8892a4;'>Success Rate</div>
<div style='color:#ffcc00;font-weight:bold;'>{selected_agent['success_rate']:.0%}</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

with agent_col2:
    st.markdown("### 📈 Agent Confidence Over Time")
    dates = pd.date_range(end=datetime.now(), periods=24, freq='H')
    confidence_history = [selected_agent['confidence'] + (i * 0.01 * (1 if i % 2 == 0 else -1)) for i in range(24)]
    confidence_history = [max(0.1, min(0.99, c)) for c in confidence_history]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=confidence_history, mode='lines+markers',
        line=dict(color=layer_info['color'], width=2), marker=dict(size=8, color=layer_info['color']),
        fill='tozeroy',
        fillcolor=f"rgba{tuple(int(layer_info['color'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.1,)}"
    ))
    fig.update_layout(
        template='plotly_dark', paper_bgcolor='rgba(10, 14, 23, 1)',
        plot_bgcolor='rgba(10, 14, 23, 1)', height=300,
        xaxis=dict(showgrid=False),
        yaxis=dict(title='Confidence', showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[0, 1])
    )
    st.plotly_chart(fig, use_container_width=True)