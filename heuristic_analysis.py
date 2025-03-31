import numpy as np
from collections import defaultdict
from itertools import combinations
import time
from main import  Othello
# Assuming you have these heuristics and MinMaxPlayer implemented
from heuristics import coin_parity_heuristic, stability_heuristic, corner_heuristic, mobility_heuristic, hybrid_heuristic
from minmax import MinMaxPlayer
from player import Player
import random

class HeuristicAnalysis:
    def __init__(self, heuristics, depth=5, games_per_match=20):
        self.heuristics = heuristics
        self.depth = depth
        self.games_per_match = games_per_match
        self.results = {}

    def run_match(self, heuristic1, heuristic2):
        wins, losses, draws = 0, 0, 0
        
        # Random opening position games
        for _ in range(self.games_per_match ):
            # opening = self.create_random_opening(self.random_openings)
            
            # Randomize who gets which heuristic
            p1 = MinMaxPlayer(1, heuristic1, self.depth)
            p2 = MinMaxPlayer(-1, heuristic2, self.depth)

            result = Othello(p1, p2, True).play()
            
            # Count results from heuristic1's perspective
            if ((p1.heuristic_function == heuristic1 and result == 1) or 
                (p2.heuristic_function == heuristic1 and result == -1)):
                wins += 1
            elif result == 0:
                draws += 1
            else:
                losses += 1
        
        return wins, losses, draws

    def run_analysis(self):
        heuristic_names = list(self.heuristics.keys())
        self.results = {h: {h2: None for h2 in heuristic_names} for h in heuristic_names}
        
        for h1, h2 in combinations(heuristic_names, 2):
            print(f"Testing {h1} vs {h2}...")
            start = time.time()
            
            wins, losses, draws = self.run_match(self.heuristics[h1], self.heuristics[h2])
            self.results[h1][h2] = (wins, losses, draws)
            self.results[h2][h1] = (losses, wins, draws)
            
            print(f"Completed in {time.time()-start:.2f}s: {wins}W/{losses}L/{draws}D")

# Example usage
heuristics = {
    "Disk parity": coin_parity_heuristic,
    "Stability": stability_heuristic,
    "Corner": corner_heuristic,
    "Mobility": mobility_heuristic,
    "Hybrid": hybrid_heuristic
}

analysis = HeuristicAnalysis(heuristics, depth=5, games_per_match=20)
analysis.run_analysis()