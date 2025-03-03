import chess
import random

def evaluate_board(board):
    """
    Evaluates the board using a simple material count.
    Positive values favor White and negative values favor Black.
    """
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  # The king's value is omitted since its loss ends the game.
    }
    score = 0
    for piece in board.piece_map().values():
        if piece.color == chess.WHITE:
            score += piece_values[piece.piece_type]
        else:
            score -= piece_values[piece.piece_type]
    return score

def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):
    """
    Implements the minimax algorithm with alpha-beta pruning.
    Recursively evaluates moves up to a specified depth.
    """
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    
    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval

def get_best_move(board, depth):
    """
    Iterates through all legal moves and returns the move with the best minimax evaluation.
    """
    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    for move in board.legal_moves:
        board.push(move)
        move_value = minimax_alpha_beta(board, depth - 1, alpha, beta, False)
        board.pop()
        if move_value > best_value:
            best_value = move_value
            best_move = move
        alpha = max(alpha, best_value)
    return best_move

def main():
    board = chess.Board()
    print("Welcome to the Variable Depth Chess Bot with Alpha-Beta Pruning!")
    print(board)
    
    # Ask the user for the desired search depth.
    depth_input = input("Enter desired search depth (e.g., 2, 3, 4): ")
    try:
        depth = int(depth_input)
    except ValueError:
        print("Invalid input, using default depth of 2.")
        depth = 2

    # Game loop: human (White) vs. bot (Black)
    while not board.is_game_over():
        # Human move
        user_move = input("Enter your move in UCI format (e.g., e2e4): ")
        try:
            move = chess.Move.from_uci(user_move)
            if move in board.legal_moves:
                board.push(move)
            else:
                print("Illegal move. Try again.")
                continue
        except Exception as e:
            print("Invalid move format. Please try again.", e)
            continue
        
        if board.is_game_over():
            break
        
        # Bot move
        print("Bot is thinking with depth", depth, "...")
        bot_move = get_best_move(board, depth)
        # Fallback: if no move is found, choose randomly.
        if bot_move is None:
            bot_move = random.choice(list(board.legal_moves))
        board.push(bot_move)
        print("Bot played:", bot_move)
        print(board)
    
    print("Game over!")
    print("Result:", board.result())

if __name__ == "__main__":
    main()
