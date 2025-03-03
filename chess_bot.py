import chess
import random
import time

# Global transposition table to store board evaluations.
transposition_table = {}

# Material values (in centipawns) for each piece.
piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

# Piece-square tables (from White's perspective)
pawn_table = [
      0,   0,   0,   0,   0,   0,   0,   0,
     50,  50,  50,  50,  50,  50,  50,  50,
     10,  10,  20,  30,  30,  20,  10,  10,
      5,   5,  10,  25,  25,  10,   5,   5,
      0,   0,   0,  20,  20,   0,   0,   0,
      5,  -5, -10,   0,   0, -10,  -5,   5,
      5,  10,  10, -20, -20,  10,  10,   5,
      0,   0,   0,   0,   0,   0,   0,   0
]

knight_table = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   5,   5,   0, -20, -40,
    -30,   5,  10,  15,  15,  10,   5, -30,
    -30,   0,  15,  20,  20,  15,   0, -30,
    -30,   5,  15,  20,  20,  15,   5, -30,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

bishop_table = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,   5,   0,   0,   0,   0,   5, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,   0,  10,  10,  10,  10,   0, -10,
    -10,   5,   5,  10,  10,   5,   5, -10,
    -10,   0,   5,  10,  10,   5,   0, -10,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

rook_table = [
      0,   0,   0,   5,   5,   0,   0,   0,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
      5,  10,  10,  10,  10,  10,  10,   5,
      0,   0,   0,   0,   0,   0,   0,   0
]

queen_table = [
    -20, -10, -10,  -5,  -5, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,   5,   5,   5,   5,   0, -10,
     -5,   0,   5,   5,   5,   5,   0,  -5,
      0,   0,   5,   5,   5,   5,   0,  -5,
    -10,   5,   5,   5,   5,   5,   0, -10,
    -10,   0,   5,   0,   0,   0,   0, -10,
    -20, -10, -10,  -5,  -5, -10, -10, -20
]

king_table_mid = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
     20,  20,   0,   0,   0,   0,  20,  20,
     20,  30,  10,   0,   0,  10,  30,  20
]

king_table_end = [
    -50, -30, -30, -30, -30, -30, -30, -50,
    -30, -30,   0,   0,   0,   0, -30, -30,
    -30, -10,  20,  30,  30,  20, -10, -30,
    -30, -10,  30,  40,  40,  30, -10, -30,
    -30, -10,  30,  40,  40,  30, -10, -30,
    -30, -10,  20,  30,  30,  20, -10, -30,
    -30, -20, -10,   0,   0, -10, -20, -30,
    -50, -40, -30, -20, -20, -30, -40, -50
]

def is_endgame(board):
    """
    Determines whether the position is likely an endgame.
    A simple heuristic is used here.
    """
    pieces = board.piece_map().values()
    num_queens = sum(1 for p in pieces if p.piece_type == chess.QUEEN)
    num_rooks = sum(1 for p in pieces if p.piece_type == chess.ROOK)
    # If neither side has significant heavy pieces, we assume endgame.
    return num_queens == 0 or (num_rooks <= 1 and num_queens <= 1)

def evaluate_board(board):
    """
    Evaluates the board from White's perspective.
    Combines material count with positional (piece-square) values.
    Returns a score in centipawns.
    """
    if board.is_checkmate():
        # A checkmate is assigned a very high/low score.
        return -99999 if board.turn == chess.WHITE else 99999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    endgame = is_endgame(board)
    for square, piece in board.piece_map().items():
        value = piece_values[piece.piece_type]
        if piece.piece_type == chess.PAWN:
            table = pawn_table
        elif piece.piece_type == chess.KNIGHT:
            table = knight_table
        elif piece.piece_type == chess.BISHOP:
            table = bishop_table
        elif piece.piece_type == chess.ROOK:
            table = rook_table
        elif piece.piece_type == chess.QUEEN:
            table = queen_table
        elif piece.piece_type == chess.KING:
            table = king_table_end if endgame else king_table_mid
        # For White, use the table as is; for Black, mirror the square.
        if piece.color == chess.WHITE:
            score += value + table[square]
        else:
            score -= value + table[chess.square_mirror(square)]
    return score

def quiescence_search(board, alpha, beta):
    """
    Extends the search at the leaf nodes to evaluate "noisy" positions.
    Only capture moves are considered until the position becomes quiet.
    """
    stand_pat = evaluate_board(board)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiescence_search(board, -beta, -alpha)
            board.pop()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha

def alpha_beta(board, depth, alpha, beta, maximizing_player):
    """
    Alpha-beta search with transposition table and quiescence search.
    """
    # Check the transposition table.
    board_key = board.fen()
    if board_key in transposition_table:
        stored_depth, stored_value = transposition_table[board_key]
        if stored_depth >= depth:
            return stored_value

    if depth == 0:
        return quiescence_search(board, alpha, beta)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
            if max_eval > alpha:
                alpha = max_eval
            if beta <= alpha:
                break  # Beta cutoff.
        transposition_table[board_key] = (depth, max_eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
            if min_eval < beta:
                beta = min_eval
            if beta <= alpha:
                break  # Alpha cutoff.
        transposition_table[board_key] = (depth, min_eval)
        return min_eval

def iterative_deepening(board, max_depth, time_limit):
    """
    Uses iterative deepening to search for the best move until a maximum depth or time limit is reached.
    """
    best_move = None
    start_time = time.time()
    for depth in range(1, max_depth + 1):
        current_best_move = None
        best_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = alpha_beta(board, depth - 1, float('-inf'), float('inf'), False)
            board.pop()
            if eval > best_eval:
                best_eval = eval
                current_best_move = move
        best_move = current_best_move
        print(f"Depth {depth}: Best Eval = {best_eval}, Best Move = {best_move}")
        if time.time() - start_time > time_limit:
            break
    return best_move

def get_best_move(board, max_depth=4, time_limit=5):
    """
    Returns the best move for the current board position using iterative deepening.
    """
    return iterative_deepening(board, max_depth, time_limit)

def main():
    board = chess.Board()
    print("Welcome to the Advanced Chess Bot!")
    print(board)
    
    # Game loop: Human (White) vs. Bot (Black)
    while not board.is_game_over():
        # Human move (input in UCI format, e.g., "e2e4", or type "quit" to exit)
        user_move = input("Enter your move in UCI format (or type 'quit' to exit): ").strip()
        if user_move.lower() == "quit":
            print("Exiting the game. Goodbye!")
            break
        
        try:
            move = chess.Move.from_uci(user_move)
            if move in board.legal_moves:
                board.push(move)
            else:
                print("Illegal move. Try again.")
                continue
        except Exception as e:
            print("Invalid move format. Try again.", e)
            continue
        
        if board.is_game_over():
            break
        
        # Bot move.
        print("Bot is thinking...")
        best_move = get_best_move(board, max_depth=4, time_limit=5)
        if best_move is None:
            best_move = random.choice(list(board.legal_moves))
        board.push(best_move)
        print("Bot played:", best_move)
        print(board)
    
    if board.is_game_over():
        print("Game over!")
        print("Result:", board.result())

if __name__ == "__main__":
    main()
