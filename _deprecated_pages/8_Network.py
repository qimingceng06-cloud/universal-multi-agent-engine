import textwrap
"""
Social Network Page - Agent interaction network visualization
Shows relationships, influence flows, and communication patterns
"""

import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.demo_data import (
    AGENTS, NETWORK, LAYER_NAMES, MOODS,
    NETWORK_LAYOUT, DEGREE_CENTRALITY, BETWEENNESS_CENTRALITY,
    NETWORK_DENSITY, NETWORK_COMPONENTS, NETWORK_AVG_DEGREE
)

st.set_page_config(page_title="Social Network", page_icon="🕸️", layout="wide")

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("# 🕸️ Social Network Analysis")
st.markdown("*Visualize agent interactions and influence flows*")
st.markdown("---")

# ===== NETWORK STATS (use pre-computed values) =====
net_col1, net_col2, net_col3, net_col4, net_col5 = st.columns(5)

with net_col1:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>TOTAL NODES</div>
<div style='font-size:2rem;font-weight:bold;color:#00ff88;'>{NETWORK.number_of_nodes()}</div>
</div>
""", unsafe_allow_html=True)

with net_col2:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>TOTAL EDGES</div>
<div style='font-size:2rem;font-weight:bold;color:#00d4ff;'>{NETWORK.number_of_edges()}</div>
</div>
""", unsafe_allow_html=True)

with net_col3:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>DENSITY</div>
<div style='font-size:2rem;font-weight:bold;color:#ffcc00;'>{NETWORK_DENSITY:.3f}</div>
</div>
""", unsafe_allow_html=True)

with net_col4:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>AVG DEGREE</div>
<div style='font-size:2rem;font-weight:bold;color:#b400ff;'>{NETWORK_AVG_DEGREE:.1f}</div>
</div>
""", unsafe_allow_html=True)

with net_col5:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>COMPONENTS</div>
<div style='font-size:2rem;font-weight:bold;color:#ff8800;'>{NETWORK_COMPONENTS}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===== MAIN NETWORK VISUALIZATION (use pre-computed layout) =====
st.markdown("### 🌐 Interaction Network Graph")

pos = NETWORK_LAYOUT

node_x, node_y, node_colors, node_sizes, node_text = [], [], [], [], []
node_ids = list(NETWORK.nodes())

for node_id in node_ids:
    x, y = pos[node_id]
    node_x.append(x)
    node_y.append(y)
    agent = next((a for a in AGENTS if a['id'] == node_id), None)
    if agent:
        node_colors.append(LAYER_NAMES[agent['layer']]['color'])
        node_sizes.append(agent['influence'] * 40 + 10)
        node_text.append(f"{agent['name']}<br>Layer: {agent['layer']}<br>Influence: {agent['influence']:.2f}")
    else:
        node_colors.append('#8892a4')
        node_sizes.append(10)
        node_text.append(node_id)

edge_x, edge_y = [], []
for edge in NETWORK.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

fig = go.Figure()
fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines',
    line=dict(color='rgba(0, 255, 136, 0.2)', width=1), hoverinfo='none', showlegend=False))
fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers',
    marker=dict(size=node_sizes, color=node_colors, line=dict(color='white', width=1), opacity=0.8),
    text=node_text, hoverinfo='text', showlegend=False))
fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(10, 14, 23, 1)',
    plot_bgcolor='rgba(10, 14, 23, 1)', height=600,
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    title=dict(text='Agent Interaction Network', font=dict(size=20, color='#e0e6ed')))
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

# ===== CENTRALITY ANALYSIS (use pre-computed values) =====
st.markdown("### 📊 Centrality Analysis")

cent_col1, cent_col2 = st.columns(2)

top_degree = sorted(DEGREE_CENTRALITY.items(), key=lambda x: x[1], reverse=True)[:10]
top_betweenness = sorted(BETWEENNESS_CENTRALITY.items(), key=lambda x: x[1], reverse=True)[:10]

with cent_col1:
    st.markdown("#### 🔝 Top 10 by Degree Centrality")
    for rank, (node_id, cent) in enumerate(top_degree, 1):
        agent = next((a for a in AGENTS if a['id'] == node_id), None)
        if agent:
            layer_info = LAYER_NAMES[agent['layer']]
            st.markdown(f"""
<div style='display:flex;align-items:center;padding:0.5rem;margin:0.25rem 0;background:#151a27;border-radius:8px;'>
<span style='font-size:1.5rem;font-weight:bold;color:#8892a4;width:2rem;'>{rank}</span>
<span style='font-size:1.2rem;margin:0 0.5rem;'>{layer_info['icon']}</span>
<div style='flex:1;'>
<div style='font-weight:bold;color:#e0e6ed;'>{agent['name']}</div>
<div style='font-size:0.75rem;color:#8892a4;'>L{agent['layer']}</div>
</div>
<div style='text-align:right;'><div style='font-weight:bold;color:#00ff88;'>{cent:.3f}</div></div>
</div>
""", unsafe_allow_html=True)

with cent_col2:
    st.markdown("#### 🌉 Top 10 by Betweenness Centrality")
    for rank, (node_id, cent) in enumerate(top_betweenness, 1):
        agent = next((a for a in AGENTS if a['id'] == node_id), None)
        if agent:
            layer_info = LAYER_NAMES[agent['layer']]
            st.markdown(f"""
<div style='display:flex;align-items:center;padding:0.5rem;margin:0.25rem 0;background:#151a27;border-radius:8px;'>
<span style='font-size:1.5rem;font-weight:bold;color:#8892a4;width:2rem;'>{rank}</span>
<span style='font-size:1.2rem;margin:0 0.5rem;'>{layer_info['icon']}</span>
<div style='flex:1;'>
<div style='font-weight:bold;color:#e0e6ed;'>{agent['name']}</div>
<div style='font-size:0.75rem;color:#8892a4;'>L{agent['layer']}</div>
</div>
<div style='text-align:right;'><div style='font-weight:bold;color:#b400ff;'>{cent:.3f}</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===== CROSS-LAYER INTERACTIONS =====
st.markdown("### 🔄 Cross-Layer Interaction Matrix")

interaction_matrix = np.zeros((4, 4))
for edge in NETWORK.edges():
    agent1 = next((a for a in AGENTS if a['id'] == edge[0]), None)
    agent2 = next((a for a in AGENTS if a['id'] == edge[1]), None)
    if agent1 and agent2:
        interaction_matrix[agent1['layer']-1][agent2['layer']-1] += 1
        interaction_matrix[agent2['layer']-1][agent1['layer']-1] += 1

layer_labels = [f"L{i}" for i in range(1, 5)]
fig = go.Figure(data=go.Heatmap(z=interaction_matrix, x=layer_labels, y=layer_labels,
    colorscale='Viridis', text=interaction_matrix.astype(int), texttemplate='%{text}',
    textfont=dict(size=16), showscale=True))
fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(10, 14, 23, 1)', height=400,
    title='Cross-Layer Interaction Count', xaxis_title='Target Layer', yaxis_title='Source Layer')
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ===== COMMUNITY DETECTION =====
st.markdown("### 👥 Community Detection")

try:
    communities = list(nx.community.girvan_newman(NETWORK))
    if communities:
        first_level = communities[0]
        st.markdown(f"**Found {len(first_level)} communities in the network**")
        comm_cols = st.columns(min(4, len(first_level)))
        for idx, community in enumerate(first_level[:4]):
            with comm_cols[idx]:
                comm_agents = [a for a in AGENTS if a['id'] in community]
                if comm_agents:
                    avg_influence = sum(a['influence'] for a in comm_agents) / len(comm_agents)
                    avg_confidence = sum(a['confidence'] for a in comm_agents) / len(comm_agents)
                    st.markdown(f"""
<div class='stat-card'>
<div style='font-weight:bold;color:#00ff88;margin-bottom:0.5rem;'>Community {idx + 1}</div>
<div style='font-size:0.9rem;color:#8892a4;'>{len(community)} members</div>
<div style='margin-top:0.75rem;display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;font-size:0.8rem;'>
<div><div style='color:#8892a4;'>Avg Influence</div><div style='color:#b400ff;font-weight:bold;'>{avg_influence:.2f}</div></div>
<div><div style='color:#8892a4;'>Avg Confidence</div><div style='color:#00d4ff;font-weight:bold;'>{avg_confidence:.0%}</div></div>
</div>
</div>
""", unsafe_allow_html=True)
                    top_members = sorted(comm_agents, key=lambda x: x['influence'], reverse=True)[:3]
                    for member in top_members:
                        layer_info = LAYER_NAMES[member['layer']]
                        st.markdown(f"{layer_info['icon']} {member['name']}")
except Exception:
    st.info("Community detection analysis in progress...")