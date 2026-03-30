import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

class CognitiveAgent(Agent):
    """
    A 'Cognitive Generative Agent' with heterogeneous personalities (Cautious, Skeptic, Socialite).
    Uses BDI-inspired reasoning and memory to make decisions.
    """
    def __init__(self, model, unique_id, personality, initial_health=False):
        super().__init__(model)
        self.unique_id = unique_id
        self.personality = personality  # "Cautious", "Skeptic", or "Socialite"
        
        # 1. Memory: List of past experiences
        self.memory = []
        
        # 2. Beliefs: Internal state & perceived environment
        self.beliefs = {
            "infected": initial_health,
            "perceived_risk": 0.1 if personality != "Cautious" else 0.3,
            "neighbors_infected_count": 0,
            "social_signals": []
        }
        
        # 3. Desires: Goals based on personality
        if personality == "Cautious":
            self.desires = {"stay_safe": 0.8, "socialize": 0.2}
        elif personality == "Skeptic":
            self.desires = {"stay_safe": 0.2, "socialize": 0.8}
        else:  # Socialite
            self.desires = {"stay_safe": 0.4, "socialize": 0.9}
        
        # 4. Intentions
        self.intention = "wander"

    def retrieve_memory(self, keywords):
        relevant_memories = [m for m in self.memory if any(k in m.lower() for k in keywords)]
        return relevant_memories[-3:]

    def mock_llm_reasoning(self):
        """Advanced reasoning influenced by personality and social signals."""
        risk_score = self.beliefs["perceived_risk"]
        
        # Neighbors influence risk
        if self.beliefs["neighbors_infected_count"] > 0:
            increment = 0.2 if self.personality != "Skeptic" else 0.05
            risk_score += increment * self.beliefs["neighbors_infected_count"]
        
        # Social signals influence risk based on personality
        for signal in self.beliefs["social_signals"]:
            if "high" in signal.lower():
                risk_score += 0.15 if self.personality != "Skeptic" else 0.02
            elif "safe" in signal.lower():
                risk_score -= 0.1 if self.personality != "Cautious" else 0.02
        
        self.beliefs["social_signals"] = [] # Clear for next step
        risk_score = max(0.0, min(1.0, risk_score))
        
        # Decision weights
        safety_priority = self.desires["stay_safe"] * risk_score
        social_priority = self.desires["socialize"] * (1 - risk_score)
        
        if safety_priority > social_priority:
            return "stay_home" if risk_score > 0.7 else "wear_mask"
        return "wander"

    def step(self):
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
        self.beliefs["neighbors_infected_count"] = sum(1 for n in neighbors if n.beliefs["infected"])
        
        self.intention = self.mock_llm_reasoning()
        
        if self.intention != "stay_home":
            self.move()
            
        self.interact(neighbors)
        self.reflect()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def interact(self, neighbors):
        # Communication
        for neighbor in neighbors:
            msg = "Risk is high" if self.beliefs["perceived_risk"] > 0.5 else "Safe to go out"
            neighbor.receive_message(self.unique_id, msg)
            
        # Infection
        if self.beliefs["infected"]:
            for neighbor in neighbors:
                chance = 0.4 if neighbor.intention != "wear_mask" else 0.05
                if random.random() < chance:
                    neighbor.get_infected()

    def receive_message(self, sender_id, message):
        self.memory.append(f"Communication: Heard '{message}' from agent {sender_id}.")
        self.beliefs["social_signals"].append(message)

    def get_infected(self):
        if not self.beliefs["infected"]:
            self.beliefs["infected"] = True
            self.memory.append("Event: I am infected. My priorities have shifted.")
            self.beliefs["perceived_risk"] = 1.0
            self.desires = {"stay_safe": 1.0, "socialize": 0.0}

    def reflect(self):
        status = "infected" if self.beliefs["infected"] else "healthy"
        mem = f"Step {self.model.schedule.steps}: Intention={self.intention}, Status={status}."
        self.memory.append(mem)
        
        # Risk decay or growth
        if self.beliefs["neighbors_infected_count"] == 0:
            self.beliefs["perceived_risk"] = max(0.05, self.beliefs["perceived_risk"] - 0.02)
        else:
            self.beliefs["perceived_risk"] = min(1.0, self.beliefs["perceived_risk"] + 0.05)

class PandemicModel(Model):
    def __init__(self, N, width, height, initial_infected=2):
        super().__init__()
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        
        personalities = ["Cautious", "Skeptic", "Socialite"]
        for i in range(N):
            pers = random.choice(personalities)
            is_inf = (i < initial_infected)
            a = CognitiveAgent(self, i, pers, initial_health=is_inf)
            self.schedule.add(a)
            self.grid.place_agent(a, (random.randrange(width), random.randrange(height)))

    def step(self):
        self.schedule.step()
        self.render_grid()

    def render_grid(self):
        """ASCII visualization of the simulation state."""
        print(f"\n--- Step {self.schedule.steps} ---")
        grid_repr = ""
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                agents = self.grid.get_cell_list_contents((x, y))
                if not agents:
                    grid_repr += ". "
                else:
                    a = agents[0]
                    if a.beliefs["infected"]:
                        grid_repr += "I "
                    elif a.intention == "wear_mask":
                        grid_repr += "M "
                    else:
                        grid_repr += "H "
            grid_repr += "\n"
        print(grid_repr)

if __name__ == "__main__":
    N_AGENTS = 25
    model = PandemicModel(N=N_AGENTS, width=10, height=10)
    
    for _ in range(15):
        model.step()
        inf = sum(1 for a in model.schedule.agents if a.beliefs["infected"])
        print(f"Total Infected: {inf}/{N_AGENTS}")

    print("\n--- Personality Breakdown ---")
    stats = {}
    for a in model.schedule.agents:
        if a.personality not in stats:
            stats[a.personality] = {"total": 0, "infected": 0}
        stats[a.personality]["total"] += 1
        if a.beliefs["infected"]:
            stats[a.personality]["infected"] += 1
    
    for p, s in stats.items():
        rate = (s["infected"] / s["total"]) * 100
        print(f"{p}: {s['infected']}/{s['total']} infected ({rate:.1f}%)")
