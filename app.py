from os import name
from flask import Flask, render_template, request, redirect, session
# from flask.signals import Namespace
from flask_session import Session
from tempfile import mkdtemp
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from werkzeug.utils import redirect
from chess import *
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket = SocketIO(app, ping_timeout=10, ping_interval=5, manage_session=False)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

USERS = []
GAMES = []


BOARDS = {}
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

TURNS = {}


@app.route('/')
def index():
    if session.get('name') is None or session.get('color') is None:
        return render_template('login.html')
    else:
        session.clear()
        return redirect("/")


@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        if not (not request.form.get('name') or not request.form.get('color')):
            if request.form.get('color') in ['Black', 'White']:
                session['name'] = escape(request.form.get('name'))
                session['color'] = request.form.get('color')

                return redirect("/waiting")
    return redirect("/")


@app.route("/waiting")
def waiting():
    if session.get('name') is None or session.get('color') is None:
        return redirect("/")
    else:
        return render_template("waiting.html")


@socket.on('waiting_room', namespace="/waiting")
def waiting_room(result):
    print(result)
    if session.get('name') is None or session.get('color') is None:
        return redirect("/")
    else:
        data = {'name': session['name'], 'sid': request.sid,
                'color': session['color'], 'code': result['code']}
        USERS.append(data)

        for user in USERS:
            if user['color'] != session['color'] and user['code'] == result['code']:
                emit('is_ready', {'ready?': ""}, room=user['sid'])
                emit('is_ready', {'ready?': ""}, room=request.sid)

                data = {'code': user['code'], 'White': None,
                        'Black': None, 'status': 'init'}
                token = secrets.token_hex(16)
                data['token'] = token

                GAMES.append(data)


@socket.on('start', namespace='/waiting')
def start(result):
    if session.get('name') is None or session.get('color') is None:
        return redirect("/")
    else:
        for user in USERS:
            if user['sid'] == request.sid:
                for data in GAMES:
                    if data['code'] == user['code'] and data['status'] == 'init':
                        token = data['token']
                        if user['color'] == 'Black':
                            data['Black'] = request.sid
                        else:
                            data['White'] = request.sid
                        session['token'] = token

                        if data['Black'] != None and data['White'] != None:
                            data['status'] = 'playing'
                            BOARDS[token] = copy.deepcopy(board)
                            TURNS[token] = 'White'
                        emit('start', {'Starting': ""}, room=request.sid)


@socket.on("disconnect", namespace="/waiting")
def waiting_disconnect():
    delete = True
    for data in GAMES:
        if (data['Black'] == request.sid or data['White'] == request.sid) and data['status'] == 'playing':
            delete = False
            break
    if delete == True:
        for user in USERS:
            if request.sid == user['sid']:
                USERS.remove(user)
                break
        token = session['token']
        emit("Oppo_Disconnect", 'Sorry your opponent disconnected',
             room=token, namespace="/waiting")


"""
------------------------------------------
-------------- Start Game ----------------
------------------------------------------
"""


@ app.route("/game")
def game():
    print(USERS)
    if session.get('name') is None or session.get('color') is None:
        return redirect("/")
    else:
        token = session['token']
        for data in GAMES:
            if data['token'] == token and data['status'] == 'playing':
                if session['color'] == 'White':
                    return render_template('game.html', color='white', num=2)
                else:
                    return render_template('game.html', color='black', num=1)

        return redirect("/")


@ socket.on("connect", namespace="/game")
def on_connect():
    if session.get('name') is None or session.get('color') is None or session.get('token') is None:
        return redirect("/")
    else:
        token = session['token']
        join_room(token)
        data = send_moves(BOARDS[token], 'White')
        emit('update_moves', data, room=token, namespace='/game')


@socket.on("disconnect", namespace="/game")
def on_disconnect():
    token = session['token']
    for data in GAMES:
        if data['token'] == token:
            for user in USERS:
                if request.sid == user['sid']:
                    if data['status'] == 'ended':
                        session['token'] = None
                    else:
                        emit("Oppo_Disconnect", 'Sorry your opponent disconnected',
                             room=token, namespace="/game")
            USERS.remove(user)
            GAMES.remove(data)


@ socket.on('make_move', namespace='/game')
def make_move(response):
    if session.get('name') is None or session.get('color') is None or session.get('token') is None:
        return redirect("/")
    else:
        token = session['token']
        turn = TURNS[token]
        if turn != session['color']:
            print("Disconnecting")
            emit('disconnect', {}, room=request.sid)
        elif type(response) == dict:
            move_type = list(response.keys())[0]
            if move_type == 'move':
                # Unpack data
                x1 = int(response['move'][0][0])
                y1 = int(response['move'][0][1])
                x2 = int(response['move'][1][0])
                y2 = int(response['move'][1][1])

                if BOARDS[token][x1][y1] != None and (x2, y2) in BOARDS[token][x1][y1].get_moves(BOARDS[token]):
                    # Assign old cell to selected cell
                    BOARDS[token][x2][y2] = BOARDS[token][x1][y1]
                    BOARDS[token][x2][y2].change_pos(x2, y2)

                    # Remove Old Object Completely from memory
                    buffer = BOARDS[token][x1][y1]
                    BOARDS[token][x1][y1] = None
                    del buffer

                emit('make_move', {
                    'color': BOARDS[token][x2][y2].get_color(), 'move': [(x1, y1), (x2, y2)]}, room=token, namespace='/game')
            elif move_type == 'promation':
                # Unpack data
                if response['name'] in ['rook', 'knight', 'queen', 'bishop']:
                    print(response['name'])
                    x1 = int(response['promation'][0][0])
                    y1 = int(response['promation'][0][1])
                    x2 = int(response['promation'][1][0])
                    y2 = int(response['promation'][1][1])

                    if BOARDS[token][x1][y1] != None and (x2, y2) in BOARDS[token][x1][y1].get_promation(BOARDS[token]):
                        if response['name'] == 'queen':
                            temp = Queen(
                                x2, y2, BOARDS[token][x1][y1].get_color())

                        elif response['name'] == 'bishop':
                            temp = Bishop(
                                x2, y2, BOARDS[token][x1][y1].get_color())

                        elif response['name'] == 'knight':
                            temp = Knight(
                                x2, y2, BOARDS[token][x1][y1].get_color())

                        elif response['name'] == 'rook':
                            temp = Rook(
                                x2, y2, BOARDS[token][x1][y1].get_color())

                        BOARDS[token][x2][y2] = temp
                        buffer = BOARDS[token][x1][y1]
                        BOARDS[token][x1][y1] = None
                        del buffer
                    emit('make_move', {
                        'color': BOARDS[token][x2][y2].get_color(), 'move': [(x1, y1), (x2, y2)]}, room=token, namespace='/game')
                    emit('make_move', {
                        'color': BOARDS[token][x2][y2].get_color(), 'promation': [x2, y2, response['name']]}, room=token, namespace='/game')

            elif move_type == 'castle':
                # Unpack data
                x1 = int(response['castle'][0][0])
                y1 = int(response['castle'][0][1])
                x2 = int(response['castle'][1][0])
                y2 = int(response['castle'][1][1])

                # King Castle
                castle = BOARDS[token][x1][y1].get_castle(BOARDS[token])
                if castle != None:
                    for kx2, ky2, rx1, ry1, rx2, ry2 in castle:
                        if x2 == kx2 and y2 == ky2:
                            # Assign old King to selected cell
                            BOARDS[token][kx2][ky2] = BOARDS[token][x1][y1]
                            BOARDS[token][kx2][ky2].change_pos(kx2, ky2)

                            # Remove Old King Completely from memory
                            buffer = BOARDS[token][x1][y1]
                            BOARDS[token][x1][y1] = None
                            del buffer

                            # Assign old Rook to selected cell
                            BOARDS[token][rx2][ry2] = BOARDS[token][rx1][ry1]
                            BOARDS[token][rx2][ry2].change_pos(rx2, ry2)

                            # Remove Old Rook Completely from memory
                            buffer = BOARDS[token][rx1][ry1]
                            BOARDS[token][rx1][ry1] = None
                            del buffer

                            emit('make_move', {
                                'color': BOARDS[token][x2][y2].get_color(), 'move': [(x1, y1), (kx2, ky2)]}, room=token, namespace='/game')
                            emit('make_move', {
                                'color': BOARDS[token][x2][y2].get_color(), 'move': [(rx1, ry1), (rx2, ry2)]}, room=token, namespace='/game')

            TURNS[token] = 'Black' if turn == 'White' else 'White'
            turn = TURNS[token]
            data, king = send_moves(BOARDS[token], turn)

            emit('update_moves', data, room=token, namespace='/game')

            for row in data:
                if row['color'] != turn and (('move' in row and row['move'][1] == king) or
                                             ('castle' in row and row['castle'][3] == king) or
                                             ('promation' in row and row['promation'][1] == king)):
                    emit('check', {'king': king}, room=token, namespace='/game')
                    break

            white_result = []
            black_result = []
            for i in range(8):
                for j in range(8):
                    if BOARDS[token][i][j] != None and len(BOARDS[token][i][j].get_moves(BOARDS[token])):
                        if BOARDS[token][i][j].get_color() == 'White':
                            white_result.append(BOARDS[token][i][j].get_name())
                        else:
                            black_result.append(BOARDS[token][i][j].get_name())

            print("Checking if game Ended")
            ended = False
            if len(black_result) == 0 and turn == 'Black':
                emit('end_game', 'White', room=token, namespace='/game')
                ended = True
            elif len(white_result) == 0 and turn == 'White':
                emit('end_game', 'Black', room=token, namespace='/game')
                ended = True
            elif len(black_result) == 1 and len(white_result) == 1 and \
                    black_result[0] == 'King' and white_result[0] == 'King':
                emit('end_game', 'Tie', room=token, namespace='/game')
                ended = True

            if ended == True:
                for data in GAMES:
                    if data['token'] == token:
                        data['status'] = 'ended'
            print("game not  Ended")


if __name__ == '__main__':
    socket.run(app)
