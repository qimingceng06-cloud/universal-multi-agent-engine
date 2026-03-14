import textwrap
"""
World Map Page - Visualize the simulation world
Shows agent positions, world zones, and interaction flows
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.demo_data import AGENTS, WORLD_OVERVIEW, LAYER_NAMES, MOODS

st.set_page_config(page_title="World Map", page_icon="🌐", layout="wide")

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("# 🌐 Simulation World Map")
st.markdown("*Real-time visualization of agent positions and interactions*")
st.markdown("---")

# ===== WORLD STATS =====
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.markdown("""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>WORLD STATUS</div>
<div style='font-size:1.5rem;font-weight:bold;color:#00ff88;'>ACTIVE</div>
</div>
""", unsafe_allow_html=True)

with stat_col2:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>TOTAL AGENTS</div>
<div style='font-size:1.5rem;font-weight:bold;color:#00d4ff;'>{len(AGENTS)}</div>
</div>
""", unsafe_allow_html=True)

with stat_col3:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>MARKET CONDITION</div>
<div style='font-size:1.5rem;font-weight:bold;color:#ffcc00;'>{WORLD_OVERVIEW['world_condition']}</div>
</div>
""", unsafe_allow_html=True)

with stat_col4:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>SIMULATION TICK</div>
<div style='font-size:1.5rem;font-weight:bold;color:#b400ff;'>#{WORLD_OVERVIEW['simulation_tick']}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===== MAIN WORLD VISUALIZATION =====

# Generate positions for agents in a circular layout
def generate_world_positions(agents):
    """Generate 2D positions for agents based on their layer and influence"""
    positions = {}
    
    # Layer centers (forming a diamond pattern)
    layer_centers = {
        1: (0, 3),    # Top center
        2: (-3, 0),   # Left
        3: (3, 0),    # Right
        4: (0, -3)    # Bottom
    }
    
    for agent in agents:
        layer = agent["layer"]
        center_x, center_y = layer_centers[layer]
        
        # Add some randomness around the layer center
        angle = np.random.uniform(0, 2 * np.pi)
        radius = np.random.uniform(0.5, 2.0) * (1 + (4 - layer) * 0.3)
        
        x = center_x + radius * np.cos(angle)
        y = center_y + radius * np.sin(angle)
        
        positions[agent["id"]] = {
            "x": x,
            "y": y,
            "name": agent["name"],
            "layer": layer,
            "mood": agent["mood"],
            "influence": agent["influence"],
            "action": agent["action"]
        }
    
    return positions

world_positions = generate_world_positions(AGENTS)

# Create the world map figure
fig = go.Figure()

# Add background zones for each layer
zone_colors = {
    1: "rgba(180, 0, 255, 0.1)",
    2: "rgba(0, 212, 255, 0.1)",
    3: "rgba(0, 255, 136, 0.1)",
    4: "rgba(255, 204, 0, 0.1)"
}

layer_centers = {1: (0, 3), 2: (-3, 0), 3: (3, 0), 4: (0, -3)}

for layer_id, center in layer_centers.items():
    fig.add_shape(
        type="circle",
        x0=center[0]-2.5, y0=center[1]-2.5,
        x1=center[0]+2.5, y1=center[1]+2.5,
        fillcolor=zone_colors[layer_id],
        line=dict(color=LAYER_NAMES[layer_id]["color"], width=2, dash="dash")
    )

# Add agents to the map
for layer_id in [1, 2, 3, 4]:
    layer_agents = [a for a in AGENTS if a["layer"] == layer_id]
    
    x_vals = [world_positions[a["id"]]["x"] for a in layer_agents]
    y_vals = [world_positions[a["id"]]["y"] for a in layer_agents]
    
    # Size based on influence
    sizes = [a["influence"] * 30 + 10 for a in layer_agents]
    
    # Color based on mood
    colors = [MOODS[a["mood"]]["color"] for a in layer_agents]
    
    hover_text = [
        f"<b>{a['name']}</b><br>"
        f"Layer: {layer_id}<br>"
        f"Mood: {a['mood']}<br>"
        f"Action: {a['action']}<br>"
        f"Influence: {a['influence']:.2f}<br>"
        f"Confidence: {a['confidence']:.0%}"
        for a in layer_agents
    ]
    
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode="markers+text",
        marker=dict(
            size=sizes,
            color=colors,
            line=dict(color="white", width=1),
            opacity=0.8
        ),
        text=[LAYER_NAMES[layer_id]["icon"] for _ in layer_agents],
        textposition="middle center",
        textfont=dict(size=12),
        name=f"Layer {layer_id}: {LAYER_NAMES[layer_id]['name_en']}",
        hovertext=hover_text,
        hoverinfo="text"
    ))

# Add layer labels
for layer_id, center in layer_centers.items():
    fig.add_annotation(
        x=center[0], y=center[1] + 3,
        text=f"<b>{LAYER_NAMES[layer_id]['icon']} Layer {layer_id}</b><br>{LAYER_NAMES[layer_id]['name_en']}",
        showarrow=False,
        font=dict(size=12, color=LAYER_NAMES[layer_id]["color"]),
        bgcolor="rgba(10, 14, 23, 0.8)",
        bordercolor=LAYER_NAMES[layer_id]["color"],
        borderwidth=1,
        borderpad=4
    )

# Update layout
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(10, 14, 23, 1)",
    plot_bgcolor="rgba(10, 14, 23, 1)",
    title=dict(
        text="🎮 Agent World Map",
        font=dict(size=24, color="#e0e6ed", family="Orbitron")
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        range=[-8, 8]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        range=[-8, 8],
        scaleanchor="x"
    ),
    showlegend=True,
    legend=dict(
        bgcolor="rgba(26, 31, 46, 0.8)",
        bordercolor="rgba(0, 255, 136, 0.3)",
        borderwidth=1
    ),
    height=700
)

st.plotly_chart(fig, use_container_width=True)

# ===== ZONE DETAILS =====
st.markdown("---")
st.markdown("### 🏛️ Zone Details")

zone_cols = st.columns(4)

for idx, (layer_id, layer_info) in enumerate(LAYER_NAMES.items()):
    with zone_cols[idx]:
        layer_agents = [a for a in AGENTS if a["layer"] == layer_id]
        
        # Calculate zone stats
        avg_conf = sum(a["confidence"] for a in layer_agents) / len(layer_agents)
        avg_influence = sum(a["influence"] for a in layer_agents) / len(layer_agents)
        
        # Count actions
        action_counts = {}
        for a in layer_agents:
            action_counts[a["action"]] = action_counts.get(a["action"], 0) + 1
        
        top_action = max(action_counts.items(), key=lambda x: x[1])[0] if action_counts else "N/A"
        
        st.markdown(f"""
<div class='stat-card' style='border-left:3px solid {layer_info["color"]};'>
<div style='display:flex;justify-content:space-between;align-items:center;'>
<span style='font-size:2rem;'>{layer_info['icon']}</span>
<span class='layer-badge l{layer_id}'>L{layer_id}</span>
</div>
<div style='font-size:1.2rem;font-weight:bold;margin:0.5rem 0;color:{layer_info["color"]};'>
{layer_info['name_en']}
</div>
<div style='color:#8892a4;font-size:0.9rem;margin-bottom:1rem;'>
{len(layer_agents)} agents in zone
</div>
<div style='display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;font-size:0.8rem;'>
<div style='text-align:center;padding:0.5rem;background:rgba(255,255,255,0.03);border-radius:4px;'>
<div style='color:#8892a4;'>Avg Confidence</div>
<div style='color:#00d4ff;font-weight:bold;font-size:1.1rem;'>{avg_conf:.0%}</div>
</div>
<div style='text-align:center;padding:0.5rem;background:rgba(255,255,255,0.03);border-radius:4px;'>
<div style='color:#8892a4;'>Avg Influence</div>
<div style='color:#b400ff;font-weight:bold;font-size:1.1rem;'>{avg_influence:.2f}</div>
</div>
</div>
<div style='margin-top:0.75rem;text-align:center;padding:0.5rem;background:rgba(0, 255, 136, 0.1);border-radius:4px;'>
<div style='color:#8892a4;font-size:0.75rem;'>DOMINANT ACTION</div>
<div style='color:#00ff88;font-weight:bold;font-size:1.2rem;'>{top_action}</div>
</div>
</div>
""", unsafe_allow_html=True)

# ===== INTERACTION FLOW =====
st.markdown("---")
st.markdown("### 🔄 Cross-Layer Interaction Flow")

# Create Sankey diagram for cross-layer interactions
flow_data = {
    "source": [],
    "target": [],
    "value": []
}

# Simulate interaction flows between layers
interaction_matrix = {
    (1, 2): 150, (1, 3): 80, (1, 4): 30,
    (2, 1): 100, (2, 3): 200, (2, 4): 50,
    (3, 1): 60, (3, 2): 150, (3, 4): 300,
    (4, 1): 20, (4, 2): 40, (4, 3): 250
}

for (src, tgt), value in interaction_matrix.items():
    flow_data["source"].append(src - 1)
    flow_data["target"].append(tgt - 1)
    flow_data["value"].append(value)

labels = [f"L{i}: {LAYER_NAMES[i]['name_en']}" for i in range(1, 5)]
colors = [LAYER_NAMES[i]["color"] for i in range(1, 5)]

sankey_fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color=colors
    ),
    link=dict(
        source=flow_data["source"],
        target=flow_data["target"],
        value=flow_data["value"],
        color=["rgba(0, 255, 136, 0.2)"] * len(flow_data["source"])
    )
)])

sankey_fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(10, 14, 23, 1)",
    title=dict(
        text="Inter-Layer Influence Flow",
        font=dict(size=18, color="#e0e6ed")
    ),
    height=400
)

st.plotly_chart(sankey_fig, use_container_width=True)