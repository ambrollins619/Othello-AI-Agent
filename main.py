import numpy as np
import pygame
import random
import copy
from player import Player
from minmax import MinMaxPlayer
from heuristics import coin_parity_heuristic, mobility_heuristic, corner_heuristic, stability_heuristic, hybrid_heuristic
from mcts import MCTSAgent

class Othello:
    def __init__(self, player1, player2, isopeningRandom = False):
        pygame.init()
        pygame.font.init()
        self.board = np.zeros((8, 8), dtype=int)  # 0 = empty, 1 = black, -1 = white
        if not isopeningRandom:
            self.board[3, 3], self.board[4, 4] = -1, -1  # Initial white pieces
            self.board[3, 4], self.board[4, 3] = 1, 1    # Initial black pieces
        
        else :
            self.board = self.create_random_opening().board
            
        self.players = {1: player1, -1: player2}
        self.current_player = 1  # Black starts
        self.cell_size = 60
        self.width = self.cell_size * 8
        self.height = self.cell_size * 8 + 40  # Extra space for text
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Othello")
        self.running = True
        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)
        
    def create_random_opening(self, moves=4):
        """Create a random opening position by playing random moves"""
        game = Othello(Player('random', 1), Player('random', -1))
        for _ in range(moves):
            valid_moves = game.valid_moves(game.current_player)
            if valid_moves:
                move = random.choice(list(valid_moves))
                game.apply_move(move, game.current_player)
                game.current_player *= -1
            else:
                break
        return game
    
    def copy(self):
        """Returns a new Othello object with the same game state, excluding pygame-related elements."""
        new_game = Othello(self.players[1],self.players[-1])
        new_game.board = np.copy(self.board)  # Deep copy of board
        new_game.current_player = self.current_player  # Copy current player
        return new_game

    def valid_moves(self, player):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        moves = set()
        
        for r in range(8):
            for c in range(8):
                if self.board[r, c] != player:
                    continue
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    found_opponent = False
                    while 0 <= nr < 8 and 0 <= nc < 8:
                        if self.board[nr, nc] == -player:
                            found_opponent = True
                        elif self.board[nr, nc] == 0 and found_opponent:
                            moves.add((nr, nc))
                            break
                        else:
                            break
                        nr += dr
                        nc += dc
        return moves

    def apply_move(self, move, player):
        if move not in self.valid_moves(player):
            return False
        r, c = move
        self.board[r, c] = player
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            pieces_to_flip = []
            nr, nc = r + dr, c + dc
            while 0 <= nr < 8 and 0 <= nc < 8:
                if self.board[nr, nc] == -player:
                    pieces_to_flip.append((nr, nc))
                elif self.board[nr, nc] == player:
                    for flip_r, flip_c in pieces_to_flip:
                        self.board[flip_r, flip_c] = player
                    break
                else:
                    break
                nr += dr
                nc += dc
        return True

    def is_game_over(self):
        return not (self.valid_moves(1) or self.valid_moves(-1))

    def get_winner(self):
        black_count = np.sum(self.board == 1)
        white_count = np.sum(self.board == -1)
        if black_count > white_count:
            return "Black wins!"
        elif white_count > black_count:
            return "White wins!"
        else:
            return "It's a draw!"

    def draw_board(self):
        self.screen.fill((0, 128, 0))
        for r in range(8):
            for c in range(8):
                pygame.draw.rect(self.screen, (0, 0, 0), (c * self.cell_size, r * self.cell_size, self.cell_size, self.cell_size), 1)
                if self.board[r, c] == 1:
                    pygame.draw.circle(self.screen, (0, 0, 0), (c * self.cell_size + self.cell_size // 2, r * self.cell_size + self.cell_size // 2), self.cell_size // 2 - 5)
                elif self.board[r, c] == -1:
                    pygame.draw.circle(self.screen, (255, 255, 255), (c * self.cell_size + self.cell_size // 2, r * self.cell_size + self.cell_size // 2), self.cell_size // 2 - 5)
                elif (r,c) in self.valid_moves(self.current_player):
                    if self.current_player == 1:
                        pygame.draw.circle(self.screen, (0, 0, 0), (c * self.cell_size + self.cell_size // 2, r * self.cell_size + self.cell_size // 2), self.cell_size // 2 - 17)
                    else:
                        pygame.draw.circle(self.screen, (255, 255, 255), (c * self.cell_size + self.cell_size // 2, r * self.cell_size + self.cell_size // 2), self.cell_size // 2 - 17)
        turn_text = "Black's Turn" if self.current_player == 1 else "White's Turn"
        text_surface = self.font.render(turn_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, self.height - 35))
        pygame.display.flip()

    def play(self):
        pygame.init()
        while self.running:
            self.draw_board()
            current_player_obj = self.players[self.current_player]
            if current_player_obj.player_type == 'human':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        if y < self.cell_size * 8:
                            move = (y // self.cell_size, x // self.cell_size)
                            if move in self.valid_moves(self.current_player):
                                self.apply_move(move, self.current_player)
                                if self.valid_moves(-self.current_player):
                                    self.current_player *= -1
            else:
                pygame.time.delay(500)  # AI thinking time
                move = current_player_obj.get_move(self)
                if move:
                    self.apply_move(move, self.current_player)
                    if self.valid_moves(-self.current_player):
                        self.current_player *= -1
            
            if self.is_game_over():
                self.show_winner()
                pygame.time.delay(3000)
                self.running = False

                
        pygame.quit()
        black_count = np.sum(self.board == 1)
        white_count = np.sum(self.board == -1)

        if(black_count == white_count): return 0
        elif ( black_count > white_count): return 1
        else : return -1
    
    def show_winner(self):
        winner_text = self.get_winner()
        self.screen.fill((0, 0, 0))
        text_surface = self.font.render(winner_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.width // 4, self.height // 2))
        pygame.display.flip()


if __name__ == "__main__":
    # player1 = Player('human', 1)
    player1 = MinMaxPlayer(1, heuristic_function=coin_parity_heuristic, depth=3)
    player2 = MCTSAgent(-1)
    # player2 = MinMaxPlayer(-1, heuristic_function=hybrid_heuristic, depth=3)
    game = Othello(player1, player2)
    game.play()