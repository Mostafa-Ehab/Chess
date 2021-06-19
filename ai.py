from board import *
from piece import *
from func import *
import numpy as np
import random
import copy

AI_BOARDS = []


class AI_Board:
    def __init__(self, board, turn):
        self.board = copy.deepcopy(board)
        self.turn = turn
        self.value = None

    def __eq__(self, other):
        if self.turn == other.turn:
            for i in range(8):
                for j in range(8):
                    if (self.board[i, j] != None and other.board[i, j] != None) and \
                        ((self.board[i, j].get_name() != other.board[i, j].get_name()) or
                         (self.board[i, j].get_color() != other.board[i, j].get_color()) or
                         (self.board[i, j].moved != other.board[i, j].moved)):
                        return False
            return True
        else:
            return False

    def get_val(self):
        # If Value is not calculated before
        if self.value == None:
            self.value = 0
            for i in range(8):
                for j in range(8):
                    if self.board[i, j] != None:
                        self.value += self.board[i, j].get_value()
        # If Value already calculated
        else:
            return self.value


def get_best_move(board):
    actions = board.get_action()
    # return random.choice(actions)

    if board.get_turn() == 'White':
        Max = float('-INF')
        for action in actions:
            print(f"Trying action {action}")
            v = min_value(result(board, action), 5, Max)
            if v > Max:
                Max = v
                best = action
        return best
    elif board.get_turn() == 'Black':
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
    #     temp = copy.deepcopy(board)


def max_value(board, i, Min):
    if board.is_end() or i == 0:
        val = board.get_value()
        print(f"Reached End with value {val}")
        return board.get_value()

    # if board in AI_BOARDS:
    #     return board.get_value

    actions = board.get_action()
    v = float('-INF')
    for action in actions:
        v_max = min_value(result(board, action), i-1, v)
        v = max(v, v_max)
        if v > Min:
            print("Breaking Max")
            return v
    return v


def min_value(board, i, Max):
    if board.is_end() or i == 0:
        val = board.get_value()
        print(f"Reached End with value {val}")
        return board.get_value()

    actions = board.get_action()
    v = float('INF')
    for action in actions:
        v_min = max_value(result(board, action), i-1, v)
        v = min(v, v_min)
        if v < Max:
            print("Breaking Min")
            return v
    return v


def result(board, action):
    # if board in AI_BOARDS:
    board = copy.deepcopy(board)
    board.make_action(action)
    print(board.get_turn())
    prettyList(board.board.tolist())
    return board
