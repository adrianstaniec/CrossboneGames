from random import randrange

from backend import model


class AI1:
    def mark_spot(self, matrix, player):
        """First empty spot"""
        for y in range(3):
            for x in range(3):
                if matrix[x][y] == 0:
                    matrix[x][y] = player
                    return (matrix, model.change_player(player))

class AI2:
    def mark_spot(self, matrix, player):
        """Random empty spot"""
        while True:
            guess = randrange(9)
            x = guess // 3
            y = guess % 3
            if matrix[x][y] == 0:
                matrix[x][y] = player
                return (matrix, model.change_player(player))
