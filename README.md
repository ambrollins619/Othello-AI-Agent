# Othello AI Game

### Overview

This project implements an AI-powered Othello (Reversi) game using the Minimax algorithm with optional Alpha-Beta pruning. The AI supports multiple heuristic functions for move evaluation and allows users to compare different heuristic strategies.

### Features

- **Minimax Algorithm**: Implements the standard Minimax strategy for AI decision-making.

- **Alpha-Beta Pruning**: Optimizes Minimax by reducing the number of nodes evaluated.

- **Multiple Heuristics**: Supports various heuristics such as mobility, stability, corner control, and hybrid heuristics.

- **Heuristic Comparison**: Simulates multiple games between different heuristics and visualizes results.

- **Pygame Interface**: Interactive GUI using Pygame for playing against AI or watching AI vs. AI battles.

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

1. Disk Parity Heuristic: The Disk Parity Heuristic evaluates the *difference in the number of disks between the player and the opponent*. It calculates the percentage difference relative to the total number of disks on the board. It provides a straightforward measure of dominance in terms of disk count.

2. Mobility Heuristic: The Mobility Heuristic assesses both *actual* and *potential* mobility for the player and the opponent. This heuristic aims to maximize the player's flexibility and options for future moves while restricting the opponent's options, thus maintaining strategic advantage.
    - *Actual mobility* refers to the number of legal moves available to the player.
    - *Potential mobility* refers to the number of potential moves (empty cells adjacent to the opponent's disks).

3. Corner Control Heuristic: The corner control heuristic evaluates the *control of corner squares* (A1, A8, H1, H8). It considers both the number of *corners occupied* and the *potential to occupy corners* (possible moves to corner positions). Controlling corners is highly advantageous in Othello as it provides stable positions that are difficult for the opponent to flip. This heuristic prioritizes securing these key positions.

4. Stability Heuristic: The stability heuristic evaluates the number of stable and unstable disks. This heuristic aims to *maximize the number of stable disks* while *minimizing the number of unstable disks*, ensuring a lasting advantage on the board.
    - *Stable disks* are those that cannot be flipped for the rest of the game.
    - *Unstable disks* are those that can be flipped at the next move of the opponent.

5. Hybrid Heuristic: The Hybrid Heuristic combines *multiple heuristics, including Disk Parity, Mobility, Corner Control, and Stability, with **weighted scores*. It aims to overcome the limitations of individual heuristics by integrating multiple factors for a more comprehensive evaluation of the board state. The current weights are the following :
- *Disk Parity Heuristic*: $({1 + ({number\_of\_disks \over 64})})^6$ This scales exponentially as the game progresses.
- *Mobility Heuristic*: 20
- *Corner Control Heuristic*: 50
- *Stability Heuristic*: 40


#### Heuristics Analysis

To test the performances of our heuristics, we decided to make our *MinMaxAgents* play against each others for *20 games* with *different heuristics* and with a *depth of 5*. The results are expressed as follow : (win/loss/draw) winrate

| Heuristics     | Disk Parity | Stability | Corner | Mobility | Hybrid |
|----------      |---------------|----------|----------|---------|------|
| Disk parity    | -   |  - | -  |-  | -   |
| Stability      | (*20/0/0) **100%*  | -   | -  | -    | -   |
| Corner         | (*12/8/0) **60%*  | (4/15/1) **20%*      | -       | -      | -   |
| Mobility       | (8/*10/2) **40%*  |(4/16/0) **20%* | (6/*14/0) **30%* | -   | -|
| Hybrid         | (*20/0/0) **100%*  | (*20/0/0) **100%* | (*18/2/0) **90%* | (*20/0/0) **100%*  | -   |

The results revealed interesting insights into each heuristic's performance. The Stability heuristic stood out as particularly promising, achieving a perfect win rate against all other heuristics except for the Corner heuristic, against which it still performed well but not flawlessly. This implies that the Corner heuristic's strategy of quickly securing corner positions can effectively disrupt Stability’s aim to establish stable disks. Disk Parity, as expected, performed poorly, demonstrating that having the most disks before the game's end is not necessarily an advantage. Instead, it provides more mobility to the opponent, allowing them to capture more pieces.

Finally, the Hybrid heuristic outperformed all other heuristics, showcasing the effectiveness of combining multiple evaluation criteria. These results indicate that a multifaceted approach provides a robust and adaptable strategy for Othello gameplay.


### Optimizations

Alpha-Beta Pruning: Reduces the number of nodes searched, improving performance.

