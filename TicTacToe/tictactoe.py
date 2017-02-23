"""TicTacToe.
"""

from time import sleep
import pygame
from docopt import docopt
import argparse

from backend import model
from backend import ai


class State:
    player = model.PLAYER1
    cursor = (1, 1)
    matrix = [[model.NOONE, model.NOONE, model.NOONE],
              [model.NOONE, model.NOONE, model.NOONE],
              [model.NOONE, model.NOONE, model.NOONE]]

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--level", type=int,
                        help="run in single player mode on difficulty level [1-2]")
    args = parser.parse_args()

    single_player = False
    bot = None
    if args.level:
        single_player = True
        if args.level == 1:
            bot = ai.AI1()
        else:
            bot = ai.AI2()

    state = State()
    view = View()

    while True:
        view.draw_board(state.matrix, state.player, state.cursor)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    view.game_over(model.NOONE)

                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    state.matrix, state.player = model.mark_spot(state.matrix, state.player, state.cursor)
                    winner = model.check_winner(state.matrix)
                    if winner != model.NOONE:
                        view.game_over(winner)
                    if single_player and state.player == model.PLAYER2:
                        state.matrix, state.player = bot.mark_spot(state.matrix, state.player)
                        winner = model.check_winner(state.matrix)
                        if winner != model.NOONE:
                            view.game_over(winner)

                if event.key == pygame.K_LEFT or event.key == pygame.K_h:
                    state.cursor = model.move_cursor(state.cursor, (-1, 0))
                if event.key == pygame.K_DOWN or event.key == pygame.K_j:
                    state.cursor = model.move_cursor(state.cursor, (0, 1))
                if event.key == pygame.K_UP or event.key == pygame.K_k:
                    state.cursor = model.move_cursor(state.cursor, (0, -1))
                if event.key == pygame.K_RIGHT or event.key == pygame.K_l:
                    state.cursor = model.move_cursor(state.cursor, (1, 0))
