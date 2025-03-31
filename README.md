# Othello AI Game

### Overview

This project implements an AI-powered Othello (Reversi) game using the Minimax algorithm with optional Alpha-Beta pruning. The AI supports multiple heuristic functions for move evaluation and allows users to compare different heuristic strategies.

### Features

Minimax Algorithm: Implements the standard Minimax strategy for AI decision-making.

Alpha-Beta Pruning: Optimizes Minimax by reducing the number of nodes evaluated.

Multiple Heuristics: Supports various heuristics such as mobility, stability, corner control, and hybrid heuristics.

Heuristic Comparison: Simulates multiple games between different heuristics and visualizes results.

Pygame Interface: Interactive GUI using Pygame for playing against AI or watching AI vs. AI battles.

### Installation

Prerequisites

Ensure you have Python installed (Python 3.7+ recommended). Then, install the required dependencies:
```
pip install numpy pygame numba matplotlib
```

## Usage

Running the Game

To start the game with AI players using different heuristics:
```
python main.py
```
You can modify main.py to test different AI strategies.

### Customizing AI Players

You can initialize the AI with a specific heuristic function:
```
player1 = MinMaxPlayer(1, mobility_heuristic, depth=3)
player2 = MinMaxPlayer(-1, stability_heuristic, depth=3)
game = Othello(player1, player2)
game.play()
```

### Running Heuristic Comparisons

To compare heuristics using simulations:
```
python heuristic_comparison.py
```
This will run multiple games between different heuristic pairs and generate a performance plot.

### Heuristics Implemented

Disk Parity - Evaluates the difference in disk counts.

Mobility - Measures the number of valid moves available.

Corner Control - Rewards controlling stable corner positions.

Stability - Differentiates stable and unstable disks.

Hybrid Heuristic - A weighted combination of the above heuristics.

### Optimizations

Alpha-Beta Pruning: Reduces the number of nodes searched, improving performance.