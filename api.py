from flask import Flask, request, jsonify
from flask_cors import CORS
from numpy import convolve
from bot import get_best_move
import chess

app = Flask(__name__)
CORS(app)  # Allows requests from your React frontend

@app.route("/best-move", methods=["POST"])
def best_move():
    data = request.get_json()
    fen = data.get("fen")

    if not fen:
        return jsonify({"error": "FEN string is required"}), 400
   
    board = chess.Board(fen)

    if(chess.Board.is_game_over(board)):
        return jsonify({"error": "Game is already over"}), 400
    move = get_best_move(board) # your existing logic returning a chess.Move object
    move_uci = move.uci()      # convert to string like "e2e4"
    return jsonify({"move": move_uci})

if __name__ == "__main__":
    app.run(debug=True)
