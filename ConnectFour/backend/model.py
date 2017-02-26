import numpy as np


EMPTY = NOONE = ' '
PLAYER_X = 'x'
PLAYER_O = 'o'
DRAW = '='

class State:
    def __init__(self, player=PLAYER_X):
        self.player = player
        self.winner = NOONE
        self.pick_loc = None
        self.cursor = 3
        self.matrix = np.array([[' ',' ',' ',' ',' ',' ',' '],
                                [' ',' ',' ',' ',' ',' ',' '],
                                [' ',' ',' ',' ',' ',' ',' '],
                                [' ',' ',' ',' ',' ',' ',' '],
                                [' ',' ',' ',' ',' ',' ',' '],
                                [' ',' ',' ',' ',' ',' ',' ']])

def move_cursor(pos, vec):
    new_pos = pos + vec
    if new_pos >= 0 and new_pos < 7:
        return new_pos
    return pos

def opponent(player):
    if player == PLAYER_X:
        return PLAYER_O
    else:
        return PLAYER_X

def place(matrix, player, cursor):
    for r in reversed(range(6)):
        if matrix[r,cursor] == EMPTY:
            matrix[r,cursor] = player
            player = opponent(player)
            break
    return matrix, player

def __check_for_four(line):
    if 4 * PLAYER_X in line:
        return PLAYER_X
    elif 4 * PLAYER_O in line:
        return PLAYER_O
    else:
        return NOONE

def check_winner(matrix):
    winner = NOONE
    for row in range(matrix.shape[0]):
        winner = __check_for_four(''.join(matrix[row,:]))
        if winner != NOONE:
            return winner
    for col in range(matrix.shape[1]):
        winner = __check_for_four(''.join(matrix[:,col]))
        if winner != NOONE:
            return winner
    for diag in range(-matrix.shape[0]+4, matrix.shape[1]-3):
        winner = __check_for_four(''.join(matrix.diagonal(diag)))
        if winner != NOONE:
            return winner
    for diag in range(-matrix.shape[0]+4, matrix.shape[1]-3):
        winner = __check_for_four(''.join(np.fliplr(matrix).diagonal(diag)))
        if winner != NOONE:
            return winner
    num_marks = 0
    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            mark = matrix[row][col]
            if mark == PLAYER_X or mark == PLAYER_O:
                num_marks += 1
    if num_marks == matrix.size:
        return DRAW
    return NOONE
