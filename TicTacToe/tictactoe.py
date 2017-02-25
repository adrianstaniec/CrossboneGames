"""TicTacToe.
"""

from time import sleep
import pygame
import argparse

from backend import model
from backend import ai


class View:
    SIZE = 600
    board = pygame.image.load("resources/board.png")
    ends = {model.PLAYER_X : pygame.image.load("resources/end_X.png"),
            model.PLAYER_O : pygame.image.load("resources/end_O.png")}
    markers = {model.PLAYER_X : pygame.image.load("resources/marker_X.png"),
               model.PLAYER_O : pygame.image.load("resources/marker_O.png")}
    cursors = {model.PLAYER_X : pygame.image.load("resources/cursor_X.png"),
               model.PLAYER_O : pygame.image.load("resources/cursor_O.png")}

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SIZE, self.SIZE))

    def draw_board(self, matrix):
        self.screen.fill(0) #clear screen
        self.screen.blit(self.board, (0, 0))
        for x in range(3):
            for y in range(3):
                if matrix[x][y] != model.EMPTY:
                    self.screen.blit(self.markers[matrix[x][y]],
                                     (30+200*y, 30+200*x))

    def draw_cursor(self, player, cursor):
        x = cursor[0]
        y = cursor[1]
        self.screen.blit(self.cursors[player], (30+200*y, 30+200*x))
        pygame.display.flip() #update screen

    def game_over(self, winner):
        if winner == model.PLAYER_X or winner == model.PLAYER_O:
            self.screen.blit(self.ends[winner], (0, 0))
        else:
            self.screen.blit(self.ends[model.PLAYER_X], (0, 0))
            self.screen.blit(self.ends[model.PLAYER_O], (0, 0))
        pygame.display.flip() #update screen
        sleep(1)

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

    stats = {model.PLAYER_X : 0,
             model.PLAYER_O : 0,
             model.DRAW : 0}
    starting_player = model.PLAYER_X

    view = View()

    abort = False

    while True: # game loop
        state = model.State(starting_player)
        view.draw_board(state.matrix)
        view.draw_cursor(state.player, state.cursor)

        while True: # move loop
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                abort = True
                break
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    abort = True
                    break

                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if state.player == model.PLAYER_X or not single_player:
                        state.matrix, state.player = model.mark_spot(state.matrix,
                                                                     state.player,
                                                                     state.cursor)
                        state.winner = model.check_winner(state.matrix)
                        if state.winner != model.NOONE:
                            view.draw_board(state.matrix)
                            break

                if event.key == pygame.K_LEFT or event.key == pygame.K_h:
                    state.cursor = model.move_cursor(state.cursor, (0, -1))
                if event.key == pygame.K_DOWN or event.key == pygame.K_j:
                    state.cursor = model.move_cursor(state.cursor, (1, 0))
                if event.key == pygame.K_UP or event.key == pygame.K_k:
                    state.cursor = model.move_cursor(state.cursor, (-1, 0))
                if event.key == pygame.K_RIGHT or event.key == pygame.K_l:
                    state.cursor = model.move_cursor(state.cursor, (0, 1))

            if single_player and state.player == model.PLAYER_O:
                state.matrix, state.player = bot.mark_spot(state.matrix,
                                                           state.player)
                state.winner = model.check_winner(state.matrix)
                if state.winner != model.NOONE:
                    view.draw_board(state.matrix)
                    break

            view.draw_board(state.matrix)
            view.draw_cursor(state.player, state.cursor)

        if abort:
            break
        view.game_over(state.winner)
        stats[state.winner] += 1
        print(stats)
        starting_player = model.opponent(starting_player)

    view.quit_game()
