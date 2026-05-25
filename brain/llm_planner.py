import json

class LLMPlanner:
    def __init__(self):
        # In a real scenario, initialize your API client here (e.g., OpenAI/Groq)
        self.locations = {
            "warehouse": [2, 8],
            "charging station": [9, 9],
            "entry gate": [0, 0],
            "sorting area": [5, 5],
            "office": [1, 1],       
            "emergency exit": [0, 9], 
            "manager desk": [7, 2]
        }

    def get_coordinates(self, prompt):
        # Convert user input to lowercase to prevent matching errors
        clean_prompt = prompt.lower().strip()
        
        for loc, coords in self.locations.items():
            if loc in clean_prompt:
                return coords
        
        # Default to current position if nothing is found 
        # (This prevents the agent from running to [0,0] by mistake)
        return None