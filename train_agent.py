import os
import gymnasium as gym
from stable_baselines3 import PPO
from environment.simulator import ExecutableIntelligenceEnv

def train():
    # 1. Initialize Environment
    env = ExecutableIntelligenceEnv()

    # 2. Define Model with Exploration Boost
    # ent_coef: Higher value (0.01) forces the agent to explore more 
    # instead of just bouncing in one spot.
    model = PPO(
        "MlpPolicy", 
        env, 
        verbose=1, 
        tensorboard_log="./assets/logs/",
        learning_rate=0.0003,
        n_steps=2048,
        ent_coef=0.01,  
        batch_size=64,
        n_epochs=10
    )

    print("--- Training Started: Executable Intelligence Phase ---")
    
    # 3. Increased Training Steps
    # For a 10x10 grid with dynamic goals, 50,000 steps ensures 
    # the agent learns the relation between its position and the goal.
    model.learn(total_timesteps=50000)

    # 4. Save Intelligence
    model_dir = "assets/models"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "rl_model_v1")
    model.save(model_path)
    
    print(f"--- Training Complete ---")
    print(f"New Brain Saved: {model_path}.zip")

if __name__ == "__main__":
    train()