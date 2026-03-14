import random

class TemplateAgent:
    """零 API 成本的規則驅動 Agent"""
    
    def __init__(self, agent_id: str, archetype: str, personality_seed: int):
        self.agent_id = agent_id
        self.archetype = archetype
        self.rng = random.Random(personality_seed)
        self.traits = {"seed": personality_seed}
    
    def decide(self, world_state: dict) -> str:
        """基於規則表決策，不呼叫 API"""
        action = f"按照 {self.archetype} 的常規行事"
        return action
