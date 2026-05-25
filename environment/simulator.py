import gymnasium as gym
from gymnasium import spaces
import numpy as np

class ExecutableIntelligenceEnv(gym.Env):
    def __init__(self, size=10):
        super().__init__()
        self.size = size
        self.action_space = spaces.Discrete(4) 
        self.observation_space = spaces.Box(low=0, high=size-1, shape=(4,), dtype=np.int32)


        self.state = np.array([0, 0], dtype=np.int32)
        self.goal = np.array([size-1, size-1], dtype=np.int32)

    def _get_obs(self):
        return np.concatenate([self.state, self.goal]).astype(np.int32)
 
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = np.array([0, 0], dtype=np.int32)
        return self._get_obs(), {}

    def step(self, action):
        # Ensure we are working with standard integers for logic
        action = int(action)
        
        # 0: UP, 1: DOWN, 2: LEFT, 3: RIGHT
        if action == 0 and self.state[1] < self.size - 1:
            self.state[1] += 1
        elif action == 1 and self.state[1] > 0:
            self.state[1] -= 1
        elif action == 2 and self.state[0] > 0:
            self.state[0] -= 1
        elif action == 3 and self.state[0] < self.size - 1:
            self.state[0] += 1

        # Check if goal reached
        done = bool(np.array_equal(self.state, self.goal))
        
        # Reward structure
        if done:
            reward = 10.0
        else:
            # Manhattan distance penalty (encourages moving TOWARDS goal)
            dist = np.linalg.norm(self.state - self.goal)
            reward = -0.1 * dist 

        return self._get_obs().copy(), reward, done, False, {}