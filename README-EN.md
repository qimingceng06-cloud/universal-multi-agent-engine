<div align="right">
  <a href="./README.md"><strong>繁體中文</strong></a> | <a href="./README-EN.md"><strong>English</strong></a>
</div>

<div align="center">

# Universal Multi-Agent Simulation Engine

### A layered simulation engine for large-scale social systems, market dynamics, policy shocks, and complex world modeling

<p>
  <a href="./README.md"><img src="https://img.shields.io/badge/Language-繁體中文-0F766E?style=for-the-badge" alt="Traditional Chinese"></a>
  <a href="./README-EN.md"><img src="https://img.shields.io/badge/Language-English-1D4ED8?style=for-the-badge" alt="English"></a>
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Status-MVP-16A34A?style=for-the-badge" alt="Status MVP">
  <img src="https://img.shields.io/badge/Architecture-Layered-7C3AED?style=for-the-badge" alt="Layered Architecture">
  <img src="https://img.shields.io/badge/Simulation-Scenario--Driven-E11D48?style=for-the-badge" alt="Scenario Driven">
  <img src="https://img.shields.io/badge/Focus-Research%20Grade-F59E0B?style=for-the-badge" alt="Research Grade">
</p>

<p>
  <a href="#overview">Overview</a> •
  <a href="#feature-matrix">Feature Matrix</a> •
  <a href="#visual-showcase">Visual Showcase</a> •
  <a href="#quick-navigation">Quick Navigation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#roadmap">Roadmap</a>
</p>

</div>

---

[![Architecture Banner](../images/universal-multi-agent-simulation-engine-architecture-banner.png)](../images/universal-multi-agent-simulation-engine-architecture-banner.png)

> A flagship-grade, GitHub-native multi-agent simulation repository designed to look strong at first glance and stay technically convincing on closer inspection.

---

## Quick Navigation

| Section | What you get |
|---|---|
| [Overview](#overview) | Project positioning, core value, and problem space |
| [Feature Matrix](#feature-matrix) | A fast table-based view of the key capabilities |
| [Visual Showcase](#visual-showcase) | Clickable visuals and architecture entry points |
| [Visual Architecture](#visual-architecture) | Plain-text architecture readable without rendering |
| [Scenario Gallery](#scenario-gallery) | A quick view of supported simulation scenarios |
| [Quick Start](#quick-start) | The shortest path to getting started |
| [Roadmap](#roadmap) | Where the project can go next |

---

## Overview

Universal Multi-Agent Simulation Engine is an engineering-first framework for building complex, scalable, cost-aware simulated worlds.

It is not just a conceptual white paper, and it is not a one-off demo scaffold limited to a single scenario. The goal of this project is to provide a unified simulation core that can host key individuals, dense template agents, archetype groups, and macro-scale statistical populations in the same runtime.

### Best suited for

- market and pricing simulations
- social interaction and group behavior systems
- policy shock and institutional response models
- multi-layer agent worlds that balance fidelity and cost
- public-facing research-grade GitHub flagship repositories

---

## Hero Positioning

```text
+--------------------------------------------------------------------------------------+
|  Not just a demo. Not just a paper. Not just an idea.                                |
|                                                                                      |
|  This repository is structured as a runnable simulation engine with layered agents,  |
|  scenario-driven execution, and a cost-aware architecture for complex worlds.        |
+--------------------------------------------------------------------------------------+
```

---

## Feature Matrix

| Capability | Description | Current State |
|---|---|---|
| Layered Agent World | Combines key individuals, template agents, archetype groups, and statistical populations | Ready |
| Runnable Simulation Core | Includes engine, router, memory, scheduler, and world state | Ready |
| Scenario-Driven Design | Switches simulation modes through YAML scenarios | Ready |
| Cost-Aware Architecture | Focuses expensive reasoning on the roles and events that matter most | Ready |
| Extensible Adapters | Leaves a clear path for real model and service integrations | Partial |
| Replay and Analytics | Richer replay, evaluation, and observability layers | Planned |

---

## Visual Showcase

| Preview | Destination | Purpose |
|---|---|---|
| [![Architecture Banner](../images/universal-multi-agent-simulation-engine-architecture-banner.png)](../images/universal-multi-agent-simulation-engine-architecture-banner.png) | Banner | Main homepage visual anchor |
| [![Architecture Overview](../images/architecture-overview-v2.png)](../images/architecture-overview-v2.png) | Overview Graphic | High-level system view |
| [![Architecture Detail](../images/architecture-detail-v2.png)](../images/architecture-detail-v2.png) | Detailed Graphic | Deeper module breakdown |

> These previews are intentionally clickable in GitHub so the README feels closer to a polished flagship repository rather than a plain technical note.

---

## Why This Project Matters

Most multi-agent systems get stuck at the same trade-off:

```text
If every agent is highly intelligent:
  -> cost becomes too high
  -> reasoning becomes too slow
  -> scaling becomes difficult

If everything is reduced to aggregate abstractions:
  -> individual variation disappears
  -> behavior loses depth
  -> interpretability drops
```

The core value of this engine is that it creates a practical middle path between those extremes:

```text
                High Fidelity Where It Matters
                             |
                             v
  +---------------------------------------------------------------+
  |  Layer 1  Key Individuals: strategic roles, critical choices  |
  |  Layer 2  Template Agents: stable low-cost local behaviors    |
  |  Layer 3  Archetype Groups: grouped approximations at scale   |
  |  Layer 4  Statistical Population: macro pressure and context  |
  +---------------------------------------------------------------+
                             |
                             v
                   Scalable Simulation at Lower Cost
```

---

## Signature Highlights

| Highlight | Why it matters |
|---|---|
| Fidelity where it matters | High-fidelity intelligence is reserved for the actors and events that shape outcomes |
| Scale by design | Scale and budget are architectural inputs from day one, not late-stage fixes |
| Engineering over hype | The project prioritizes runnable, testable, maintainable systems over pure concept demos |
| Research-to-product bridge | It works as both a research prototype and a foundation for future platformization |

---

## Visual Architecture

This README intentionally uses plain-text visualization so the architecture remains readable directly on GitHub without external rendering.

```text
                                   UNIVERSAL MULTI-AGENT SIMULATION ENGINE

        +--------------------------------------------------------------------------------------+
        |                                      CONFIG LAYER                                     |
        |         YAML scenarios . env settings . runtime parameters . adapter mode            |
        +-----------------------------------------------+--------------------------------------+
                                                        |
                                                        v
+--------------------------------------------------------------------------------------------------------------+
|                                         SIMULATION ENGINE CORE                                                |
|                                                                                                              |
|   +------------------+   +------------------+   +------------------+   +------------------+                 |
|   |   World State    |   |    Scheduler     |   |      Router      |   |      Memory      |                 |
|   |   state graph    |   | event timeline   |   | interaction path |   | state retention  |                 |
|   +------------------+   +------------------+   +------------------+   +------------------+                 |
|                                                                                                              |
|   +------------------------------------------------------------------------------------------------------+   |
|   |                                         Semantic Cache                                              |   |
|   |                         reuse repeated reasoning and reduce duplicate work                           |   |
|   +------------------------------------------------------------------------------------------------------+   |
+--------------------------------------------------------------------------------------------------------------+
                                                        |
                                                        v
+--------------------------------------------------------------------------------------------------------------+
|                                            AGENT POPULATION                                                   |
|                                                                                                              |
|   Layer 1: Key Individuals        -> high-importance actors, strategic behavior, narrative impact          |
|   Layer 2: Adaptive Templates     -> repeatable decision patterns with local variation                      |
|   Layer 3: Archetype Groups       -> grouped behaviors for scalable approximation                           |
|   Layer 4: Statistical Population -> macro-level environment, pressure, demand, and social background      |
+--------------------------------------------------------------------------------------------------------------+
                                                        |
                                                        v
+--------------------------------------------------------------------------------------------------------------+
|                                        OUTPUTS AND ANALYSIS                                                   |
|                           logs . traces . policy outcomes . market shifts . scenario results                 |
+--------------------------------------------------------------------------------------------------------------+
```

---

## System Philosophy

```text
+----------------------------------------------------------------------------------+
|  Principle 1  Fidelity where it matters                                          |
|  Reserve high-fidelity intelligence for the roles and events that matter most    |
+----------------------------------------------------------------------------------+
|  Principle 2  Scale by design                                                    |
|  Scaling is part of the architecture from the start, not an afterthought         |
+----------------------------------------------------------------------------------+
|  Principle 3  Engineering over hype                                              |
|  Prioritize runnable, testable, maintainable systems over pure concept demos     |
+----------------------------------------------------------------------------------+
|  Principle 4  Configurable worlds                                                |
|  Keep domain knowledge in the config layer and the engine broadly reusable       |
+----------------------------------------------------------------------------------+
```

---

## Repository Snapshot

| Area | Included |
|---|---|
| Core Runtime | engine, router, memory, scheduler, world |
| Agent Layers | agents and population abstractions |
| Adapter Path | current mock adapters and extension route |
| Scenario Configs | minimal, market, policy, supply_chain, showcase |
| Examples | runnable example scripts |
| Testing | automated test coverage |
| Packaging | pyproject.toml, requirements.txt |
| CI | GitHub Actions workflow |

---

## Project Structure

```text
universal-multi-agent-simulation-engine/
|
|-- README.md
|-- README-EN.md
|-- pyproject.toml
|-- requirements.txt
|-- .env.example
|
|-- configs/
|   |-- minimal.yaml
|   |-- market_ecosystem.yaml
|   |-- policy_shock.yaml
|   |-- supply_chain_resilience.yaml
|   `-- showcase_v2.yaml
|
|-- docs/
|   `-- architecture.md
|
|-- examples/
|   |-- minimal_simulation.py
|   |-- market_simulation.py
|   |-- policy_shock_simulation.py
|   `-- README.md
|
|-- src/universal_multi_agent_sim/
|   |-- agents/
|   |-- adapters/
|   |-- cache.py
|   |-- engine.py
|   |-- logging_utils.py
|   |-- memory.py
|   |-- router.py
|   |-- scheduler.py
|   |-- types.py
|   `-- world.py
|
|-- tests/
|   `-- ...
|
`-- .github/workflows/
    `-- ci.yml
```

---

## Scenario Gallery

| Scenario | What it demonstrates | Positioning |
|---|---|---|
| Minimal | smallest runnable simulation loop | Fast start |
| Market Ecosystem | market-style interaction and behavioral dynamics | Economic simulation |
| Policy Shock | institutional change and systemic response | Policy modeling |
| Supply Chain Resilience | dependency and adaptation under disruption | Resilience study |
| Showcase V2 | presentation-oriented flagship configuration | Homepage demo |

---

## Runtime Flow

```text
Step 1   Load scenario config
Step 2   Build simulation world
Step 3   Initialize layered agent population
Step 4   Route interactions through engine core
Step 5   Update world state and memory
Step 6   Reuse cached reasoning when possible
Step 7   Produce logs, outputs, and scenario results
```

---

## Quick Start

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd universal-multi-agent-simulation-engine
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -e .[dev]
```

### 4. Run tests

```bash
pytest
```

### 5. Run example scenarios

```bash
python examples/minimal_simulation.py
python examples/market_simulation.py
PYTHONPATH=src python examples/policy_shock_simulation.py
PYTHONPATH=src python -c "from universal_multi_agent_sim.engine import run_from_config; print(run_from_config('configs/showcase_v2.yaml'))"
```

---

## Configuration

Scenario switching is centered around `configs/`. You can reshape system behavior through configuration rather than rewriting the core engine.

Environment variables can follow `.env.example`:

```bash
SIM_ENV=development
SIM_LOG_LEVEL=INFO
SIM_OUTPUT_DIR=outputs/run_local
SIM_ADAPTER_MODE=mock
SIM_API_BASE_URL=
SIM_API_KEY=
SIM_MODEL_NAME=
SIM_ENABLE_TRACING=false
SIM_TRACE_PROJECT=
```

---

## Use Cases

- large-scale social interaction simulation
- market, production, and supply chain modeling
- policy shock and institutional analysis
- organizational, governance, and collective decision research
- agent simulation platforms balancing fidelity and cost

---

## Engineering Status

This project is not an empty shell. It is already a working MVP with a runnable simulation core. It is suitable for:

- continued research prototyping
- use as a GitHub flagship portfolio repository
- serving as the backbone of a larger simulation platform
- acting as the base layer for future real adapters or model integrations

| Dimension | Status |
|---|---|
| Runnable examples | Done |
| Automated tests | Done |
| Config-driven scenarios | Done |
| Layered abstractions | Done |
| CI workflow | Done |
| Rich replay layer | In progress |
| Budget dashboard | Planned |
| Real external adapters | Planned |

---

## Visual Presentation Strategy

```text
Top Layer
  -> title, badges, language switch, quick links, hero image

Middle Layer
  -> feature tables, architecture blocks, showcase previews

Bottom Layer
  -> quick start, status, roadmap, license
```

This structure gives the repository a much stronger flagship feel than a plain feature checklist.

---

## Roadmap

```text
Near Term
  -> richer scenario packs
  -> stronger replay and evaluation
  -> better cost and fidelity benchmarking

Mid Term
  -> real-world adapters
  -> more advanced policy and dependency modeling
  -> larger population orchestration

Long Term
  -> full research-grade simulation platform
  -> comparative scenario lab
  -> extensible agent systems for economics, governance, and society
```

---

## License

Before public release, add the license you want to use, such as MIT or Apache-2.0.
