import textwrap
"""
Memory System Page - SALM (Structured Agent Memory) Visualization
Shows working memory, long-term memory, and memory operations
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.demo_data import AGENTS, LAYER_NAMES

st.set_page_config(page_title="Memory System", page_icon="🧠", layout="wide")

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("# 🧠 SALM Memory System")
st.markdown("*Structured Agent Long-term Memory - Monitor memory operations across all agents*")
st.markdown("---")

# ===== MEMORY OVERVIEW =====
mem_col1, mem_col2, mem_col3, mem_col4, mem_col5 = st.columns(5)

total_memory_slots = sum(a['memory_slots'] for a in AGENTS)
avg_memory_usage = random.uniform(0.4, 0.7)

with mem_col1:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>TOTAL MEMORY SLOTS</div>
<div style='font-size:2rem;font-weight:bold;color:#00ff88;'>{total_memory_slots}</div>
</div>
""", unsafe_allow_html=True)

with mem_col2:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>MEMORY USAGE</div>
<div style='font-size:2rem;font-weight:bold;color:#00d4ff;'>{avg_memory_usage:.0%}</div>
</div>
""", unsafe_allow_html=True)

with mem_col3:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>CACHE HIT RATE</div>
<div style='font-size:2rem;font-weight:bold;color:#ffcc00;'>{random.uniform(0.6, 0.9):.0%}</div>
</div>
""", unsafe_allow_html=True)

with mem_col4:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>ACTIVE MEMORIES</div>
<div style='font-size:2rem;font-weight:bold;color:#b400ff;'>{random.randint(500, 2000):,}</div>
</div>
""", unsafe_allow_html=True)

with mem_col5:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>DEDUPLICATION RATE</div>
<div style='font-size:2rem;font-weight:bold;color:#ff8800;'>{random.uniform(0.3, 0.5):.0%}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===== MEMORY ARCHITECTURE =====
st.markdown("### 🏗️ SALM Architecture")

arch_col1, arch_col2 = st.columns([1, 2])

with arch_col1:
    st.markdown("""
<div class='stat-card'>
<div style='font-size:1.2rem;font-weight:bold;color:#00ff88;margin-bottom:1rem;'>
📦 Memory Layers
</div>
<div style='margin-bottom:1rem;padding:0.75rem;background:rgba(180, 0, 255, 0.1);border-radius:8px;'>
<div style='font-weight:bold;color:#b400ff;'>🔮 Working Memory</div>
<div style='font-size:0.8rem;color:#8892a4;'>Current context & active thoughts</div>
<div style='font-size:0.75rem;color:#e0e6ed;margin-top:0.25rem;'>
Capacity: 7±2 items | TTL: 5 minutes
</div>
</div>
<div style='margin-bottom:1rem;padding:0.75rem;background:rgba(0, 212, 255, 0.1);border-radius:8px;'>
<div style='font-weight:bold;color:#00d4ff;'>💾 Short-term Memory</div>
<div style='font-size:0.8rem;color:#8892a4;'>Recent events & decisions</div>
<div style='font-size:0.75rem;color:#e0e6ed;margin-top:0.25rem;'>
Capacity: 50 items | TTL: 1 hour
</div>
</div>
<div style='margin-bottom:1rem;padding:0.75rem;background:rgba(0, 255, 136, 0.1);border-radius:8px;'>
<div style='font-weight:bold;color:#00ff88;'>🗄️ Long-term Memory</div>
<div style='font-size:0.8rem;color:#8892a4;'>Persistent knowledge & patterns</div>
<div style='font-size:0.75rem;color:#e0e6ed;margin-top:0.25rem;'>
Capacity: 500+ items | TTL: Permanent
</div>
</div>
<div style='padding:0.75rem;background:rgba(255, 204, 0, 0.1);border-radius:8px;'>
<div style='font-weight:bold;color:#ffcc00;'>🔗 Shared Memory Pool</div>
<div style='font-size:0.8rem;color:#8892a4;'>Cross-agent knowledge sharing</div>
<div style='font-size:0.75rem;color:#e0e6ed;margin-top:0.25rem;'>
Hash-based deduplication
</div>
</div>
</div>
""", unsafe_allow_html=True)

with arch_col2:
    st.markdown("### 📊 Memory Operations (Last 24h)")
    operations = ['READ', 'WRITE', 'UPDATE', 'DELETE', 'SEARCH']
    hours = [f"{h:02d}:00" for h in range(24)]
    op_data = []
    for hour in hours:
        for op in operations:
            op_data.append({'Hour': hour, 'Operation': op, 'Count': random.randint(10, 500)})
    df_ops = pd.DataFrame(op_data)
    fig = px.line(df_ops, x='Hour', y='Count', color='Operation',
        color_discrete_map={'READ': '#00ff88', 'WRITE': '#00d4ff', 'UPDATE': '#ffcc00', 'DELETE': '#ff0055', 'SEARCH': '#b400ff'})
    fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(10, 14, 23, 1)',
        plot_bgcolor='rgba(10, 14, 23, 1)', height=400,
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ===== AGENT MEMORY INSPECTION =====
st.markdown("### 🔍 Agent Memory Inspector")

agent_names = [a['name'] for a in AGENTS]
selected_agent_name = st.selectbox("Select Agent", agent_names, key="memory_agent_select")
selected_agent = next(a for a in AGENTS if a['name'] == selected_agent_name)

agent_col1, agent_col2 = st.columns([1, 1])

with agent_col1:
    layer_info = LAYER_NAMES[selected_agent['layer']]
    st.markdown(f"""
<div class='agent-card layer-{selected_agent['layer']}'>
<div style='display:flex;justify-content:space-between;align-items:center;'>
<div>
<span style='font-size:2rem;'>{layer_info['icon']}</span>
<span style='font-size:1.5rem;font-weight:bold;color:#e0e6ed;margin-left:0.5rem;'>{selected_agent['name']}</span>
</div>
<span class='layer-badge l{selected_agent['layer']}'>L{selected_agent['layer']}</span>
</div>
<div style='margin-top:1rem;display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;'>
<div style='text-align:center;padding:0.75rem;background:rgba(255,255,255,0.03);border-radius:8px;'>
<div style='color:#8892a4;font-size:0.8rem;'>Memory Slots</div>
<div style='font-size:1.5rem;font-weight:bold;color:#00ff88;'>{selected_agent['memory_slots']}</div>
</div>
<div style='text-align:center;padding:0.75rem;background:rgba(255,255,255,0.03);border-radius:8px;'>
<div style='color:#8892a4;font-size:0.8rem;'>Token Usage</div>
<div style='font-size:1.5rem;font-weight:bold;color:#00d4ff;'>{selected_agent['token_usage']:,}</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

with agent_col2:
    st.markdown("### 📝 Working Memory")
    working_memory = [
        {"type": "thought", "content": "World showing bullish divergence on RSI", "age": "2m ago"},
        {"type": "observation", "content": "Volume spike detected in tech sector", "age": "5m ago"},
        {"type": "decision", "content": "Decided to HOLD position until confirmation", "age": "8m ago"},
        {"type": "social", "content": "Layer 1 agent 'Buffett' signaled BUY", "age": "12m ago"},
    ]
    for mem in working_memory:
        type_colors = {"thought": "#00d4ff", "observation": "#00ff88", "decision": "#ffcc00", "social": "#b400ff"}
        color = type_colors.get(mem["type"], "#8892a4")
        st.markdown(f"""
<div style='background:#151a27;border-left:3px solid {color};padding:0.75rem;margin:0.5rem 0;border-radius:0 8px 8px 0;'>
<div style='display:flex;justify-content:space-between;'>
<span style='color:{color};font-size:0.75rem;font-weight:bold;'>{mem['type'].upper()}</span>
<span style='color:#8892a4;font-size:0.7rem;'>{mem['age']}</span>
</div>
<div style='margin-top:0.25rem;color:#e0e6ed;font-size:0.9rem;'>{mem['content']}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===== MEMORY STATISTICS BY LAYER =====
st.markdown("### 📊 Memory Statistics by Layer")

layer_mem_col1, layer_mem_col2, layer_mem_col3, layer_mem_col4 = st.columns(4)

for idx, layer_id in enumerate([1, 2, 3, 4]):
    with [layer_mem_col1, layer_mem_col2, layer_mem_col3, layer_mem_col4][idx]:
        layer_agents = [a for a in AGENTS if a['layer'] == layer_id]
        layer_info = LAYER_NAMES[layer_id]
        total_slots = sum(a['memory_slots'] for a in layer_agents)
        avg_usage = random.uniform(0.4, 0.8)
        st.markdown(f"""
<div class='stat-card' style='border-left:3px solid {layer_info['color']};'>
<div style='display:flex;justify-content:space-between;align-items:center;'>
<span style='font-size:1.5rem;'>{layer_info['icon']}</span>
<span class='layer-badge l{layer_id}'>L{layer_id}</span>
</div>
<div style='font-size:1rem;font-weight:bold;margin:0.5rem 0;color:{layer_info['color']};'>{layer_info['name_en']}</div>
<div style='margin-top:0.75rem;'>
<div style='display:flex;justify-content:space-between;font-size:0.8rem;color:#8892a4;'>
<span>Total Slots</span><span>{total_slots}</span>
</div>
<div style='display:flex;justify-content:space-between;font-size:0.8rem;color:#8892a4;margin-top:0.25rem;'>
<span>Avg Usage</span><span>{avg_usage:.0%}</span>
</div>
<div class='stat-bar' style='margin-top:0.5rem;'>
<div class='stat-bar-fill confidence' style='width:{avg_usage*100:.0f}%;'></div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===== MEMORY DEDUPLICATION =====
st.markdown("### 🔄 Memory Deduplication Engine")

dedup_col1, dedup_col2 = st.columns(2)

with dedup_col1:
    st.markdown("""
<div class='stat-card'>
<div style='font-size:1.2rem;font-weight:bold;color:#00ff88;margin-bottom:1rem;'>🔑 Hash-Based Deduplication</div>
<div style='font-size:0.9rem;color:#e0e6ed;line-height:1.6;'>
<p>The SALM system uses content-based hashing to detect and eliminate duplicate memories across agents.</p>
<div style='margin:1rem 0;padding:1rem;background:rgba(0,255,136,0.05);border-radius:8px;'>
<div style='color:#00ff88;font-weight:bold;'>How It Works:</div>
<ol style='margin:0.5rem 0;padding-left:1.5rem;'>
<li>Generate SHA-256 hash of memory content</li>
<li>Check hash against global memory index</li>
<li>If match found, reference existing memory</li>
<li>If new, store with hash as key</li>
</ol>
</div>
<div style='display:flex;gap:1rem;margin-top:1rem;'>
<div style='flex:1;text-align:center;padding:0.75rem;background:rgba(0,212,255,0.1);border-radius:8px;'>
<div style='font-size:1.5rem;font-weight:bold;color:#00d4ff;'>{random.randint(1000, 5000)}</div>
<div style='font-size:0.75rem;color:#8892a4;'>Unique Memories</div>
</div>
<div style='flex:1;text-align:center;padding:0.75rem;background:rgba(255,204,0,0.1);border-radius:8px;'>
<div style='font-size:1.5rem;font-weight:bold;color:#ffcc00;'>{random.randint(500, 2000)}</div>
<div style='font-size:0.75rem;color:#8892a4;'>Deduplicated</div>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

with dedup_col2:
    st.markdown("""
<div class='stat-card'>
<div style='font-size:1.2rem;font-weight:bold;color:#b400ff;margin-bottom:1rem;'>📊 Token Savings from Dedup</div>
</div>
""", unsafe_allow_html=True)
    
    savings_data = {
        'Category': ['Hash Cache', 'Group Delegation', 'Template Reuse', 'Memory Share'],
        'Saved Tokens': [random.randint(5000, 20000), random.randint(3000, 15000),
                        random.randint(8000, 30000), random.randint(2000, 10000)],
        'Saved USD': [round(random.uniform(0.5, 3), 2), round(random.uniform(0.3, 2), 2),
                     round(random.uniform(0.8, 4), 2), round(random.uniform(0.2, 1.5), 2)]
    }
    df_savings = pd.DataFrame(savings_data)
    fig = px.bar(df_savings, x='Category', y='Saved Tokens',
        color='Category', color_discrete_sequence=['#00ff88', '#00d4ff', '#ffcc00', '#b400ff'])
    fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(10, 14, 23, 1)',
        plot_bgcolor='rgba(10, 14, 23, 1)', height=300, showlegend=False,
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'))
    st.plotly_chart(fig, use_container_width=True)
    
    total_tokens = sum(savings_data['Saved Tokens'])
    total_usd = sum(savings_data['Saved USD'])
    st.markdown(f"""
<div style='text-align:center;margin-top:1rem;'>
<div style='font-size:0.9rem;color:#8892a4;'>Total Tokens Saved</div>
<div style='font-size:2.5rem;font-weight:bold;color:#00ff88;'>{total_tokens:,}</div>
<div style='font-size:1rem;color:#ffcc00;'>≈ ${total_usd:.2f} USD</div>
</div>
""", unsafe_allow_html=True)