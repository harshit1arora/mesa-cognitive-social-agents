# Mesa-Cognitive: Generative Agents for Social Simulation

[![Mesa](https://img.shields.io/badge/Mesa-3.0%2B-blue.svg)](https://github.com/projectmesa/mesa)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![GSoC](https://img.shields.io/badge/GSoC-2026-orange.svg)](https://summerofcode.withgoogle.com/)

## Project Overview

**Mesa-Cognitive** is a high-fidelity prototype designed for a **Google Summer of Code (GSoC)** proposal. It bridges the gap between traditional **Agent-Based Modeling (ABM)** and modern **Generative AI** by introducing "Cognitive Agents" into the Mesa framework.

Unlike standard rule-based agents (if-then logic), these agents utilize a **BDI (Belief-Desire-Intention)** architecture paired with a **semantic memory system** to make complex, context-aware decisions in a pandemic simulation.

---

## Key Features

### 1. Cognitive BDI Architecture
Agents operate on a sophisticated reasoning loop:
- **Beliefs**: Internal state (health) and environmental perception (neighbor infection counts).
- **Desires**: High-level goals (Stay Safe vs. Socialize) that dynamically compete.
- **Intentions**: Concrete actions chosen via a "Mock LLM" reasoning engine that weighs beliefs and past memories.

### 2. Heterogeneous Personalities
The population is not a monolith. Emergent behavior is driven by three distinct personality types:
- **🛡️ Cautious**: Risk-averse, early adopters of masks, highly responsive to social warnings.
- **🤨 Skeptic**: Risk-dismissive, prioritizes social freedom, requires significant evidence to change behavior.
- **💃 Socialite**: High social drive, likely to maintain interaction even when risk is perceived.

### 3. Semantic Memory & Social Influence
- **Memory Logs**: Agents store past interactions, infection events, and social messages.
- **Social Feedback Loop**: Agents broadcast "Social Signals" (e.g., "Risk is high") that propagate through the grid, influencing the collective risk perception of the population.

### 4. Real-time ASCII Visualization
A lightweight render engine provides immediate visual feedback of the simulation state directly in the terminal.

---

## Technical Implementation

- **Framework**: [Mesa 3.0+](https://mesa.readthedocs.io/) (utilizing the latest `Agent` and `Model` standards).
- **Language**: Python 3.10+.
- **Visualization**: Custom ASCII Grid Render.
- **Reasoning**: Deterministic "Mock LLM" function simulating LLM prompt-response behavior for performance and cost-efficiency.

---

## How to Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/mesa-cognitive.git
   cd mesa-cognitive
   ```

2. **Install Dependencies**:
   ```bash
   pip install mesa
   ```

3. **Execute the Simulation**:
   ```bash
   python pandemic_sim.py
   ```

---

## Sample Output

During execution, you will see a live-updating grid:
- `.` : Empty Space
- `H` : Healthy Agent
- `M` : Masked Agent (Cognitive decision)
- `I` : Infected Agent

At the end of the simulation, a **Personality Breakdown** is provided to analyze the epidemiological impact of different cognitive traits.

---

## GSoC Proposal Context

This project serves as a proof-of-concept for the proposal: **"Integrating LLM-Driven Cognitive Architectures into Mesa for Advanced Social Simulation"**. 

**Planned Enhancements for GSoC:**
- [ ] Integration with real LLM APIs (OpenAI/Anthropic/Local LLMs).
- [ ] Vector database integration (ChromaDB/FAISS) for advanced memory retrieval.
- [ ] Interactive Solara-based dashboard for real-time data visualization.
- [ ] Sophisticated reflection steps for recursive agent learning.

---

## License
MIT License. See `LICENSE` for details.
