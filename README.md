<div align="right">
  <a href="./README.md"><strong>繁體中文</strong></a> | <a href="./README-EN.md"><strong>English</strong></a>
</div>

<div align="center">

# Universal Multi-Agent Simulation Engine

### 為大規模社會系統、市場動態、政策衝擊與複雜世界建模而生的分層多智能體模擬引擎

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
| [Overview](#overview) | 專案定位、核心價值與適用問題 |
| [Feature Matrix](#feature-matrix) | 用表格快速看懂能力與特性 |
| [Visual Showcase](#visual-showcase) | 可點擊的首頁圖像與架構入口 |
| [Visual Architecture](#visual-architecture) | 不用渲染也能直接看的純文字架構圖 |
| [Scenario Gallery](#scenario-gallery) | 各模擬場景用途總覽 |
| [Quick Start](#quick-start) | 最短上手流程 |
| [Roadmap](#roadmap) | 後續可升級方向 |

---

## Overview

Universal Multi-Agent Simulation Engine 是一個以工程可執行性為核心的多智能體模擬框架，專門用來建構高複雜度、可擴展、具備成本意識的模擬世界。

它不是只停留在概念層的 white paper，也不是只能做單一場景 demo 的實驗腳手架。這個專案的目標，是提供一個能夠同時承載關鍵個體、高密度模板代理、原型群組與宏觀統計人口的統一模擬核心。

### 最適合拿來做什麼

- 市場與價格系統模擬
- 社會互動與群體行為推演
- 政策衝擊與制度回應建模
- 兼顧保真度與成本的多層級 agent world
- 作為公開展示的研究級 GitHub flagship repository

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
| Layered Agent World | 同一模擬世界中整合關鍵個體、模板代理、原型群組與統計人口 | Ready |
| Runnable Simulation Core | 內建 engine、router、memory、scheduler、world state | Ready |
| Scenario-Driven Design | 透過 YAML 場景配置切換不同模擬模式 | Ready |
| Cost-Aware Architecture | 把高成本推理聚焦在真正重要的角色與事件 | Ready |
| Extensible Adapters | 保留外部模型與真實服務接入路徑 | Partial |
| Replay and Analytics | 更完整的回放、評估與觀測層 | Planned |

---

## Visual Showcase

| Preview | Destination | Purpose |
|---|---|---|
| [![Architecture Banner](../images/universal-multi-agent-simulation-engine-architecture-banner.png)](../images/universal-multi-agent-simulation-engine-architecture-banner.png) | Banner | 首頁視覺主橫幅 |
| [![Architecture Overview](../images/architecture-overview-v2.png)](../images/architecture-overview-v2.png) | Overview Graphic | 整體架構預覽 |
| [![Architecture Detail](../images/architecture-detail-v2.png)](../images/architecture-detail-v2.png) | Detailed Graphic | 細部模組結構圖 |

> 這些圖片在 GitHub README 中都可以直接點擊放大或跳轉，屬於最常見也最有效的展示型首頁做法。

---

## Why This Project Matters

大多數 multi-agent 專案最後都會卡在同一個地方：

```text
如果每個 agent 都做得很聰明:
  -> 成本太高
  -> 推理太慢
  -> 難以擴展

如果全部都做成抽象群體:
  -> 失去個體差異
  -> 缺少行為層次
  -> 缺少可解釋性
```

這個引擎的核心價值，就是在兩者之間建立可落地的平衡：

```text
                High Fidelity Where It Matters
                             |
                             v
  +---------------------------------------------------------------+
  |  Layer 1  關鍵個體: 重要角色, 高價值決策, 深度互動            |
  |  Layer 2  模板代理: 可變規則, 成本低, 行為穩定               |
  |  Layer 3  原型群組: 群組級推進, 行為近似, 大幅節省計算         |
  |  Layer 4  統計人口: 宏觀分布, 社會背景, 系統級動態             |
  +---------------------------------------------------------------+
                             |
                             v
                   Scalable Simulation at Lower Cost
```

---

## Signature Highlights

| Highlight | Why it matters |
|---|---|
| Fidelity where it matters | 高保真能力只放在真正影響系統結果的角色與事件上 |
| Scale by design | 一開始就把規模與成本當成架構條件，不是事後補救 |
| Engineering over hype | 優先可執行、可測試、可維護，而不是只停留在概念展示 |
| Research-to-product bridge | 既可用於研究，也可作為未來產品平台骨架 |

---

## Visual Architecture

這份 README 刻意使用純文字可視化，不依賴外部渲染，在 GitHub 頁面上就能直接閱讀。

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
|  把高保真能力保留給真正重要的角色與事件                                             |
+----------------------------------------------------------------------------------+
|  Principle 2  Scale by design                                                    |
|  不是等系統變大才考慮擴展, 而是一開始就用分層模型設計規模路徑                       |
+----------------------------------------------------------------------------------+
|  Principle 3  Engineering over hype                                              |
|  優先可運行、可測試、可維護, 而不是只做概念展示                                    |
+----------------------------------------------------------------------------------+
|  Principle 4  Configurable worlds                                                |
|  讓場景知識進入配置層, 核心引擎保持通用                                             |
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
| Minimal | 最小可執行模擬迴圈 | Fast start |
| Market Ecosystem | 市場式互動與行為動態 | Economic simulation |
| Policy Shock | 制度變動與系統回應 | Policy modeling |
| Supply Chain Resilience | 干擾下的依賴與適應 | Resilience study |
| Showcase V2 | 展示型旗艦配置 | Homepage demo |

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

### 3. Install dependencies (安裝套件庫)

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables (設定金鑰)

```bash
cp .env.example .env
# 請打開 .env 檔案，並填入您的 GEMINI_API_KEY 以啟用最高等級推演
```

### 5. Launch the Universal Dashboard! (啟動控制台) 🔥

```bash
streamlit run app.py
```

---

## Configuration

場景切換的核心在 `configs/`。你可以透過配置調整系統行為，而不是直接修改引擎程式碼。

環境變數可參考 `.env.example`:

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

- 大規模社會互動模擬
- 市場、生產與供應鏈系統推演
- 政策衝擊與制度設計分析
- 組織、治理與群體決策研究
- 高保真與低成本兼顧的 agent simulation platform

---

## Engineering Status

這個專案目前不是空殼，而是一個已經具備可執行核心的 MVP。它適合：

- 作為研究原型繼續發展
- 作為 GitHub 展示型作品集首頁
- 作為更大型 simulation platform 的基礎骨架
- 作為未來串接真實 adapter 或外部模型的起點

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

這種排法會比單純列功能清單更像高品質旗艦專案。

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

公開發佈前，建議補上你要使用的授權條款，例如 MIT 或 Apache-2.0。
