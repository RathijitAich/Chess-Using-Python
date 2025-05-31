import chess


pawn_table = [
     0, 0, 0, 0, 0, 0, 0, 0,
     5, 5, 5, 5, 5, 5, 5, 5,
     1, 1, 2, 3, 3, 2, 1, 1,
     0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5,
     0, 0, 0, 2, 2, 0, 0, 0,
     0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5,
     0.5, 1, 1, -2, -2, 1, 1, 0.5,
     0, 0, 0, 0, 0, 0, 0, 0
]

knight_table = [
    -5, -4, -3, -3, -3, -3, -4, -5,
    -4, -2, 0, 0, 0, 0, -2, -4,
    -3, 0, 1, 1.5, 1.5, 1, 0, -3,
    -3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3,
    -3, 0, 1.5, 2, 2, 1.5, 0, -3,
    -3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3,
    -4, -2, 0, 0.5, 0.5, 0, -2, -4,
    -5, -4, -3, -3, -3, -3, -4, -5
]

bishop_table = [
    -2, -1, -1, -1, -1, -1, -1, -2,
    -1, 0, 0, 0, 0, 0, 0, -1,
    -1, 0, 0.5, 1, 1, 0.5, 0, -1,
    -1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1,
    -1, 0, 1, 1, 1, 1, 0, -1,
    -1, 1, 1, 1, 1, 1, 1, -1,
    -1, 0.5, 0, 0, 0, 0, 0.5, -1,
    -2, -1, -1, -1, -1, -1, -1, -2
]

rook_table = [
     0, 0, 0, 0, 0, 0, 0, 0,
     0.5, 1, 1, 1, 1, 1, 1, 0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
     0, 0, 0, 0.5, 0.5, 0, 0, 0
]

queen_table = [
    -2, -1, -1, -0.5, -0.5, -1, -1, -2,
    -1, 0, 0, 0, 0, 0, 0, -1,
    -1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1,
    -0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,
     0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,
    -1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1,
    -1, 0, 0.5, 0, 0, 0, 0, -1,
    -2, -1, -1, -0.5, -0.5, -1, -1, -2
]

king_table = [
    -3, -4, -4, -5, -5, -4, -4, -3,
    -3, -4, -4, -5, -5, -4, -4, -3,
    -3, -4, -4, -5, -5, -4, -4, -3,
    -3, -4, -4, -5, -5, -4, -4, -3,
    -2, -3, -3, -4, -4, -3, -3, -2,
    -1, -2, -2, -2, -2, -2, -2, -1,
     2, 2, 0, 0, 0, 0, 2, 2,
     2, 3, 1, 0, 0, 1, 3, 2
]



def piece_square_value(piece, square):
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
        table = king_table
    else:
        return 0

    if piece.color == chess.WHITE:
        return table[square]
    else:
        # Mirror the square vertically for Black
        return -table[chess.square_mirror(square)]




# Basic piece values
piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 4,
    chess.ROOK: 5,
    chess.QUEEN: 10,
    chess.KING: 0  # Not evaluated directly
}

def evaluate_board(board):
    value = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            base_value = piece_values[piece.piece_type]
            ps_value = piece_square_value(piece, square)
            if piece.color == chess.WHITE:
                value += base_value + ps_value
            else:
                value -= base_value + ps_value
    return value


# Minimax with alpha-beta pruning
def minimax(board, depth, alpha, beta, is_maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None

    if is_maximizing:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval, best_move

# Entry point for getting best move
def get_best_move(board, depth=3):
    _, best_move = minimax(board, depth, float('-inf'), float('inf'), board.turn == chess.WHITE)
    return best_move


