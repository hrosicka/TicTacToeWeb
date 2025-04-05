from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

class TicTacToe:
    """
    Represents the Tic Tac Toe game logic.
    Encapsulates the game state and provides methods to manipulate it.
    """
    def __init__(self):
        """
        Initializes the Tic Tac Toe game.
        Sets up the game board, randomly selects the starting player, and initializes the winner to None.
        """
        self.board = [''] * 9  # Represents the 3x3 game board as a list.
        self.current_player = random.choice(['X', 'O']) # Randomly selects 'X' or 'O' as the starting player.
        self.winner = None  # Stores the winner of the game (X, O, or Tie).

    def reset(self):
        """
        Resets the game to its initial state.
        Clears the board, selects a new starting player, and resets the winner.
        """
        self.board = [''] * 9
        self.current_player = random.choice(['X', 'O'])
        self.winner = None

    def check_winner(self):
        """
        Checks if there is a winner or a tie.
        Evaluates all possible winning combinations and checks if any player has won.
        If no winner and the board is full, it returns 'Tie'.
        Returns the winner ('X' or 'O'), 'Tie', or None if the game is still in progress.
        """
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != '':
                return self.board[combo[0]]  # Returns the winning player ('X' or 'O').
        if '' not in self.board:
            return 'Tie'  # Returns 'Tie' if the board is full and no winner.
        return None  # Returns None if the game is still in progress.

    def make_move(self, index):
        """
        Makes a move on the game board.
        Updates the board with the current player's symbol at the specified index.
        Checks for a winner after the move and switches players if no winner.
        Returns True if the move was successful, False otherwise.
        """
        if self.board[index] == '' and not self.winner:
            self.board[index] = self.current_player
            self.winner = self.check_winner()
            if not self.winner:
                self.current_player = 'O' if self.current_player == 'X' else 'X'  # Switches players.
            return True  # Move successful.
        return False  # Move failed (cell already occupied or game over).

game = TicTacToe()  # Creates an instance of the TicTacToe game.

@app.route('/', methods=['GET'])
def index():
    """
    Renders the index.html template and initializes a new game.
    Resets the game state and passes game data to the template.
    """
    game.reset()
    return render_template('index.html', board=game.board, current_player=game.current_player, winner=game.winner)

@app.route('/move', methods=['POST'])
def make_move():
    """
    Handles player moves via POST requests.
    Receives the cell index from the request, makes the move, and returns the updated game state as JSON.
    """
    data = request.get_json()
    index = data['index']
    game.make_move(index)  # Makes the move on the game board.
    return jsonify({
        'board': game.board,
        'current_player': game.current_player,
        'winner': game.winner
    })

if __name__ == '__main__':
    app.run(debug=True)