# Examples

## minimal_simulation.py

A minimal end-to-end example that demonstrates:

- a simple adapter implementation
- a lightweight routing policy
- a runtime step that assigns different reasoning tiers

Run it with:

```bash
python examples/minimal_simulation.py
```

## market_simulation.py

A compact market-oriented scenario with moderate demand, pressure spikes, and layered agent responses.

Run it with:

```bash
python examples/market_simulation.py
```

## policy_shock_simulation.py

A policy-driven scenario showing how scheduled shocks propagate through the four agent layers.

Run it with:

```bash
PYTHONPATH=src python examples/policy_shock_simulation.py
```

## v0.2 showcase scenario

The new showcase config lives at `configs/showcase_v2.yaml` and is designed to make v0.2 behavior more visible:

- multiple scheduled shocks across the run
- explicit policy and macro deltas
- richer world metrics including volatility, confidence, liquidity, and stress
- all four layers active in one scenario, from key individuals to macro population
- a longer memory window so metrics history is more meaningful across steps

You can run it with any existing entry pattern that calls `run_from_config`, for example:

```bash
PYTHONPATH=src python -c "from universal_multi_agent_sim.engine import run_from_config; print(run_from_config('configs/showcase_v2.yaml'))"
```
