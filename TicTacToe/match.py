"""TicTacToe.
"""

import argparse

from backend import model
from backend import ai


def play(level_a, level_b, num_matches):
    bot_1 = ai.Factory(level_a)
    bot_2 = ai.Factory(level_b)

    summary = {model.PLAYER_X : 0,
               model.PLAYER_O : 0,
               model.DRAW : 0}

    for i in range(num_matches):

        if i < num_matches / 2:
            state = model.State(model.PLAYER_X)
        else:
            state = model.State(model.PLAYER_O)

        while True:
            if state.player == model.PLAYER_X:
                state.matrix, state.player = bot_1.mark_spot(state.matrix, state.player)
                # print(state.matrix)
            winner = model.check_winner(state.matrix)
            if winner != model.NOONE:
                summary[winner] += 1
                # print("{}: {}".format(i, winner))
                break
            if state.player == model.PLAYER_O:
                state.matrix, state.player = bot_2.mark_spot(state.matrix, state.player)
                # print(state.matrix)
            winner = model.check_winner(state.matrix)
            if winner != model.NOONE:
                summary[winner] += 1
                # print("{}: {}".format(i, winner))
                break
    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", type=int, required=True,
                        help="player 1 level [0-{}]".format(ai.NUM-1))
    parser.add_argument("-b", type=int, required=True,
                        help="player 2 level [0-{}]".format(ai.NUM-1))
    parser.add_argument("-n", type=int, default=10,
                        help="number of matches")
    args = parser.parse_args()

    summary = play(args.a, args.b, args.n)
    print("Player {} (level {}):".format(model.PLAYER_X, args.a), end='')
    print(str(summary[model.PLAYER_X]).rjust(5))
    print("Player {} (level {}):".format(model.PLAYER_O, args.b), end='')
    print(str(summary[model.PLAYER_O]).rjust(5))
    print("Draws             :", end='')
    print(str(summary[model.DRAW]).rjust(5))
