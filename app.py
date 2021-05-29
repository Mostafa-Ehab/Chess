from flask import Flask, render_template, request
from chess import *
import json

app = Flask(__name__)

board = [
        [Rook(0, 0, "Black"), Knight(0, 1, "Black"), Bishop(0, 2, "Black"), Queen(0, 3, "Black"),
         King(0, 4, "Black"), Bishop(0, 5, "Black"), Knight(0, 6, "Black"), Rook(0, 7, "Black")],
        [Pawn(1, i, "Black") for i in range(8)],
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [Pawn(6, i, "White") for i in range(8)],
        [Rook(7, 0, "White"), Knight(7, 1, "White"), Bishop(7, 2, "White"), Queen(7, 3, "White"),
         King(7, 4, "White"), Bishop(7, 5, "White"), Knight(7, 6, "White"), Rook(7, 7, "White")],
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_moves", methods=['GET', 'POST'])
def get_moves():
    if len(request.form) == 2:
        x = int(request.form['x'])
        y = int(request.form['y'])
        print(board)

        result = json.dumps(board[x][y].get_moves(board))
        print(result)
        return result


@app.route("/make_move", methods=['GET', 'POST'])
def make_move():
    if len(request.form) == 4:
        # From
        x1 = int(request.form['x1'])
        y1 = int(request.form['y1'])

        # To
        x2 = int(request.form['x2'])
        y2 = int(request.form['y2'])

        if ((x2, y2) in board[x1][y1].get_moves(board)):
            # Assign old cell to selected cell
            board[x2][y2] = board[x1][y1]
            board[x2][y2].change_pos(x2, y2)

            # Remove Old Object Completely from memory
            buffer = board[x1][y1]
            board[x1][y1] = None
            del buffer

            return str(0)

        return "Error"


if __name__ == '__main__':
    app.run()
