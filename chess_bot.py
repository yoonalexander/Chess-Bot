import chess

board = chess.Board()
print(board)

def evaluate_board(board):
    piece_values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}
    score = sum(piece_values[piece.piece_type] for piece in board.piece_map().values() if piece.color == chess.WHITE)
    score -= sum(piece_values[piece.piece_type] for piece in board.piece_map().values() if piece.color == chess.BLACK)
    return score

def minimax(board, depth, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing:
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