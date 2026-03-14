import textwrap
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random
from datetime import datetime, timedelta
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.demo_data import AGENTS, LAYER_NAMES, MOODS, ACTIONS

st.set_page_config(page_title="Dialogue", page_icon="Chat", layout="wide")
st.markdown("# Agent Dialogue Console")
st.markdown("*Real-time agent conversations visualization*")

with st.sidebar:
    st.markdown("## Controls")
    auto_refresh = st.toggle("Auto Refresh", value=True)
    time_range = st.select_slider("Time Range", options=["5min","15min","30min","1hr","All"], value="30min")

def gen_dialogues():
    dialogs = []
    flows = [("L1->L2","Order"), ("L2->L3","Dispatch"), ("L3->L3","Collab"), ("L4->L3","Report"), ("System","Event")]
    msgs = ["Analyze world conditions", "Activate contingency plan", "Collect world data", "Scan sentiment", "Data collection complete", "Volatility detected", "Processing complete 94%", "3 patterns found", "Model updated", "Cost savings 73%"]
    base = datetime.now()
    for i in range(40):
        f, t = random.choice(flows)
        a = random.choice(AGENTS)
        dialogs.append({'ts': base-timedelta(minutes=random.randint(0,120)), 'flow':f, 'type':t, 'agent':a, 'layer':a['layer'], 'mood':random.choice(list(MOODS.keys())), 'msg':random.choice(msgs), 'tokens':random.randint(50,500), 'conf':random.uniform(0.7,0.99)})
    dialogs.sort(key=lambda x: x['ts'], reverse=True)
    return dialogs

dialogues = gen_dialogues()

c1,c2,c3,c4 = st.columns(4)
with c1: st.metric("Messages", len(dialogues))
with c2: st.metric("Avg Conf", f"{sum(d['conf'] for d in dialogues)/len(dialogues):.1%}")
with c3: st.metric("Tokens", f"{sum(d['tokens'] for d in dialogues):,}")
with c4: st.metric("Active", len(set(d['agent']['id'] for d in dialogues[:20])))

st.markdown("---")
t1,t2,t3 = st.tabs(["Live Chat", "Flow Analysis", "Search"])

with t1:
    st.markdown("### Live Feed")
    for d in dialogues[:20]:
        a = d['agent']
        icon = LAYER_NAMES[a['layer']]['icon']
        st.markdown(f"<div style='padding:10px;margin:5px;background:#161b22;border-radius:8px;border-left:3px solid {LAYER_NAMES[d['layer']]['color']}'><b style='color:{LAYER_NAMES[d['layer']]['color']}'>{icon} {a['name']}</b><br>{d['msg']}<br><small style='color:#8b949e'>{d['ts'].strftime('%H:%M')} | {d['flow']} | {d['tokens']}t</small></div>", unsafe_allow_html=True)

with t2:
    st.markdown("### Analysis")
    tc = {}
    for d in dialogues: tc[d['type']] = tc.get(d['type'], 0) + 1
    fig = go.Figure(data=[go.Pie(labels=list(tc.keys()), values=list(tc.values()), hole=0.4)])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e0e6ed'), height=350)
    st.plotly_chart(fig, use_container_width=True)
    fc = {}
    for d in dialogues: fc[d['flow']] = fc.get(d['flow'], 0) + 1
    fig2 = go.Figure(data=[go.Bar(x=list(fc.keys()), y=list(fc.values()))])
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e0e6ed'), height=350)
    st.plotly_chart(fig2, use_container_width=True)

with t3:
    st.markdown("### Search")
    q = st.text_input("Search messages...")
    if q:
        res = [d for d in dialogues if q.lower() in d['msg'].lower()]
        st.markdown(f"Found {len(res)} results")
        for r in res[:10]:
            icon = LAYER_NAMES[r['agent']['layer']]['icon']
            st.markdown(f"{icon} **{r['agent']['name']}** | {r['ts'].strftime('%Y-%m-%d %H:%M')}\n> {r['msg']}")
    else:
        st.info("Enter keywords to search")
