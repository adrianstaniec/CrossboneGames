"""Match - plays n matches between two algorithms
"""
import argparse

from backend import model
from backend import ai


def play_once(agents, state, verbose=False):
    trace = []
    while True:
        state.matrix, state.player = agents[state.player].mark_spot(state.matrix)
        if verbose:
            print(state.matrix, end='\n\n')
        trace.append(state.matrix)
        winner = model.check_winner(state.matrix)
        if winner != model.NOONE:
            break
    return winner, trace


def play_multiple(x_level, o_level, num_matches, verbose=False):
    agents = {model.PLAYER_X: ai.Factory(model.PLAYER_X, x_level),
              model.PLAYER_O: ai.Factory(model.PLAYER_O, o_level)}

    stats = {model.PLAYER_X: 0,
             model.PLAYER_O: 0,
             model.DRAW: 0}

    for i in range(num_matches):
        if i < num_matches / 2:
            state = model.State(model.PLAYER_X)
        else:
            state = model.State(model.PLAYER_O)
        winner, _ = play_once(agents, state, verbose)
        stats[winner] += 1

    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-x", type=int, default=1,
                        help="X player level [0-{}]".format(ai.NUM-1))
    parser.add_argument("-o", type=int, default=2,
                        help="O player level [0-{}]".format(ai.NUM-1))
    parser.add_argument("-n", type=int, default=10,
                        help="number of matches")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print board after every move")
    args = parser.parse_args()

    stats = play_multiple(args.x, args.o, args.n, args.verbose)

    print(" X (L{}) | O (L{}) |   =    ".format(args.x, args.o))
    print("{: ^8}|{: ^8}|{: ^8}".format(stats[model.PLAYER_X],
                                        stats[model.PLAYER_O],
                                        stats[model.DRAW]))
