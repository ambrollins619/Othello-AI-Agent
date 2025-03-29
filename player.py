import random


class Player:
    def __init__(self, player_type, color):
        self.player_type = player_type  # 'human' or 'ai'
        self.color = color

    def get_move(self, game):
        if self.player_type == 'human':
            return None  # Human player will select via UI
        elif self.player_type == 'ai':
            valid_moves = list(game.valid_moves(self.color))
            return random.choice(valid_moves) if valid_moves else None