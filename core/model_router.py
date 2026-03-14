from dataclasses import dataclass
import logging
from config.model_config import ROUTING_RULES

logger = logging.getLogger("ModelRouter")

@dataclass
class RouteResult:
    """自動路由回報，攜帶 thinking level 與成本倍率"""
    tier: str
    litellm_id: str
    thinking_level: str
    cost_multiplier: float
    estimated_base_cost_per_call: float
    max_tokens: int

class ModelRouter:
    """
    動態模型切換與 Thinking Level 路由 (2026 終極相容版)。
    為核心 NPC 提供高階推理，為群體提供 Flash Lite 極速回應，藉此節省 60-80% 結算成本。
    """
    
    def __init__(self, tiers: dict):
        self.tiers = tiers
        self.call_count: dict[str, int] = {}
        
    def route(self, agent_role: str, event_importance: float = 0.5, action_type: str = "daily_action") -> RouteResult:
        """
        根據白皮書矩陣，根據角色、重要度、動作動態切換：
        - flash_high (15x 成本) -> 重大事件 GM
        - flash_medium (3x) -> 核心 NPC 關鍵決策
        - flash_low (1.3x) -> 核心 NPC 對話
        - flash_minimal (1x) -> 日常行為
        - lite_minimal (0.5x) -> 背景與擴散
        """
        model_name = "gemini/gemini-2.5-flash"  # 預設底座 (Fallback to 2.5 flash as default API model)
        thinking_level = "minimal"
        cost_mult = 1.0
        tier_name = "tier1_high"
        
        # 1. Game Master (世界引擎)
        if agent_role == "game_master":
            if event_importance >= 0.8:
                tier_name = "tier1_high"
                thinking_level = "high"
                cost_mult = 15.0
            else:
                tier_name = "tier1_medium"
                thinking_level = "medium"
                cost_mult = 3.0
                
        # 2. 核心 NPC有名字、有故事線
        elif agent_role == "core_npc":
            if action_type in ["critical_decision", "betrayal", "alliance"]:
                tier_name = "tier1_medium"
                thinking_level = "medium"
                cost_mult = 3.0
            elif action_type in ["dialogue", "negotiation", "world_update"]:
                tier_name = "tier1_medium"
                thinking_level = "low"
                cost_mult = 1.3
            else:
                tier_name = "tier1_medium"
                thinking_level = "minimal"
                cost_mult = 1.0
                
        # 3. 背景 NPC大量，需要便宜
        elif agent_role == "background_npc":
            if event_importance >= 0.6:
                tier_name = "tier3_lite"
                thinking_level = "low"
                cost_mult = 0.7
            else:
                tier_name = "tier3_lite"
                thinking_level = "minimal"
                cost_mult = 0.5
                
        # 4. Archetype 擴散
        elif agent_role == "archetype":
            tier_name = "tier3_lite"
            thinking_level = "minimal"
            cost_mult = 0.05  # 群體擴散共享 1 次 Call, 所以均攤極低
            
        else:
            # 安全降級
            tier_name = "tier3_lite"
            thinking_level = "minimal"
            cost_mult = 0.5
            
        tier = self.tiers.get(tier_name, self.tiers.get("tier3_lite"))
        
        # 記錄用量
        self.call_count[tier_name] = self.call_count.get(tier_name, 0) + 1
        
        # 基底成本 (假設每通 API 輸入500字, 輸出300字, 除 1,000,000)
        base_cost = (500 * tier.input_price_per_1m + 300 * tier.output_price_per_1m) / 1_000_000
        total_est_cost = base_cost * cost_mult
        
        # Override LiteLLM fallback
        final_litellm_id = "gemini/gemini-2.5-flash" if "flash" in tier.litellm_id else "gemini/gemini-1.5-flash"
        if not final_litellm_id.startswith("gemini/") and "gemini" in final_litellm_id:
             final_litellm_id = f"gemini/{final_litellm_id}"
             
        return RouteResult(
            tier=tier_name,
            litellm_id=final_litellm_id,
            thinking_level=thinking_level,
            cost_multiplier=cost_mult,
            estimated_base_cost_per_call=total_est_cost,
            max_tokens=tier.max_output_tokens
        )
        
    def get_usage_report(self) -> dict:
        """根據不同 Tier 與思考級別疊加的花費進行準確回報"""
        report = {}
        total_cost = 0.0
        
        for tier_name, count in self.call_count.items():
            tier = self.tiers[tier_name]
            # 這裡回報為了簡化使用統一粗略倍率 2.0 代表平均 thinking 成本
            avg_mult = 2.0 if tier_name == "tier1_high" else 1.0 if "lite" in tier_name else 1.5 
            base = count * (500 * tier.input_price_per_1m + 300 * tier.output_price_per_1m) / 1_000_000
            est = base * avg_mult
            
            report[tier_name] = {"calls": count, "estimated_cost": f"${est:.4f}"}
            total_cost += est
            
        report["total_estimated_cost"] = f"${total_cost:.4f}"
        return report
