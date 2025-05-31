import tensorflow as tf
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Step 1: Load the data
fen_strings = []
moves = []

with open("positions_moves.txt", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        *fen_parts, move = line.split()
        fen = " ".join(fen_parts)
        fen_strings.append(fen)
        moves.append(move)

print(f"Loaded {len(fen_strings)} positions and moves.")

# Step 2: Encode the FENs as input features
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


X = np.array([fen_to_array(fen) for fen in fen_strings])

# Step 3: Encode the labels (moves)
encoder = LabelEncoder()
y = encoder.fit_transform(moves)

# Step 4: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Step 5: Define the model
model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(65,)),  # 8x8 board
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(len(encoder.classes_), activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Step 6: Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Step 7: Save the model and the encoder
model.save("my_chess_bot.h5")
import pickle
with open("move_encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)
