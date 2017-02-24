"""TicTacToe.
"""

from time import sleep
import pygame
from docopt import docopt
import argparse

from backend import model
from backend import ai


class View:
    SIZE = 600
    board = pygame.image.load("resources/board.png")
    ends = {'X' : pygame.image.load("resources/end_X.png"),
            'O' : pygame.image.load("resources/end_O.png")}
    markers = {'X' : pygame.image.load("resources/marker_X.png"),
               'O' : pygame.image.load("resources/marker_O.png")}
    cursors = {'X' : pygame.image.load("resources/cursor_X.png"),
               'O' : pygame.image.load("resources/cursor_O.png")}

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SIZE, self.SIZE))

    def draw_board(self, matrix, player, cursor):
        self.screen.fill(0) #clear screen
        self.screen.blit(self.board, (0, 0))
        for x in range(3):
            for y in range(3):
                if matrix[x][y] != model.EMPTY:
                    self.screen.blit(self.markers[matrix[x][y]],
                                     (30+200*y, 30+200*x))
        x = cursor[0]
        y = cursor[1]
        self.screen.blit(self.cursors[player], (30+200*y, 30+200*x))
        pygame.display.flip() #update screen

    def game_over(self, winner):
        self.screen.fill(0)
        if winner == model.PLAYER1 or winner == model.PLAYER2:
            self.screen.blit(self.ends[winner], (0, 0))
        else:
            self.screen.blit(self.ends[model.PLAYER1], (0, 0))
            self.screen.blit(self.ends[model.PLAYER2], (0, 0))
        pygame.display.flip() #update screen
        sleep(1)
        return model.State()

    def quit_game(self):
        pygame.quit()
        exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--level", type=int,
                        help=("run in single player mode on difficulty level"
                              "[0-{}]").format(ai.NUM-1))
    args = parser.parse_args()

    single_player = False
    bot = None

    if args.level:
        single_player = True
        bot = ai.Factory(args.level)

    state = model.State()
    view = View()

    while True:
        view.draw_board(state.matrix, state.player, state.cursor)

        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            break

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                break

            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                state.matrix, state.player = model.mark_spot(state.matrix, state.player, state.cursor)
                winner = model.check_winner(state.matrix)
                if winner != model.NOONE:
                    state = view.game_over(winner)
                    continue
                if single_player and state.player == model.PLAYER2:
                    state.matrix, state.player = bot.mark_spot(state.matrix, state.player)
                    winner = model.check_winner(state.matrix)
                    if winner != model.NOONE:
                        state = view.game_over(winner)
                        continue

            if event.key == pygame.K_LEFT or event.key == pygame.K_h:
                state.cursor = model.move_cursor(state.cursor, (0, -1))
            if event.key == pygame.K_DOWN or event.key == pygame.K_j:
                state.cursor = model.move_cursor(state.cursor, (1, 0))
            if event.key == pygame.K_UP or event.key == pygame.K_k:
                state.cursor = model.move_cursor(state.cursor, (-1, 0))
            if event.key == pygame.K_RIGHT or event.key == pygame.K_l:
                state.cursor = model.move_cursor(state.cursor, (0, 1))

    view.quit_game()
