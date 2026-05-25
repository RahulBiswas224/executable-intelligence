import sys
import os
import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import numpy as np

# Ensure local modules are discoverable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from environment.simulator import ExecutableIntelligenceEnv
from brain.llm_planner import LLMPlanner
from brain.rl_agent import RLAgent

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Executable Intelligence v1.0")
        self.geometry("600x700")
        self.configure(bg="#f0f0f0")

        # 1. Initialize Modules
        self.env = ExecutableIntelligenceEnv()
        self.planner = LLMPlanner()
        self.agent = RLAgent()

        # 2. UI Elements - Canvas
        self.canvas = tk.Canvas(self, width=400, height=400, bg="#ffffff", highlightthickness=1, highlightbackground="#ccc")
        self.canvas.pack(pady=20)
       # --- MAP LEGEND PANEL ---
        # Positioned to the right of the canvas
        self.legend_frame = tk.Frame(self, bg="#2c3e50", bd=2, relief="groove")
        self.legend_frame.place(x=360, y=20, width=200, height=400)
        
        tk.Label(self.legend_frame, text="MAP LEGEND", font=("Arial", 10, "bold"), 
                 bg="#2c3e50", fg="#ecf0f1").pack(pady=10)
        
        # Pull locations directly from the planner
        for loc, coord in self.planner.locations.items():
            # Formatting: "Warehouse: [2, 8]"
            display_text = f"{loc.title()}:{coord}"
            
            lbl = tk.Label(self.legend_frame, text=display_text, font=("Consolas", 9), 
                           bg="#2c3e50", fg="#bdc3c7", justify="left")
            lbl.pack(pady=5, anchor="w", padx=10)
        # ---------------------------------------------------
        
        # UI Elements - Input
        self.entry = tk.Entry(self, width=50, font=("Arial", 12))
        self.entry.pack(pady=10)
        self.entry.insert(0, "Move the agent to the warehouse")

        # UI Elements - Button (Uses threading to prevent UI freezing)
        self.btn = tk.Button(self, text="Execute Command", command=self.run_thread, 
                             bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=20)
        self.btn.pack(pady=5)

        # UI Elements - Terminal Log
        self.log = scrolledtext.ScrolledText(self, width=70, height=10, bg="#222", fg="#0f0", font=("Consolas", 10))
        self.log.pack(pady=20)

        # Initial Render
        self.render_env()

    def render_env(self):
        self.canvas.delete("all")
        cell_size = 40
        
        # Draw Agent (Blue Square)
        x, y = self.env.state
        # Use simple mapping first to see if it fixes the 'sticking'
        self.canvas.create_rectangle(x*cell_size, (9-y)*cell_size, 
                                     (x+1)*cell_size, (9-y+1)*cell_size, 
                                     fill="#2196F3")
        
        # Draw Goal (Red Circle)
        gx, gy = self.env.goal
        self.canvas.create_oval(gx*cell_size+10, (9-gy)*cell_size+10, 
                                (gx+1)*cell_size-10, (9-gy+1)*cell_size-10, 
                                fill="#FF5252")


    def run_thread(self):
        """Starts the logic in a background thread so the GUI stays responsive."""
        thread = threading.Thread(target=self.execute_logic, daemon=True)
        thread.start()

    def execute_logic(self):
        """The core loop: LLM Plans, then RL Executes."""
        # A. Planning Phase
        command = self.entry.get()
        if not command.strip():
            return

        self.log.insert(tk.END, f"[LLM] Parsing: {command}...\n")
        self.log.see(tk.END)
        
        # Get coordinates from LLM and update the environment goal
        target_coords = self.planner.get_coordinates(command)
        if target_coords is None:
            self.log.insert(tk.END, f"[ERROR] Could not find location for: '{command}'\n")
            self.log.see(tk.END)
            return
        self.env.goal = np.array(target_coords)
        
        self.log.insert(tk.END, f"[LLM] Target Set to: {target_coords}\n")
        self.log.see(tk.END)

        # B. Execution Phase
        print(f"[System] Starting movement to {target_coords}...")
        
        done = False
        while not done:
            current_pos = self.env.state
            target_pos = self.env.goal

            # 1. Exit condition: Are we at the target?
            if np.array_equal(current_pos, target_pos):
                done = True
                break

            # 2. Get action from RL Brain (Concatenates 4-input state inside)
            action = self.agent.predict_action(current_pos, target_pos)
            # action = 3
            # 3. Move the agent in the simulator
            self.env.step(action)
            print(f"Action Taken: {action} | Current Pos: {self.env.state}")

            # 4. Refresh the Canvas
            self.after(0, self.render_env)
            
            # 5. Sleep to make the movement visible
            time.sleep(0.15) 

        self.log.insert(tk.END, "[SYSTEM] Executable Goal Reached Successfully.\n---\n")
        self.log.see(tk.END)

if __name__ == "__main__":
    app = App()
    app.mainloop()