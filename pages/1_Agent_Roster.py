import textwrap
"""
Agent Grid Page - Professional Agent Roster with Radar Profiles
Filter by layer, mood, action with detailed attribute radar charts
"""

import streamlit as st
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.demo_data import AGENTS, LAYER_NAMES, MOODS, ACTIONS, PERSONALITIES
from core.ui_utils import (
    load_css, pro_header, section_header, status_bar,
    stat_card, radar_chart, gauge_chart, status_dot,
    status_light_bar, corner_badge, LAYER_COLORS,
    hex_to_rgba_str
)

st.set_page_config(page_title="Agent Roster", page_icon="◈", layout="wide")
load_css()

# Header
st.markdown(pro_header("◈ AGENT ROSTER", "4-Layer Agent Management System"), unsafe_allow_html=True)

# Status bar
st.markdown(status_bar([
    {"label": "TOTAL", "value": str(len(AGENTS)), "status": "online"},
    {"label": "ACTIVE", "value": str(sum(1 for a in AGENTS if a['confidence'] > 0.5)), "status": "online"},
    {"label": "ACT SIGNAL", "value": str(sum(1 for a in AGENTS if a['action'] == 'ACT')), "status": "processing"},
    {"label": "OBSERVE SIGNAL", "value": str(sum(1 for a in AGENTS if a['action'] == 'OBSERVE')), "status": "warning"},
]), unsafe_allow_html=True)

# ===== FILTERS =====
st.markdown(section_header("⚙️", "FILTERS"), unsafe_allow_html=True)

filter_cols = st.columns(5)
with filter_cols[0]:
    layer_filter = st.multiselect(
        "Layer", options=[1, 2, 3, 4], default=[1, 2, 3, 4],
        format_func=lambda x: f"L{x} - {LAYER_NAMES[x]['name_en']}",
        key="layer_filter"
    )
with filter_cols[1]:
    mood_filter = st.multiselect(
        "Mood", options=list(MOODS.keys()), default=list(MOODS.keys()), key="mood_filter"
    )
with filter_cols[2]:
    action_filter = st.multiselect(
        "Action", options=ACTIONS, default=ACTIONS, key="action_filter"
    )
with filter_cols[3]:
    personality_filter = st.multiselect(
        "Personality", options=PERSONALITIES, default=PERSONALITIES, key="personality_filter"
    )
with filter_cols[4]:
    min_confidence = st.slider("Min Confidence", 0.0, 1.0, 0.0, 0.1, key="min_conf_slider")

# Apply filters
filtered_agents = [
    a for a in AGENTS
    if a["layer"] in layer_filter
    and a["mood"] in mood_filter
    and a["action"] in action_filter
    and a["personality"] in personality_filter
    and a["confidence"] >= min_confidence
]

st.markdown(f"<div style='color:#6b7a90;font-size:0.8rem;margin-bottom:1rem;'>Showing <span style='color:#00ff88;font-weight:bold;'>{len(filtered_agents)}</span> of {len(AGENTS)} agents</div>", unsafe_allow_html=True)

# ===== SELECTED AGENT DETAIL (if any) =====
selected_agent_id = st.session_state.get("selected_agent", None)
selected_agent = next((a for a in AGENTS if a["id"] == selected_agent_id), None)

if selected_agent:
    layer_info = LAYER_NAMES[selected_agent["layer"]]
    mood_info = MOODS[selected_agent["mood"]]
    layer_color = LAYER_COLORS[selected_agent["layer"]]
    
    st.markdown(section_header("🔍", f"AGENT PROFILE: {selected_agent['name'].upper()}"), unsafe_allow_html=True)
    
    detail_col1, detail_col2, detail_col3 = st.columns([1, 1, 1])
    
    with detail_col1:
        # Agent info card
        st.markdown(f"""
<div class='stat-card' style='border-left:3px solid {layer_color};'>
<div style='display:flex;align-items:center;gap:1rem;margin-bottom:1rem;'>
<span style='font-size:2.5rem;'>{layer_info['icon']}</span>
<div>
<div style='font-size:1.4rem;font-weight:bold;color:#e8edf4;'>{selected_agent['name']}</div>
<div style='font-size:0.8rem;color:#6b7a90;'>{selected_agent['id']}</div>
<span class='layer-badge l{selected_agent['layer']}'>L{selected_agent['layer']}</span>
</div>
</div>
<div style='margin-bottom:0.75rem;'>
<div style='color:#6b7a90;font-size:0.7rem;letter-spacing:1px;'>PERSONALITY</div>
<div style='color:#e8edf4;font-size:0.9rem;'>{selected_agent['personality']}</div>
</div>
<div style='display:flex;align-items:center;gap:0.5rem;'>
<span style='font-size:1.5rem;'>{mood_info['emoji']}</span>
<span style='color:{mood_info['color']};font-weight:bold;letter-spacing:1px;'>{selected_agent['mood'].upper()}</span>
</div>
{status_light_bar(['green' if selected_agent['confidence']>0.6 else 'yellow' if selected_agent['confidence']>0.3 else 'red'], 5)}
</div>
""", unsafe_allow_html=True)
        
        # Stats bars
        for stat_name, stat_key, bar_class, icon in [
            ("HP", "hp", "hp", "❤️"),
            ("MP", "mp", "mp", "💧"),
            ("Confidence", "confidence", "confidence", "🎯")
        ]:
            val = selected_agent[stat_key]
            display_val = f"{val:.0%}" if stat_key == "confidence" else f"{val}/100"
            pct = val * 100 if stat_key == "confidence" else val
            st.markdown(f"""
<div style='margin-top:0.5rem;'>
<div style='display:flex;justify-content:space-between;font-size:0.7rem;color:#6b7a90;'>
<span>{icon} {stat_name}</span><span>{display_val}</span>
</div>
<div class='stat-bar'>
<div class='stat-bar-fill {bar_class}' style='width:{pct}%;'></div>
</div>
</div>
""", unsafe_allow_html=True)
    
    with detail_col2:
        # Radar chart
        radar_categories = ["HP", "MP", "Confidence", "Influence", "Success Rate", "Activity"]
        radar_values = [
            selected_agent["hp"],
            selected_agent["mp"],
            selected_agent["confidence"] * 100,
            selected_agent["influence"] * 100,
            selected_agent["success_rate"] * 100,
            min(selected_agent["interaction_count"] / 2, 100)
        ]
        
        st.plotly_chart(
            radar_chart(
                radar_categories, radar_values,
                title=f"{selected_agent['name']} - Attribute Profile",
                fill_color=hex_to_rgba_str(layer_color, 0.15),
                line_color=layer_color,
                height=320
            ),
            use_container_width=True
        )
    
    with detail_col3:
        # Agent thought
        st.markdown(f"""
<div class='thought-bubble'>
<div style='font-size:0.7rem;color:#00d4ff;margin-bottom:0.35rem;font-family:Orbitron,sans-serif;'>CURRENT THOUGHT</div>
<div style='font-size:0.85rem;line-height:1.6;color:#e8edf4;'>{selected_agent['thought']}</div>
</div>
""", unsafe_allow_html=True)
        
        # Metrics grid
        metrics = [
            ("Followers", f"{selected_agent['followers']:,}", "#00d4ff"),
            ("Total Actions", str(selected_agent["total_actions"]), "#ffcc00"),
            ("Success Rate", f"{selected_agent['success_rate']:.0%}", "#00ff88"),
            ("Token Usage", f"{selected_agent['token_usage']:,}", "#ff8800"),
            ("Memory Slots", str(selected_agent["memory_slots"]), "#b400ff"),
            ("Interactions", str(selected_agent["interaction_count"]), "#00d4ff"),
        ]
        
        m_cols = st.columns(3)
        for i, (label, value, color) in enumerate(metrics):
            with m_cols[i % 3]:
                st.markdown(f"""
<div style='background:rgba(255,255,255,0.03);border-radius:8px;padding:0.75rem;text-align:center;margin-bottom:0.5rem;'>
<div style='font-size:0.6rem;color:#6b7a90;letter-spacing:1px;text-transform:uppercase;'>{label}</div>
<div style='font-size:1.1rem;font-weight:bold;color:{color};margin-top:0.25rem;font-family:Orbitron,sans-serif;'>{value}</div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("---")

# ===== AGENT GRID =====
st.markdown(section_header("👥", "AGENT GRID"), unsafe_allow_html=True)

cols_per_row = 4
for i in range(0, len(filtered_agents), cols_per_row):
    cols = st.columns(cols_per_row)
    
    for j, agent in enumerate(filtered_agents[i:i+cols_per_row]):
        with cols[j]:
            layer_info = LAYER_NAMES[agent["layer"]]
            mood_info = MOODS[agent["mood"]]
            layer_color = LAYER_COLORS[agent["layer"]]
            action_color_map = {"ACT": "#00ff88", "OBSERVE": "#ff0055", "HOLD": "#ffcc00", "WAIT": "#8892a4", "RESEARCH": "#00d4ff"}
            action_color = action_color_map.get(agent["action"], "#8892a4")
            
            # Determine status lights
            status_lights = []
            if agent["confidence"] > 0.7:
                status_lights = ["green", "green", "green"]
            elif agent["confidence"] > 0.5:
                status_lights = ["green", "yellow"]
            elif agent["confidence"] > 0.3:
                status_lights = ["yellow"]
            else:
                status_lights = ["red"]
            
            is_selected = agent["id"] == selected_agent_id
            selected_style = f"box-shadow: 0 0 30px rgba({','.join(str(int(layer_color[i:i+2], 16)) for i in (1,3,5))},0.3);" if is_selected else ""
            
            st.markdown(f"""
<div class='agent-card layer-{agent['layer']}' style='{selected_style}position:relative;'>
{corner_badge(f"L{agent['layer']}", layer_color) if not is_selected else ''}
<!-- Header -->
<div style='display:flex;justify-content:space-between;align-items:flex-start;'>
<div>
<div style='font-size:1.1rem;font-weight:bold;color:#e8edf4;'>
{layer_info['icon']} {agent['name']}
</div>
<div style='font-size:0.7rem;color:#6b7a90;font-family:JetBrains Mono,monospace;'>{agent['id']}</div>
</div>
<div style='text-align:right;'>
<div style='font-size:1.5rem;'>{mood_info['emoji']}</div>
<div style='font-size:0.6rem;color:{mood_info['color']};letter-spacing:1px;font-family:Orbitron,sans-serif;'>{agent['mood'].upper()}</div>
</div>
</div>
<!-- Personality -->
<div style='margin-top:0.5rem;padding:0.35rem 0.5rem;background:rgba(255,255,255,0.03);border-radius:6px;'>
<span style='font-size:0.7rem;color:#6b7a90;'>{agent['personality']}</span>
</div>
<!-- Stats Bars -->
<div style='margin-top:0.5rem;'>
<div style='display:flex;justify-content:space-between;font-size:0.65rem;color:#6b7a90;'>
<span>❤️ HP</span><span>{agent['hp']}/100</span>
</div>
<div class='stat-bar'><div class='stat-bar-fill hp' style='width:{agent['hp']}%;'></div></div>
</div>
<div style='margin-top:0.35rem;'>
<div style='display:flex;justify-content:space-between;font-size:0.65rem;color:#6b7a90;'>
<span>💧 MP</span><span>{agent['mp']}/100</span>
</div>
<div class='stat-bar'><div class='stat-bar-fill mp' style='width:{agent['mp']}%;'></div></div>
</div>
<div style='margin-top:0.35rem;'>
<div style='display:flex;justify-content:space-between;font-size:0.65rem;color:#6b7a90;'>
<span>🎯 Confidence</span><span>{agent['confidence']:.0%}</span>
</div>
<div class='stat-bar'><div class='stat-bar-fill confidence' style='width:{agent['confidence']*100:.0f}%;'></div></div>
</div>
<!-- Action Badge -->
<div style='margin-top:0.5rem;text-align:center;padding:0.35rem;background:{hex_to_rgba_str(action_color, 0.08)};border:1px solid {hex_to_rgba_str(action_color, 0.3)};border-radius:6px;'>
<span style='font-weight:bold;color:{action_color};font-size:0.85rem;font-family:Orbitron,sans-serif;letter-spacing:1px;'>{agent['action']}</span>
</div>
<!-- Mini Stats -->
<div style='margin-top:0.5rem;display:grid;grid-template-columns:1fr 1fr;gap:0.35rem;font-size:0.65rem;'>
<div style='text-align:center;padding:0.25rem;background:rgba(255,255,255,0.02);border-radius:4px;'>
<div style='color:#6b7a90;'>Influence</div>
<div style='color:#b400ff;font-weight:bold;'>{agent['influence']:.2f}</div>
</div>
<div style='text-align:center;padding:0.25rem;background:rgba(255,255,255,0.02);border-radius:4px;'>
<div style='color:#6b7a90;'>Success</div>
<div style='color:#00ff88;font-weight:bold;'>{agent['success_rate']:.0%}</div>
</div>
<div style='text-align:center;padding:0.25rem;background:rgba(255,255,255,0.02);border-radius:4px;'>
<div style='color:#6b7a90;'>Followers</div>
<div style='color:#00d4ff;font-weight:bold;'>{agent['followers']:,}</div>
</div>
<div style='text-align:center;padding:0.25rem;background:rgba(255,255,255,0.02);border-radius:4px;'>
<div style='color:#6b7a90;'>Trades</div>
<div style='color:#ffcc00;font-weight:bold;'>{agent['total_actions']}</div>
</div>
</div>
<!-- Status Light Bar -->
{status_light_bar(status_lights, 5)}
<!-- Last Active -->
<div style='margin-top:0.35rem;text-align:center;font-size:0.6rem;color:#3d4b5e;font-family:JetBrains Mono,monospace;'>
last: {agent['last_active']}
</div>
</div>
""", unsafe_allow_html=True)
            
            if st.button("Select", key=f"select_{agent['id']}", use_container_width=True):
                st.session_state.selected_agent = agent["id"]
                st.rerun()

# ===== FILTERED SUMMARY =====
st.markdown("---")
st.markdown(section_header("📊", "FILTERED SUMMARY"), unsafe_allow_html=True)

if filtered_agents:
    sum_cols = st.columns(4)
    with sum_cols[0]:
        avg_conf = sum(a["confidence"] for a in filtered_agents) / len(filtered_agents)
        st.markdown(stat_card("Avg Confidence", f"{avg_conf:.0%}", "#00d4ff"), unsafe_allow_html=True)
    with sum_cols[1]:
        avg_inf = sum(a["influence"] for a in filtered_agents) / len(filtered_agents)
        st.markdown(stat_card("Avg Influence", f"{avg_inf:.2f}", "#b400ff"), unsafe_allow_html=True)
    with sum_cols[2]:
        total_follow = sum(a["followers"] for a in filtered_agents)
        st.markdown(stat_card("Total Followers", f"{total_follow:,}", "#00ff88"), unsafe_allow_html=True)
    with sum_cols[3]:
        buy_c = sum(1 for a in filtered_agents if a["action"] == "ACT")
        sell_c = sum(1 for a in filtered_agents if a["action"] == "OBSERVE")
        st.markdown(stat_card("Active/Idle Ratio", f"{buy_c}:{sell_c}", "#ffcc00"), unsafe_allow_html=True)