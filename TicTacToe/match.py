"""TicTacToe.
"""

import argparse

from backend import model
from backend import ai


class State:
    def __init__(self):
        self.player = model.PLAYER1
        self.matrix = [[model.NOONE, model.NOONE, model.NOONE],
                       [model.NOONE, model.NOONE, model.NOONE],
                       [model.NOONE, model.NOONE, model.NOONE]]

    def __init__(self, player):
        self.player = player
        self.matrix = [[model.NOONE, model.NOONE, model.NOONE],
                       [model.NOONE, model.NOONE, model.NOONE],
                       [model.NOONE, model.NOONE, model.NOONE]]

def play(level_a, level_b, num_matches):
    bot_1 = ai.AiFactory(level_a)
    bot_2 = ai.AiFactory(level_b)
    summary = [0, 0, 0]

    for i in range(num_matches):

        if i < num_matches / 2:
            state = State(model.PLAYER1)
        else:
            state = State(model.PLAYER2)

        while True:
            if state.player == model.PLAYER1:
                state.matrix, state.player = bot_1.mark_spot(state.matrix, state.player)
                # print(state.matrix)
            winner = model.check_winner(state.matrix)
            if winner != model.NOONE:
                summary[winner-1] += 1
                # print("{}: {}".format(i, winner))
                break
            if state.player == model.PLAYER2:
                state.matrix, state.player = bot_2.mark_spot(state.matrix, state.player)
                # print(state.matrix)
            winner = model.check_winner(state.matrix)
            if winner != model.NOONE:
                summary[winner-1] += 1
                # print("{}: {}".format(i, winner))
                break
    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", type=int, required=True,
                        help="player 1 level [1-7]")
    parser.add_argument("-b", type=int, required=True,
                        help="player 2 level [1-7]")
    parser.add_argument("-n", type=int, default=10,
                        help="number of matches")
    args = parser.parse_args()

    summary = play(args.a, args.b, args.n)
    print("Player A (level {}) wins:".format(args.a) + str(summary[0]).rjust(5))
    print("Player B (level {}) wins:".format(args.b) + str(summary[1]).rjust(5))
    print("Draws                  :"                 + str(summary[2]).rjust(5))
