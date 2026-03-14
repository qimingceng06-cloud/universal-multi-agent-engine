import textwrap
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random
from datetime import datetime, timedelta
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.demo_data import AGENTS, LAYER_NAMES

st.set_page_config(page_title="Notifications", page_icon="Bell", layout="wide")
st.markdown("# Notification Center")
st.markdown("*Real-time alerts and system notifications*")

with st.sidebar:
    st.markdown("## Filters")
    severity_filter = st.multiselect("Severity", ["critical", "warning", "info", "success"], default=["critical", "warning"])
    type_filter = st.multiselect("Type", ["world", "agent", "system", "memory", "cost"], default=["world", "agent", "system"])
    auto_refresh = st.toggle("Auto Refresh", value=True)

def gen_notifications():
    notifs = []
    templates = [
        ("critical", "world", "World volatility exceeded threshold", "BTC price dropped 5% in 10 minutes"),
        ("critical", "agent", "Agent health critical", "Agent HP below 20%, immediate action required"),
        ("warning", "world", "Unusual trading volume detected", "Volume 3x higher than average"),
        ("warning", "agent", "Agent confidence dropping", "Prediction confidence fell below 70%"),
        ("warning", "system", "High token consumption rate", "Current rate: 1,200 tokens/min"),
        ("info", "agent", "Agent role switch", "Agent switched from Analyst to Risk Control"),
        ("info", "memory", "Memory consolidation complete", "SALM compressed 2,340 entries"),
        ("info", "system", "Model update available", "New prediction model v3.2 ready"),
        ("success", "cost", "Cost optimization achieved", "Saved 15% tokens via Group Delegation"),
        ("success", "world", "Target price reached", "ETH reached target price of $3,500"),
        ("critical", "system", "Pipeline failure detected", "Data pipeline #7 stopped responding"),
        ("warning", "memory", "Memory usage high", "Working memory at 85% capacity")
    ]
    base = datetime.now()
    for i in range(40):
        sev, typ, title, detail = random.choice(templates)
        ag = random.choice(AGENTS)
        notifs.append({
            'id': f'notif_{i:04d}',
            'timestamp': base - timedelta(minutes=random.randint(0, 1440)),
            'severity': sev,
            'type': typ,
            'title': title,
            'detail': detail,
            'agent': ag,
            'read': random.random() > 0.3,
            'acknowledged': random.random() > 0.6
        })
    notifs.sort(key=lambda x: x['timestamp'], reverse=True)
    return notifs

notifications = gen_notifications()

sev_colors = {"critical": "#ff0055", "warning": "#ffd700", "info": "#00d4ff", "success": "#00ff88"}
sev_icons = {"critical": "CRIT", "warning": "WARN", "info": "INFO", "success": "OK"}

c1,c2,c3,c4 = st.columns(4)
with c1: st.metric("Total Alerts", len(notifications))
with c2: st.metric("Critical", sum(1 for n in notifications if n['severity']=='critical'))
with c3: st.metric("Unread", sum(1 for n in notifications if not n['read']))
with c4: st.metric("Pending", sum(1 for n in notifications if not n['acknowledged']))

st.markdown("---")

t1,t2,t3 = st.tabs(["All Notifications", "Alert Timeline", "Settings"])

with t1:
    st.markdown("### Recent Notifications")
    filtered = [n for n in notifications if n['severity'] in severity_filter and n['type'] in type_filter]
    for n in filtered[:20]:
        sev = n['severity']
        ag = n['agent']
        icon = LAYER_NAMES[ag['layer']]['icon']
        opacity = "1.0" if not n['read'] else "0.6"
        st.markdown(f"""
<div style='padding:12px;margin:8px 0;background:#161b22;border-radius:8px;border-left:4px solid {sev_colors[sev]};opacity:{opacity}'>
<div style='display:flex;justify-content:space-between;align-items:center'>
<div>
<span style='color:{sev_colors[sev]};font-weight:bold;'>[{sev.upper()}]</span>
<span style='font-weight:bold;margin-left:8px'>{n['title']}</span>
</div>
<small style='color:#8b949e'>{n['timestamp'].strftime('%m-%d %H:%M')}</small>
</div>
<div style='margin-top:6px;color:#c9d1d9'>{n['detail']}</div>
<div style='margin-top:4px;font-size:0.8em;color:#8b949e'>{icon} {ag['name']} | Type: {n['type']} | {'Read' if n['read'] else 'Unread'} | {'Acked' if n['acknowledged'] else 'Pending'}</div>
</div>
""", unsafe_allow_html=True)

with t2:
    st.markdown("### Alert Timeline")
    df = pd.DataFrame([{'time': n['timestamp'], 'severity': n['severity'], 'type': n['type']} for n in notifications])
    df['hour'] = df['time'].dt.floor('H')
    timeline = df.groupby(['hour', 'severity']).size().reset_index(name='count')
    fig = go.Figure()
    for sev in ['critical', 'warning', 'info', 'success']:
        sev_data = timeline[timeline['severity']==sev]
        fig.add_trace(go.Bar(x=sev_data['hour'], y=sev_data['count'], name=sev.upper(), marker_color=sev_colors[sev]))
    fig.update_layout(barmode='stack', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#e0e6ed'), height=400, xaxis=dict(gridcolor='#30363d'), yaxis=dict(gridcolor='#30363d'))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Severity Distribution")
    sev_counts = {}
    for n in notifications: sev_counts[n['severity']] = sev_counts.get(n['severity'], 0) + 1
    fig2 = go.Figure(data=[go.Pie(labels=list(sev_counts.keys()), values=list(sev_counts.values()), hole=0.4, marker=dict(colors=[sev_colors[s] for s in sev_counts.keys()]))])
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e0e6ed'), height=350)
    st.plotly_chart(fig2, use_container_width=True)

with t3:
    st.markdown("### Notification Settings")
    st.checkbox("Enable critical alerts", value=True)
    st.checkbox("Enable warning alerts", value=True)
    st.checkbox("Enable info alerts", value=False)
    st.checkbox("Enable success alerts", value=False)
    st.markdown("---")
    st.slider("Alert cooldown (seconds)", 0, 300, 30)
    st.selectbox("Notification sound", ["None", "Beep", "Chime", "Alert"])
    st.checkbox("Email notifications", value=False)
    st.checkbox("Desktop notifications", value=True)
