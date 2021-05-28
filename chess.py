class Peice:
    def __init__(self, x, y, color):
        self.pos = (x, y)
        self.color = color

    def get_pos(self):
        return self.pos

    def get_color(self):
        return self.color


class Rook(Peice):
    def get_moves(self, board=None):
        moves = []
        for i in range(self.x + 1, 9):
            moves.append((i, self.y))

        for i in range(self.x, -1, -1):
            moves.append((i, self.y))

        for j in range(self.y + 1, 9):
            moves.append((self.x, j))

        for j in range(self.y + 1, -1, -1):
            moves.append((self.x, j))


class Bishop(Peice):
    def get_moves(self, board=None):
        moves = []
        for (i, j) in zip(range(self.x + 1, 9), range(self.y + 1, 9)):
            moves.append((i, j))

        for (i, j) in zip(range(self.x + 1, 9), range(self.y - 1, -1, -1)):
            moves.append((i, j))

        for (i, j) in zip(range(self.x - 1, -1, -1), range(self.y + 1, 9)):
            moves.append((i, j))

        for (i, j) in zip(range(self.x - 1, -1, -1), range(self.y - 1, -1, -1)):
            moves.append((i, j))


class Knight(Peice):
    def get_moves(self, board=None):
        moves = []
        moves.append((self.x + 2, self.y + 1))
        moves.append((self.x + 2, self.y - 1))

        moves.append((self.x - 2, self.y + 1))
        moves.append((self.x - 2, self.y - 1))

        moves.append((self.x + 1, self.y + 2))
        moves.append((self.x + 1, self.y - 2))

        moves.append((self.x - 1, self.y + 2))
        moves.append((self.x - 1, self.y - 2))


class Pawn(Peice):
    def get_moves(self, board=None):
        moves = []
        moves.append((self.x + 1, self.y))
        moves.append((self.x + 1, self.y))

        moves.append((self.x + 1, self.y - 1))
        moves.append((self.x + 1, self.y - 1))


class Queen(Peice):
    def get_moves(self, board=None):
        moves = []
        for i in range(self.x + 1, 9):
            moves.append((i, self.y))

        for i in range(self.x, -1, -1):
            moves.append((i, self.y))

        for j in range(self.y + 1, 9):
            moves.append((self.x, j))

        for j in range(self.y + 1, -1, -1):
            moves.append((self.x, j))

        for (i, j) in zip(range(self.x + 1, 9), range(self.y + 1, 9)):
            moves.append((i, j))

        for (i, j) in zip(range(self.x + 1, 9), range(self.y - 1, -1, -1)):
            moves.append((i, j))

        for (i, j) in zip(range(self.x - 1, -1, -1), range(self.y + 1, 9)):
            moves.append((i, j))

        for (i, j) in zip(range(self.x - 1, -1, -1), range(self.y - 1, -1, -1)):
            moves.append((i, j))


class King(Peice):
    def get_moves(self, board):
        moves = []
        for i in range(self.x - 1, self.x + 1):
            for j in range(self.y - 1, self.y + 1):
                if not (i == self.x and j == self.y):
                    moves.append((i, j))
