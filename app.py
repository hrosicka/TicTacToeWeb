from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Globální proměnné
board = [''] * 9
current_player = 'X'
winner = None

def check_winner():
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != '':
            return board[combo[0]]
    if '' not in board:
        return 'Tie'
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    global board, current_player, winner
    if request.method == 'POST':
        index = int(request.form['index'])
        if board[index] == '' and not winner:
            board[index] = current_player
            winner = check_winner()
            if not winner:
                current_player = 'O' if current_player == 'X' else 'X'
    else:
        board = [''] * 9
        current_player = random.choice(['X', 'O'])
        winner = None
    return render_template('index.html', board=board, current_player=current_player, winner=winner)

if __name__ == '__main__':
    app.run(debug=True)