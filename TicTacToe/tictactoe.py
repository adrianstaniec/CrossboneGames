from time import sleep
import pygame
import numpy as np


NOONE = 0
PLAYER1 = 1
PLAYER2 = 2
DRAW = 3

class State:
# current player
    player = PLAYER1
    cursor = (1, 1)
    matrix = [[NOONE, NOONE, NOONE],
              [NOONE, NOONE, NOONE],
              [NOONE, NOONE, NOONE]]

class View:
    SIZE = 600
    board = pygame.image.load("resources/board.png")
    ends = [pygame.image.load("resources/end0.png"),
            pygame.image.load("resources/end1.png")]
    markers = [pygame.image.load("resources/marker0.png"),
               pygame.image.load("resources/marker1.png")]
    cursors = [pygame.image.load("resources/cursor0.png"),
               pygame.image.load("resources/cursor1.png")]

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SIZE, self.SIZE))

    def draw_board(self, matrix, player, cursor):
        self.screen.fill(0) #clear screen
        self.screen.blit(self.board, (0, 0))
        for x in range(3):
            for y in range(3):
                if matrix[x][y] != 0:
                    self.screen.blit(self.markers[matrix[x][y]-1],
                                     (30+200*x, 30+200*y))
        x = cursor[0]
        y = cursor[1]
        self.screen.blit(self.cursors[player-1], (30+200*x, 30+200*y))
        pygame.display.flip() #update screen

    def game_over(self, winner):
        self.screen.fill(0)
        if winner == 1 or winner == 2:
            self.screen.blit(self.ends[winner-1], (0, 0))
        else:
            self.screen.blit(self.ends[0], (0, 0))
            self.screen.blit(self.ends[1], (0, 0))
        pygame.display.flip() #update screen
        sleep(1)
        pygame.quit()
        exit(0)

class Model:
    @staticmethod
    def move_cursor(pos, vec):
        pos = np.array(pos)
        vec = np.array(vec)
        new_pos = pos + vec
        if new_pos[0] >= 0 and new_pos[0] <= 2:
            if new_pos[1] >= 0 and new_pos[1] <= 2:
                return tuple(new_pos)
        return tuple(pos)

    @staticmethod
    def change_player(player):
            if player == PLAYER1:
                return PLAYER2
            else:
                return PLAYER1

    @staticmethod
    def mark_spot(matrix, player, cursor):
        x = cursor[0]
        y = cursor[1]
        if matrix[x][y] == 0:
            matrix[x][y] = player
            player = Model.change_player(player)
        return (matrix, player)

    @staticmethod
    def check_winner(matrix):
        # horizontals
        for row in range(3):
            if matrix[row][0] == matrix[row][1]:
                if matrix[row][1] == matrix[row][2]:
                    return matrix[row][0]
        # verticals
        for col in range(3):
            if matrix[0][col] == matrix[1][col]:
                if matrix[1][col] == matrix[2][col]:
                    return matrix[0][col]
        # diagonals
        if matrix[0][0] == matrix[1][1]:
            if matrix[1][1] == matrix[2][2]:
                return matrix[1][1]
        if matrix[2][0] == matrix[1][1]:
            if matrix[1][1] == matrix[0][2]:
                return matrix[1][1]
        # draw
        num_marks = 0
        for row in range(3):
            for col in range(3):
                if matrix[row][col]:
                    num_marks += 1
        if num_marks == 9:
            return DRAW
        # still playing
        return NOONE


if __name__ == "__main__":
    state = State()
    view = View()

    while True:
        view.draw_board(state.matrix, state.player, state.cursor)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    view.game_over(NOONE)

                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    state.matrix, state.player = Model.mark_spot(state.matrix, state.player, state.cursor)
                    winner = Model.check_winner(state.matrix)
                    if winner != NOONE:
                        view.game_over(winner)

                if event.key == pygame.K_LEFT or event.key == pygame.K_h:
                    state.cursor = Model.move_cursor(state.cursor, (-1, 0))
                if event.key == pygame.K_DOWN or event.key == pygame.K_j:
                    state.cursor = Model.move_cursor(state.cursor, (0, 1))
                if event.key == pygame.K_UP or event.key == pygame.K_k:
                    state.cursor = Model.move_cursor(state.cursor, (0, -1))
                if event.key == pygame.K_RIGHT or event.key == pygame.K_l:
                    state.cursor = Model.move_cursor(state.cursor, (1, 0))
