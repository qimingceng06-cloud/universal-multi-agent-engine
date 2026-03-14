from universal_multi_agent_sim.router import ModelRouter


def test_router_selects_key_individual_layer_when_importance_is_high():
    router = ModelRouter({"key_individual": 0.8, "templated_adaptive": 0.5, "archetype_group": 0.25}, budget=1.0)
    assert router.route(0.95, 0.2, 1) == "Layer 1 Key Individual Agents"


def test_router_falls_back_to_statistical_population_when_low_signal():
    router = ModelRouter({"key_individual": 0.8, "templated_adaptive": 0.5, "archetype_group": 0.25}, budget=0.05)
    assert router.route(0.05, 0.05, 1) == "Layer 4 Macro Statistical Population"


def test_router_uses_templated_adaptive_layer_for_mid_signal():
    router = ModelRouter({"key_individual": 0.8, "templated_adaptive": 0.5, "archetype_group": 0.25}, budget=1.0)
    assert router.route(0.55, 0.15, 1) == "Layer 2 Templated Adaptive Agents"


def test_router_consume_budget_reduces_available_budget():
    router = ModelRouter({"key_individual": 0.8, "templated_adaptive": 0.5, "archetype_group": 0.25}, budget=1.0)
    router.consume_budget("Layer 1 Key Individual Agents")
    assert router.budget < 1.0
