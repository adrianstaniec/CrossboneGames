from random import randrange
import numpy as np
from backend import model

def first_from_left(matrix, player):
    for col in range(7):
        new_matrix, new_player = model.place(matrix, player, col)
        if new_player != player: 
            return new_matrix, model.opponent(player)

def __random(matrix, player):
    while True:
        col = randrange(7)
        new_matrix, new_player = model.place(matrix, player, col)
        if new_player != player: 
            return matrix, model.opponent(player)

class AI:
    steps = []

    def __init__(self, steps=[first_from_left]):
        self.steps = steps

    def place(self, matrix, player):
        matrix = np.array(matrix)
        for f in self.steps:
            new_matrix, new_player = f(matrix, player)
            if new_player != player:
                return new_matrix, new_player


__algorithms = {0 : [first_from_left],
                1 : [__random]}

def Factory(level):
    return AI(__algorithms[level])


NUM = len(__algorithms)
