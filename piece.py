class Peice:
    def __init__(self, x, y, color, value):
        self.x = x
        self.y = y
        self.color = color
        self.moved = False
        self.value = value
        # self.name = None

    # def __eq__(self, other):
    #     if self.get_name() == other.get_name() and self.get_color() == other.get_color() and self.moved == other.moved:
    #         return True
    #     return False

    def get_color(self):
        return self.color

    def get_pos(self):
        return (self.x, self.y)

    def get_value(self):
        return self.value

    def change_pos(self, x, y):
        self.x = x
        self.y = y
        self.moved = True


class Rook(Peice):
    def __str__(self):
        return self.get_color() + "Rook"

    def get_name(self):
        return "Rook"

    def get_action(self, board):
        actions = []
        for i in range(self.x + 1, 8):
            if board[i, self.y] != None and board[i, self.y].get_color() == self.get_color():
                break
            actions.append({"move": (self.get_pos(), (i, self.y))})
            if board[i, self.y] != None and board[i, self.y].get_color() != self.get_color():
                break

        for i in range(self.x - 1, -1, -1):
            if board[i, self.y] != None and board[i, self.y].get_color() == self.get_color():
                break
            actions.append({"move": (self.get_pos(), (i, self.y))})
            if board[i, self.y] != None and board[i, self.y].get_color() != self.get_color():
                break

        for j in range(self.y + 1, 8):
            if board[self.x, j] != None and board[self.x, j].get_color() == self.get_color():
                break
            actions.append({"move": (self.get_pos(), (self.x, j))})
            if board[self.x, j] != None and board[self.x, j].get_color() != self.get_color():
                break

        for j in range(self.y - 1, -1, -1):
            if board[self.x, j] != None and board[self.x, j].get_color() == self.get_color():
                break
            actions.append({"move": (self.get_pos(), (self.x, j))})
            if board[self.x, j] != None and board[self.x, j].get_color() != self.get_color():
                break

        return actions


class Bishop(Peice):
    def __str__(self):
        return self.get_color() + "Bishop"

    def get_name(self):
        return "Bishop"

    def get_action(self, board):
        actions = []
        for (i, j) in zip(range(self.x + 1, 8), range(self.y + 1, 8)):
            if board[i, j] != None and board[i, j].get_color() == self.get_color():
                break
            actions.append({"move": (self.get_pos(), (i, j))})
            if board[i, j] != None and board[i, j].get_color() != self.get_color():
                break

        for (i, j) in zip(range(self.x + 1, 8), range(self.y - 1, -1, -1)):
            if board[i, j] != None and board[i, j].get_color() == self.get_color():
                break
            actions.append({"move": (self.get_pos(), (i, j))})
            if board[i, j] != None and board[i, j].get_color() != self.get_color():
                break

        for (i, j) in zip(range(self.x - 1, -1, -1), range(self.y + 1, 8)):
            if board[i, j] != None and board[i, j].get_color() == self.get_color():
                break
            actions.append({"move": (self.get_pos(), (i, j))})
            if board[i, j] != None and board[i, j].get_color() != self.get_color():
                break

        for (i, j) in zip(range(self.x - 1, -1, -1), range(self.y - 1, -1, -1)):
            if board[i, j] != None and board[i, j].get_color() == self.get_color():
                break
            actions.append({"move": (self.get_pos(), (i, j))})
            if board[i, j] != None and board[i, j].get_color() != self.get_color():
                break

        return actions


class Knight(Peice):
    def __str__(self):
        return self.get_color() + "Knight"

    def get_name(self):
        return "Knight"

    def get_action(self, board):
        actions = []

        actions.append({"move": (self.get_pos(), (self.x + 2, self.y + 1))})
        actions.append({"move": (self.get_pos(), (self.x + 2, self.y - 1))})

        actions.append({"move": (self.get_pos(), (self.x + 1, self.y + 2))})
        actions.append({"move": (self.get_pos(), (self.x + 1, self.y - 2))})

        actions.append({"move": (self.get_pos(), (self.x - 2, self.y + 1))})
        actions.append({"move": (self.get_pos(), (self.x - 2, self.y - 1))})

        actions.append({"move": (self.get_pos(), (self.x - 1, self.y + 2))})
        actions.append({"move": (self.get_pos(), (self.x - 1, self.y - 2))})

        return actions


class Pawn(Peice):
    def __str__(self):
        return self.get_color() + "Pawn"

    def get_name(self):
        return "Pawn"

    def get_action(self, board):
        actions = []
        if self.get_color() == "Black":
            if board[self.x + 1, self.y] == None:
                if self.x == 6:
                    actions.append(
                        {"promation": (self.get_pos(), (self.x + 1, self.y)), "name": "rook"})
                    actions.append(
                        {"promation": (self.get_pos(), (self.x + 1, self.y)), "name": "knight"})
                    actions.append(
                        {"promation": (self.get_pos(), (self.x + 1, self.y)), "name": "bishop"})
                    actions.append(
                        {"promation": (self.get_pos(), (self.x + 1, self.y)), "name": "queen"})
                else:
                    actions.append(
                        {"move": (self.get_pos(), (self.x + 1, self.y))})

            if self.moved == False and board[self.x + 2, self.y] == None:
                actions.append(
                    {"move": (self.get_pos(), (self.x + 2, self.y))})

            if self.y in range(7) and board[self.x + 1, self.y + 1] != None and board[self.x + 1, self.y + 1].get_color() == 'White':
                if self.x == 6:
                    actions.append(
                        {"promation": (self.get_pos(), (self.x + 1, self.y + 1)), "name": "rook"})
                    actions.append(
                        {"promation": (self.get_pos(), (self.x + 1, self.y + 1)), "name": "knight"})
                    actions.append(
                        {"promation": (self.get_pos(), (self.x + 1, self.y + 1)), "name": "bishop"})
                    actions.append(
                        {"promation": (self.get_pos(), (self.x + 1, self.y + 1)), "name": "queen"})
                else:
                    actions.append(
                        {"move": (self.get_pos(), (self.x + 1, self.y + 1))})

            if self.y in range(1, 8) and board[self.x + 1, self.y - 1] != None and board[self.x + 1, self.y - 1].get_color() == 'White':
                if self.x == 6:
                    actions.append(
                        {"promation": (self.get_pos(), (self.x + 1, self.y - 1)), "name": "rook"})
                    actions.append(
                        {"promation": (self.get_pos(), (self.x + 1, self.y - 1)), "name": "knight"})
                    actions.append(
                        {"promation": (self.get_pos(), (self.x + 1, self.y - 1)), "name": "bishop"})
                    actions.append(
                        {"promation": (self.get_pos(), (self.x + 1, self.y - 1)), "name": "queen"})
                else:
                    actions.append(
                        {"move": (self.get_pos(), (self.x + 1, self.y - 1))})

        else:
            if board[self.x - 1, self.y] == None:
                if self.x == 1:
                    actions.append(
                        {"promation": (self.get_pos(), (self.x - 1, self.y)), "name": "rook"})
                    actions.append(
                        {"promation": (self.get_pos(), (self.x - 1, self.y)), "name": "knight"})
                    actions.append(
                        {"promation": (self.get_pos(), (self.x - 1, self.y)), "name": "bishop"})
                    actions.append(
                        {"promation": (self.get_pos(), (self.x - 1, self.y)), "name": "queen"})
                else:
                    actions.append(
                        {"move": (self.get_pos(), (self.x - 1, self.y))})

            if self.moved == False and board[self.x - 2, self.y] == None:
                actions.append(
                    {"move": (self.get_pos(), (self.x - 2, self.y))})

            if self.y in range(7) and board[self.x - 1, self.y + 1] != None and board[self.x - 1, self.y + 1].get_color() == 'Black':
                if self.x == 1:
                    actions.append(
                        {"promation": (self.get_pos(), (self.x - 1, self.y + 1)), "name": "rook"})
                    actions.append(
                        {"promation": (self.get_pos(), (self.x - 1, self.y + 1)), "name": "knight"})
                    actions.append(
                        {"promation": (self.get_pos(), (self.x - 1, self.y + 1)), "name": "bishop"})
                    actions.append(
                        {"promation": (self.get_pos(), (self.x - 1, self.y + 1)), "name": "queen"})
                else:
                    actions.append(
                        {"move": (self.get_pos(), (self.x - 1, self.y + 1))})

            if self.y in range(1, 8) and board[self.x - 1, self.y - 1] != None and board[self.x - 1, self.y - 1].get_color() == 'Black':
                if self.x == 1:
                    actions.append(
                        {"promation": (self.get_pos(), (self.x - 1, self.y - 1)), "name": "rook"})
                    actions.append(
                        {"promation": (self.get_pos(), (self.x - 1, self.y - 1)), "name": "knight"})
                    actions.append(
                        {"promation": (self.get_pos(), (self.x - 1, self.y - 1)), "name": "bishop"})
                    actions.append(
                        {"promation": (self.get_pos(), (self.x - 1, self.y - 1)), "name": "queen"})
                else:
                    actions.append(
                        {"move": (self.get_pos(), (self.x - 1, self.y - 1))})

        return actions


class Queen(Peice):
    def __str__(self):
        return self.get_color() + "Queen"

    def get_name(self):
        return "Queen"

    def get_action(self, board):
        actions = []
        for i in range(self.x + 1, 8):
            if board[i, self.y] != None and board[i, self.y].get_color() == self.get_color():
                break
            actions.append({"move": (self.get_pos(), (i, self.y))})
            if board[i, self.y] != None and board[i, self.y].get_color() != self.get_color():
                break

        for i in range(self.x - 1, -1, -1):
            if board[i, self.y] != None and board[i, self.y].get_color() == self.get_color():
                break
            actions.append({"move": (self.get_pos(), (i, self.y))})
            if board[i, self.y] != None and board[i, self.y].get_color() != self.get_color():
                break

        for j in range(self.y + 1, 8):
            if board[self.x, j] != None and board[self.x, j].get_color() == self.get_color():
                break
            actions.append({"move": (self.get_pos(), (self.x, j))})
            if board[self.x, j] != None and board[self.x, j].get_color() != self.get_color():
                break

        for j in range(self.y - 1, -1, -1):
            if board[self.x, j] != None and board[self.x, j].get_color() == self.get_color():
                break
            actions.append({"move": (self.get_pos(), (self.x, j))})
            if board[self.x, j] != None and board[self.x, j].get_color() != self.get_color():
                break

        for (i, j) in zip(range(self.x + 1, 8), range(self.y + 1, 8)):
            if board[i, j] != None and board[i, j].get_color() == self.get_color():
                break
            actions.append({"move": (self.get_pos(), (i, j))})
            if board[i, j] != None and board[i, j].get_color() != self.get_color():
                break

        for (i, j) in zip(range(self.x + 1, 8), range(self.y - 1, -1, -1)):
            if board[i, j] != None and board[i, j].get_color() == self.get_color():
                break
            actions.append({"move": (self.get_pos(), (i, j))})
            if board[i, j] != None and board[i, j].get_color() != self.get_color():
                break

        for (i, j) in zip(range(self.x - 1, -1, -1), range(self.y + 1, 8)):
            if board[i, j] != None and board[i, j].get_color() == self.get_color():
                break
            actions.append({"move": (self.get_pos(), (i, j))})
            if board[i, j] != None and board[i, j].get_color() != self.get_color():
                break

        for (i, j) in zip(range(self.x - 1, -1, -1), range(self.y - 1, -1, -1)):
            if board[i, j] != None and board[i, j].get_color() == self.get_color():
                break
            actions.append({"move": (self.get_pos(), (i, j))})
            if board[i, j] != None and board[i, j].get_color() != self.get_color():
                break

        return actions


class King(Peice):
    def __str__(self):
        return self.get_color() + "King"

    def get_name(self):
        return "King"

    def get_action(self, board):
        actions = []
        for i in range(self.x - 1, self.x + 2):
            for j in range(self.y - 1, self.y + 2):
                if i in range(8) and j in range(8) and (board[i, j] == None or board[i, j].get_color() != self.get_color()):
                    actions.append({"move": (self.get_pos(), (i, j))})

        if self.moved == False:
            x, y = self.get_pos()
            if board[x, y + 1] == board[x, y + 2] == None:
                if board[x, y + 3] != None and board[x, y + 3].moved == False:
                    actions.append(
                        {"castle": (self.get_pos(), (x, y + 2), (x, y + 3), (x, y + 1))})

            if board[x, y - 1] == board[x, y - 2] == None:
                if board[x, y - 4] != None and board[x, y - 4].moved == False:
                    actions.append(
                        {"castle": (self.get_pos(), (x, y - 2), (x, y - 4), (x, y - 1))})

        return actions
