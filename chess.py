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

    def change_pos(self, x, y):
        self.x = x
        self.y = y
        self.moved = True


class Rook(Peice):
    def __str__(self):
        return self.get_color() + "Rook"

    def get_moves(self, board):
        moves = []
        for i in range(self.x + 1, 8):
            valid = check_validity(self.x, self.y, i, self.y, board)
            if valid == False:
                break
            elif valid == 'Last':
                moves.append((i, self.y))
                break

            moves.append((i, self.y))

        for i in range(self.x - 1, -1, -1):
            valid = check_validity(self.x, self.y, i, self.y, board)
            if valid == False:
                break
            elif valid == 'Last':
                moves.append((i, self.y))
                break

            moves.append((i, self.y))

        for j in range(self.y + 1, 8):
            valid = check_validity(self.x, self.y, self.x, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                moves.append((self.x, j))
                break
            moves.append((self.x, j))

        for j in range(self.y - 1, -1, -1):
            valid = check_validity(self.x, self.y, self.x, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                moves.append((self.x, j))
                break
            moves.append((self.x, j))

        return moves


class Bishop(Peice):
    def __str__(self):
        return self.get_color() + "Bishop"

    def get_moves(self, board):
        moves = []
        for (i, j) in zip(range(self.x + 1, 8), range(self.y + 1, 8)):
            valid = check_validity(self.x, self.y, i, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                moves.append((i, j))
                break
            moves.append((i, j))

        for (i, j) in zip(range(self.x + 1, 8), range(self.y - 1, -1, -1)):
            valid = check_validity(self.x, self.y, i, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                moves.append((i, j))
                break
            moves.append((i, j))

        for (i, j) in zip(range(self.x - 1, -1, -1), range(self.y + 1, 8)):
            valid = check_validity(self.x, self.y, i, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                moves.append((i, j))
                break
            moves.append((i, j))

        for (i, j) in zip(range(self.x - 1, -1, -1), range(self.y - 1, -1, -1)):
            valid = check_validity(self.x, self.y, i, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                moves.append((i, j))
                break
            moves.append((i, j))

        return moves


class Knight(Peice):
    def __str__(self):
        return self.get_color() + "Knight"

    def get_moves(self, board):
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

        return moves


class Pawn(Peice):
    def __str__(self):
        return self.get_color() + "Pawn"

    def get_moves(self, board):
        temps = []
        if self.get_color() == "Black":
            temps.append((self.x + 1, self.y))

            temps.append((self.x + 2, self.y))

            temps.append((self.x + 1, self.y + 1))

            temps.append((self.x + 1, self.y - 1))

        else:
            temps.append((self.x - 1, self.y))

            temps.append((self.x - 2, self.y))

            temps.append((self.x - 1, self.y + 1))

            temps.append((self.x - 1, self.y - 1))

        moves = []
        for temp in temps:
            if check_validity(self.x, self.y, temp[0], temp[1], board):
                moves.append(temp) if self.check(
                    temp[0], temp[1], board) else ""

        return moves

    def check(self, x2, y2, board):
        pass


class Queen(Peice):
    def __str__(self):
        return self.get_color() + "Queen"

    def get_moves(self, board):
        moves = []
        for i in range(self.x + 1, 8):
            valid = check_validity(self.x, self.y, i, self.y, board)
            if valid == False:
                break
            elif valid == 'Last':
                moves.append((i, self.y))
                break

            moves.append((i, self.y))

        for i in range(self.x - 1, -1, -1):
            valid = check_validity(self.x, self.y, i, self.y, board)
            if valid == False:
                break
            elif valid == 'Last':
                moves.append((i, self.y))
                break

            moves.append((i, self.y))

        for j in range(self.y + 1, 8):
            valid = check_validity(self.x, self.y, self.x, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                moves.append((self.x, j))
                break
            moves.append((self.x, j))

        for j in range(self.y - 1, -1, -1):
            valid = check_validity(self.x, self.y, self.x, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                moves.append((self.x, j))
                break
            moves.append((self.x, j))

        for (i, j) in zip(range(self.x + 1, 8), range(self.y + 1, 8)):
            valid = check_validity(self.x, self.y, i, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                moves.append((i, j))
                break
            moves.append((i, j))

        for (i, j) in zip(range(self.x + 1, 8), range(self.y - 1, -1, -1)):
            valid = check_validity(self.x, self.y, i, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                moves.append((i, j))
                break
            moves.append((i, j))

        for (i, j) in zip(range(self.x - 1, -1, -1), range(self.y + 1, 8)):
            valid = check_validity(self.x, self.y, i, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                moves.append((i, j))
                break
            moves.append((i, j))

        for (i, j) in zip(range(self.x - 1, -1, -1), range(self.y - 1, -1, -1)):
            valid = check_validity(self.x, self.y, i, j, board)
            if valid == False:
                break
            elif valid == 'Last':
                moves.append((i, j))
                break
            moves.append((i, j))

        return moves


class King(Peice):
    def __str__(self):
        return self.get_color() + "King"

    def get_moves(self, board):
        moves = []
        for i in range(self.x - 1, self.x + 2):
            for j in range(self.y - 1, self.y + 2):
                if check_validity(self.x, self.y, i, j, board):
                    moves.append((i, j))

        return moves


def check_validity(x1, y1, x2, y2, board):
    print(board[x1][y1])
    print((x2, y2))
    print()
    if x1 == x2 and y1 == y2:
        return False

    elif (x2 not in range(8)) or (y2 not in range(8)):
        return False

    elif board[x2][y2] == None:
        return True

    elif (board[x1][y1].get_color() != board[x2][y2].get_color()):
        return 'Last'

    else:
        return False
