#!/usr/bin/python3
"""ConnectFour
"""

from time import sleep
import pygame
import argparse

from backend import model
from backend import ai


class View:
    WIDTH = 700
    HEIGHT = 600
    tile = pygame.image.load("resources/tile.png")
    markers = {model.PLAYER_X : pygame.image.load("resources/marker_X.png"),
               model.PLAYER_O : pygame.image.load("resources/marker_O.png")}
    cursors = {model.PLAYER_X : pygame.image.load("resources/cursor_X.png"),
               model.PLAYER_O : pygame.image.load("resources/cursor_O.png")}
    ends = {model.PLAYER_X : pygame.image.load("resources/end_X.png"),
            model.PLAYER_O : pygame.image.load("resources/end_O.png")}

    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont("Verdana", 18)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def draw_board(self, matrix):
        self.screen.fill(0) #clear screen
        for x in range(6):
            for y in range(7):
                self.screen.blit(self.tile, (100*y, 100*x))
        for x in range(6):
            for y in range(7):
                if matrix[x][y] != ' ':
                    self.screen.blit(self.markers[matrix[x][y]], (10+100*y, 10+100*x))
        text_color = (255,255,100)
        label_x = self.font.render("x:{}".format(stats['x']), 1, text_color)
        label_o = self.font.render("o:{}".format(stats['o']), 1, text_color)
        label_d = self.font.render("=:{}".format(stats['=']), 1, text_color)
        self.screen.blit(label_x, ( 10, 575))
        self.screen.blit(label_d, (335, 575))
        self.screen.blit(label_o, (660, 575))

    def draw_cursor(self, player, cursor):
        self.screen.blit(self.cursors[player], (10+100*cursor, 10))
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
    if args.level != None:
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

                if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_DOWN, pygame.K_j]:
                    if state.player == model.PLAYER_X or not single_player:
                        state.matrix, state.player = model.place(state.matrix,
                                                                 state.player,
                                                                 state.cursor)
                        state.winner = model.check_winner(state.matrix)
                        if state.winner != model.NOONE:
                            view.draw_board(state.matrix)
                            break

                if event.key == pygame.K_LEFT or event.key == pygame.K_h:
                    state.cursor = model.move_cursor(state.cursor, -1)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_l:
                    state.cursor = model.move_cursor(state.cursor,  1)

            if single_player and state.player == model.PLAYER_O:
                state.matrix, state.player = bot.place(state.matrix,
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
        starting_player = model.opponent(starting_player)

    view.quit_game()
