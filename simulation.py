import numpy as np
import pygame
import random
import itertools
import matplotlib.pyplot as plt
from player import Player
from main import Othello
from minmax import MinMaxPlayer  # Assuming you saved your MinMaxPlayer class
from heuristics import coin_parity_heuristic, mobility_heuristic, corner_heuristic, stability_heuristic, hybrid_heuristic

# List of heuristics
heuristics = {
    "Disk Parity": coin_parity_heuristic,
    "Mobility": mobility_heuristic,
    "Corner": corner_heuristic,
    "Stability": stability_heuristic,
    "Hybrid": hybrid_heuristic
}

# Store results
results = {heuristic: 0 for heuristic in heuristics.keys()}  # Wins count

# Simulate games between all heuristic pairs
num_games = 5  # Number of games per heuristic pair

for (heuristic1, func1), (heuristic2, func2) in itertools.combinations(heuristics.items(), 2):
    print(f"Playing {num_games} games: {heuristic1} vs {heuristic2}")

    for _ in range(num_games):
        player1 = MinMaxPlayer(1, heuristic_function=func1)
        player2 = MinMaxPlayer(-1, heuristic_function=func2)
        game = Othello(player1, player2)
        winner = game.play()  # Assuming play() returns the winner (1 or -1)

        if winner == 1:
            results[heuristic1] += 1
        elif winner == -1:
            results[heuristic2] += 1

# Plot the results

plt.figure(figsize=(10, 6))
plt.bar(results.keys(), results.values(), color=['blue', 'green', 'red', 'purple', 'orange'])
plt.xlabel("Heuristic")
plt.ylabel("Number of Wins")
plt.title("Performance of Heuristics (Higher is Better)")
plt.show()