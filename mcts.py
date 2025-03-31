import time
import numpy as np
import random
from collections import defaultdict

class MCTSAgent:
    """
    Class for a Monte Carlo Tree Search (MCTS) Agent adapted for Othello game.
    """
    def __init__(self, player_id, time_limit=3, nb_iterations=1000, nb_rollouts=1, c_param=1.4, verbose=False):
        """
        Initializes the MCTSAgent with specified parameters.

        Parameters:
            player_id (int): 1 for black, -1 for white
            time_limit (float): The time limit for the MCTS search in seconds.
            nb_iterations (int): The number of iterations for the MCTS search.
            nb_rollouts (int): The number of rollouts for the MCTS search.
            c_param (float): The exploration parameter for the MCTS search.
            verbose (bool): If True, prints debug information during search.
        """
        self.id = player_id
        self.time_limit = time_limit
        self.nb_iterations = nb_iterations
        self.verbose = verbose
        self.c_param = c_param
        self.nb_rollouts = nb_rollouts
        self.player_type = 'ai'
        
        # Tree storage
        self.children = defaultdict(list)  # Maps nodes to their children
        self.node_info = defaultdict(dict)  # Stores visit counts and wins for nodes
        
    def copy(self):
        """
        Returns a new instance of MCTSAgent with the same parameters as the current instance.

        Returns:
            MCTSAgent: A new instance with the same parameters.
        """
        return MCTSAgent(
            player_id=self.id,
            time_limit=self.time_limit,
            nb_iterations=self.nb_iterations,
            c_param=self.c_param,
            nb_rollouts=self.nb_rollouts,
            verbose=self.verbose
        )
    
    def get_node_key(self, game_state):
        """
        Creates a unique key for a game state to use in the tree.
        """
        return tuple(map(tuple, game_state.board))
    
    def selection(self, game_state):
        """
        Selects a node to expand using UCB1.
        """
        node_key = self.get_node_key(game_state)
        
        # If node not in tree or has no children, return it
        if node_key not in self.node_info or not self.children[node_key]:
            return game_state.copy()
            
        # Use UCB1 to select best child
        log_parent_visits = np.log(self.node_info[node_key]['visits'])
        
        def ucb1(child_key):
            child_info = self.node_info[child_key]
            exploitation = child_info['wins'] / child_info['visits']
            exploration = self.c_param * np.sqrt(log_parent_visits / child_info['visits'])
            return exploitation + exploration
        
        best_child_key = max(self.children[node_key], key=ucb1)
        
        # Find the move that leads to the best child
        for move in game_state.valid_moves(game_state.current_player):
            new_state = game_state.copy()
            new_state.apply_move(move, new_state.current_player)
            new_state.current_player *= -1
            if self.get_node_key(new_state) == best_child_key:
                return self.selection(new_state)
                
        return game_state.copy()  # Fallback
    
    def expansion(self, game_state):
        """
        Expands the tree by adding a new child node.
        """
        node_key = self.get_node_key(game_state)
        
        # Initialize if not done already
        if 'untried_moves' not in self.node_info[node_key]:
            self.node_info[node_key]['untried_moves'] = list(game_state.valid_moves(game_state.current_player))
            self.node_info[node_key]['visits'] = 0
            self.node_info[node_key]['wins'] = 0
            
        # If no untried moves, return the current state
        if not self.node_info[node_key]['untried_moves']:
            return game_state.copy()
            
        # Select and remove a random untried move
        move = random.choice(self.node_info[node_key]['untried_moves'])
        self.node_info[node_key]['untried_moves'].remove(move)
        
        # Create new state
        new_state = game_state.copy()
        new_state.apply_move(move, new_state.current_player)
        new_state.current_player *= -1
        
        # Add to tree
        new_key = self.get_node_key(new_state)
        self.children[node_key].append(new_key)
        self.node_info[new_key]['visits'] = 0
        self.node_info[new_key]['wins'] = 0
        self.node_info[new_key]['untried_moves'] = None  # To be initialized when needed
        
        return new_state
    
    def simulation(self, game_state):
        """
        Performs a random simulation (rollout) from the given state.
        """
        current_state = game_state.copy()
        current_player = current_state.current_player
        
        while not current_state.is_game_over():
            possible_moves = list(current_state.valid_moves(current_state.current_player))
            if possible_moves:
                move = random.choice(possible_moves)
                current_state.apply_move(move, current_state.current_player)
            current_state.current_player *= -1
        
        # Determine the winner
        black_count = np.sum(current_state.board == 1)
        white_count = np.sum(current_state.board == -1)
        
        # Return the result from the perspective of the original player
        if current_player == 1:  # Black
            return 1 if black_count > white_count else (0.5 if black_count == white_count else 0)
        else:  # White
            return 1 if white_count > black_count else (0.5 if white_count == black_count else 0)
    
    def backpropagation(self, node_key, result):
        """
        Backpropagates the simulation result through the tree.
        """
        while node_key is not None:
            self.node_info[node_key]['visits'] += 1
            self.node_info[node_key]['wins'] += result
            result = 1 - result  # Alternate perspective for parent nodes
            
            # Find parent node
            parent_key = None
            for key, children in self.children.items():
                if node_key in children:
                    parent_key = key
                    break
            node_key = parent_key
    
    def timed_search(self, game_state):
        """
        Conducts a timed MCTS search to determine the best move.
        """
        root_key = self.get_node_key(game_state)
        best_move = None
        iterations = 0
        
        start_time = time.time()
        
        while time.time() - start_time < self.time_limit:
            # Selection
            selected_state = self.selection(game_state.copy())
            selected_key = self.get_node_key(selected_state)
            
            # Expansion
            expanded_state = self.expansion(selected_state.copy())
            expanded_key = self.get_node_key(expanded_state)
            
            # Simulation
            for _ in range(self.nb_rollouts):
                result = self.simulation(expanded_state.copy())
                # Backpropagation
                self.backpropagation(expanded_key, result)
            
            iterations += 1
        
        if self.verbose:
            print(f"Player {self.id} completed {iterations} iterations in {time.time()-start_time:.2f}s")
        
        # Select best move (most visited)
        if root_key not in self.children or not self.children[root_key]:
            return None  # No valid moves
        
        # Find the child with most visits
        best_child_key = max(self.children[root_key], key=lambda k: self.node_info[k]['visits'])
        
        # Find the move that leads to the best child
        for move in game_state.valid_moves(game_state.current_player):
            new_state = game_state.copy()
            new_state.apply_move(move, new_state.current_player)
            new_state.current_player *= -1
            if self.get_node_key(new_state) == best_child_key:
                best_move = move
                break
                
        return best_move
    
    def get_move(self, game, events=None):
        """
        Determines the best move for the player using the MCTS algorithm.

        Parameters:
            game (Othello): The current game state.
            events: Ignored, kept for compatibility.

        Returns:
            tuple: The best move (row, col) for the player.
        """
        if self.time_limit is not None:
            best_move = self.timed_search(game)
        else:
            # Fallback to iterative search if no time limit (not recommended)
            best_move = None
            root_key = self.get_node_key(game)
            
            for _ in range(self.nb_iterations):
                # Selection
                selected_state = self.selection(game.copy())
                selected_key = self.get_node_key(selected_state)
                
                # Expansion
                expanded_state = self.expansion(selected_state.copy())
                expanded_key = self.get_node_key(expanded_state)
                
                # Simulation
                for _ in range(self.nb_rollouts):
                    result = self.simulation(expanded_state.copy())
                    # Backpropagation
                    self.backpropagation(expanded_key, result)
            
            # Select best move (most visited)
            if root_key in self.children and self.children[root_key]:
                best_child_key = max(self.children[root_key], key=lambda k: self.node_info[k]['visits'])
                
                # Find the move that leads to the best child
                for move in game.valid_moves(game.current_player):
                    new_state = game.copy()
                    new_state.apply_move(move, new_state.current_player)
                    new_state.current_player *= -1
                    if self.get_node_key(new_state) == best_child_key:
                        best_move = move
                        break
            
            if self.verbose:
                print(f"Player {self.id} completed {self.nb_iterations} iterations")
        
        return best_move