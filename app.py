from typing import cast
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

turn = 'White'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_moves", methods=['GET', 'POST'])
def get_moves():
    if len(request.form) == 2:
        x = int(request.form['x'])
        y = int(request.form['y'])
        print(board)
        if board[x][y] != None:
            result = board[x][y].get_moves(board)
            print(result)
            return json.dumps(result)

    return 'Error'


@app.route("/make_move", methods=['GET', 'POST'])
def make_move():
    global turn
    if len(request.form) == 4:
        # From
        x1 = int(request.form['x1'])
        y1 = int(request.form['y1'])

        # To
        x2 = int(request.form['x2'])
        y2 = int(request.form['y2'])

        if board[x1][y1] != None and board[x1][y1].get_color() == turn:

            if ((x2, y2) in board[x1][y1].get_moves(board)):
                # Assign old cell to selected cell
                board[x2][y2] = board[x1][y1]
                board[x2][y2].change_pos(x2, y2)

                # Remove Old Object Completely from memory
                buffer = board[x1][y1]
                board[x1][y1] = None
                del buffer

                turn = 'Black' if turn == 'White' else 'White'

                ended = check_end(board, turn)
                return ended if ended != False else str(0)

    return "Error"


@app.route("/promation", methods=['GET', 'POST'])
def promation():
    global turn
    if len(request.form) == 5:
        # From
        x1 = int(request.form['x1'])
        y1 = int(request.form['y1'])

        y2 = int(request.form['y2'])

        name = request.form['name']
        if board[x1][y1].get_color() == turn and name in ['queen', 'bishop', 'knight', 'rook'] and \
                board[x1][y1] != None and board[x1][y1].get_name() == 'Pawn' and \
                board[x1][y1].get_pos()[0] in [1, 6] and board[x1][y1].moved == True \
                and y2 in [y1, y1 + 1, y1 - 1]:
            if name == 'queen':
                temp = Queen(0 if x1 == 1 else 7, y2,
                             board[x1][y1].get_color())
            elif name == 'bishop':
                temp = Bishop(0 if x1 == 1 else 7, y2,
                              board[x1][y1].get_color())
            elif name == 'knight':
                temp = Knight(0 if x1 == 1 else 7, y2,
                              board[x1][y1].get_color())
            elif name == 'rook':
                temp = Rook(0 if x1 == 1 else 7, y2,
                            board[x1][y1].get_color())

            board[0 if x1 == 1 else 7][y2] = temp
            buffer = board[x1][y1]
            board[x1][y1] = None
            del buffer

            turn = 'Black' if turn == 'White' else 'White'

            ended = check_end(board, turn)
            return ended if ended != False else str(0)
    return 'Error'


@app.route("/make_castle", methods=['GET', 'POST'])
def make_castle():
    global turn
    if len(request.form) == 4:
        # From
        x1 = int(request.form['x1'])
        y1 = int(request.form['y1'])

        # To
        x2 = int(request.form['x2'])
        y2 = int(request.form['y2'])

        if board[x1][y1].get_color() == turn and board[x1][y1] != None and board[x1][y1].get_name() == 'King':
            castle = board[x1][y1].check_castle(board)

            if castle != None:
                if x2 == castle[1][0] and y2 == castle[1][1]:
                    castle = castle[1]
                elif len(castle) == 3 and x2 == castle[2][0] and y2 == castle[2][1]:
                    castle = castle[2]
                else:
                    return "Error"
                # Assign old cell to selected cell
                board[x2][y2] = board[x1][y1]
                board[x2][y2].change_pos(x2, y2)

                # Remove Old Object Completely from memory
                buffer = board[x1][y1]
                board[x1][y1] = None
                del buffer

                if y1 > y2:
                    board[x2][y2 + 1] = board[x1][0]
                    board[x2][y2 + 1].change_pos(x2, y2 + 1)

                    # Remove Old Object Completely from memory
                    buffer = board[x1][0]
                    board[x1][0] = None
                    del buffer

                else:
                    board[x2][y2 - 1] = board[x1][7]
                    board[x2][y2 - 1].change_pos(x2, y2 - 1)

                    # Remove Old Object Completely from memory
                    buffer = board[x1][0]
                    board[x1][0] = None
                    del buffer

                turn = 'Black' if turn == 'White' else 'White'

                ended = check_end(board, turn)
                return ended if ended != False else str(0)

    return 'Error'


@app.route("/check_king", methods=['GET', 'POST'])
def check_king():
    if len(request.form) == 2:
        x1 = x2 = int(request.form['x'])
        y1 = y2 = int(request.form['y'])
        return '1' if check_king_state(x1, y1, x2, y2, board) == True else '-1'


if __name__ == '__main__':
    app.run()
