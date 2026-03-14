"""
UI Utility Functions - Professional Simulation Components
Provides all reusable visual components for the dashboard
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import os
import random

# ===== SHARED COLOR CONSTANTS =====

ACTION_COLORS = {
    "ACT": "#00ff88",
    "OBSERVE": "#ff0055",
    "HOLD": "#ffcc00",
    "WAIT": "#8892a4",
    "RESEARCH": "#00d4ff"
}

TYPE_COLORS = {
    "action": "#00ff88",
    "thought": "#00d4ff",
    "interaction": "#b400ff",
    "world": "#ffcc00",
    "milestone": "#ff8800"
}

MOOD_COLORS = {
    "thought": "#00d4ff",
    "observation": "#00ff88",
    "decision": "#ffcc00",
    "social": "#b400ff"
}

LAYER_COLORS = {
    1: "#b400ff",
    2: "#00d4ff",
    3: "#00ff88",
    4: "#ffcc00"
}

# ===== COLOR UTILITIES =====

def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color (#RRGGBB) to (r, g, b) tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def hex_to_rgba_str(hex_color: str, alpha: float = 0.1) -> str:
    """Convert hex color to rgba(r,g,b,a) CSS string."""
    r, g, b = hex_to_rgb(hex_color)
    return f"rgba({r},{g},{b},{alpha})"

def get_delta_color(value: float) -> str:
    """Return green for positive, red for negative, yellow for zero."""
    if value > 0:
        return "#00ff88"
    elif value < 0:
        return "#ff0055"
    return "#ffcc00"

# ===== CSS LOADING =====
def load_css():
    """Load the global CSS file."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "style.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===== PLOTLY THEME =====

PLOTLY_DARK_LAYOUT = dict(
    template='plotly_white',
    paper_bgcolor='rgba(255, 255, 255, 1)',
    plot_bgcolor='rgba(248, 250, 252, 1)',
    font=dict(color='#0f172a', family='Inter, sans-serif', size=11),
    xaxis=dict(showgrid=False, zeroline=False, linecolor='#e2e8f0'),
    yaxis=dict(showgrid=True, gridcolor='#e2e8f0', zeroline=False),
    margin=dict(l=40, r=20, t=40, b=40),
    hoverlabel=dict(
        bgcolor='#ffffff',
        bordercolor='#e2e8f0',
        font=dict(color='#0f172a', family='Inter, sans-serif', size=11)
    )
)

def apply_dark_theme(fig: go.Figure, height: int = 400, showlegend: bool = False,
                     y_range: list = None, y_title: str = None, title: str = None) -> go.Figure:
    """Apply consistent dark theme to a Plotly figure."""
    layout_updates = {**PLOTLY_DARK_LAYOUT, 'height': height, 'showlegend': showlegend}
    if title:
        layout_updates['title'] = dict(text=title, font=dict(size=13, color='#e8edf4'))
    if y_range:
        layout_updates['yaxis'] = dict(
            title=y_title or '',
            showgrid=True,
            gridcolor='rgba(255,255,255,0.04)',
            range=y_range,
            zeroline=False
        )
    elif y_title:
        layout_updates['yaxis'] = dict(
            title=y_title,
            showgrid=True,
            gridcolor='rgba(255,255,255,0.04)',
            zeroline=False
        )
    fig.update_layout(**layout_updates)
    return fig

# ===== HTML COMPONENT HELPERS =====

def pro_header(title: str, subtitle: str = None) -> str:
    """Generate a professional header bar."""
    sub_html = f'<div class="header-subtitle">{subtitle}</div>' if subtitle else ''
    return f'<div class="pro-header"><div><div class="header-title">{title}</div>{sub_html}</div></div>'

def status_dot(status: str = "online") -> str:
    """Generate a status indicator dot. Statuses: online, warning, offline, processing."""
    return f'<span class="status-dot {status}"></span>'

def status_bar(items: list) -> str:
    """Generate a system status bar.
    items: list of dicts with keys: label, value, status (optional)
    Example: [{"label": "AGENTS", "value": "42", "status": "online"}]
    """
    items_html = ""
    for item in items:
        dot = status_dot(item.get("status", "online"))
        items_html += f'<div class="status-item">{dot}<span class="status-label">{item["label"]}:</span><span class="status-value">{item["value"]}</span></div>'
    return f'<div class="system-status-bar">{items_html}</div>'

def ticker_bar(symbols: list) -> str:
    """Generate a scrolling ticker bar.
    symbols: list of dicts with keys: symbol, price, change_pct
    Example: [{"symbol": "SPX", "price": "5,234.12", "change_pct": 1.2}]
    """
    items = ""
    for s in symbols:
        cls = "up" if s.get("change_pct", 0) >= 0 else "down"
        arrow = "▲" if s.get("change_pct", 0) >= 0 else "▼"
        items += f'<span class="ticker-item"><span class="symbol">{s["symbol"]}</span><span class="price">{s.get("price", "")}</span><span class="{cls}">{arrow} {abs(s.get("change_pct", 0)):.2f}%</span></span>'
    # Duplicate for seamless scroll
    return f'<div class="ticker-bar"><div class="ticker-content">{items * 3}</div></div>'

def stat_card(label: str, value: str, color: str = '#00ff88', delta: str = None) -> str:
    """Generate a stat card HTML string."""
    delta_html = f"<div style='font-size:0.75rem;color:var(--success);margin-top:0.25rem;'>{delta}</div>" if delta else ""
    return f"<div class='stat-card'><div class='section-title'>{label}</div><div class='counter-value' style='color:{color};margin-top:0.25rem;'>{value}</div>{delta_html}</div>"

def stat_card_large(label: str, value: str, color: str = '#00ff88') -> str:
    """Generate a large stat card HTML string."""
    return f"<div class='stat-card'><div style='color:#6b7a90;font-size:0.7rem;letter-spacing:1px;text-transform:uppercase;font-family:Orbitron,sans-serif;'>{label}</div><div style='font-size:2.2rem;font-weight:bold;color:{color};margin-top:0.25rem;font-family:Orbitron,sans-serif;'>{value}</div></div>"

def counter_card(label: str, value: str, color: str = '#00ff88', icon: str = None) -> str:
    """Generate a counter card with animated styling."""
    icon_html = f"<span style='font-size:1.5rem;margin-right:0.5rem;'>{icon}</span>" if icon else ""
    return f"<div class='stat-card' style='text-align:center;'><div style='color:#6b7a90;font-size:0.7rem;letter-spacing:1px;text-transform:uppercase;font-family:Orbitron,sans-serif;margin-bottom:0.5rem;'>{icon_html}{label}</div><div class='counter-value' style='color:{color};'>{value}</div></div>"

def gauge_chart(value: float, label: str, max_val: float = 100, unit: str = "%",
                color: str = "#00ff88", size: int = 180) -> go.Figure:
    """Create a professional gauge chart."""
    # Determine color based on value
    if value >= max_val * 0.7:
        bar_color = "#00ff88"
    elif value >= max_val * 0.4:
        bar_color = "#ffcc00"
    else:
        bar_color = "#ff0055"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number=dict(
            suffix=unit,
            font=dict(size=28, family='Orbitron', color='#e8edf4')
        ),
        gauge=dict(
            axis=dict(
                range=[0, max_val],
                tickwidth=1,
                tickcolor="rgba(255,255,255,0.2)",
                tickfont=dict(size=10, color='#6b7a90')
            ),
            bar=dict(color=bar_color, thickness=0.7),
            bgcolor="rgba(255,255,255,0.04)",
            borderwidth=0,
            steps=[
                dict(range=[0, max_val*0.3], color="rgba(255,0,85,0.08)"),
                dict(range=[max_val*0.3, max_val*0.7], color="rgba(255,204,0,0.08)"),
                dict(range=[max_val*0.7, max_val], color="rgba(0,255,136,0.08)")
            ],
            threshold=dict(
                line=dict(color=bar_color, width=2),
                thickness=0.75,
                value=value
            )
        )
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e8edf4'),
        height=size,
        margin=dict(l=20, r=20, t=40, b=10),
        title=dict(text=label, font=dict(size=11, color='#6b7a90'), x=0.5)
    )
    return fig

def radar_chart(categories: list, values: list, title: str = "Agent Profile",
                 fill_color: str = "rgba(0,255,136,0.2)", line_color: str = "#00ff88",
                 height: int = 300) -> go.Figure:
    """Create a radar/spider chart for agent attributes."""
    # Close the polygon
    categories = categories + [categories[0]]
    values = values + [values[0]]
    
    fig = go.Figure(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor=fill_color,
        line=dict(color=line_color, width=2),
        marker=dict(size=6, color=line_color)
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showline=False,
                gridcolor='rgba(255,255,255,0.06)',
                tickfont=dict(size=9, color='#6b7a90')
            ),
            angularaxis=dict(
                gridcolor='rgba(255,255,255,0.06)',
                tickfont=dict(size=10, color='#e8edf4')
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=height,
        margin=dict(l=40, r=40, t=40, b=40),
        title=dict(text=title, font=dict(size=12, color='#6b7a90'), x=0.5)
    )
    return fig

def sparkline(data: list, color: str = "#00ff88", height: int = 50) -> go.Figure:
    """Create a minimal sparkline chart."""
    fig = go.Figure(go.Scatter(
        y=data,
        mode='lines',
        line=dict(color=color, width=1.5),
        fill='tozeroy',
        fillcolor=hex_to_rgba_str(color, 0.1)
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=height,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False
    )
    return fig

def progress_ring(value: float, max_val: float = 100, size: int = 120,
                  color: str = "#00ff88", label: str = "") -> str:
    """Generate an SVG progress ring."""
    radius = (size - 10) / 2
    circumference = 2 * 3.14159 * radius
    pct = min(value / max_val, 1.0)
    offset = circumference * (1 - pct)
    
    return f'<svg class="progress-ring" width="{size}" height="{size}"><circle stroke="rgba(255,255,255,0.06)" stroke-width="6" fill="transparent" r="{radius}" cx="{size/2}" cy="{size/2}"/><circle stroke="{color}" stroke-width="6" stroke-linecap="round" fill="transparent" r="{radius}" cx="{size/2}" cy="{size/2}" stroke-dasharray="{circumference} {circumference}" stroke-dashoffset="{offset}"/><text x="50%" y="50%" text-anchor="middle" dy="0.3em" fill="#e8edf4" font-family="Orbitron" font-size="{size*0.18}px" font-weight="bold">{value:.0f}{label}</text></svg>'

def heatmap_cell(value: float, label: str, min_val: float = 0, max_val: float = 100,
                 color_low: str = "#ff0055", color_high: str = "#00ff88") -> str:
    """Generate a heatmap cell with interpolated color."""
    pct = (value - min_val) / (max_val - min_val) if max_val != min_val else 0.5
    pct = max(0, min(1, pct))
    
    # Interpolate colors
    r1, g1, b1 = hex_to_rgb(color_low)
    r2, g2, b2 = hex_to_rgb(color_high)
    r = int(r1 + (r2 - r1) * pct)
    g = int(g1 + (g2 - g1) * pct)
    b = int(b1 + (b2 - b1) * pct)
    bg = f"rgba({r},{g},{b},0.2)"
    border = f"rgba({r},{g},{b},0.4)"
    
    return f'<div class="heatmap-cell" style="background:{bg};border:1px solid {border};color:rgb({r},{g},{b});"><div style="font-size:0.65rem;color:#6b7a90;">{label}</div><div style="font-weight:bold;font-size:1rem;">{value:.0f}</div></div>'

def event_card(event_type: str, timestamp: str, description: str, color: str) -> str:
    """Generate an event feed card HTML string."""
    return f"<div class='event-card' style='border-left-color:{color};'><div style='display:flex;justify-content:space-between;'><span style='color:{color};font-size:0.75rem;font-weight:600;letter-spacing:0.5px;'>{event_type}</span><span style='color:var(--text-dim);font-size:0.75rem;font-family:\"JetBrains Mono\",monospace;'>{timestamp}</span></div><div style='margin-top:0.35rem;color:var(--text-primary);font-size:0.85rem;line-height:1.4;'>{description}</div></div>"

def thought_bubble(thought: str, agent_name: str = None) -> str:
    """Generate a thought bubble for agent thinking display."""
    agent_html = f"<div style='font-size:0.7rem;color:#00d4ff;margin-bottom:0.35rem;font-family:Orbitron,sans-serif;'>{agent_name}</div>" if agent_name else ""
    return f"<div class='thought-bubble'>{agent_html}<div style='font-size:0.85rem;line-height:1.5;'>{thought}</div></div>"

def section_header(icon: str, title: str) -> str:
    """Generate a section header with icon and line."""
    return f'<div class="section-header"><span class="section-icon">{icon}</span><span class="section-title">{title}</span><div class="section-line"></div></div>'

def status_light_bar(active_colors: list, total: int = 5) -> str:
    """Generate a status light bar (like a server rack indicator).
    active_colors: list of color strings for active lights
    """
    lights = ""
    for i in range(total):
        if i < len(active_colors):
            color = active_colors[i]
            cls = f"{color} active" if color in ['green','blue','purple','yellow'] else f"{color}"
            lights += f'<div class="status-light {cls}"></div>'
        else:
            lights += '<div class="status-light dim"></div>'
    return f'<div class="status-light-bar">{lights}</div>'

def corner_badge(text: str, color: str = "#00ff88") -> str:
    """Generate a corner badge for cards."""
    return f"<span class='corner-badge' style='color:{color};border-color:{color};'>{text}</span>"

def kpi_row(kpis: list) -> str:
    """Generate a row of KPI cards.
    kpis: list of dicts with keys: label, value, color, delta (optional), sparkline_data (optional)
    """
    cards = ""
    for kpi in kpis:
        delta_html = ""
        if "delta" in kpi and kpi["delta"] is not None:
            d = kpi["delta"]
            d_color = get_delta_color(d)
            arrow = "▲" if d > 0 else ("▼" if d < 0 else "●")
            delta_html = f"<div style='font-size:0.7rem;color:{d_color};margin-top:0.25rem;'>{arrow} {abs(d):.1f}%</div>"
        cards += stat_card(kpi["label"], kpi["value"], kpi.get("color", "#00ff88"), delta_html if delta_html else None)
    return f"<div style='display:grid;grid-template-columns:repeat({len(kpis)},1fr);gap:1rem;'>{cards}</div>"

# ===== INIT (call in app.py once) =====

def init_page():
    """Standard page initialization: load CSS and set up session state."""
    load_css()
    if "sim_running" not in st.session_state:
        st.session_state.sim_running = False
    if "sim_tick" not in st.session_state:
        st.session_state.sim_tick = 0
    if "sim_speed" not in st.session_state:
        st.session_state.sim_speed = 5