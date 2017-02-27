"""TicTacToe.
"""

import argparse

from backend import model
from backend import ai

def play_once(agents, starting_player):
    state = model.State(starting_player)
    trace = []
    while True:
        state.matrix, state.player = agents[state.player].mark_spot(state.matrix, state.player)
        trace.append(state.matrix)
        winner = model.check_winner(state.matrix)
        if winner != model.NOONE:
            break
    return winner, trace


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", type=int, required=True,
                        help="player 1 level [0-{}]".format(ai.NUM-1))
    parser.add_argument("-b", type=int, required=True,
                        help="player 2 level [0-{}]".format(ai.NUM-1))
    parser.add_argument("-n", type=int, default=10,
                        help="number of matches")
    args =  parser.parse_args()

    agents = { model.PLAYER_X : ai.Factory(level_a),
               model.PLAYER_O : ai.Factory(level_b)}

    summary = {model.PLAYER_X : 0,
               model.PLAYER_O : 0,
               model.DRAW : 0}

    for i in range(num_matches):
        if i < num_matches / 2:
            winner, _ = play_once(agents, model.PLAYER_X)
            summary[winner] += 1
        else:
            winner, _ = play_once(agents, model.PLAYER_O)
            summary[winner] += 1

    summary = play(args.a, args.b, args.n)
    print(" X (L{}) | Y (L{}) |   =    ".format(args.a, args.b))
    print("{: ^8}|{: ^8}|{: ^8}".format(summary[model.PLAYER_X],
                                        summary[model.PLAYER_O],
                                        summary[model.DRAW]))
