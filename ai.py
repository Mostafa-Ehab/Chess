import copy
from chess import *
from helper import *
import random
import json


def get_actions(board, turn):
    actions, _ = get_moves(board, turn)
    moves = []
    for action in actions:
        action_type = list(action.keys())[0]

        if action_type == 'move':
            i = action['move'][0][0]
            j = action['move'][0][1]

            if board[i][j].get_color() == turn:
                moves.append(action)
        elif action_type == 'promation':
            i = action['promation'][0][0]
            j = action['promation'][0][1]

            if board[i][j].get_color() == turn:
                for name in ['rook', 'knight', 'queen', 'bishop']:
                    promat = {}
                    promat['promation'] = action['promation']
                    promat['name'] = name
                    moves.append(promat)

        elif action_type == 'castle':
            i = action['castle'][0][0]
            j = action['castle'][0][1]

            if board[i][j].get_color() == turn:
                moves.append(action)

    return moves


def ai_get_move(board, turn, recursion):
    actions = get_actions(board, turn)
    # results = []
    # for action in actions:
    #     print(f"Trying to apply action {action}")
    #     results.append([utility(result(board, action), turn), action])

    if turn == 'White':
        # results = []
        Max = float('-INF')
        for action in actions:
            print(f"Trying action {action}")
            v = min_value(result(board, action), 5, Max)
            if v > Max:
                Max = v
                best = action
        return best

        # results.append([min_value(result(board, action), 5), action])

        # print(results)

        # for i in results:
        #     if i[0] > Max:
        #         Max = i[0]
        #         action = i[1]
        # return action

    elif turn == 'Black':
        # results = []
        Min = float('INF')
        print(Min)
        for action in actions:
            print(f"Trying action {action}")
            v = max_value(result(board, action), 1, Min)
            if v < Min:
                Min = v
                best = action
        return best

        # for action in actions:
        #     print(f"Trying action {action}")
        #     results.append(
        #         [max_value(result(board, action), 2), action])

        # print(results)
        # Min = float('INF')
        # for i in results:
        #     if i[0] < Min:
        #         Min = i[0]
        #         action = i[1]
        # return action
        # return random.choice(moves)


def utility(board, turn):
    winner = check_end(board, turn)
    if winner == None:
        value = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] != None:
                    value += board[i][j].get_value()
        return value
    else:
        if winner == 'White':
            return 500
        if winner == 'Black':
            return -500
        else:
            return 0


def minimax():
    pass


def result(main_board, action):
    board = copy.deepcopy(main_board)
    move_type = list(action.keys())[0]

    if move_type == 'move':
        # Unpack data
        x1 = int(action['move'][0][0])
        y1 = int(action['move'][0][1])
        x2 = int(action['move'][1][0])
        y2 = int(action['move'][1][1])

        if board[x1][y1] != None and (x2, y2) in board[x1][y1].get_moves(board):
            # Assign old cell to selected cell
            board[x2][y2] = board[x1][y1]
            board[x2][y2].change_pos(x2, y2)

            # Remove Old Object Completely from memory
            buffer = board[x1][y1]
            board[x1][y1] = None
            del buffer

            return board
    elif move_type == 'promation':
        # Unpack data
        if action['name'] in ['rook', 'knight', 'queen', 'bishop']:
            x1 = int(action['promation'][0][0])
            y1 = int(action['promation'][0][1])
            x2 = int(action['promation'][1][0])
            y2 = int(action['promation'][1][1])

            if board[x1][y1] != None and (x2, y2) in board[x1][y1].get_promation(board):
                if action['name'] == 'queen':
                    temp = Queen(
                        x2, y2, board[x1][y1].get_color(), 100 if x1 == 6 else -100)

                elif action['name'] == 'bishop':
                    temp = Bishop(
                        x2, y2, board[x1][y1].get_color(), 23 if x1 == 6 else -23)

                elif action['name'] == 'knight':
                    temp = Knight(
                        x2, y2, board[x1][y1].get_color(), 24 if x1 == 6 else -24)

                elif action['name'] == 'rook':
                    temp = Rook(
                        x2, y2, board[x1][y1].get_color(), 25 if x1 == 6 else -25)

                board[x2][y2] = temp
                buffer = board[x1][y1]
                board[x1][y1] = None
                del buffer

                return board

    elif move_type == 'castle':
        # Unpack data
        x1 = int(action['castle'][0][0])
        y1 = int(action['castle'][0][1])
        x2 = int(action['castle'][1][0])
        y2 = int(action['castle'][1][1])

        # King Castle
        castle = board[x1][y1].get_castle(board)
        if castle != None:
            for kx2, ky2, rx1, ry1, rx2, ry2 in castle:
                if x2 == kx2 and y2 == ky2:
                    # Assign old King to selected cell
                    board[kx2][ky2] = board[x1][y1]
                    board[kx2][ky2].change_pos(kx2, ky2)

                    # Remove Old King Completely from memory
                    buffer = board[x1][y1]
                    board[x1][y1] = None
                    del buffer

                    # Assign old Rook to selected cell
                    board[rx2][ry2] = board[rx1][ry1]
                    board[rx2][ry2].change_pos(rx2, ry2)

                    # Remove Old Rook Completely from memory
                    buffer = board[rx1][ry1]
                    board[rx1][ry1] = None
                    del buffer

                    return board


def max_value(board, i, Min):
    turn = 'White'
    if check_end(board, turn) or i == 0:
        val = utility(board, turn)
        print(f"Reached End with value {val}")
        return utility(board, turn)

    actions = get_actions(board, turn)
    v = float('-INF')
    for action in actions:
        v_max = min_value(result(board, action), i-1, v)
        v = max(v, v_max)
        if v > Min:
            print("Breaking Max")
            return v

    return v


def min_value(board, i, Max):
    turn = 'Black'
    if check_end(board, turn) or i == 0:
        val = utility(board, turn)
        print(f"Reached End with value {val}")
        return utility(board, turn)

    actions = get_actions(board, turn)
    v = float('INF')
    for action in actions:
        v_min = max_value(result(board, action), i-1, v)
        v = min(v, v_min)
        if v < Max:
            print("Breaking Min")
            return v

    return v
