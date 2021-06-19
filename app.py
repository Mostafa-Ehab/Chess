from flask import Flask, session, render_template, redirect
from flask.globals import request
from flask_session import Session
from flask_socketio import SocketIO, Namespace, emit, join_room
from tempfile import mkdtemp
import secrets
import logging

from board import *
from func import *
from ai import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket = SocketIO(app, ping_timeout=10, ping_interval=5, manage_session=False)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

log = logging.getLogger('werkzeug')
log.disabled = True

USERS = []
GAMES = []
AI_GAMES = []
AI_USERS = []
# BOARDS = []


@app.route("/")
def index():
    if session.get("token") is None or session.get("color") is None:
        return render_template('login.html')
    else:
        session.clear()
        return redirect("/")


@app.route("/login", methods=['POST'])
def login():
    if request.method == "POST":
        if request.form.get("color") and request.form.get("color") in ["Black", "White"]:
            # Check form Validity
            token = secrets.token_hex(16)
            session["token"] = token
            session["color"] = request.form.get("color")

            # CHeck opponent
            if request.form.get("vs") and request.form.get("vs") == "vs Friend":
                return redirect("/waiting")
            else:
                return redirect("/ai-game")
    return redirect("/")


@app.route("/waiting")
def waiting():
    if session.get("token"):
        return render_template("waiting.html")
    return redirect("/")


class Waiting(Namespace):
    def on_connect(self):
        if session.get("token"):
            # Add User to USERS List
            user = {"token": session['token'],
                    "code": None,
                    "color": session['color'],
                    "status": None,
                    "sid": None}

            USERS.append(user)

            # Set Room with token for easy communication
            join_room(session['token'])

    def on_disconnect(self):
        for user in USERS:
            if user['sid'] == request.sid:
                USERS.remove(user)
                del user
                break
        gc.collect()

    def on_code(self, data):
        if session.get("token"):
            for user in USERS:
                # Setup User Data
                if user['token'] == session.get('token'):
                    user['status'] = "waiting"
                    user['code'] = data['code']
                    session['code'] = data['code']
                    break

            for user in USERS:
                # Search for Waiting opponent with the same Code and opposite color
                if user['code'] == session['code'] and user['color'] != session['color'] and user['status'] != "playing":
                    emit("ready", {"ready": None}, room=user['token'])
                    emit("ready", {"ready": None})

                    white = user['token'] if user['color'] == "White" else session['token']
                    black = user['token'] if user['color'] == "Black" else session['token']

                    board = Board(secrets.token_hex(
                        16), white, black)
                    # BOARDS.append(board)
                    GAMES.append(board)
                    break

    def on_ready(self, data):
        if session.get("token"):
            # Change User State and Send Start
            for user in USERS:
                if user['token'] == session.get('token'):
                    user['status'] = "playing"
                    session['status'] = "playing"
                    break
            emit("start", {"start": None})


socket.on_namespace(Waiting("/waiting"))


@app.route("/game")
def game():
    if session.get("token"):
        for user in USERS:
            if user['status'] == "playing":
                if session['color'] == 'White':
                    return render_template('game.html', color='white', num='Player 2', vs='friend')
                else:
                    return render_template('game.html', color='black', num='Player 1', vs='friend')
                    # return render_template('game.html', color='white', num='Player 1', vs='friend')

    return redirect("/")


class Game(Namespace):
    def on_connect(self):
        if session.get("token"):
            for board in GAMES:
                if board.get_white() == session['token'] or board.get_black() == session['token']:
                    # Add user to Room with board token for easier communication
                    join_room(board.get_token())
                    join_room(session['token'])

                    # Add SID to USERS
                    for user in USERS:
                        if user['token'] == session['token']:
                            user["sid"] = request.sid

                    # Send Actions
                    if session['color'] == board.get_turn():
                        actions = board.get_action()
                        emit("update_action", actions)
                        board.set_last_actions(actions)
                    break

    def on_disconnect(self):
        Ended = False
        for board in GAMES:
            if board.is_end() == True:
                print("Game Ended")
                Ended = True
                # Remove User and its opponent
                white = board.get_white()
                for user in USERS:
                    if user['token'] == white:
                        USERS.remove(user)
                        del user
                        break
                black = board.get_black()
                for user in USERS:
                    if user['token'] == black:
                        USERS.remove(user)
                        del user
                        break
                # Delete Board from GAMES
                GAMES.remove(board)
                del board
                break
        # If Opponent Disconnected and Game not Ended
        if Ended == False:
            for user in USERS:
                if user['sid'] == request.sid:
                    # Send Alert to The other player
                    for board in GAMES:
                        if user['token'] in [board.get_black(), board.get_white()]:
                            emit("oppo_disconnect",
                                 'Sorry your opponent disconnected',
                                 room=board.get_token())
                            # Remove User and its opponent
                            white = board.get_white()
                            for user in USERS:
                                if user['token'] == white:
                                    USERS.remove(user)
                                    del user
                                    break
                            black = board.get_black()
                            for user in USERS:
                                if user['token'] == black:
                                    USERS.remove(user)
                                    del user
                                    break
                            # Delete Board from GAMES
                            GAMES.remove(board)
                            del board
                            break
                    break
        gc.collect()

    def on_make_action(self, action):
        if session.get("token"):
            for board in GAMES:
                if board.get_turn_token() == session['token']:
                    print(action)

                    # Convert Recieved Action List to Tuple For easily compare
                    action_type = list(action.keys())[0]
                    action[action_type] = to_tuple(action[action_type])

                    # Check Action Validity and Apply it
                    actions = board.get_last_actions()
                    for act in actions:
                        if str(act) == str(action):
                            # Apply Action on Server
                            board.make_action(action, real=True)

                            # Send Action to Next Player
                            turn_token = board.get_turn_token()
                            new_actions = board.get_action()
                            emit("make_action", action, room=turn_token)

                            # Send new actions to the Next Player
                            emit("update_action", new_actions, room=turn_token)
                            # print(new_actions)
                            board.set_last_actions(new_actions)
                            break

                    game_token = board.get_token()
                    # Check if Check Mate
                    temp = copy.deepcopy(board)
                    temp.change_turn()
                    if temp.is_check_mate() == False:
                        emit("check_mate",
                             {"king": board.get_king_pos()},
                             room=game_token)
                    del temp

                    # Check game End
                    if board.is_end():
                        emit("end_game",
                             {"winner": board.get_winner()},
                             room=game_token)
                    break
            gc.collect()


socket.on_namespace(Game("/game"))


@app.route("/ai-game")
def ai_game():
    if session.get("token"):
        if session['color'] == 'White':
            return render_template('game.html', color='white', num='Computer', vs='ai')
        else:
            return render_template('game.html', color='black', num='Computer', vs='ai')
    return redirect("/")


class AI_Game(Namespace):
    def on_connect(self):
        if session.get("token"):
            # white = session['token'] if session['color'] == "White" else session['token']
            # black = user['token'] if user['color'] == "Black" else session['token']
            # Initiate Game
            board = Board(session['token'], session['token'], session['token'])
            AI_GAMES.append(board)

            # Add SID to USERS
            user = {"token": session['token'],
                    "sid": request.sid, "color": session['color']}
            AI_USERS.append(user)

            # Send Actions
            if session['color'] == board.get_turn():
                actions = board.get_action()
                emit("update_action", actions)
                board.set_last_actions(actions)
            else:
                # Get AI Move and send to the Player
                print("Called AI Func")
                action = get_best_move(board)
                board.make_action(action, real=True)
                emit("make_action", action)

            # Add to room for easier communication
            join_room(session['token'])

    def on_disconnect(self):
        Ended = False
        for board in AI_GAMES:
            if board.is_end() == True:
                print("Game Ended")
                Ended = True
                # Remove User from AI_USERS
                for user in AI_USERS:
                    if user['sid'] == request.sid:
                        AI_USERS.remove(user)
                        del user
                        break
                # Delete Board from AI_GAMES
                AI_GAMES.remove(board)
                del board
                break
        # If Opponent Disconnected and Game not Ended
        if Ended == False:
            for user in AI_USERS:
                if user['sid'] == request.sid:
                    # Send Alert to The other player
                    for board in AI_GAMES:
                        if user['token'] == board.get_token():
                            # Delete User from AI_USERS
                            AI_USERS.remove(user)
                            del user
                            # Delete Board from AI_GAMES
                            AI_GAMES.remove(board)
                            del board
                            break
                    break
        gc.collect()

    def on_make_action(self, action):
        if session.get("token"):
            for board in AI_GAMES:
                if board.get_token() == session['token']:
                    token = board.get_turn_token()
                    print(action)

                    # Convert Recieved Action List to Tuple For easily compare
                    action_type = list(action.keys())[0]
                    action[action_type] = to_tuple(action[action_type])

                    # Check Action Validity and Apply it
                    actions = board.get_last_actions()
                    for act in actions:
                        if str(act) == str(action):
                            # Apply Action on Server
                            board.make_action(action, real=True)
                            board.set_last_actions(board.get_action())

                            # Check if Check Mate
                            temp = copy.deepcopy(board)
                            temp.change_turn()
                            if temp.is_check_mate() == False:
                                emit("check_mate",
                                     {"king": board.get_king_pos()},
                                     room=token)
                            del temp

                            # Check game End
                            if board.is_end():
                                emit("end_game",
                                     {"winner": board.get_winner()},
                                     room=token)
                            else:
                                # Get AI Move
                                print("Called AI Func")
                                action = get_best_move(board)
                                board.make_action(action, real=True)

                                # Send Action and new actions to the Player
                                new_actions = board.get_action()
                                emit("make_action", action, room=token)
                                emit("update_action", new_actions, room=token)
                                # print(new_actions)
                                board.set_last_actions(new_actions)

                                # Check if Check Mate
                                temp = copy.deepcopy(board)
                                temp.change_turn()
                                if temp.is_check_mate() == False:
                                    emit("check_mate",
                                         {"king": board.get_king_pos()},
                                         room=token)
                                del temp

                                # Check game End
                                if board.is_end():
                                    emit("end_game",
                                         {"winner": board.get_winner()},
                                         room=token)
                            break
                    break


socket.on_namespace(AI_Game("/ai-game"))
