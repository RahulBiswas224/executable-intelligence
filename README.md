# 🤖 Executable Intelligence
### Reinforcement Learning meets Large Language Models: Enabling Autonomous Navigation

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![PPO](https://img.shields.io/badge/Algorithm-PPO-orange?style=for-the-badge)
![Gymnasium](https://img.shields.io/badge/Environment-Gymnasium-green?style=for-the-badge)
![Tkinter](https://img.shields.io/badge/UI-Tkinter-lightblue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

**A hybrid AI system where a Large Language Model understands human commands and a Reinforcement Learning agent physically executes them — in real time.**

</div>

---

## 📌 What is this project?

Traditional navigation systems like Dijkstra's Algorithm are **static** — they cannot understand human language or adapt to changing goals. This project solves that by combining two AI systems:

| Component | Role | Technology |
|-----------|------|------------|
| 🧠 **LLM Planner** | Reads natural language → extracts destination coordinates | Python keyword extractor (simulating LLM behaviour) |
| 🦾 **RL Agent** | Navigates the grid autonomously using a trained neural network | PPO (Proximal Policy Optimization) via Stable Baselines 3 |
| 🗺️ **Environment** | 10×10 grid world with dynamic goal setting | Gymnasium |
| 🖥️ **Dashboard** | Real-time visualization of agent movement | Tkinter |

**Example:** You type → *"The battery is low, find the charging station"*
The system extracts **"charging station"** → sets goal to **[9, 9]** → the agent navigates there autonomously. ✅

---

## 🎬 Demo

```
User types:   "Move the agent to the warehouse"
LLM extracts: warehouse → [2, 8]
RL Agent:     navigates step by step from [0,0] to [2,8]
Result:       ✅ Goal Reached Successfully
```

The agent moves live on a canvas — you can watch every step in real time.

---

## 🗂️ Project Structure

```
executable-intelligence/
│
├── 📄 main.py                  # Entry point — Tkinter UI + main execution loop
├── 📄 train_agent.py           # PPO training script
│
├── 🧠 brain/
│   ├── __init__.py
│   ├── llm_planner.py          # Natural language → coordinate mapping
│   └── rl_agent.py             # PPO model loader + action predictor
│
├── 🌍 environment/
│   ├── __init__.py
│   └── simulator.py            # Gymnasium 10×10 grid environment
│
├── 🛠️ utils/
│   ├── __init__.py
│   └── logger.py               # Timestamped event logger
│
└── 📦 assets/
    └── models/
        └── rl_model_v1.zip     # Pre-trained PPO model
```

---

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/RahulBiswas224/executable-intelligence.git
cd executable-intelligence
```

### 2. Install dependencies
```bash
pip install stable-baselines3 gymnasium numpy
```

### 3. Run the application
```bash
python main.py
```

A desktop window opens. Type a command and click **Execute Command**.

---

## 🗺️ Available Locations

| Location | Coordinates | Example Command |
|----------|-------------|-----------------|
| Warehouse | [2, 8] | *"Go to the warehouse"* |
| Charging Station | [9, 9] | *"The battery is low, find the charging station"* |
| Entry Gate | [0, 0] | *"Move to the entry gate"* |
| Sorting Area | [5, 5] | *"Navigate to the sorting area"* |
| Office | [1, 1] | *"I left my coffee in the office"* |
| Emergency Exit | [0, 9] | *"Security alert near the emergency exit!"* |
| Manager Desk | [7, 2] | *"Take these documents to the manager desk"* |

---

## 🔁 System Architecture

```
┌─────────────────┐     Natural Language      ┌──────────────────┐
│   User Input    │ ────────────────────────► │   LLM Planner    │
│ (Tkinter UI)    │                           │  llm_planner.py  │
└─────────────────┘                           └────────┬─────────┘
                                                       │ Coordinates [x, y]
                                                       ▼
┌─────────────────┐     Action (0-3)          ┌──────────────────┐
│  Gymnasium Env  │ ◄──────────────────────── │    RL Agent      │
│  simulator.py   │                           │   rl_agent.py    │
│                 │ ──── Observation ────────► │  (PPO Model)     │
└────────┬────────┘    [cx, cy, gx, gy]       └──────────────────┘
         │
         │ State update
         ▼
┌─────────────────┐
│  Tkinter Canvas │  ← Real-time visualization
│  (Live render)  │
└─────────────────┘
```

---

## 🏋️ Training the Agent

To retrain the PPO model from scratch:
```bash
python train_agent.py
```

Training config:
```python
model = PPO(
    "MlpPolicy",
    env,
    learning_rate = 0.0003,
    n_steps       = 2048,
    ent_coef      = 0.01,    # Encourages exploration
    batch_size    = 64,
    n_epochs      = 10,
    total_timesteps = 50000
)
```

Monitor training with TensorBoard:
```bash
tensorboard --logdir ./assets/logs/
```

Training takes **~2 minutes** on a standard laptop CPU. The model is saved to `assets/models/rl_model_v1.zip`.

---

## 🧠 How the RL Agent Learns

The agent is trained on a **Markov Decision Process (MDP)**:

- **State:** `[current_x, current_y, goal_x, goal_y]` — 4 integers (0–9)
- **Actions:** 4 discrete moves — `UP(0)`, `DOWN(1)`, `LEFT(2)`, `RIGHT(3)`
- **Reward:** `+10` when goal is reached | `-0.1 × distance` per step (encourages shortest path)
- **Algorithm:** PPO (Proximal Policy Optimization) — Actor-Critic neural network

---

## 🔭 Future Scope

- [ ] **Dynamic Obstacle Avoidance** — Train agent to navigate around moving barriers
- [ ] **Live LLM API** — Replace keyword extractor with OpenAI/Gemini API for true semantic understanding
- [ ] **Online Learning** — Agent continues learning post-deployment without full retraining
- [ ] **Multi-Agent Coordination** — Fleet of robots coordinating in the same grid (MARL)
- [ ] **3D Continuous Environments** — Upgrade from 2D grid to MuJoCo/Isaac Gym physics simulation
- [ ] **Conversational Planning** — Multi-turn dialogue for ambiguous instructions

---

## 📚 References

1. Schulman et al. (2017) — *Proximal Policy Optimization Algorithms* — OpenAI
2. Farama Foundation (2023) — *Gymnasium: An Open-Source Python Library for RL*
3. Vaswani et al. (2017) — *Attention is All You Need* — Foundation of LLMs
4. Ahn et al. (2022) — *Do As I Can, Not As I Say: Grounding Language in Robotic Affordances (SayCan)* — Google

---

## 👨‍💻 Team

| Name | Roll Number | Role |
|------|-------------|------|
| **Rahul Biswas** | BWU/BCA/23/224 | Lead Developer |
| **Sourav** | BWU/BCA/23/234 | Member |
| **Arpita** | BWU/BCA/23/190 | Member |

**Department of Computational Sciences**
**Brainware University** — BCA 6th Semester Project

---

## 📄 License

This project is licensed under the MIT License — free to use, modify, and distribute with attribution.

---

<div align="center">
  <b>⭐ If this project helped you, give it a star on GitHub! ⭐</b>
</div>