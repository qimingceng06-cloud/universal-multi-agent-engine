"""
Universal Engine Dashboard - Clean Professional Edition
"""
import streamlit as st
import asyncio
import os
import yaml
import json
import random
from datetime import datetime
import agentscope

from config.model_config import get_model_configs
from core.model_router import ModelRouter
from core.memory_manager import MemoryManager
from core.context_cache import ContextCacheManager
from core.semantic_cache import SemanticCache
from core.async_gateway import AsyncLLMGateway
from core.agent_factory import AgentFactory
from core.world_engine import WorldEngine

from core.demo_data import (
    AGENTS, WORLD_OVERVIEW, EVENTS, LAYER_NAMES, MOODS
)

from core.ui_utils import (
    load_css, pro_header, status_bar, ticker_bar,
    stat_card, gauge_chart, status_dot, status_light_bar, corner_badge,
    TYPE_COLORS, section_header, event_card
)

# ===== PAGE CONFIG =====
st.set_page_config(page_title="Universal Engine Control", layout="wide")
load_css()

# ===== SESSION STATE INIT =====
if "sim_running" not in st.session_state:
    st.session_state.sim_running = False
if "sim_tick" not in st.session_state:
    st.session_state.sim_tick = 0
if "engine" not in st.session_state:
    st.session_state.engine = None
if "live_events" not in st.session_state:
    st.session_state.live_events = []
if "ui_agents" not in st.session_state:
    st.session_state.ui_agents = []
if "cost_data" not in st.session_state:
    st.session_state.cost_data = {"total_estimated_cost": "$0.00", "tokens": 0}

async def init_engine(provider, api_key, scenario):
    tiers, as_configs = get_model_configs(provider, api_key)
    agentscope.init(project="UniversalSim")
    
    router = ModelRouter(tiers)
    gateway = AsyncLLMGateway(api_key, max_concurrent=5)
    
    comp_model_id = tiers["tier3_lite"].litellm_id
    memory_mgr = MemoryManager(gateway, comp_model_id)
    cache_mgr = ContextCacheManager(api_key=api_key)
    
    factory = AgentFactory(memory_mgr)
    agents = factory.build_from_scenario(f"scenarios/{scenario}")
    
    engine = WorldEngine(router, memory_mgr, cache_mgr, gateway)
    with open(f"scenarios/{scenario}/world.yaml", "r", encoding="utf-8") as f:
        world_config = yaml.safe_load(f)
    await engine.initialize(agents, world_config)
    
    # Init UI Agents
    ui_agents = []
    if "game_master" in agents:
        ui_agents.append({"id": "GM", "name": "Game Master", "layer": 1, "action": "WAIT", "confidence": 0.95, "influence": 1.0, "personality": "System", "mood": "neutral"})
    for a in agents.get("llm_agents", []):
        ui_agents.append({"id": a.agent_id, "name": a.name, "layer": 2, "action": "WAIT", "confidence": 0.8, "influence": 0.7, "personality": getattr(a, "personality", "Neutral"), "mood": "neutral"})
    for a in agents.get("template_agents", [])[:15]:
        ui_agents.append({"id": a.agent_id, "name": getattr(a, "name", a.agent_id), "layer": random.choice([3,4]), "action": "WAIT", "confidence": 0.5, "influence": 0.3, "personality": "Standard", "mood": "neutral"})
        
    st.session_state.ui_agents = ui_agents
    return engine

async def run_step():
    res = await st.session_state.engine.step()
    st.session_state.sim_tick = res["step"]
    
    now_str = datetime.now().strftime("%H:%M:%S")
    for action in res.get("actions", []):
        etype = "thought" if "think" in action["result"].lower() or "{" in action["result"] else "interaction"
        st.session_state.live_events.insert(0, {
            "type": etype,
            "timestamp": now_str,
            "description": f"{action['agent']}: {action['result'][:80]}...",
            "agent": action["agent"]
        })
        for ui_a in st.session_state.ui_agents:
            if ui_a["name"] == action["agent"] or ui_a["id"] == action["agent"]:
                ui_a["action"] = "ACTING"
                ui_a["confidence"] = min(1.0, random.uniform(0.6, 0.99))
                
    st.session_state.live_events = st.session_state.live_events[:20]
    return res

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("<div style='text-align:center;padding:0.5rem 0;'><div style='font-size:1.2rem;font-weight:700;color:var(--text-primary);letter-spacing:1px;'>CONTROL CENTER</div></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    provider = st.selectbox("LLM Provider", ["Google", "OpenAI", "DeepSeek", "Ollama"])
    api_key = st.text_input("API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    
    scenario_type = st.radio("Scenario Type", ["Preset", "Custom"], horizontal=True)
    
    if scenario_type == "Preset":
        scenarios = [d for d in os.listdir("scenarios") if os.path.isdir(os.path.join("scenarios", d)) and d != "custom"]
        scenario_option = st.selectbox("Scenario", scenarios if scenarios else ["medieval_town"])
        custom_name = ""
        custom_desc = ""
        custom_era = ""
    else:
        scenario_option = "custom"
        custom_name = st.text_input("Name", value="Mars Colony Survival")
        custom_desc = st.text_area("Description", value="Settlers resolving psychological stress on Mars.")
        custom_era = st.text_input("Era", value="2050")
    
    st.markdown("---")
    sim_status = "ONLINE" if st.session_state.sim_running else "PAUSED"
    dot_color = "online" if st.session_state.sim_running else "warning"
    st.markdown(f"{status_dot(dot_color)} **Status:** {sim_status}", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶ START", use_container_width=True) and not st.session_state.sim_running:
            if not st.session_state.engine:
                if not api_key:
                    st.error("API Key Required")
                else:
                    if scenario_option == "custom":
                        os.makedirs("scenarios/custom", exist_ok=True)
                        with open("scenarios/custom/world.yaml", "w", encoding="utf-8") as f:
                            yaml.dump({"name": custom_name, "description": custom_desc, "era": custom_era}, f, allow_unicode=True)
                        with open("scenarios/custom/npcs.yaml", "w", encoding="utf-8") as f:
                            yaml.dump({
                                "llm_agents": [
                                    {"id": "agent_alpha", "name": "Alpha Observer", "role": "core_npc", "importance": 0.9, "personality": "Analytical, Strategic", "goals": "Objective Analysis", "description": "Primary scenario observer."},
                                    {"id": "agent_beta", "name": "Beta Participant", "role": "core_npc", "importance": 0.7, "personality": "Reactive, Emotional", "goals": "Survive and Prosper", "description": "Secondary actor representing public sentiment."}
                                ],
                                "template_agents": {"archetypes": [{"type": "generic_actor", "count": 20}]},
                                "statistical_crowd": {"demographics": {"general_population": 500}, "model": "simple"}
                            }, f, allow_unicode=True)
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    st.session_state.engine = loop.run_until_complete(init_engine(provider, api_key, scenario_option))
            st.session_state.sim_running = True
            st.rerun()
    with col2:
        if st.button("⏸ PAUSE", use_container_width=True):
            st.session_state.sim_running = False
            st.rerun()
            
    if st.button("↻ RESET", use_container_width=True):
        st.session_state.engine = None
        st.session_state.sim_tick = 0
        st.session_state.sim_running = False
        st.session_state.live_events = []
        st.session_state.ui_agents = []
        st.rerun()

# Run Engine if Active
if st.session_state.sim_running and st.session_state.engine:
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        step_res = loop.run_until_complete(run_step())
        report = st.session_state.engine.router.get_usage_report()
        st.session_state.cost_data["total_estimated_cost"] = report.pop("total_estimated_cost", "$0.00")
        st.session_state.cost_data["tokens"] = sum(v for k,v in report.items() if isinstance(v, int))
    except Exception as e:
        st.error(f"⚠️ Simulation Step Failed: {str(e)}")
        st.session_state.sim_running = False
        if "Authentication" in str(e) or "API Key" in str(e):
            st.warning("Please check your GEMINI_API_KEY in the sidebar or .env file.")

# Dynamic Fallback to Demo Data or Real Data
engine_active = st.session_state.engine is not None

if engine_active:
    engine = st.session_state.engine
    cnt = 1 # Game master
    cnt += len(engine.agents.get("llm_agents", []))
    cnt += len(engine.agents.get("template_agents", []))
    if engine.agents.get("statistical_crowd"):
        # The crowd represents the massive backdrop population
        cnt += 100000
    active_agents = cnt
else:
    active_agents = WORLD_OVERVIEW["active_agents"]

cost_display = st.session_state.cost_data["total_estimated_cost"] if engine_active else "$0.00"

if scenario_option == "custom":
    scenario_meta = {
        "name": custom_name,
        "description": custom_desc,
        "era": custom_era
    }
else:
    scenario_meta = {"name": scenario_option.upper(), "description": "No description provided for this scenario.", "era": "Simulation"}
    try:
        with open(f"scenarios/{scenario_option}/world.yaml", "r", encoding="utf-8") as f:
            meta = yaml.safe_load(f)
            if meta:
                scenario_meta["name"] = meta.get("name", scenario_meta["name"])
                scenario_meta["description"] = meta.get("description", scenario_meta["description"])
                scenario_meta["era"] = meta.get("era", scenario_meta["era"])
    except Exception:
        pass

# ===== TICKER BAR =====
ticker_symbols = [
    {"symbol": "SCENARIO", "price": scenario_option.upper(), "change_pct": 0},
    {"symbol": "STEP", "price": str(st.session_state.sim_tick) if engine_active else "0", "change_pct": 1.0},
    {"symbol": "COST", "price": cost_display, "change_pct": 0},
    {"symbol": "AGENTS", "price": str(active_agents), "change_pct": 0},
    {"symbol": "PROVIDER", "price": provider, "change_pct": 0},
    {"symbol": "SCORE", "price": f"{WORLD_OVERVIEW['global_score']:,.0f}", "change_pct": 1.23},
]
st.markdown(ticker_bar(ticker_symbols), unsafe_allow_html=True)

# ===== HEADER =====
st.markdown(pro_header("UNIVERSAL AGENT DASHBOARD", f"Active Scenario: {scenario_meta['name']}"), unsafe_allow_html=True)

st.markdown(f"<div style='background:var(--bg-card);border-left:4px solid var(--primary);padding:1.5rem;margin:1rem 0;border-radius:0 8px 8px 0;box-shadow:0 1px 3px rgba(0,0,0,0.05);'><div style='font-size:1.1rem;font-weight:600;color:var(--text-primary);margin-bottom:0.5rem;'>📖 Scenario Overview: {scenario_meta['name']} <span style='font-size:0.8rem;color:var(--text-secondary);font-weight:400;'>| Era: {scenario_meta['era']}</span></div><div style='color:var(--text-secondary);font-size:0.95rem;line-height:1.6;'>{scenario_meta['description']}</div></div>", unsafe_allow_html=True)

# ===== SYSTEM STATUS BAR =====
world_time = st.session_state.engine.world_state.get('time', 'Init') if engine_active else 'N/A'
st.markdown(status_bar([
    {"label": "SYSTEM", "value": "OPERATIONAL" if st.session_state.sim_running else "IDLE", "status": "online" if st.session_state.sim_running else "warning"},
    {"label": "TICK", "value": f"#{st.session_state.sim_tick}", "status": "processing" if st.session_state.sim_running else "warning"},
    {"label": "WORLD TIME", "value": str(world_time), "status": "online"},
    {"label": "AGENTS", "value": str(active_agents), "status": "online"},
    {"label": "COST", "value": cost_display, "status": "online"}
]), unsafe_allow_html=True)

# ===== KPI ROW =====
kpi_cols = st.columns(5)
with kpi_cols[0]:
    st.markdown(stat_card("Total Agents", str(active_agents), "var(--primary)"), unsafe_allow_html=True)
with kpi_cols[1]:
    active_action = sum(1 for a in st.session_state.ui_agents if a["action"] == "ACTING") if engine_active else sum(1 for a in AGENTS if a['action'] in ['ACT','OBSERVE'])
    st.markdown(stat_card("Active Actions", str(active_action), "var(--success)"), unsafe_allow_html=True)
with kpi_cols[2]:
    # UI Confidence logic based only on the tracked UI agents to avoid zeroing out from total population
    ui_len = len(st.session_state.ui_agents) if (engine_active and st.session_state.ui_agents) else 1
    conf = sum(a['confidence'] for a in st.session_state.ui_agents)/ui_len if engine_active else WORLD_OVERVIEW['avg_confidence']
    st.markdown(stat_card("Avg Confidence", f"{conf:.2f}", "var(--secondary)"), unsafe_allow_html=True)
with kpi_cols[3]:
    st.markdown(stat_card("Session Events", str(len(st.session_state.live_events) if engine_active else 0), "var(--purple)"), unsafe_allow_html=True)
with kpi_cols[4]:
    st.markdown(stat_card("Session Cost", cost_display, "var(--danger)"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===== LAYER OVERVIEW =====
st.markdown(section_header("🏛️", "LAYER OVERVIEW"), unsafe_allow_html=True)
layer_cols = st.columns(4)
for idx, (layer_id, layer_info) in enumerate(LAYER_NAMES.items()):
    agents_in_layer = [a for a in st.session_state.ui_agents if a["layer"] == layer_id] if engine_active else [a for a in AGENTS if a["layer"] == layer_id]
    with layer_cols[idx]:
        avg_conf = sum(a["confidence"] for a in agents_in_layer) / max(len(agents_in_layer), 1)
        active_lights = ["green" if getattr(a, "confidence", 0.5) > 0.6 else "yellow" for a in agents_in_layer[:5]]
        st.markdown(f"<div class='stat-card' style='border-left:4px solid {layer_info['color']};'>{corner_badge(f'L{layer_id}')}<div style='display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;'><span style='font-size:1.5rem;'>{layer_info['icon']}</span><div><div style='font-weight:600;color:var(--text-primary);font-size:0.95rem;'>{layer_info['name_en']}</div><div style='font-size:0.75rem;color:var(--text-secondary);'>{len(agents_in_layer)} agents</div></div></div><div style='margin-top:1rem;'><div style='display:flex;justify-content:space-between;font-size:0.75rem;color:var(--text-secondary);margin-bottom:4px;font-weight:500;'><span>CONFIDENCE</span><span>{avg_conf:.0%}</span></div><div class='stat-bar'><div class='stat-bar-fill confidence' style='width:{avg_conf*100:.0f}%;background:{layer_info['color']};'></div></div></div>{status_light_bar(active_lights, 5)}</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===== LIVE FEED & TOP AGENTS =====
feed_col, agents_col = st.columns([1, 1])

with feed_col:
    st.markdown(section_header("📡", "LIVE EVENT FEED"), unsafe_allow_html=True)
    events_to_show = st.session_state.live_events if engine_active else EVENTS
    if not events_to_show:
        st.markdown("<div style='color:var(--text-dim);text-align:center;padding:2rem;'>AWAITING SIMULATION START...</div>", unsafe_allow_html=True)
    for event in events_to_show[:6]:
        color = TYPE_COLORS.get(event["type"], "var(--text-dim)")
        st.markdown(event_card(event["type"].upper(), event["timestamp"], event["description"], color), unsafe_allow_html=True)

with agents_col:
    st.markdown(section_header("🏆", "CORE AGENTS STATUS"), unsafe_allow_html=True)
    agents_to_show = sorted(st.session_state.ui_agents, key=lambda x: x["influence"], reverse=True)[:5] if engine_active else sorted(AGENTS, key=lambda x: x["influence"], reverse=True)[:5]
    if not agents_to_show:
        st.markdown("<div style='color:var(--text-dim);text-align:center;padding:2rem;'>AWAITING ENGINE INIT...</div>", unsafe_allow_html=True)
    
    for agent in agents_to_show:
        layer_color = LAYER_NAMES.get(agent["layer"], {}).get("color", "var(--border-subtle)")
        st.markdown(f"<div class='agent-card' style='border-left:4px solid {layer_color};'><div style='display:flex;justify-content:space-between;align-items:center;'><div><div style='font-weight:600;color:var(--text-primary);font-size:0.95rem;'>{agent['name']}</div><div style='font-size:0.8rem;color:var(--text-secondary);'>{agent.get('personality', 'Standard')}</div></div></div><div style='margin-top:1rem;display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.75rem;font-size:0.8rem;'><div style='text-align:center;padding:0.5rem;background:var(--bg-page);border-radius:6px;border:1px solid var(--border-subtle);'><div style='color:var(--text-secondary);font-size:0.65rem;font-weight:600;'>INFLUENCE</div><div style='color:var(--text-primary);font-weight:700;'>{agent['influence']:.2f}</div></div><div style='text-align:center;padding:0.5rem;background:var(--bg-page);border-radius:6px;border:1px solid var(--border-subtle);'><div style='color:var(--text-secondary);font-size:0.65rem;font-weight:600;'>CONFIDENCE</div><div style='color:var(--text-primary);font-weight:700;'>{agent['confidence']:.0%}</div></div><div style='text-align:center;padding:0.5rem;background:var(--success-light);border-radius:6px;border:1px solid rgba(16,185,129,0.2);'><div style='color:var(--success);font-size:0.65rem;font-weight:600;'>ACTION</div><div style='color:var(--success);font-weight:700;'>{agent.get('action', 'WAIT')}</div></div></div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===== SYSTEM INDICATORS =====
st.markdown(section_header("📊", "SYSTEM INDICATORS"), unsafe_allow_html=True)
gauge_cols = st.columns(4)
with gauge_cols[0]:
    st.plotly_chart(gauge_chart(WORLD_OVERVIEW["system_tension"], "System Tension", 100, "", size=200), use_container_width=True)
with gauge_cols[1]:
    ui_len = len(st.session_state.ui_agents) if (engine_active and st.session_state.ui_agents) else 1
    c_val = sum(a['confidence'] for a in st.session_state.ui_agents)/ui_len if engine_active else WORLD_OVERVIEW["avg_confidence"]
    st.plotly_chart(gauge_chart(c_val*100, "Avg Confidence", 100, "%", size=200), use_container_width=True)
with gauge_cols[2]:
    active_ratio = 50.0  # Placeholder for normal logic
    st.plotly_chart(gauge_chart(active_ratio, "Active/Idle Ratio", 100, "%", size=200), use_container_width=True)
with gauge_cols[3]:
    st.plotly_chart(gauge_chart(WORLD_OVERVIEW["token_budget_remaining"]*100, "Token Budget", 100, "%", size=200), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===== QUICK NAVIGATION =====
st.markdown(section_header("🗺️", "QUICK NAVIGATION"), unsafe_allow_html=True)
nav_cols = st.columns(6)
page_map = {
    "Agents": "pages/1_Agent_Roster.py",
    "Analytics": "pages/2_Cost_Analytics.py",
    "Replay": "pages/3_Replay_Analysis.py",
}
nav_icons = {"Agents": "👤", "Analytics": "📊", "Replay": "⏮"}

for idx, (name, path) in enumerate(page_map.items()):
    with nav_cols[idx]:
        if st.button(f"{nav_icons.get(name, '◈')} {name}", key=f"nav_{name}", use_container_width=True):
            try:
                st.switch_page(path)
            except Exception as e:
                st.error("Page not found")

# Footer
st.markdown("---")
st.markdown("<div style='text-align:center;padding:1rem 0;color:var(--text-dim);font-size:0.8rem;font-weight:500;'><span>Universal Agent Dashboard v3.0</span> &nbsp;|&nbsp;<span>4-Layer Architecture</span> &nbsp;|&nbsp;<span>All Systems Operational</span></div>", unsafe_allow_html=True)

if st.session_state.sim_running:
    import time
    time.sleep(1)
    st.rerun()
