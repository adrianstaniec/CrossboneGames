#!/usr/bin/python3
"""TicTacToe.
"""

from time import sleep
import pygame
import argparse
import numpy as np

from backend import model
from backend import ai


class View:
    SIZE = 600
    board = pygame.image.load("resources/board.png")
    ends = {model.PLAYER_X: pygame.image.load("resources/end_X.png"),
            model.PLAYER_O: pygame.image.load("resources/end_O.png")}
    markers = {model.PLAYER_X: pygame.image.load("resources/marker_X.png"),
               model.PLAYER_O: pygame.image.load("resources/marker_O.png")}
    cursors = {model.PLAYER_X: pygame.image.load("resources/cursor_X.png"),
               model.PLAYER_O: pygame.image.load("resources/cursor_O.png")}

    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont("Verdana", 18)
        self.screen = pygame.display.set_mode((self.SIZE, self.SIZE))

    def draw_board(self, matrix, stats):
        self.screen.fill(0)  # clear screen
        self.screen.blit(self.board, (0, 0))
        for x in range(3):
            for y in range(3):
                if matrix[x][y] != model.EMPTY:
                    self.screen.blit(self.markers[matrix[x][y]],
                                     (30 + 200 * y, 30 + 200 * x))
        text_color = (255, 255, 100)
        label_x = self.font.render("x:{}".format(stats['x']), 1, text_color)
        label_o = self.font.render("o:{}".format(stats['o']), 1, text_color)
        label_d = self.font.render("=:{}".format(stats['=']), 1, text_color)
        self.screen.blit(label_x, (10, 575))
        self.screen.blit(label_d, (285, 575))
        self.screen.blit(label_o, (560, 575))

    def draw_cursor(self, player, cursor):
        x = cursor[0]
        y = cursor[1]
        self.screen.blit(self.cursors[player], (30 + 200 * y, 30 + 200 * x))
        pygame.display.flip()  # update screen

    def game_over(self, winner):
        if winner == model.PLAYER_X or winner == model.PLAYER_O:
            self.screen.blit(self.ends[winner], (0, 0))
        else:
            self.screen.blit(self.ends[model.PLAYER_X], (0, 0))
            self.screen.blit(self.ends[model.PLAYER_O], (0, 0))
        pygame.display.flip()  # update screen
        sleep(1)

    def quit_game(self):
        pygame.quit()
        exit(0)


class Human:
    def __init__(self, player):
        self.player = player

    def mark_spot(self, matrix, cursor):
        player = self.player
        row = cursor[0]
        col = cursor[1]
        if matrix[row][col] == model.EMPTY:
            matrix[row][col] = self.player
            player = model.opponent(self.player)
        return matrix, player


def move_cursor(pos, vec):
    pos = np.array(pos)
    vec = np.array(vec)
    new_pos = pos + vec
    if 0 <= new_pos[0] <= 2:
        if 0 <= new_pos[1] <= 2:
            return tuple(new_pos)
    return tuple(pos)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--level", type=int,
                        help=("run in single player mode on difficulty level"
                              "[0-{}]").format(ai.NUM - 1))
    args = parser.parse_args()

    if args.level == None:
        single_player = False
        agents = {model.PLAYER_X: Human(model.PLAYER_X),
                  model.PLAYER_O: Human(model.PLAYER_O)}
    else:
        single_player = True
        agents = {model.PLAYER_X: Human(model.PLAYER_X),
                  model.PLAYER_O: ai.Factory(model.PLAYER_O, args.level)}

    view = View()
    cursor = np.array([1, 1])

    stats = {model.PLAYER_X: 0,
             model.PLAYER_O: 0,
             model.DRAW: 0}

    starting_player = model.PLAYER_X
    abort = False

    while True:  # game loop
        state = model.State(starting_player)
        view.draw_board(state.matrix, stats)
        view.draw_cursor(state.player, cursor)

        while True:  # move loop
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                abort = True
                break

            if event.type == pygame.KEYDOWN:

                if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                    abort = True
                    break

                if event.key in [pygame.K_h, pygame.K_a, pygame.K_LEFT]:
                    cursor = move_cursor(cursor, (0, -1))
                if event.key in [pygame.K_j, pygame.K_s, pygame.K_DOWN]:
                    cursor = move_cursor(cursor, (1, 0))
                if event.key in [pygame.K_k, pygame.K_w, pygame.K_UP]:
                    cursor = move_cursor(cursor, (-1, 0))
                if event.key in [pygame.K_l, pygame.K_d, pygame.K_RIGHT]:
                    cursor = move_cursor(cursor, (0, 1))

                if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    if state.player == model.PLAYER_X or not single_player:
                        state.matrix, state.player = agents[
                            state.player].mark_spot(state.matrix, cursor)
                        state.winner = model.check_winner(state.matrix)
                        if state.winner != model.NOONE:
                            view.draw_board(state.matrix, stats)
                            break

            if single_player and state.player == model.PLAYER_O:
                state.matrix, state.player = agents[state.player].mark_spot(
                    state.matrix)
                state.winner = model.check_winner(state.matrix)
                if state.winner != model.NOONE:
                    view.draw_board(state.matrix, stats)
                    break

            view.draw_board(state.matrix, stats)
            view.draw_cursor(state.player, cursor)

        if abort:
            break
        view.game_over(state.winner)
        stats[state.winner] += 1
        starting_player = model.opponent(starting_player)

    view.quit_game()
