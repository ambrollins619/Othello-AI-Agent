from utils import find_valid_moves, find_empty_neighbors, find_stable_disks, find_unstable_disks

def coin_parity_heuristic(game, player):
    """
    Evaluates the board based on coin parity.
    A higher score favors the player with more pieces.
    """
    player_count = sum(sum(game.board == player))
    opponent_count = sum(sum(game.board == -player))
    
    if player_count + opponent_count == 0:
        return 0  # Avoid division by zero
    
    return 100 * (player_count - opponent_count) / (player_count + opponent_count)


def mobility_heuristic(game, player):
    """
    Computes the mobility heuristic for a 2D Othello board.
    
    Args:
        game.board (list[list[int]]): 2D representation of the Othello board.
        player (int): The player ID (1 or 2).
    
    Returns:
        int: Mobility heuristic value.
    """
    player_moves_a = len(find_valid_moves(game.board, player))
    opponent_moves_a = len(find_valid_moves(game.board, -player))
    
    player_moves_p = len(find_empty_neighbors(game.board, player))
    opponent_moves_p = len(find_empty_neighbors(game.board, -player))
    
    if(player_moves_a + opponent_moves_a !=0):
        actual_mobility_heuristic = 100 * (player_moves_a - opponent_moves_a)/(player_moves_a + opponent_moves_a)
    else:
        actual_mobility_heuristic = 0
        
    if(player_moves_p + opponent_moves_p !=0):
        potential_mobility_heuristic = 100 * (player_moves_p - opponent_moves_p)/(player_moves_p + opponent_moves_p)
    else:
        potential_mobility_heuristic = 0
        
    mobility_heuristic = (actual_mobility_heuristic + potential_mobility_heuristic)/2
    
    return mobility_heuristic

def corner_heuristic(game, player):
    """
    Compute the corner control heuristic.

    Args:
        game: The Othello game instance.
        player (int): The player (1 or -1).

    Returns:
        float: The corner heuristic score.
    """
    board = game.board  # 2D board representation

    # Define corner positions
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]

    player_corners = 0
    opponent_corners = 0
    player_potential_corners = 0
    opponent_potential_corners = 0

    # Count captured corners
    for x, y in corners:
        if board[x][y] == player:
            player_corners += 1
        elif board[x][y] == -player:
            opponent_corners += 1

    # Check potential corner moves
    possible_moves = game.valid_moves(player)  # List of (row, col) tuples
    for move in possible_moves:
        if move in corners:
            player_potential_corners += 1

    opponent_moves = game.valid_moves(-player)
    for move in opponent_moves:
        if move in corners:
            opponent_potential_corners += 1

    # Define weights
    CORNER_CAPTURED_WEIGHT = 2
    POTENTIAL_CORNER_WEIGHT = 1

    # Compute heuristic value
    player_score = (CORNER_CAPTURED_WEIGHT * player_corners) + (POTENTIAL_CORNER_WEIGHT * player_potential_corners)
    opponent_score = (CORNER_CAPTURED_WEIGHT * opponent_corners) + (POTENTIAL_CORNER_WEIGHT * opponent_potential_corners)

    # Normalize the score
    if player_score + opponent_score != 0:
        return 100 * (player_score - opponent_score) / (player_score + opponent_score)
    return 0

def stability_heuristic(game, player):
    """
    Compute the stability heuristic.

    Args:
        game: The Othello game instance.
        player (int): The player (1 or -1).

    Returns:
        float: The stability heuristic score.
    """
    board = game.board  # 2D board representation
    opponent = -player

    player_stable = find_stable_disks(board, player)
    opponent_stable = find_stable_disks(board, opponent)

    player_unstable = find_unstable_disks(board, player, game.valid_moves(opponent))
    opponent_unstable = find_unstable_disks(board, opponent, game.valid_moves(player))

    STABLE_WEIGHT = 2
    UNSTABLE_WEIGHT = 1

    # Compute normalized values
    stable_diff = (
        100 * (player_stable - opponent_stable) / (player_stable + opponent_stable)
        if (player_stable + opponent_stable) != 0
        else 0
    )

    unstable_diff = (
        100 * (opponent_unstable - player_unstable) / (player_unstable + opponent_unstable)
        if (player_unstable + opponent_unstable) != 0
        else 0
    )

    # Weighted heuristic score
    return (STABLE_WEIGHT * stable_diff + UNSTABLE_WEIGHT * unstable_diff) / (STABLE_WEIGHT + UNSTABLE_WEIGHT)

def hybrid_heuristic(game, player):
    """
    Evaluate the board state using a hybrid heuristic.

    The hybrid heuristic combines multiple heuristics to evaluate the board state:
    - Disk Parity: Measures the difference in the number of disks.
    - Mobility: Evaluates actual and potential mobility.
    - Corner Control: Assesses control and potential control of corner squares.
    - Stability: Measures the number of stable and unstable disks.

    Each heuristic is weighted and combined to compute a final evaluation score.
    
    Args:
        game: The current state of the game
        player_id (int16): The ID of the player (1 or 2).

    Returns:
        final_score: The final hybrid heuristic score.
    """
    
    board = game.board
    
    # =============== Heuristics Values ===============
    
    disk_parity_heuristic_value = coin_parity_heuristic(game, player)

    mobility_heuristic_value = mobility_heuristic(game, player)

    corner_heuristic_value = corner_heuristic(game, player)
        
    stability_heuristic_value = stability_heuristic(game, player)
    
    # =============== Disks count ===============
    
    player_disks = sum(sum(game.board == player))
    opponent_disks = sum(sum(game.board == -player))
    
    # =============== Final Score ===============
    
    disk_nb = player_disks+opponent_disks
    
    # scale exponentially the weight of this heursitic as the game progresses 
    disk_parity_weight = (1+(disk_nb/64))**6
    mobility_weight = 20
    corner_weight = 50
    stability_weight = 40
    
    final_score = disk_parity_weight*disk_parity_heuristic_value + mobility_weight*mobility_heuristic_value \
                + corner_weight*corner_heuristic_value + stability_weight*stability_heuristic_value
                
    final_score /= (disk_parity_weight + mobility_weight + corner_weight + stability_weight)
    
    return final_score
