"""
Demo Data Generator for Universal Simulator
Generates realistic simulated data based on the 4-Layer Architecture
"""

import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any
import networkx as nx

# ===== CONSTANTS =====
LAYER_NAMES = {
    1: {"name": "關鍵人物", "name_en": "Key Figures", "color": "#b400ff", "icon": "👑"},
    2: {"name": "組織與派系", "name_en": "Factions", "color": "#00d4ff", "icon": "🏛️"},
    3: {"name": "群體部落", "name_en": "Groups & Tribes", "color": "#00ff88", "icon": "👥"},
    4: {"name": "統計環境", "name_en": "Populations", "color": "#ffcc00", "icon": "📊"}
}

PERSONALITIES = ["保守", "激進", "分析", "直覺", "從眾", "叛逆"]
ACTIONS = ["ACT", "OBSERVE", "PLAN", "WAIT", "SOCIALIZE"]
MOODS = {
    "positive": {"emoji": "🟢", "color": "#00ff88"},
    "negative": {"emoji": "🔴", "color": "#ff0055"},
    "neutral": {"emoji": "🟡", "color": "#ffcc00"},
    "uncertain": {"emoji": "⚪", "color": "#8892a4"},
    "fearful": {"emoji": "😱", "color": "#ff4444"},
    "aggressive": {"emoji": "🔥", "color": "#ffcc00"}
}

WORLD_CONDITIONS = ["和平", "衝突", "繁榮", "衰退", "擴張", "停滯"]

class AgentGenerator:
    """Generate realistic agent data for the 4-Layer system"""
    
    def __init__(self, seed: int = 42):
        random.seed(seed)
        np.random.seed(seed)
        self.agent_counter = 0
        self.thought_templates = self._load_thought_templates()
    
    def _load_thought_templates(self) -> Dict[int, List[str]]:
        return {
            1: [
                "局勢正在改變，我必須重新評估策略以維持影響力。",
                "這個區域的資源分配似乎出現了不平衡，這是一個機會。",
                "這群人的忠誠度正在動搖，我需要立刻採取行動。",
                "我們應該尋求結盟，單憑現在的力量不足以應對即將到來的威脅。",
                "最新傳聞證實了我的疑慮，我們必須準備防禦。",
                "這項新技術或工具能大幅提升我們的生產力。"
            ],
            2: [
                "內部意見分歧正在導致我們的行動遲緩。",
                "我們的儲備資產正在快速消耗，必須找到新的來源。",
                "敵對勢力的邊界推進對我們構成了直接威脅。",
                "派遣探索隊或許能為我們解開當前的困境。",
                "民眾的滿意度下降，我們需要舉辦活動來安撫人心。"
            ],
            3: [
                "大家都在談論最近的異常現象，氣氛越來越緊張。",
                "目前的分配規則並不公平，許多人感到不滿。",
                "跟隨首領的決定通常是最安全的選擇。",
                "我們發現了一條新的捷徑，這可能會改變現狀。",
                "流言蜚語傳播得很快，我們不知道該相信什麼。"
            ],
            4: [
                "整體環境的穩定性指標下降，顯示壓力正在累積。",
                "資源消耗率高於再生率，這是一個不可持續的趨勢。",
                "人口流動數據顯示這片區域正在經歷結構性改變。",
                "事件發生頻率增加，系統的熵值正在上升。",
                "宏觀參數顯示即將達到臨界點。"
            ]
        }
    
    def generate_agent(self, layer: int, agent_type: str = None) -> Dict[str, Any]:
        self.agent_counter += 1
        names_pool = {
            1: ["領主", "將軍", "大主教", "商會會長", "首席學者", "治安官", "反叛領袖", "探險家"],
            2: ["市政廳", "城衛軍", "盜賊公會", "法師塔", "神殿", "傭兵團", "鐵匠工會"],
            3: ["農民群體", "市集商人", "流浪者", "難民", "工人階級"],
            4: ["環境參數", "氣候系統", "資源分配網", "人口統計模型"]
        }
        name = random.choice(names_pool.get(layer, [f"Entity_{self.agent_counter}"]))
        personality = random.choice(PERSONALITIES)
        mood = random.choice(list(MOODS.keys()))
        base_hp = {1: 100, 2: 80, 3: 60, 4: 40}
        base_mp = {1: 100, 2: 70, 3: 50, 4: 30}
        return {
            "id": f"ENTITY-{layer}-{self.agent_counter:04d}",
            "name": name, "layer": layer, "layer_info": LAYER_NAMES[layer],
            "personality": personality, "mood": mood, "mood_info": MOODS[mood],
            "hp": random.randint(base_hp[layer] - 20, base_hp[layer]),
            "mp": random.randint(base_mp[layer] - 20, base_mp[layer]),
            "confidence": round(random.uniform(0.3, 0.95), 2),
            "influence": round(random.uniform(0.1, 1.0), 2),
            "action": random.choice(ACTIONS),
            "thought": random.choice(self.thought_templates[layer]),
            "followers": random.randint(0, 500) if layer == 1 else random.randint(10, 1000),
            "success_rate": round(random.uniform(0.4, 0.8), 2),
            "total_actions": random.randint(50, 500),
            "last_active": (datetime.now() - timedelta(minutes=random.randint(0, 120))).strftime("%H:%M"),
            "token_usage": random.randint(500, 5000),
            "memory_slots": random.randint(5, 20),
            "interaction_count": random.randint(10, 200)
        }
    
    def generate_population(self, counts: Dict[int, int] = None) -> List[Dict[str, Any]]:
        if counts is None:
            counts = {1: 8, 2: 15, 3: 30, 4: 10}
        agents = []
        for layer, count in counts.items():
            for _ in range(count):
                agents.append(self.generate_agent(layer))
        return agents


class WorldDataGenerator:
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
    
    def generate_metric_series(self, days: int = 30, start_val: float = 100.0) -> pd.DataFrame:
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        changes = np.random.normal(0.001, 0.02, days)
        changes = np.convolve(changes, [0.3, 0.5, 0.2], mode='same')
        values = start_val * np.exp(np.cumsum(changes))
        activity = np.random.lognormal(10, 1, days).astype(int)
        return pd.DataFrame({'date': dates, 'value': values, 'activity': activity,
                            'change': np.concatenate([[0], np.diff(np.log(values))])})
    
    def generate_world_overview(self) -> Dict[str, Any]:
        return {
            "world_condition": random.choice(WORLD_CONDITIONS),
            "global_score": round(random.uniform(4500, 5200), 2),
            "regional_index": round(random.uniform(14000, 16000), 2),
            "volatility": round(random.uniform(12, 25), 2),
            "system_tension": random.randint(20, 80),
            "total_agents": 63, "active_agents": random.randint(45, 60),
            "avg_confidence": round(random.uniform(0.5, 0.75), 2),
            "total_interactions": random.randint(500, 2000),
            "token_usage_today": random.randint(50000, 200000),
            "token_budget_remaining": round(random.uniform(0.3, 0.8), 2),
            "simulation_tick": random.randint(1, 1000),
            "uptime": f"{random.randint(0, 23)}h {random.randint(0, 59)}m"
        }


class NetworkGenerator:
    def __init__(self, seed: int = 42):
        random.seed(seed)
        np.random.seed(seed)
    
    def generate_network(self, agents: List[Dict]) -> nx.Graph:
        G = nx.Graph()
        for agent in agents:
            G.add_node(agent["id"], name=agent["name"], layer=agent["layer"],
                      influence=agent["influence"], mood=agent["mood"])
        for i, a1 in enumerate(agents):
            for j, a2 in enumerate(agents[i+1:], i+1):
                prob = 0.4 if a1["layer"] == a2["layer"] else 0.1
                if random.random() < prob:
                    G.add_edge(a1["id"], a2["id"], weight=round(random.uniform(0.1, 1.0), 2))
        return G


class EventGenerator:
    def __init__(self, seed: int = 42):
        random.seed(seed)
    
    def generate_events(self, count: int = 50) -> List[Dict[str, Any]]:
        events = []
        base_time = datetime.now() - timedelta(hours=24)
        for i in range(count):
            event_type = random.choice(["action", "thought", "interaction", "world", "milestone"])
            timestamp = base_time + timedelta(minutes=random.randint(0, 1440))
            if event_type == "action":
                description = f"Entity_{random.randint(1,63)} {random.choice(['gathered resources', 'moved to a new location', 'rested', 'crafted an item'])}."
            elif event_type == "thought":
                description = random.choice([
                    "Changed long-term objective based on recent events.",
                    "Increased confidence after successful interaction.",
                    "Became cautious due to perceived threats.",
                    "Started planning a new cooperative endeavor."])
            elif event_type == "interaction":
                description = f"Layer {random.randint(1,2)} entity influenced a group of {random.randint(5, 50)} members."
            elif event_type == "world":
                description = random.choice([
                    "Weather shifted to heavy rain.",
                    "A new rumor is spreading across the valley.",
                    "Resource depletion noticed in Sector B.",
                    "Seasonal change implemented in the environment."])
            else:
                description = f"Tick {random.randint(100, 1000)} reached - world state saved."
            events.append({
                "id": i + 1, "timestamp": timestamp.strftime("%Y-%m-%d %H:%M"),
                "type": event_type, "description": description,
                "impact": round(random.uniform(-1.0, 1.0), 2)
            })
        return sorted(events, key=lambda x: x["timestamp"], reverse=True)


class CostTracker:
    def generate_usage_data(self) -> Dict[str, Any]:
        return {
            "daily": {
                "total_tokens": random.randint(100000, 500000),
                "input_tokens": random.randint(60000, 300000),
                "output_tokens": random.randint(40000, 200000),
                "cost_usd": round(random.uniform(5, 50), 2),
                "api_calls": random.randint(500, 2000)
            },
            "by_layer": {
                1: {"tokens": random.randint(30000, 100000), "cost": round(random.uniform(3, 15), 2)},
                2: {"tokens": random.randint(20000, 80000), "cost": round(random.uniform(2, 10), 2)},
                3: {"tokens": random.randint(10000, 50000), "cost": round(random.uniform(1, 5), 2)},
                4: {"tokens": random.randint(5000, 30000), "cost": round(random.uniform(0.5, 3), 2)}
            },
            "savings": {
                "hash_cache_hits": random.randint(100, 500),
                "group_delegation_saves": random.randint(50, 200),
                "template_reuse_saves": random.randint(200, 800),
                "total_saved_tokens": random.randint(50000, 200000),
                "total_saved_usd": round(random.uniform(5, 30), 2)
            },
            "optimization_rate": round(random.uniform(0.4, 0.7), 2)
        }


# ===== GENERATE ALL DATA (once at import) =====
agent_gen = AgentGenerator()
world_gen = WorldDataGenerator()
network_gen = NetworkGenerator()
event_gen = EventGenerator()
cost_tracker = CostTracker()

AGENTS = agent_gen.generate_population()
WORLD_OVERVIEW = world_gen.generate_world_overview()
METRIC_DATA = world_gen.generate_metric_series(days=30)
NETWORK = network_gen.generate_network(AGENTS)
EVENTS = event_gen.generate_events(count=100)
COST_DATA = cost_tracker.generate_usage_data()

# ===== PRE-COMPUTE EXPENSIVE METRICS (cached at import time) =====
NETWORK_LAYOUT = nx.spring_layout(NETWORK, k=0.5, iterations=50, seed=42)
DEGREE_CENTRALITY = nx.degree_centrality(NETWORK)
BETWEENNESS_CENTRALITY = nx.betweenness_centrality(NETWORK)
NETWORK_DENSITY = nx.density(NETWORK)
NETWORK_COMPONENTS = nx.number_connected_components(NETWORK)
NETWORK_AVG_DEGREE = sum(dict(NETWORK.degree()).values()) / max(NETWORK.number_of_nodes(), 1)

if __name__ == "__main__":
    print(f"Generated {len(AGENTS)} entities")
    print(f"Network: {NETWORK.number_of_nodes()} nodes, {NETWORK.number_of_edges()} edges")
    print(f"Events: {len(EVENTS)} events")
    print(f"World: {WORLD_OVERVIEW['world_condition']}")