import numpy as np
from tensorflow.keras.models import load_model
import pickle

# Load trained model and encoder
model = load_model("my_chess_bot.h5")
with open("move_encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

# FEN to array conversion (same as before)
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


# Provide a FEN to predict a move
fen_input = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
x_input = np.array([fen_to_array(fen_input)])

# Make prediction
predicted_index = np.argmax(model.predict(x_input), axis=1)[0]
predicted_move = encoder.inverse_transform([predicted_index])[0]

print("Predicted move:", predicted_move)
