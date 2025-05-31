from flask import Flask, request, jsonify
from flask_cors import CORS
import chess
from bot import get_best_move

import numpy as np
from tensorflow.keras.models import load_model
import pickle

app = Flask(__name__)
CORS(app)

# === Load your personalized bot model and encoder ===
model = load_model("my_chess_bot.h5")
with open("move_encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

# === FEN to input array function ===
def fen_to_array(fen):
    piece_map = {
        'p': 1, 'n': 2, 'b': 3, 'r': 4, 'q': 5, 'k': 6,
        'P': 7, 'N': 8, 'B': 9, 'R': 10, 'Q': 11, 'K': 12
    }
    board, turn, *_ = fen.split()
    rows = board.split("/")
    result = []
    for row in rows:
        for char in row:
            if char.isdigit():
                result.extend([0] * int(char))
            else:
                result.append(piece_map.get(char, 0))
    
    # Add turn info: 0 for white, 1 for black
    result.append(0 if turn == 'w' else 1)

    return result


# === Route for Stock Bot ===
@app.route("/best-move", methods=["POST"])
def best_move():
    data = request.get_json()
    fen = data.get("fen")
    if not fen:
        return jsonify({"error": "FEN string is required"}), 400

    board = chess.Board(fen)
    if board.is_game_over():
        return jsonify({"error": "Game is already over"}), 400

    move = get_best_move(board)
    move_uci = move.uci()
    return jsonify({"move": move_uci})

# === Route for Personalized Bot ===
@app.route("/best-move-mybot", methods=["POST"])
def best_move_mybot():
    data = request.get_json()
    fen = data.get("fen")
    if not fen:
        return jsonify({"error": "FEN string is required"}), 400

    board = chess.Board(fen)
    if board.is_game_over():
        return jsonify({"error": "Game is already over"}), 400

    legal_moves = list(board.legal_moves)
    legal_uci = [move.uci() for move in legal_moves]

    x_input = np.array([fen_to_array(fen)])
    prediction = model.predict(x_input, verbose=0)[0]

    # Filter predicted probabilities to legal moves
    legal_move_indices = [encoder.transform([uci])[0] for uci in legal_uci if uci in encoder.classes_]
    if not legal_move_indices:
        return jsonify({"error": "No legal move found in model output"}), 400

    legal_probs = prediction[legal_move_indices]
    best_index = np.argmax(legal_probs)
    best_move = encoder.inverse_transform([legal_move_indices[best_index]])[0]

    print(f"user played (Legal): {fen}")

    print(f"Rathijit Played (Legal): {best_move}")

    return jsonify({"move": best_move})

if __name__ == "__main__":
    app.run(debug=True)
