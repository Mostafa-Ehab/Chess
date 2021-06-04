from ai import ai_get_move
from os import name
from flask import Flask, render_template, request, redirect, session
# from flask.signals import Namespace
from flask_session import Session
from tempfile import mkdtemp
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from werkzeug.utils import redirect
from chess import *
from helper import *
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
AI_GAME = []


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
            if request.form.get('color') in ['Black', 'White'] and request.form.get('vs') in ['vs Friend', 'vs AI']:
                session['name'] = escape(request.form.get('name'))
                session['color'] = request.form.get('color')
                if request.form.get('vs') == 'vs Friend':
                    return redirect("/waiting")
                else:
                    token = secrets.token_hex(16)
                    session['token'] = token
                    BOARDS[token] = copy.deepcopy(board)
                    TURNS[token] = 'White'

                    data = {'token': token, 'status': 'playing'}
                    AI_GAME.append(data)

                    return redirect("/ai-game")
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
--------- Start Game VS Friend -----------
------------------------------------------
"""


@app.route("/game")
def game():
    print(USERS)
    if session.get('name') is None or session.get('color') is None:
        return redirect("/")
    else:
        token = session['token']
        for data in GAMES:
            if data['token'] == token and data['status'] == 'playing':
                if session['color'] == 'White':
                    return render_template('game.html', color='white', num='Player 2', vs='friend')
                else:
                    return render_template('game.html', color='black', num='Player 1', vs='friend')

        return redirect("/")


@socket.on("connect", namespace="/game")
def on_game_connect():
    if session.get('name') is None or session.get('color') is None or session.get('token') is None:
        return redirect("/")
    else:
        token = session['token']
        join_room(token)
        data = get_moves(BOARDS[token], 'White')
        emit('update_moves', data, room=token, namespace='/game')


@socket.on("disconnect", namespace="/game")
def on_game_disconnect():
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


@socket.on('make_move', namespace='/game')
def make_game_move(response):
    if session.get('name') is None or session.get('color') is None or session.get('token') is None:
        return redirect("/")
    else:
        token = session['token']
        turn = TURNS[token]

        # Try to Cheat
        if turn != session['color']:
            print("Disconnecting")
            emit('disconnect', {}, room=request.sid)

        # A valid move
        elif type(response) == dict:
            # Make move and send it to the other player
            moves = make_move(BOARDS[token], response)
            for row in moves:
                emit('make_move', row, room=token, namespace='/game')

            # Change turn
            TURNS[token] = 'Black' if turn == 'White' else 'White'
            turn = TURNS[token]

            # Get all available moves and send it to both players
            data, king = get_moves(BOARDS[token], turn)
            emit('update_moves', data, room=token, namespace='/game')

            # Check if King is Checked
            if is_checked(data, king, turn) != None:
                emit('check', {'king': king}, room=token, namespace='/game')

            # Check if game Ended
            ended = check_end(BOARDS[token], turn)
            if ended != None:
                emit('end_game', ended, room=token, namespace='/game')
                # End Game
                for data in GAMES:
                    if data['token'] == token:
                        data['status'] = 'ended'


"""
------------------------------------------
----------- Start Game VS AI -------------
------------------------------------------
"""


@app.route('/ai-game')
def ai_game():
    if session.get('name') is None or session.get('color') is None:
        return redirect("/")
    else:
        if session['color'] == 'White':
            return render_template('game.html', color='white', num='Computer', vs='ai')
        else:
            return render_template('game.html', color='black', num='Computer', vs='ai')


@socket.on("connect", namespace="/ai-game")
def on_ai_game_connect():
    if session.get('name') is None or session.get('color') is None or session.get('token') is None:
        return redirect("/")
    else:
        token = session['token']
        data = get_moves(BOARDS[token], 'White')
        emit('update_moves', data, namespace='/ai-game')


@socket.on("disconnect", namespace="/ai-game")
def on_ai_game_disconnect():
    token = session['token']
    for data in AI_GAME:
        if data['token'] == token:
            for user in USERS:
                if request.sid == user['sid']:
                    if data['status'] == 'ended':
                        session['token'] = None
                    else:
                        USERS.remove(user)
                    AI_GAME.remove(data)


@socket.on('make_move', namespace='/ai-game')
def make_ai_game_move(response):
    if session.get('name') is None or session.get('color') is None or session.get('token') is None:
        return redirect("/")
    else:
        token = session['token']
        turn = TURNS[token]
        if turn != session['color']:
            print("Disconnecting")
            emit('disconnect', {}, room=request.sid)
        elif type(response) == dict:
            # Make move and send it to the other player
            make_move(BOARDS[token], response)

            # Change turn
            TURNS[token] = 'Black' if turn == 'White' else 'White'
            turn = TURNS[token]

            # Check if game Ended
            ended = check_end(BOARDS[token], turn)
            if ended != None:
                emit('end_game', ended, namespace='/ai-game')
                # End Game
                for data in GAMES:
                    if data['token'] == token:
                        data['status'] = 'ended'

            # Call AI to play
            response = ai_get_move()

            # Apply AI Play and send it to the player
            moves = make_move(BOARDS[token], response)
            for row in moves:
                emit('make_move', row, namespace='/ai-game')

            # Get all available moves and send it to the player
            data, king = get_moves(BOARDS[token], turn)
            emit('update_moves', data, namespace='/ai-game')

            # Change turn
            TURNS[token] = 'Black' if turn == 'White' else 'White'
            turn = TURNS[token]

            # Check if King is Checked
            if is_checked(data, king, turn) != None:
                emit('check', {'king': king}, namespace='/ai-game')

            # Check if game Ended
            ended = check_end(BOARDS[token], turn)
            if ended != None:
                emit('end_game', ended, namespace='/ai-game')
                # End Game
                for data in GAMES:
                    if data['token'] == token:
                        data['status'] = 'ended'


if __name__ == '__main__':
    socket.run(app)
