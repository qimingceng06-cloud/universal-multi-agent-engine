from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class ModelTier:
    tier_name: str
    litellm_id: str
    agentscope_type: str
    input_price_per_1m: float
    output_price_per_1m: float
    max_output_tokens: int

def get_model_configs(provider: str, api_key: str, base_url: str = "", 
                      m_high_override: str = "", m_low_override: str = "") -> Tuple[Dict[str, ModelTier], list]:
    # 2026 最新模型費率校準
    pricing = {
        "Google": (0.075, 0.30, 0.075, 0.30),  # Gemini 2.5 Flash 費率
        "OpenAI": (1.00, 3.00, 0.15, 0.60),    # o3-mini 費率
        "DeepSeek": (0.14, 0.28, 0.14, 0.28), 
        "Ollama": (0.0, 0.0, 0.0, 0.0),
    }
    
    if provider == "Google":
        # 實測證明此 Key 支援 2.5 與 3.1 系列
        m_high = m_high_override or "gemini/gemini-3.1-pro-preview" 
        m_low = m_low_override or "gemini/gemini-2.5-flash"
        as_type = "gemini_chat"
    elif provider == "OpenAI":
        m_high = m_high_override or "openai/o3-mini"
        m_low = m_low_override or "gpt-4o-mini"
        as_type = "openai_chat"
    elif provider == "DeepSeek":
        m_high = m_high_override or "deepseek/deepseek-chat"
        m_low = m_low_override or "deepseek/deepseek-chat"
        as_type = "openai_chat"
        base_url = base_url or "https://api.deepseek.com/v1"
    else: # Ollama
        m_high = m_high_override or "ollama/gemma-3-27b"
        m_low = m_low_override or "ollama/gemma-3-4b"
        as_type = "openai_chat"
        base_url = base_url or "http://localhost:11434/v1"
        
    p_high_in, p_high_out, p_low_in, p_low_out = pricing.get(provider, (0,0,0,0))
    
    tiers = {
        "tier1_high": ModelTier("tier1_high", m_high, as_type, p_high_in, p_high_out, 4000),
        "tier1_medium": ModelTier("tier1_medium", m_high, as_type, p_high_in, p_high_out, 2000),
        "tier2_low": ModelTier("tier2_low", m_high, as_type, p_high_in, p_high_out, 1000),
        "tier2_minimal": ModelTier("tier2_minimal", m_low, as_type, p_low_in, p_low_out, 1000),
        "tier3_lite": ModelTier("tier3_lite", m_low, as_type, p_low_in, p_low_out, 500),
    }
    
    agentscope_configs = [
        {
            "model_type": as_type,
            "config_name": "model_high",
            "model_name": m_high.split("/")[-1] if "/" in m_high else m_high,
            "api_key": api_key,
            "client_args": {"base_url": base_url} if base_url else {},
        },
        {
            "model_type": as_type,
            "config_name": "model_low",
            "model_name": m_low.split("/")[-1] if "/" in m_low else m_low,
            "api_key": api_key,
            "client_args": {"base_url": base_url} if base_url else {},
        }
    ]
    
    return tiers, agentscope_configs

ROUTING_RULES = {
    "game_master": {
        "critical_event":   "tier1_high",
        "world_update":     "tier1_medium",
        "minor_event":      "tier2_low",
    },
    "core_npc": {
        "critical_decision": "tier1_medium",
        "dialogue":          "tier2_low",
        "daily_action":      "tier2_minimal",
    },
    "background_npc": {
        "important_event":   "tier3_lite",
        "daily_action":      "tier3_lite",
    },
    "archetype": {
        "*":                 "tier3_lite",
    },
}
