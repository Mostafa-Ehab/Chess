import copy


class Peice:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.moved = False

    def get_pos(self):
        return self.pos

    def get_color(self):
        return self.color

    def get_pos(self):
        return (self.x, self.y)

    def change_pos(self, x, y):
        self.x = x
        self.y = y
        self.moved = True


class Rook(Peice):
    def __str__(self):
        return self.get_color() + "Rook"

    def get_name(self):
        return "Rook"

    def get_moves(self, board, king_state=True):
        temps = []
        for i in range(self.x + 1, 8):
            valid = check_validity(self.x, self.y, i, self.y, board)
            if valid == False:
                break
            elif valid == 'Last':
                temps.append((i, self.y))
                break

            temps.append((i, self.y))

        for i in range(self.x - 1, -1, -1):
            valid = check_validity(self.x, self.y, i, self.y, board)
            if valid == False:
                break
            elif valid == 'Last':
                temps.append((i, self.y))
                break

            temps.append((i, self.y))

        for j in range(self.y + 1, 8):
            valid = check_validity(self.x, self.y, self.x, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                temps.append((self.x, j))
                break
            temps.append((self.x, j))

        for j in range(self.y - 1, -1, -1):
            valid = check_validity(self.x, self.y, self.x, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                temps.append((self.x, j))
                break
            temps.append((self.x, j))

        moves = []
        if king_state:
            for x2, y2 in temps:
                if check_king_state(self.x, self.y, x2, y2, board):
                    moves.append((x2, y2))
            return moves
        else:
            return temps


class Bishop(Peice):
    def __str__(self):
        return self.get_color() + "Bishop"

    def get_name(self):
        return "Bishop"

    def get_moves(self, board, king_state=True):
        temps = []
        for (i, j) in zip(range(self.x + 1, 8), range(self.y + 1, 8)):
            valid = check_validity(self.x, self.y, i, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                temps.append((i, j))
                break
            temps.append((i, j))

        for (i, j) in zip(range(self.x + 1, 8), range(self.y - 1, -1, -1)):
            valid = check_validity(self.x, self.y, i, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                temps.append((i, j))
                break
            temps.append((i, j))

        for (i, j) in zip(range(self.x - 1, -1, -1), range(self.y + 1, 8)):
            valid = check_validity(self.x, self.y, i, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                temps.append((i, j))
                break
            temps.append((i, j))

        for (i, j) in zip(range(self.x - 1, -1, -1), range(self.y - 1, -1, -1)):
            valid = check_validity(self.x, self.y, i, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                temps.append((i, j))
                break
            temps.append((i, j))

        moves = []
        if king_state:
            for x2, y2 in temps:
                if check_king_state(self.x, self.y, x2, y2, board):
                    moves.append((x2, y2))
            return moves
        else:
            return temps


class Knight(Peice):
    def __str__(self):
        return self.get_color() + "Knight"

    def get_name(self):
        return "Knight"

    def get_moves(self, board, king_state=True):
        temps = []
        temps.append((self.x + 2, self.y + 1))
        temps.append((self.x + 2, self.y - 1))

        temps.append((self.x - 2, self.y + 1))
        temps.append((self.x - 2, self.y - 1))

        temps.append((self.x + 1, self.y + 2))
        temps.append((self.x + 1, self.y - 2))

        temps.append((self.x - 1, self.y + 2))
        temps.append((self.x - 1, self.y - 2))

        moves = []
        for temp in temps:
            if check_validity(self.x, self.y, temp[0], temp[1], board):
                moves.append(temp)

        temps = moves.copy()

        moves = []
        if king_state:
            for x2, y2 in temps:
                if check_king_state(self.x, self.y, x2, y2, board):
                    moves.append((x2, y2))
            return moves
        else:
            return temps


class Pawn(Peice):
    def __str__(self):
        return self.get_color() + "Pawn"

    def get_name(self):
        return "Pawn"

    def get_moves(self, board, king_state=True):
        temps = []
        if self.get_color() == "Black":
            if check_validity(self.x, self.y, self.x + 1, self.y, board) == True:
                temps.append((self.x + 1, self.y))

                if check_validity(self.x, self.y, self.x + 2, self.y, board) == True and self.moved == False:
                    temps.append((self.x + 2, self.y))

            if check_validity(self.x, self.y, self.x + 1, self.y + 1, board) == 'Last':
                temps.append((self.x + 1, self.y + 1))

            if check_validity(self.x, self.y, self.x + 1, self.y - 1, board) == 'Last':
                temps.append((self.x + 1, self.y - 1))

        else:
            if check_validity(self.x, self.y, self.x - 1, self.y, board) == True:
                temps.append((self.x - 1, self.y))

                if check_validity(self.x, self.y, self.x - 2, self.y, board) == True and self.moved == False:
                    temps.append((self.x - 2, self.y))

            if check_validity(self.x, self.y, self.x - 1, self.y + 1, board) == 'Last':
                temps.append((self.x - 1, self.y + 1))

            if check_validity(self.x, self.y, self.x - 1, self.y - 1, board) == 'Last':
                temps.append((self.x - 1, self.y - 1))

        moves = []
        if king_state:
            for x2, y2 in temps:
                if check_king_state(self.x, self.y, x2, y2, board):
                    moves.append((x2, y2))

            return moves
        else:
            return temps

    def get_promation(self, board):
        moves = []
        temps = self.get_moves(board)
        for x, y in temps:
            if x in [0, 7] and self.moved == True:
                moves.append((x, y))

        return moves


class Queen(Peice):
    def __str__(self):
        return self.get_color() + "Queen"

    def get_name(self):
        return "Queen"

    def get_moves(self, board, king_state=True):
        temps = []
        for i in range(self.x + 1, 8):
            valid = check_validity(self.x, self.y, i, self.y, board)
            if valid == False:
                break
            elif valid == 'Last':
                temps.append((i, self.y))
                break

            temps.append((i, self.y))

        for i in range(self.x - 1, -1, -1):
            valid = check_validity(self.x, self.y, i, self.y, board)
            if valid == False:
                break
            elif valid == 'Last':
                temps.append((i, self.y))
                break

            temps.append((i, self.y))

        for j in range(self.y + 1, 8):
            valid = check_validity(self.x, self.y, self.x, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                temps.append((self.x, j))
                break
            temps.append((self.x, j))

        for j in range(self.y - 1, -1, -1):
            valid = check_validity(self.x, self.y, self.x, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                temps.append((self.x, j))
                break
            temps.append((self.x, j))

        for (i, j) in zip(range(self.x + 1, 8), range(self.y + 1, 8)):
            valid = check_validity(self.x, self.y, i, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                temps.append((i, j))
                break
            temps.append((i, j))

        for (i, j) in zip(range(self.x + 1, 8), range(self.y - 1, -1, -1)):
            valid = check_validity(self.x, self.y, i, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                temps.append((i, j))
                break
            temps.append((i, j))

        for (i, j) in zip(range(self.x - 1, -1, -1), range(self.y + 1, 8)):
            valid = check_validity(self.x, self.y, i, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                temps.append((i, j))
                break
            temps.append((i, j))

        for (i, j) in zip(range(self.x - 1, -1, -1), range(self.y - 1, -1, -1)):
            valid = check_validity(self.x, self.y, i, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                temps.append((i, j))
                break
            temps.append((i, j))

        moves = []
        if king_state:
            for x2, y2 in temps:
                if check_king_state(self.x, self.y, x2, y2, board):
                    moves.append((x2, y2))
            return moves
        else:
            return temps


class King(Peice):
    def __str__(self):
        return self.get_color() + "King"

    def get_name(self):
        return "King"

    def get_moves(self, board, king_state=True):
        temps = []
        for i in range(self.x - 1, self.x + 2):
            for j in range(self.y - 1, self.y + 2):
                if check_validity(self.x, self.y, i, j, board):
                    temps.append((i, j))

        moves = []
        if king_state:
            for x2, y2 in temps:
                if check_king_state(self.x, self.y, x2, y2, board):
                    moves.append((x2, y2))

            return moves
        else:
            return temps

    def get_castle(self, board):
        castle = []
        if self.moved == False:
            if board[self.x][self.y + 3] != None and board[self.x][self.y + 3].moved == False \
                    and board[self.x][self.y + 1] == None and board[self.x][self.y + 2] == None:
                # Color of the King
                color = board[self.x][self.y].get_color()

                check = False
                # Check if the cell is Checked by the emeny
                for i in range(8):
                    for j in range(8):
                        if board[i][j] != None and board[i][j].get_color() != color:
                            for xk, yk in board[i][j].get_moves(board, king_state=False):
                                if xk == self.x and yk in [self.y + 1, self.y + 2]:
                                    check = True
                if not check:
                    castle.append((self.x, self.y + 2, self.x,
                                   self.y + 3, self.x, self.y + 1))

            if board[self.x][self.y - 4] != None and board[self.x][self.y - 4].moved == False \
                    and board[self.x][self.y - 1] == None and board[self.x][self.y - 2] == None and board[self.x][self.y - 3] == None:
                # Color of the King
                color = board[self.x][self.y].get_color()

                check = False
               # Check if the cells is Checked by the enemy
                for i in range(8):
                    for j in range(8):
                        if board[i][j] != None and board[i][j].get_color() != color:
                            for xk, yk in board[i][j].get_moves(board, king_state=False):
                                if xk == self.x and yk in [self.y - 1, self.y - 2]:
                                    check = True
                if not check:
                    castle.append((self.x, self.y - 2, self.x,
                                   self.y - 4, self.x, self.y - 1))

        return castle if castle != [] else None


def check_validity(x1, y1, x2, y2, board):
    if x1 == x2 and y1 == y2:
        return False

    elif (x2 not in range(8)) or (y2 not in range(8)):
        return False

    elif board[x2][y2] == None:
        return True

    elif (board[x1][y1].get_color() != board[x2][y2].get_color()):
        return 'Last'

    return False


def check_king_state(x1, y1, x2, y2, board):
    temp = copy.deepcopy(board)
    color = board[x1][y1].get_color()

    # Assign old cell to selected cell
    temp[x2][y2] = temp[x1][y1]
    temp[x2][y2].change_pos(x2, y2)

    # Remove Old Object Completely from memory
    buffer = temp[x1][y1]
    temp[x1][y1] = None
    del buffer

    for i in range(8):
        for j in range(8):
            if temp[i][j] != None and temp[i][j].get_color() != color:
                for xk, yk in temp[i][j].get_moves(temp, king_state=False):
                    if temp[xk][yk] != None and temp[xk][yk].get_name() == "King" and temp[xk][yk].get_color() == color:
                        return False

    return True