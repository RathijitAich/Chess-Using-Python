import chess.pgn

def extract_positions_and_moves(pgn_file_path):
    positions_and_moves = []

    with open(pgn_file_path) as pgn:
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break  # no more games

            board = game.board()

            for move in game.mainline_moves():
                fen_before_move = board.fen()
                uci_move = move.uci()  # move in UCI format like e2e4
                positions_and_moves.append((fen_before_move, uci_move))
                board.push(move)

    return positions_and_moves

if __name__ == "__main__":
    pgn_path = "monkey_games.pgn"  # Change this to your PGN file path
    data = extract_positions_and_moves(pgn_path)
    print(f"Extracted {len(data)} positions and moves")

    # Optional: save to a file for later use
    with open("positions_moves.txt", "w") as f:
        for fen, move in data:
            f.write(f"{fen} {move}\n")
