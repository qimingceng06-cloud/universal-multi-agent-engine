import yaml
import random
import logging
from core.memory_manager import MemoryManager
from agents.template_agent import TemplateAgent
from agents.statistical_crowd import StatisticalCrowd

# 嘗試載入真實的 AgentScope (2026 白皮書終極目標)
try:
    import agentscope
    from agentscope.agents import DialogAgent
    AGENTSCOPE_AVAILABLE = True
except ImportError:
    AGENTSCOPE_AVAILABLE = False
    
logger = logging.getLogger("AgentFactory")

class FallbackLLMAgent:
    """倘若執行環境未安裝 AgentScope，提供的原生備用代理 (具有相同的屬性介面)"""
    def __init__(self, agent_id: str, name: str, role: str, importance: float, sys_prompt: str):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.importance = importance
        self.sys_prompt = sys_prompt

class AgentFactory:
    """
    根據場景配置，建構四層混合 Agent 體系 (2026 終極架構)。
    1. Layer 1: AgentScope LLM Agent / Game Master
    2. Layer 2 & 3: Template Agent (配合 Archetype Diffusion)
    3. Layer 4: Statistical Crowd
    """
    
    def __init__(self, memory_mgr: MemoryManager):
        self.memory_mgr = memory_mgr
        
    def build_from_scenario(self, scenario_path: str) -> dict:
        """從場景 YAML 配置檔建構整個 Agent 體系"""
        with open(f"{scenario_path}/world.yaml", "r", encoding="utf-8") as f:
            world_cfg = yaml.safe_load(f)
        try:
            with open(f"{scenario_path}/npcs.yaml", "r", encoding="utf-8") as f:
                npc_cfg = yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"找無 {scenario_path}/npcs.yaml，自動注入預設 NPC 模板 ({e})")
            npc_cfg = {}
        
        result = {
            "game_master": self._build_game_master(world_cfg),
            "llm_agents": [],
            "template_agents": [],
            "statistical_crowd": None,
        }
        
        # 1. 構建核心 LLM NPC
        for npc in npc_cfg.get("llm_agents", []):
            if npc.get("role") == "game_master":
                continue
            agent = self._build_llm_agent(npc)
            result["llm_agents"].append(agent)
            
        # 2. 構建擴散原型的 Template Agent
        for archetype in npc_cfg.get("template_agents", {}).get("archetypes", []):
            # 自動限制數量避免測試環境記憶體爆炸 (如果在 Server 端則可直接放開)
            count = min(archetype.get("count", 10), 1000) 
            agents = self._build_template_group(archetype["type"], count)
            result["template_agents"].extend(agents)
            
        # 3. 構建宏觀數學群體 (Statistical Crowd)
        crowd_cfg = npc_cfg.get("statistical_crowd", {})
        if crowd_cfg:
            result["statistical_crowd"] = StatisticalCrowd(
                demographics=crowd_cfg.get("demographics", {}),
                model_type=crowd_cfg.get("model", "simple"),
            )
            
        return result
    
    def _build_game_master(self, world_cfg: dict):
        sys_prompt = f"""你是這個模擬世界的 Game Master。
你負責：
1. 判定玩家和 NPC 行動的因果結果
2. 生成世界事件（天氣、轉折、突發狀況）
3. 維護宇宙邏輯的一致性

世界設定：
{yaml.dump(world_cfg, allow_unicode=True)}

回覆格式：嚴格 JSON，必須包含 'world_events' 及 'narrative_summary'。"""
        
        return self._instantiate_agent(
            agent_id="game_master", 
            name="WorldEngineGM", 
            role="game_master", 
            importance=1.0, 
            sys_prompt=sys_prompt
        )
    
    def _build_llm_agent(self, npc_config: dict):
        agent_id = npc_config["id"]
        role = npc_config.get("role", "core_npc")
        importance = npc_config.get("importance", 0.5)
        
        # 連動註冊進真實的 SALM 記憶系統
        self.memory_mgr.create_memory(
            agent_id=agent_id,
            name=npc_config["name"],
            personality=npc_config.get("personality", "Neutral"),
            goals=npc_config.get("goals", "Survive"),
            compression_interval=6,
        )
        
        sys_prompt = f"你是 {npc_config['name']}。\n{npc_config.get('description', '')}\n請依據世界態勢，做出最符合你目標的決策(JSON格式)。"
        return self._instantiate_agent(agent_id, npc_config["name"], role, importance, sys_prompt)

    def _instantiate_agent(self, agent_id: str, name: str, role: str, importance: float, sys_prompt: str):
        """根據 AgentScope 是否可動態啟用，實例化出可操作的 Agent"""
        if AGENTSCOPE_AVAILABLE:
            # 這裡我們掛載 AgentScope 原生的 DialogAgent
            # 動態模型調度 (ModelRouter) 會在執行期 Override 它的內部調用
            logger.info(f"[{agent_id}] 實例化為 AgentScope DialogAgent 節點")
            agent = DialogAgent(
                name=name,
                sys_prompt=sys_prompt,
                model_config_name="dynamic_router" # 會被 Gateway 劫持處理
            )
            # 把自定義的屬性掛上供 Engine 使用
            agent.agent_id = agent_id
            agent.role = role
            agent.importance = importance
            return agent
        else:
            return FallbackLLMAgent(agent_id, name, role, importance, sys_prompt)

    def _build_template_group(self, archetype: str, count: int) -> list:
        return [
            TemplateAgent(
                agent_id=f"{archetype}_{i}",
                archetype=archetype,
                personality_seed=random.randint(0, 100000),
            )
            for i in range(count)
        ]
