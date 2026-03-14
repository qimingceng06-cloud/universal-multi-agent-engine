import textwrap
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random
from datetime import datetime, timedelta
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.demo_data import AGENTS, LAYER_NAMES, MOODS

st.set_page_config(page_title="Conversations", page_icon="Log", layout="wide")
st.markdown("# Conversation History")
st.markdown("*Full conversation log with agent decision threads*")

with st.sidebar:
    st.markdown("## Filters")
    date_range = st.date_input("Date Range", value=(datetime.now()-timedelta(days=7), datetime.now()))
    agent_filter = st.multiselect("Agents", [f"{LAYER_NAMES[a['layer']]['icon']} {a['name']}" for a in AGENTS[:10]])
    min_conf = st.slider("Min Confidence", 0.0, 1.0, 0.7)

def gen_conversations():
    convos = []
    topics = ["World volatility", "Risk assessment", "Sentiment tracking", "Portfolio rebalance", "Anomaly detection", "Pattern recognition", "Cost optimization", "Model training", "Data pipeline", "Alert thresholds"]
    base = datetime.now()
    for i in range(25):
        topic = random.choice(topics)
        msgs = []
        n = random.randint(3, 6)
        ct = base - timedelta(hours=random.randint(1, 168))
        for j in range(n):
            ag = random.choice(AGENTS)
            tmpl = [f"Analyzing {topic.lower()}", f"Results: {random.randint(60,99)}% confidence", f"Requesting data for {topic.lower()}", f"Recommendation: adjust thresholds", f"Alert: unexpected pattern"]
            msgs.append({'agent': ag, 'ts': ct+timedelta(minutes=j*random.randint(1,5)), 'content': random.choice(tmpl), 'tokens': random.randint(50,300), 'conf': random.uniform(0.6,0.99)})
        convos.append({'id': f'conv_{i:04d}', 'topic': topic, 'started': ct, 'msgs': msgs, 'participants': list(set(m['agent']['id'] for m in msgs)), 'total_tokens': sum(m['tokens'] for m in msgs), 'avg_conf': sum(m['conf'] for m in msgs)/len(msgs)})
    convos.sort(key=lambda x: x['started'], reverse=True)
    return convos

conversations = gen_conversations()

c1,c2,c3,c4 = st.columns(4)
with c1: st.metric("Conversations", len(conversations))
with c2: st.metric("Messages", sum(len(c['msgs']) for c in conversations))
with c3: st.metric("Tokens", f"{sum(c['total_tokens'] for c in conversations):,}")
with c4: st.metric("Avg Conf", f"{sum(c['avg_conf'] for c in conversations)/len(conversations):.1%}")

st.markdown("---")
t1,t2,t3 = st.tabs(["Conversation List", "Thread View", "Analytics"])

with t1:
    st.markdown("### Recent Conversations")
    for c in conversations[:12]:
        with st.expander(f"{c['topic']} - {c['started'].strftime('%Y-%m-%d %H:%M')} ({len(c['msgs'])} msgs)"):
            ca,cb,cc = st.columns(3)
            with ca: st.markdown(f"**Participants:** {len(c['participants'])}")
            with cb: st.markdown(f"**Tokens:** {c['total_tokens']:,}")
            with cc: st.markdown(f"**Confidence:** {c['avg_conf']:.1%}")
            for m in c['msgs']:
                ag = m['agent']
                icon = LAYER_NAMES[ag['layer']]['icon']
                st.markdown(f"<div style='padding:8px;margin:4px;background:#161b22;border-radius:8px;border-left:3px solid {LAYER_NAMES[ag['layer']]['color']}'><b style='color:{LAYER_NAMES[ag['layer']]['color']}'>{icon} {ag['name']}</b> | {m['ts'].strftime('%H:%M')}<br>{m['content']}<br><small style='color:#8b949e'>Conf: {m['conf']:.1%} | Tokens: {m['tokens']}</small></div>", unsafe_allow_html=True)

with t2:
    st.markdown("### Thread View")
    sel = st.selectbox("Select Conversation", [f"{c['topic']} ({c['started'].strftime('%m-%d %H:%M')})" for c in conversations[:15]])
    if sel:
        idx = [f"{c['topic']} ({c['started'].strftime('%m-%d %H:%M')})" for c in conversations[:15]].index(sel)
        c = conversations[idx]
        for m in c['msgs']:
            ag = m['agent']
            icon = LAYER_NAMES[ag['layer']]['icon']
            st.chat_message("assistant").markdown(f"**{icon} {ag['name']}**: {m['content']}")

with t3:
    st.markdown("### Analytics")
    tc = {}
    for c in conversations: tc[c['topic']] = tc.get(c['topic'], 0) + 1
    fig = go.Figure(data=[go.Bar(x=list(tc.keys()), y=list(tc.values()), marker_color='#00ff88')])
    fig.update_layout(title="By Topic", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#e0e6ed'), height=400)
    st.plotly_chart(fig, use_container_width=True)
    td = pd.DataFrame([{'date': c['started'].date(), 'count': 1} for c in conversations]).groupby('date').sum().reset_index()
    fig2 = go.Figure(data=[go.Scatter(x=td['date'], y=td['count'], mode='lines+markers', line=dict(color='#00d4ff'))])
    fig2.update_layout(title="Over Time", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#e0e6ed'), height=400)
    st.plotly_chart(fig2, use_container_width=True)
