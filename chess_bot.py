import chess
import random

def evaluate_board(board):
    """
    Simple static evaluation function based on material count.
    Positive scores favor White, negative scores favor Black.
    """
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  # King value is set to 0 because its loss ends the game.
    }
    score = 0
    for piece in board.piece_map().values():
        if piece.color == chess.WHITE:
            score += piece_values[piece.piece_type]
        else:
            score -= piece_values[piece.piece_type]
    return score

def minimax(board, depth, maximizing_player):
    """
    The minimax algorithm recursively simulates moves up to a certain depth.
    """
    # Base condition: when we reach the max depth or the game is over.
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    
    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, False)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, True)
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval

def get_best_move(board, depth):
    """
    Iterates through all legal moves and selects the one with the highest minimax evaluation.
    """
    best_move = None
    best_value = float('-inf')
    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, False)
        board.pop()
        if board_value > best_value:
            best_value = board_value
            best_move = move
    return best_move

def main():
    board = chess.Board()
    print("Welcome to the Chess Bot!")
    print(board)
    
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
        except Exception:
            print("Invalid move format. Please try again.")
            continue
        
        if board.is_game_over():
            break
        
        # Bot move (using minimax with depth 2)
        print("Bot is thinking...")
        bot_move = get_best_move(board, depth=2)
        # Fallback: if minimax fails, choose a random move.
        if bot_move is None:
            bot_move = random.choice(list(board.legal_moves))
        board.push(bot_move)
        print("Bot played:", bot_move)
        print(board)
    
    print("Game over!")
    print("Result:", board.result())

if __name__ == "__main__":
    main()