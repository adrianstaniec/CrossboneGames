import random
import numpy as np
from backend import model

def first_from_left(matrix, player):
    for y in range(3):
        for x in range(3):
            if matrix[x][y] == model.EMPTY:
                matrix[x][y] = player
                return (matrix, model.opponent(player))

def random_pick(matrix, player):
    while True:
        guess = random.randrange(9)
        x = guess // 3
        y = guess % 3
        if matrix[x][y] == model.EMPTY:
            matrix[x][y] = player
            return (matrix, model.opponent(player))

def __win(line, player):
    done = False
    line = list(line)
    num_player_spots = line.count(player)
    num_free_spots = line.count(model.EMPTY)
    if  num_player_spots == 2 and num_free_spots == 1:
        line = 3 * [player]
        done = True
    return done, line

def __defend(line, player):
    done = False
    line = list(line)
    num_opponent_spots = line.count(model.opponent(player))
    num_free_spots = line.count(model.EMPTY)
    if  num_opponent_spots == 2 and num_free_spots == 1:
        line = [player if spot == model.EMPTY else spot
                for spot in line]
        done = True
    return done, line

def __add_third_in_line(matrix, player, win_or_defend):
    """Look for 2 in line and try to win or defend in 1 move"""
    done = False
    opponent = model.opponent(player)
    # = horizontals
    for row in range(3):
        if not done:
            done, line = win_or_defend(matrix[row,:], player)
            if done:
                matrix[row,:] = line
                # || verticals
    for col in range(3):
        if not done:
            done, line = win_or_defend(matrix[:,col], player)
            if done:
                matrix[:,col] = line
    if not done:
        # \ diagonal
        done, line = win_or_defend(matrix.diagonal(), player)
        if done:
            matrix[np.diag_indices(3)] = line
    if not done:
        # / diagonal
        done, line = win_or_defend(np.fliplr(matrix).diagonal(), player)
        if done:
            np.fliplr(matrix)[np.diag_indices(3)] = line
    if not done:
        return matrix, player
    else:
        return matrix, opponent

win_in_1 = lambda matrix, player : __add_third_in_line(matrix, player, __win)

defend_in_1 = lambda matrix, player : __add_third_in_line(matrix, player, __defend)

def take_center(matrix, player):
    if matrix[1,1] == model.EMPTY:
        matrix[1,1] = player
        return matrix, model.opponent(player)
    return matrix, player

def take_corner(matrix, player):
    opponent = model.opponent(player)
    for row in random.sample([0, 2], 2):
        for col in random.sample([0, 2], 2):
            if matrix[row,col] == model.EMPTY:
                if matrix[row,1] == opponent or matrix[1,col] == opponent:
                    matrix[row,col] = player
                    return matrix, opponent
    return matrix, player

def take_side(matrix, player):
    opponent = model.opponent(player)
    for row, col in random.sample([(0, 1), (2, 1), (1, 0), (1, 2)], 4):
        if matrix[row,col] == model.EMPTY:
            if col == 1:
                if matrix[row,0] == opponent or matrix[row,2] == opponent:
                    matrix[row,col] = player
                    return matrix, opponent
            else:
                if matrix[0,col] == opponent or matrix[2,col] == opponent:
                    matrix[row,col] = player
                    return matrix, opponent
    return matrix, player

class AI:
    steps = []

    def __init__(self, player, steps=[first_from_left]):
        self.player = player
        self.steps = steps

    def mark_spot(self, matrix):
        matrix = np.array(matrix)
        for f in self.steps:
            new_matrix, new_player = f(matrix, self.player)
            if new_player != self.player:
                return new_matrix, new_player


__algorithms = {0 : [first_from_left],
                1 : [random_pick],
                2 : [win_in_1, random_pick],
                3 : [win_in_1, defend_in_1, random_pick],
                4 : [win_in_1, defend_in_1, take_center, random_pick],
                5 : [win_in_1, defend_in_1, take_center, take_side, random_pick],
                6 : [win_in_1, defend_in_1, take_center, take_corner, take_side, random_pick]}

def Factory(player, level):
    return AI(player, __algorithms[level])

NUM = len(__algorithms)
