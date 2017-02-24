from random import randrange
import numpy as np
from backend import model

NUM = 7

def first_empty_slot(matrix, player):
    for y in range(3):
        for x in range(3):
            if matrix[x][y] == model.EMPTY:
                matrix[x][y] = player
                return (matrix, model.opponent(player))

def random_spot(matrix, player):
    while True:
        guess = randrange(9)
        x = guess // 3
        y = guess % 3
        if matrix[x][y] == model.EMPTY:
            matrix[x][y] = player
            return (matrix, model.opponent(player))

def complete(line, player):
    done = False
    line = list(line)
    num_player_spots = line.count(player)
    num_free_spots = line.count(model.EMPTY)
    if  num_player_spots == 2 and num_free_spots == 1:
        line = 3 * [player]
        done = True
    return done, line

def block(line, player):
    done = False
    line = list(line)
    num_opponent_spots = line.count(model.opponent(player))
    num_free_spots = line.count(model.EMPTY)
    if  num_opponent_spots == 2 and num_free_spots == 1:
        line = [player if spot == model.EMPTY else spot
                for spot in line]
        done = True
    return done, line

def win_in_1(matrix, player):
    opponent = model.opponent(player)
    """Seize opportinity to win in 1 move, otherwise random"""
    done = False
    opponent = model.opponent(player)
    # = horizontals
    for row in range(3):
        if not done:
            done, line = complete(matrix[row,:], player)
            if done:
                matrix[row,:] = line
                # || verticals
    for col in range(3):
        if not done:
            done, line = complete(matrix[:,col], player)
            if done:
                matrix[:,col] = line
    if not done:
        # \ diagonal
        done, line = complete(matrix.diagonal(), player)
        if done:
            matrix[np.diag_indices(3)] = line
    if not done:
        # / diagonal
        done, line = complete(np.fliplr(matrix).diagonal(), player)
        if done:
            np.fliplr(matrix)[np.diag_indices(3)] = line

    if not done:
        return matrix, player
    else:
        return matrix, opponent

# TODO: refactor: combine with win_in_1()
def defend_in_1(matrix, player):
    """Block if opponent has an opportinity to win in 1 move"""
    done = False
    opponent = model.opponent(player)
    # = horizontals
    for row in range(3):
        if not done:
            done, line = block(matrix[row,:], player)
            if done:
                matrix[row,:] = line
                # || verticals
    for col in range(3):
        if not done:
            done, line = block(matrix[:,col], player)
            if done:
                matrix[:,col] = line
    if not done:
        # \ diagonal
        done, line = block(matrix.diagonal(), player)
        if done:
            matrix[np.diag_indices(3)] = line
    if not done:
        # / diagonal
        done, line = block(np.fliplr(matrix).diagonal(), player)
        if done:
            np.fliplr(matrix)[np.diag_indices(3)] = line
    if not done:
        return matrix, player
    else:
        return matrix, opponent

def take_center(matrix, player):
    if matrix[1,1] == model.EMPTY:
        matrix[1,1] = player
        return matrix, model.opponent(player)
    return matrix, player

def take_corner(matrix, player):
    opponent = model.opponent(player)
    for row in [0,2]:
        for col in [0,2]:
            if matrix[row,col] == model.EMPTY:
                if matrix[row,1] == opponent or matrix[1,col] == opponent:
                    matrix[row,col] = player
                    return matrix, opponent
    return matrix, player

def take_side(matrix, player):
    opponent = model.opponent(player)
    for row, col in [(0, 1), (2, 1)]:
        if matrix[row,col] == model.EMPTY:
            if matrix[row,0] == opponent or matrix[row,2] == opponent:
                matrix[row,col] = player
                return matrix, opponent
    for row, col in [(1, 0), (1, 2)]:
        if matrix[row,col] == model.EMPTY:
            if matrix[0,col] == opponent or matrix[2,col] == opponent:
                matrix[row,col] = player
                return matrix, opponent
    return matrix, player


class AI0:
    def mark_spot(self, matrix, player):
        return first_empty_slot(matrix, player)

class AI1:
    def mark_spot(self, matrix, player):
        return random_spot(matrix, player)

class AI2:
    def mark_spot(self, matrix, player):
        matrix = np.array(matrix)
        new_matrix, new_player = win_in_1(matrix, player)
        if new_player != player:
            return new_matrix, new_player
        return random_spot(matrix, player)

class AI3:
    def mark_spot(self, matrix, player):
        matrix = np.array(matrix)

        new_matrix, new_player = win_in_1(matrix, player)
        if new_player != player:
            return new_matrix, new_player

        new_matrix, new_player = defend_in_1(matrix, player)
        if new_player != player:
            return new_matrix, new_player

        return random_spot(matrix, player)

class AI4:
    def mark_spot(self, matrix, player):
        matrix = np.array(matrix)

        new_matrix, new_player = win_in_1(matrix, player)
        if new_player != player:
            return new_matrix, new_player

        new_matrix, new_player = defend_in_1(matrix, player)
        if new_player != player:
            return new_matrix, new_player

        new_matrix, new_player = take_center(matrix, player)
        if new_player != player:
            return new_matrix, new_player

        return random_spot(matrix, player)

class AI5:
    def mark_spot(self, matrix, player):
        matrix = np.array(matrix)

        new_matrix, new_player = win_in_1(matrix, player)
        if new_player != player:
            return new_matrix, new_player

        new_matrix, new_player = defend_in_1(matrix, player)
        if new_player != player:
            return new_matrix, new_player

        new_matrix, new_player = take_center(matrix, player)
        if new_player != player:
            return new_matrix, new_player

        new_matrix, new_player = take_corner(matrix, player)
        if new_player != player:
            return new_matrix, new_player

        return random_spot(matrix, player)

class AI6:
    def mark_spot(self, matrix, player):
        matrix = np.array(matrix)

        # TODO: refactor to a list of functions
        new_matrix, new_player = win_in_1(matrix, player)
        if new_player != player:
            return new_matrix, new_player

        new_matrix, new_player = defend_in_1(matrix, player)
        if new_player != player:
            return new_matrix, new_player

        new_matrix, new_player = take_center(matrix, player)
        if new_player != player:
            return new_matrix, new_player

        new_matrix, new_player = take_corner(matrix, player)
        if new_player != player:
            return new_matrix, new_player

        new_matrix, new_player = take_side(matrix, player)
        if new_player != player:
            return new_matrix, new_player

        return random_spot(matrix, player)

def Factory(level):
    factory = [AI0, AI1, AI2, AI3, AI4, AI5, AI6]
    return factory[level]()
