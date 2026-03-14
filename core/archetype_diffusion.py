import json
import numpy as np
import logging
from core.async_gateway import AsyncLLMGateway

logger = logging.getLogger("ArchetypeDiffusion")

class ArchetypeDiffusion:
    """
    白皮書 AgentTorch-Style 巨量擴散引擎 (Token Saver 技術 #5)
    一次 LLM 查詢 → 取得行動機率分佈 → Numpy 向量化矩陣運算 → 瞬間為 10,000+ Agent 賦予獨立行為，O(1) API 花費。
    """
    
    async def process_group(
        self,
        archetype_name: str,
        agents: list,
        world_state: dict,
        model_id: str,
        gateway: AsyncLLMGateway,
        cache_text: str = "",
        cached_obj = None,
        thinking_level: str = "minimal"
    ):
        """
        完整流程：使用 Lite 模型（極低成本）詢問原型群體在當前世界局勢下的行動機率。
        """
        prompt = f"""[群體決策中心]
你代表世界中所有的【{archetype_name}】群體心智。
【世界局勢】：{world_state}
【全局設定】：{cache_text[:500]}...

根據局勢，你的群體接下來最有可能做什麼？
請以 JSON 回傳 3~5 種行動及其概率（概率總和必須為 1.0）。
格式規範：{{"actions": {{"繼續種田": 0.6, "發起抗議": 0.3, "離開城鎮": 0.1}}}}"""

        try:
            # 觸發 API
            response = await gateway.call(
                model_id=model_id, 
                prompt=prompt, 
                schema=True, 
                max_tokens=300,
                cached_obj=cached_obj,
                thinking_level=thinking_level
            )
            data = json.loads(response)
            distribution = data.get("actions", {"日常待命": 1.0})
        except Exception as e:
            logger.warning(f"[{archetype_name}] 擴散查詢失敗，降級為預設行為: {e}")
            distribution = {"日常行為": 1.0}
            
        # 進入向量群體擴散
        agent_results = self.diffuse_to_group_vectorized(distribution, agents)
        
        # 將結果直接寫回 agents 本體，並回傳統計
        for idx, agent in enumerate(agents):
            agent.current_action = agent_results[idx]["action"]
            
        return agent_results
        
    def diffuse_to_group_vectorized(
        self,
        base_distribution: dict,
        agents: list,
        personality_weight: float = 0.2,
    ) -> list:
        """
        [Numpy 向量化極速運算]
        摒棄 Python for 迴圈逐一骰機率，改用多維矩陣一次算出 100,000 個人的最佳解。
        達成 0 API 成本的萬級模擬目標。
        """
        n_agents = len(agents)
        if n_agents == 0:
            return []
            
        actions = list(base_distribution.keys())
        n_actions = len(actions)
        
        # 1. Base Probabilities (shape: 1 x n_actions)
        base_probs = np.array(list(base_distribution.values()), dtype=float)
        base_probs = np.nan_to_num(base_probs, nan=0.0) # 防止 nan 崩潰
        if base_probs.sum() <= 0:
            base_probs = np.ones(n_actions)
        base_probs /= base_probs.sum()
        
        # 2. Personality Noise Matrix (shape: n_agents x n_actions)
        # 用 Dirichlet 分佈一次生成所有人的個性偏差
        # Dirichlet(ones * 5) 會產生相對集中但略有波動的分佈
        noise_matrix = np.random.dirichlet(np.ones(n_actions) * 5, size=n_agents)
        
        # 3. Personal Probs Matrix = weight_blend
        # Broadcating base_probs -> n_agents x n_actions
        personal_probs_matrix = (1 - personality_weight) * base_probs + (personality_weight * noise_matrix)
        
        # Re-normalize each row to exactly 1.0
        row_sums = personal_probs_matrix.sum(axis=1)[:, np.newaxis]
        personal_probs_matrix /= row_sums
        
        # 4. Vectorized Choice 
        # Numpy 沒有直接的 2D choice，我們用 CDF (累積算子) + uniform 來做 O(N) 一次性選定
        cdf = personal_probs_matrix.cumsum(axis=1)
        rand_vals = np.random.rand(n_agents, 1)
        # 找到第一個 cdf > rand 的 index
        chosen_indices = (cdf > rand_vals).argmax(axis=1)
        
        # 5. 回填 Python List
        results = []
        for i in range(n_agents):
            agent_id = getattr(agents[i], "agent_id", f"unknown_{i}")
            action_idx = chosen_indices[i]
            results.append({
                "agent_id": agent_id,
                "action": actions[action_idx],
                "confidence": float(personal_probs_matrix[i, action_idx])
            })
            
        return results
