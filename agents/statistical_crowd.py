import numpy as np

class StatisticalCrowd:
    """Agent-Based Model：概率分佈 + 網絡效應"""
    
    def __init__(self, demographics: dict, model_type: str = "simple"):
        self.demographics = demographics
        self.population = sum(demographics.values()) if demographics else 1000
        self.satisfaction = np.random.normal(0.6, 0.15, self.population)
    
    def step(self, world_events: list):
        """每步更新整個群體的狀態"""
        # 簡易邏輯
        return {
            "unrest_probability": float((self.satisfaction < 0.3).mean()),
            "migration_pressure": float((self.satisfaction < 0.2).mean()),
            "world_demand_shift": float(self.satisfaction.mean() - 0.5),
        }
