"""Agent Simulation Engine — 指令列啟動入口"""
import asyncio
import os
import agentscope
from dotenv import load_dotenv

from config.model_config import get_model_configs
from core.model_router import ModelRouter
from core.memory_manager import MemoryManager
from core.context_cache import ContextCacheManager
from core.semantic_cache import SemanticCache
from core.async_gateway import AsyncLLMGateway
from core.agent_factory import AgentFactory
from core.world_engine import WorldEngine

load_dotenv()

async def main():
    # === 1. 初始化模型提供者與 AgentScope ===
    # 可改寫為 OpenAI, DeepSeek, Ollama 等等
    provider = os.getenv("LLM_PROVIDER", "Google")
    api_key = os.getenv(f"{provider.upper()}_API_KEY", os.getenv("GEMINI_API_KEY", ""))
    
    print(f"啟動初始化中... 使用提供商: {provider}")
    tiers, as_configs = get_model_configs(provider, api_key)
    agentscope.init(project="UniversalSim")
    
    # === 2. 建構核心元件 ===
    router = ModelRouter(tiers)
    gateway = AsyncLLMGateway(api_key, max_concurrent=5)
    
    comp_model_id = tiers["tier3_lite"].litellm_id
    memory_mgr = MemoryManager(gateway, comp_model_id)
    cache_mgr = ContextCacheManager()
    sem_cache = SemanticCache(max_size=500, similarity_threshold=0.92)
    
    # === 3. 載入場景 & 建構 Agents ===
    factory = AgentFactory(memory_mgr)
    agents = factory.build_from_scenario("scenarios/medieval_town")
    
    # === 4. 啟動世界引擎 ===
    engine = WorldEngine(router, memory_mgr, cache_mgr, sem_cache, gateway)
    world_config = {
        "name": "風谷鎮",
        "era": "中世紀",
        "start_time": "第 1 天 早晨",
        "description": "一個寧靜的山谷小鎮，最近有盜匪出沒的傳聞...",
    }
    await engine.initialize(agents, world_config)
    
    # === 5. 運行模擬 ===
    await engine.run(num_steps=3) 
    
    # === 6. 輸出報告 ===
    print("\n=== 最終報告 ===")
    print(f"模型使用統計：{router.get_usage_report()}")

if __name__ == "__main__":
    asyncio.run(main())
