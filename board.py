from piece import *
from func import *
import copy
import numpy as np
import gc

empty_board = np.array([
    [Rook(0, 0, "Black", -25), Knight(0, 1, "Black", -24), Bishop(0, 2, "Black", -23), Queen(0, 3, "Black", -100),
     King(0, 4, "Black", 0), Bishop(0, 5, "Black", -23), Knight(0, 6, "Black", -24), Rook(0, 7, "Black", -25)],
    [Pawn(1, i, "Black", -10) for i in range(8)],
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [Pawn(6, i, "White", 10) for i in range(8)],
    [Rook(7, 0, "White", 25), Knight(7, 1, "White", 24), Bishop(7, 2, "White", 23), Queen(7, 3, "White", 100),
     King(7, 4, "White", 0), Bishop(7, 5, "White", 23), Knight(7, 6, "White", 24), Rook(7, 7, "White", 25)],
])


class Board:
    def __init__(self, token, white, black, board=empty_board, turn="White"):
        self.token = token
        self.white = white
        self.black = black
        self.board = copy.deepcopy(board)
        self.turn = turn
        self.last_actions = []
        self.ended = False

    def __str__(self):
        self.token

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

    def get_token(self):
        return self.token

    def get_turn(self):
        return self.turn

    def get_oppo(self):
        return "White" if (self.turn == "Black") else "Black"

    def get_white(self):
        return self.white

    def get_black(self):
        return self.black

    def get_turn_token(self):
        if self.get_turn() == "White":
            return self.get_white()
        else:
            return self.get_black()

    def get_value(self):
        value = 0
        for i in range(8):
            for j in range(8):
                if self.board[i, j] != None:
                    value += self.board[i, j].get_value()
        return value

    def change_turn(self):
        self.turn = "White" if (self.turn == "Black") else "Black"

    def make_action(self, actions, real=False):
        action_type = list(actions.keys())[0]

        action = actions[action_type]
        x1 = action[0][0]
        y1 = action[0][1]
        x2 = action[1][0]
        y2 = action[1][1]

        # Make Action
        self.board[x2, y2] = self.board[x1, y1]
        self.board[x2, y2].change_pos(x2, y2)
        temp = self.board[x1, y1]
        self.board[x1, y1] = None
        del temp

        # Additional Action
        if action_type == "castle":
            if (real == True):
                print("Castling")

            rx1 = action[2][0]
            ry1 = action[2][1]
            rx2 = action[3][0]
            ry2 = action[3][1]

            # Make Rook Action
            self.board[rx2, ry2] = self.board[rx1, ry1]
            self.board[rx2, ry2].change_pos(rx2, ry2)
            temp = self.board[x1, y1]
            self.board[rx1, ry1] = None
            del temp

        elif action_type == "promation":
            print("Promating")
            temp = self.board[x2, y2]
            self.board[x2, y2] = None
            del temp
            # Make Promation
            if actions['name'] == 'queen':
                val = 100 if self.get_turn() == "White" else -100
                temp = Queen(x2, y2, self.get_turn(), val)

            elif actions['name'] == 'bishop':
                val = 23 if self.get_turn() == "White" else -23
                temp = Bishop(x2, y2, self.get_turn(), val)

            elif actions['name'] == 'knight':
                val = 24 if self.get_turn() == "White" else -24
                temp = Knight(x2, y2, self.get_turn(), val)

            elif actions['name'] == 'rook':
                val = 25 if self.get_turn() == "White" else -25
                temp = Rook(x2, y2, self.get_turn(), val)

            self.board[x2, y2] = temp

        if (real == True):
            prettyList(self.board.tolist())

        self.change_turn()
        gc.collect()

    def get_action(self):
        actions = []
        for i in range(8):
            for j in range(8):
                if self.board[i, j] != None and self.board[i, j].get_color() == self.get_turn():
                    action = self.board[i, j].get_action(self.board)
                    for act in action:
                        action_type = list(act.keys())[0]
                        x, y = act[action_type][1]
                        # Move or Promation
                        if action_type in ['promation', 'move']:
                            if x in range(8) and y in range(8):
                                if self.board[i, j].get_name() == "Knight" and self.board[x, y] != None and self.board[x, y].get_color() == self.get_turn():
                                    continue
                                # Check Action Validity
                                temp = copy.deepcopy(self)
                                temp.make_action({"move": act[action_type]})
                                if temp.is_check_mate() == True:
                                    actions.append(act)
                                del temp
                        # Castle
                        else:
                            if y > j:
                                # At Casteling King Side
                                temp = copy.deepcopy(self)
                                temp.change_turn()
                                # Check that King is not checked
                                if temp.is_check_mate() == True:
                                    del temp
                                    temp = copy.deepcopy(self)
                                    temp.make_action(
                                        {"move": ((i, j), (i, j + 1))})

                                    if temp.is_check_mate() == True:
                                        del temp
                                        temp = copy.deepcopy(self)
                                        temp.make_action(
                                            {"move": ((i, j), (i, j + 2))})

                                        if temp.is_check_mate() == True:
                                            print(act)
                                            actions.append(act)
                                del temp
                            else:
                                # At Casteling Queen Side
                                temp = copy.deepcopy(self)
                                temp.change_turn()
                                # Check that King is not checked
                                if temp.is_check_mate() == True:
                                    del temp
                                    temp = copy.deepcopy(self)
                                    temp.make_action(
                                        {"move": ((i, j), (i, j - 1))})

                                    if temp.is_check_mate() == True:
                                        del temp
                                        temp = copy.deepcopy(self)
                                        temp.make_action(
                                            {"move": ((i, j), (i, j - 2))})

                                        if temp.is_check_mate() == True:
                                            print(act)
                                            actions.append(act)
                                del temp
        gc.collect()
        return actions

    def is_check_mate(self):
        for i in range(8):
            for j in range(8):
                if self.board[i, j] != None and self.board[i, j].get_color() == self.get_turn():
                    # Sure that the king is not checked
                    actions = self.board[i, j].get_action(self.board)
                    for action in actions:
                        action_type = list(action.keys())[0]
                        if action_type == "move":
                            action = action['move']
                            x = action[1][0]
                            y = action[1][1]
                            if x in range(8) and y in range(8) \
                                    and self.board[x, y] != None \
                                    and self.board[x, y].get_name() == "King" \
                                    and self.board[x, y].get_color() != self.get_turn():
                                return False

        return True

    def is_end(self):
        if self.ended == False:
            for i in range(8):
                for j in range(8):
                    if self.board[i, j] != None and self.board[i, j].get_name() != "King" and len(self.get_last_actions()) != 0:
                        return False
            self.ended = True
        return True

    def get_winner(self):
        if self.is_end():
            if len(self.get_last_actions()) > 0:
                return "Tie"
            return self.get_oppo()

    def get_king_pos(self):
        for i in range(8):
            for j in range(8):
                if self.board[i, j] != None and self.board[i, j].get_name() == "King" and self.board[i, j].get_color() == self.get_turn():
                    return (i, j)

    def get_last_actions(self):
        return self.last_actions

    def set_last_actions(self, actions):
        del self.last_actions
        self.last_actions = actions
        gc.collect()
