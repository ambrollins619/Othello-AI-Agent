def find_valid_moves(board, player):
    """
    Finds all valid moves for the given player in the 2D Othello board.
    
    Args:
        board (list[list[int]]): 2D representation of the Othello board.
        player (int): The player ID (1 or 2).
    
    Returns:
        set: A set of (row, col) tuples representing valid moves.
    """
    opponent = -player
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    valid_moves = set()
    
    for r in range(8):
        for c in range(8):
            if board[r][c] != 0:  # Skip non-empty cells
                continue
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == opponent:
                    # Move in this direction to check if it's a valid move
                    while 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == opponent:
                        nr += dr
                        nc += dc
                    
                    if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == player:
                        valid_moves.add((r, c))
                        break  # No need to check other directions
    
    return valid_moves

def find_empty_neighbors(board, player):
    """
    Finds all empty neighboring cells of a player's pieces on the board.
    
    Args:
        board (list[list[int]]): 2D representation of the Othello board.
        player (int): The player ID (1 or 2).
    
    Returns:
        set: A set of (row, col) tuples representing empty neighboring cells.
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    empty_neighbors = set()
    
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == 0:
                        empty_neighbors.add((nr, nc))
    
    return empty_neighbors


def find_stable_disks(board, player):
    """
    Find the number of stable disks for a given player.

    Stable disks are those that cannot be flipped for the rest of the game.
    A disk is considered stable if it is surrounded by friendly disks or locked in corners/edges.

    Args:
        board (list of lists): 2D Othello board.
        player (int): The player (1 or -1).

    Returns:
        int: Count of stable disks.
    """
    stable_count = 0
    rows, cols = len(board), len(board[0])
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == player:
                # A disk is stable if all directions are blocked or occupied by the player
                stable = True
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 0:
                        stable = False
                        break
                if stable:
                    stable_count += 1

    return stable_count


def find_unstable_disks(board, player, opponent_moves):
    """
    Find the number of unstable disks for a given player.

    Unstable disks are those that the opponent can flip in the next move.

    Args:
        board (list of lists): 2D Othello board.
        player (int): The player (1 or -1).
        opponent_moves (list of tuples): List of possible opponent moves.

    Returns:
        int: Count of unstable disks.
    """
    unstable_count = 0
    for move in opponent_moves:
        r, c = move
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(board) and 0 <= nc < len(board[0]) and board[nr][nc] == player:
                unstable_count += 1

    return unstable_count