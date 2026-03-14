import asyncio
import json
import time
from core.model_router import ModelRouter
from core.memory_manager import MemoryManager
from core.context_cache import ContextCacheManager
from core.archetype_diffusion import ArchetypeDiffusion
from core.async_gateway import AsyncLLMGateway

class WorldEngine:
    def __init__(
        self, router: ModelRouter, memory_mgr: MemoryManager,
        cache_mgr: ContextCacheManager, gateway: AsyncLLMGateway,
    ):
        self.router = router
        self.memory = memory_mgr
        self.cache_mgr = cache_mgr
        self.gateway = gateway
        self.diffusion = ArchetypeDiffusion()
        
        self.step_count = 0
        self.world_state: dict = {}
        self.history: list[dict] = []
    
    async def initialize(self, agents: dict, world_config: dict):
        self.agents = agents
        self.world_state = {
            "time": world_config.get("start_time", "第 1 天 早晨"),
            "weather": "晴朗",
            "recent_events": [],
            "economic_index": 0.5,
            "social_stability": 0.7,
        }
        world_text = json.dumps(world_config, ensure_ascii=False, indent=2)
        self.cache_mgr.create_cache("world_state", world_text)
    
    async def step(self) -> dict:
        self.step_count += 1
        step_start = time.time()
        step_result = {"step": self.step_count, "actions": []}
        world_cache_text = self.cache_mgr.get_cache_text("world_state")
        world_cache_obj = self.cache_mgr.get_cache_obj("world_state")
        
        gm = self.agents["game_master"]
        gm_route = self.router.route("game_master", event_importance=0.9, action_type="world_update")
        gm_prompt = f"{gm.sys_prompt}\n世界設定:\n{world_cache_text}\n當前世界狀態：{json.dumps(self.world_state, ensure_ascii=False)}\n請判定這一步的世界事件。輸出 JSON。"
        world_update = await self.gateway.call(
            gm_route.litellm_id, 
            gm_prompt, 
            schema=True, 
            max_tokens=gm_route.max_tokens,
            cached_obj=world_cache_obj,
            thinking_level=gm_route.thinking_level
        )
        
        llm_tasks = []
        for agent in self.agents["llm_agents"]:
            importance = getattr(agent, 'importance', 0.5)
            route = self.router.route("core_npc", event_importance=importance, action_type="critical_decision")
            prompt = f"{agent.sys_prompt}\n世界設定:\n{world_cache_text}\n\n{self.memory.get_prompt(agent.agent_id)}\n\n世界狀態：{self.world_state} 你要做什麼？ JSON:"
            llm_tasks.append((route.litellm_id, prompt, route.max_tokens, world_cache_obj, route.thinking_level, agent))
            
        llm_results = await self.gateway.parallel_calls([(m, p, t, c, th) for m, p, t, c, th, _ in llm_tasks])
        
        for (_, _, _, _, _, agent), result in zip(llm_tasks, llm_results):
            if result and not isinstance(result, Exception):
                await self.memory.add_experience(agent.agent_id, str(result)[:100])
                step_result["actions"].append({"agent": agent.name, "result": result})
        
        for agent in self.agents["template_agents"]:
            action = agent.decide(self.world_state)
            step_result["actions"].append({"agent": agent.agent_id, "result": action})
            
        archetype_groups = {}
        for agent in self.agents["template_agents"]:
            arch = getattr(agent, 'archetype', 'unknown')
            archetype_groups.setdefault(arch, []).append(agent)
            
        for archetype, group in archetype_groups.items():
            if len(group) >= 1: # Reduced to 1 to allow small tests to still diffusion
                route = self.router.route("archetype", action_type="daily_action")
                await self.diffusion.process_group(
                    archetype_name=archetype,
                    agents=group,
                    world_state=self.world_state,
                    model_id=route.litellm_id,
                    gateway=self.gateway,
                    cache_text=world_cache_text,
                    cached_obj=world_cache_obj,
                    thinking_level=route.thinking_level
                )
                # the diffusion automatically assigns agent.current_action, we append it to step_result
                for agent in group:
                    step_result["actions"].append({
                        "agent": getattr(agent, "agent_id", archetype),
                        "result": getattr(agent, "current_action", "Wait")
                    })
                
        crowd = self.agents.get("statistical_crowd")
        if crowd:
            crowd_stats = crowd.step(self.world_state.get("recent_events", []))
            step_result["crowd_stats"] = crowd_stats
            
        elapsed = time.time() - step_start
        step_result["elapsed_seconds"] = round(elapsed, 2)
        step_result["cost"] = self.router.get_usage_report()
        self.history.append(step_result)
        
        return step_result
        
    async def run(self, num_steps: int = 5, step_delay: float = 0.5):
        for i in range(num_steps):
            await self.step()
            await asyncio.sleep(step_delay)
