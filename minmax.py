import numpy as np
import pygame
import random
from player import Player

class MinMaxPlayer(Player):
    def __init__(self, color, heuristic_function, depth=3):
        super().__init__('minmax', color)
        self.depth = depth
        self.heuristic_function = heuristic_function  # Heuristic function parameter

    def get_move(self, game):
        _, best_move = self.minimax(game, self.depth, float('-inf'), float('inf'), True)
        return best_move

    def minimax(self, game, depth, alpha, beta, maximizing):
        if depth == 0 or game.is_game_over():
            return self.heuristic_function(game, self.color), None

        valid_moves = list(game.valid_moves(self.color if maximizing else -self.color))
        if not valid_moves:
            return self.minimax(game, depth - 1, alpha, beta, not maximizing)[0], None

        best_move = None
        if maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                new_game = game.copy()
                new_game.apply_move(move, self.color)
                eval_score, _ = self.minimax(new_game, depth - 1, alpha, beta, False)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move

                alpha = max(alpha, eval_score)
                if alpha >= beta:  # Alpha-beta pruning
                    break

            return max_eval, best_move

        else:
            min_eval = float('inf')
            for move in valid_moves:
                new_game = game.copy()
                new_game.apply_move(move, -self.color)
                eval_score, _ = self.minimax(new_game, depth - 1, alpha, beta, True)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move

                beta = min(beta, eval_score)
                if beta <= alpha:  # Alpha-beta pruning
                    break

            return min_eval, best_move
