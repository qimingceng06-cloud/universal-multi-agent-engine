import textwrap
"""
Scenario Editor Page - Create and edit simulation scenarios
YAML-based configuration with live preview
"""

import streamlit as st
import yaml
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.demo_data import LAYER_NAMES, PERSONALITIES, ACTIONS

st.set_page_config(page_title="Scenario Editor", page_icon="⚙️", layout="wide")

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("# ⚙️ Scenario Editor")
st.markdown("*Create and configure simulation scenarios*")
st.markdown("---")

# ===== PRESET SCENARIOS =====
st.markdown("### 📋 Preset Scenarios")

preset_cols = st.columns(5)

presets = [
    {"name": "📈 Stock World", "desc": "Simulate world dynamics", "icon": "📈"},
    {"name": "🗳️ Election", "desc": "Political opinion formation", "icon": "🗳️"},
    {"name": "🦠 Pandemic", "desc": "Disease spread modeling", "icon": "🦠"},
    {"name": "🌍 Climate", "desc": "Climate action simulation", "icon": "🌍"},
    {"name": "🏭 Supply Chain", "desc": "Logistics optimization", "icon": "🏭"}
]

for idx, preset in enumerate(presets):
    with preset_cols[idx]:
        if st.button(f"{preset['icon']}\n{preset['name']}", use_container_width=True, key=f"preset_{idx}"):
            st.session_state.selected_preset = preset['name']

st.markdown("---")

# ===== SCENARIO CONFIGURATION =====
config_col1, config_col2 = st.columns([1, 1])

with config_col1:
    st.markdown("### 🎯 Scenario Settings")
    
    scenario_name = st.text_input("Scenario Name", value="My Custom Scenario")
    scenario_desc = st.text_area("Description", value="A custom multi-agent simulation scenario")
    
    # World Settings
    st.markdown("#### 🌍 World Settings")
    
    world_col1, world_col2 = st.columns(2)
    with world_col1:
        world_size = st.select_slider("World Size", options=["Small", "Medium", "Large"], value="Medium")
        tick_rate = st.number_input("Tick Rate (ms)", min_value=100, max_value=5000, value=1000)
    
    with world_col2:
        max_ticks = st.number_input("Max Ticks", min_value=100, max_value=10000, value=1000)
        random_seed = st.number_input("Random Seed", min_value=0, max_value=9999, value=42)
    
    # Agent Settings
    st.markdown("#### 👥 Agent Population")
    
    agent_counts = {}
    for layer_id in range(1, 5):
        layer_info = LAYER_NAMES[layer_id]
        agent_counts[layer_id] = st.slider(
            f"{layer_info['icon']} Layer {layer_id}: {layer_info['name_en']}",
            min_value=1,
            max_value=50,
            value=[8, 15, 30, 10][layer_id-1],
            key=f"layer_{layer_id}_count"
        )
    
    # Cost Settings
    st.markdown("#### 💰 Cost Controls")
    
    cost_col1, cost_col2 = st.columns(2)
    with cost_col1:
        daily_budget = st.number_input("Daily Budget (USD)", min_value=1.0, max_value=1000.0, value=50.0)
        token_limit = st.number_input("Token Limit", min_value=10000, max_value=1000000, value=200000)
    
    with cost_col2:
        optimization_mode = st.selectbox("Optimization Mode", ["Balanced", "Aggressive", "Conservative"])
        cache_enabled = st.toggle("Enable Cache", value=True)

with config_col2:
    st.markdown("### 📝 YAML Configuration")
    
    # Generate YAML config
    config = {
        "scenario": {
            "name": scenario_name,
            "description": scenario_desc,
            "version": "1.0"
        },
        "world": {
            "size": world_size.lower(),
            "tick_rate_ms": tick_rate,
            "max_ticks": max_ticks,
            "random_seed": random_seed
        },
        "agents": {
            "layer1": {"count": agent_counts[1], "type": "key_decision_makers"},
            "layer2": {"count": agent_counts[2], "type": "organizations"},
            "layer3": {"count": agent_counts[3], "type": "groups_tribes"},
            "layer4": {"count": agent_counts[4], "type": "statistical_population"}
        },
        "cost": {
            "daily_budget_usd": daily_budget,
            "token_limit": token_limit,
            "optimization_mode": optimization_mode.lower(),
            "cache_enabled": cache_enabled
        },
        "memory": {
            "working_memory_size": 7,
            "short_term_ttl_minutes": 60,
            "long_term_enabled": True,
            "deduplication": True
        }
    }
    
    yaml_output = yaml.dump(config, default_flow_style=False, allow_unicode=True)
    
    # Editable YAML
    edited_yaml = st.text_area(
        "Edit YAML",
        value=yaml_output,
        height=500,
        key="yaml_editor"
    )
    
    # Validate YAML
    try:
        parsed_config = yaml.safe_load(edited_yaml)
        st.success("✅ Valid YAML configuration")
    except yaml.YAMLError as e:
        st.error(f"❌ Invalid YAML: {e}")

st.markdown("---")

# ===== EXPORT/IMPORT =====
st.markdown("### 💾 Export & Import")

export_col1, export_col2, export_col3, export_col4 = st.columns(4)

with export_col1:
    if st.button("📥 Export YAML", use_container_width=True):
        st.download_button(
            label="Download YAML",
            data=edited_yaml,
            file_name=f"{scenario_name.lower().replace(' ', '_')}.yaml",
            mime="text/yaml"
        )

with export_col2:
    if st.button("📥 Export JSON", use_container_width=True):
        json_output = json.dumps(config, indent=2, ensure_ascii=False)
        st.download_button(
            label="Download JSON",
            data=json_output,
            file_name=f"{scenario_name.lower().replace(' ', '_')}.json",
            mime="application/json"
        )

with export_col3:
    uploaded_file = st.file_uploader("📤 Import Config", type=['yaml', 'yml', 'json'])
    if uploaded_file:
        st.success(f"Loaded: {uploaded_file.name}")

with export_col4:
    if st.button("🚀 Launch Scenario", use_container_width=True, type="primary"):
        st.balloons()
        st.success(f"Scenario '{scenario_name}' launched!")

st.markdown("---")

# ===== SCENARIO PREVIEW =====
st.markdown("### 👁️ Scenario Preview")

preview_col1, preview_col2, preview_col3 = st.columns(3)

with preview_col1:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>TOTAL AGENTS</div>
<div style='font-size:2rem;font-weight:bold;color:#00ff88;'>{sum(agent_counts.values())}</div>
</div>
""", unsafe_allow_html=True)

with preview_col2:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>ESTIMATED RUNTIME</div>
<div style='font-size:2rem;font-weight:bold;color:#00d4ff;'>{max_ticks * tick_rate // 1000}s</div>
</div>
""", unsafe_allow_html=True)

with preview_col3:
    st.markdown(f"""
<div class='stat-card'>
<div style='color:#8892a4;font-size:0.8rem;'>ESTIMATED COST</div>
<div style='font-size:2rem;font-weight:bold;color:#ffcc00;'>${daily_budget:.2f}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===== EXAMPLE SCENARIOS =====
st.markdown("### 📚 Example Scenarios Library")

example_col1, example_col2 = st.columns(2)

with example_col1:
    st.markdown("""
<div class='stat-card'>
<div style='font-size:1.2rem;font-weight:bold;color:#00ff88;margin-bottom:1rem;'>
📈 Example: Bull World Rally
</div>
<pre style='background:#0a0e17;padding:1rem;border-radius:8px;overflow-x:auto;font-size:0.8rem;'>
scenario:
name: Bull World Rally
description: Simulate bullish world conditions
agents:
layer1: {count: 5, mood: greedy}
layer2: {count: 10, mood: bullish}
layer3: {count: 25, mood: bullish}
layer4: {count: 8, mood: neutral}
world:
initial_trend: bullish
volatility: low
momentum: strong
</pre>
</div>
""", unsafe_allow_html=True)

with example_col2:
    st.markdown("""
<div class='stat-card'>
<div style='font-size:1.2rem;font-weight:bold;color:#ff0055;margin-bottom:1rem;'>
📉 Example: World Crash Simulation
</div>
<pre style='background:#0a0e17;padding:1rem;border-radius:8px;overflow-x:auto;font-size:0.8rem;'>
scenario:
name: World Crash
description: Simulate panic selling cascade
agents:
layer1: {count: 5, mood: fearful}
layer2: {count: 10, mood: bearish}
layer3: {count: 30, mood: fearful}
layer4: {count: 10, mood: bearish}
world:
initial_trend: bearish
volatility: high
panic_threshold: 0.3
</pre>
</div>
""", unsafe_allow_html=True)

# More examples
example_col3, example_col4 = st.columns(2)

with example_col3:
    st.markdown("""
<div class='stat-card'>
<div style='font-size:1.2rem;font-weight:bold;color:#00d4ff;margin-bottom:1rem;'>
🗳️ Example: Election Simulation
</div>
<pre style='background:#0a0e17;padding:1rem;border-radius:8px;overflow-x:auto;font-size:0.8rem;'>
scenario:
name: Presidential Election
description: Opinion formation dynamics
agents:
layer1: {count: 10, type: candidates}
layer2: {count: 20, type: media_outlets}
layer3: {count: 50, type: voter_groups}
layer4: {count: 100, type: individual_voters}
opinion:
influence_decay: 0.9
swing_threshold: 0.15
</pre>
</div>
""", unsafe_allow_html=True)

with example_col4:
    st.markdown("""
<div class='stat-card'>
<div style='font-size:1.2rem;font-weight:bold;color:#b400ff;margin-bottom:1rem;'>
🦠 Example: Pandemic Spread
</div>
<pre style='background:#0a0e17;padding:1rem;border-radius:8px;overflow-x:auto;font-size:0.8rem;'>
scenario:
name: Pandemic Spread
description: Disease transmission model
agents:
layer1: {count: 5, type: health_officials}
layer2: {count: 15, type: institutions}
layer3: {count: 40, type: communities}
layer4: {count: 200, type: individuals}
disease:
r0: 2.5
incubation_days: 5
mortality_rate: 0.02
</pre>
</div>
""", unsafe_allow_html=True)