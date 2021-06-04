from chess import *


def get_moves(board, turn):
    data = []
    for i in range(8):
        for j in range(8):
            if board[i][j] != None:
                for x, y in board[i][j].get_moves(board):
                    # Normal Move
                    data.append({'move': [(i, j), (x, y)],
                                 'color': board[i][j].get_color()})

                if board[i][j].get_name() == 'King':
                    # King Castle
                    castle = board[i][j].get_castle(board)
                    if castle != None:
                        for kx2, ky2, rx1, ry1, rx2, ry2 in castle:
                            data.append(
                                {'castle': [(i, j), (kx2, ky2), (rx1, ry1), (rx2, ry2)], 'color': board[i][j].get_color()})
                    if board[i][j].get_color() == turn:
                        king = (i, j)

                if board[i][j].get_name() == 'Pawn':
                    # Pawn Promation
                    for x, y in board[i][j].get_promation(board):
                        data.append(
                            {'promation': [(i, j), (x, y)], 'color': board[i][j].get_color()})
                        data.remove(
                            {'move': [(i, j), (x, y)], 'color': board[i][j].get_color()})

    return (data, king)


def escape(s):
    """
    Escape special characters.

    https://github.com/jacebrowning/memegen#special-characters
    """
    for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                     ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
        s = s.replace(old, new)
    return s


def make_move(board, response):
    move_type = list(response.keys())[0]
    if move_type == 'move':
        # Unpack data
        x1 = int(response['move'][0][0])
        y1 = int(response['move'][0][1])
        x2 = int(response['move'][1][0])
        y2 = int(response['move'][1][1])

        if board[x1][y1] != None and (x2, y2) in board[x1][y1].get_moves(board):
            # Assign old cell to selected cell
            board[x2][y2] = board[x1][y1]
            board[x2][y2].change_pos(x2, y2)

            # Remove Old Object Completely from memory
            buffer = board[x1][y1]
            board[x1][y1] = None
            del buffer

            return [{'color': board[x2][y2].get_color(), 'move': [(x1, y1), (x2, y2)]}]
    elif move_type == 'promation':
        # Unpack data
        if response['name'] in ['rook', 'knight', 'queen', 'bishop']:
            print(response['name'])
            x1 = int(response['promation'][0][0])
            y1 = int(response['promation'][0][1])
            x2 = int(response['promation'][1][0])
            y2 = int(response['promation'][1][1])

            if board[x1][y1] != None and (x2, y2) in board[x1][y1].get_promation(board):
                if response['name'] == 'queen':
                    temp = Queen(
                        x2, y2, board[x1][y1].get_color())

                elif response['name'] == 'bishop':
                    temp = Bishop(
                        x2, y2, board[x1][y1].get_color())

                elif response['name'] == 'knight':
                    temp = Knight(
                        x2, y2, board[x1][y1].get_color())

                elif response['name'] == 'rook':
                    temp = Rook(
                        x2, y2, board[x1][y1].get_color())

                board[x2][y2] = temp
                buffer = board[x1][y1]
                board[x1][y1] = None
                del buffer

                return [{'color': board[x2][y2].get_color(), 'move': [(x1, y1), (x2, y2)]},
                        {'color': board[x2][y2].get_color(), 'promation': [x2, y2, response['name']]}]

    elif move_type == 'castle':
        # Unpack data
        x1 = int(response['castle'][0][0])
        y1 = int(response['castle'][0][1])
        x2 = int(response['castle'][1][0])
        y2 = int(response['castle'][1][1])

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

                    return [{'color': board[x2][y2].get_color(), 'move': [(x1, y1), (kx2, ky2)]},
                            {'color': board[x2][y2].get_color(), 'move': [(rx1, ry1), (rx2, ry2)]}]


def is_checked(data, king, turn):
    for row in data:
        if row['color'] != turn and (('move' in row and row['move'][1] == king) or
                                     ('castle' in row and row['castle'][3] == king) or
                                     ('promation' in row and row['promation'][1] == king)):
            return king

    return None


def check_end(board, turn):
    white_result = []
    black_result = []
    for i in range(8):
        for j in range(8):
            if board[i][j] != None and len(board[i][j].get_moves(board)):
                if board[i][j].get_color() == 'White':
                    white_result.append(board[i][j].get_name())
                else:
                    black_result.append(board[i][j].get_name())

    if len(black_result) == 0 and turn == 'Black':
        return 'White'
    elif len(white_result) == 0 and turn == 'White':
        return 'Black'
    elif len(black_result) == 1 and len(white_result) == 1 and \
            black_result[0] == 'King' and white_result[0] == 'King':
        return 'Tie'

    return None
