import streamlit as st
import json
import pandas as pd
from core.ui_utils import load_css, stat_card

st.set_page_config(page_title="Simulation Replay", page_icon="⏪", layout="wide")
load_css()

st.title("⏪ Simulation Replay & Analysis")
st.caption("Temporal inspection of world states and agent macro-behaviors over the entire simulation epoch.")

if "engine" not in st.session_state or not st.session_state.engine:
    st.info("No active simulation engine found. Please run a scenario in the main dashboard first.")
    st.stop()
    
history = st.session_state.engine.history

if not history:
    st.warning("The simulation hasn't generated any history yet. Press START on the main dashboard to advance time.")
    st.stop()

# --- Timeline Controls ---
max_step = len(history) - 1
selected_idx = st.slider("🕰️ Time Slider (Simulated Ticks)", min_value=0, max_value=max_step, value=max_step)

current_step_data = history[selected_idx]

st.markdown("---")

col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
with col_kpi1:
    st.markdown(stat_card("Tick Number", str(current_step_data.get("step", selected_idx)), "var(--primary)"), unsafe_allow_html=True)
with col_kpi2:
    st.markdown(stat_card("Agent Actions", str(len(current_step_data.get("actions", []))), "var(--success)"), unsafe_allow_html=True)
with col_kpi3:
    st.markdown(stat_card("Compute Time", f"{current_step_data.get('elapsed_seconds', 0)}s", "var(--warning)"), unsafe_allow_html=True)

st.markdown("---")

# --- World State Snapshot ---
st.subheader("🌍 World Event (Game Master Narrative)")
gm_update = current_step_data.get("gm_update", "No narrative data.")
if isinstance(gm_update, dict):
    st.info(gm_update.get("narrative", gm_update.get("narrative_summary", str(gm_update))))
elif isinstance(gm_update, str):
    st.info(gm_update)

col_world, col_action = st.columns([1, 1.5])

with col_world:
    st.subheader("📊 Macro State Snapshot")
    snapshot = current_step_data.get("world_state_snapshot", {})
    if snapshot:
        # Display as a pretty JSON tree
        st.json(snapshot, expanded=False)
    else:
        st.write("No granular world state captured at this tick.")

with col_action:
    st.subheader("🕵️ Agent Event Log")
    actions = current_step_data.get("actions", [])
    if actions:
        df = pd.DataFrame(actions)
        # Assuming df has 'agent' and 'result'
        st.dataframe(df, use_container_width=True, height=400)
    else:
        st.write("No agent actions recorded.")
        
# --- Statistical Crowd ---
crowd_stats = current_step_data.get("crowd_stats")
if crowd_stats:
    st.markdown("---")
    st.subheader("👥 Statistical Matrix Population (100,000+ Background Agents)")
    st.caption("Distribution of collective behaviors simulated via vector tensors.")
    
    st_cols = st.columns(len(crowd_stats))
    for i, (trait, dist) in enumerate(crowd_stats.items()):
        with st_cols[i % len(st_cols)]:
            st.write(f"**{trait}**")
            # Create a rapid horizontal bar or metric list
            for key, val in dist.items():
                st.metric(key, f"{val*100:.1f}%")
