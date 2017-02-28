"""Competition - plays round-robin tournament for all algorithms
"""
import argparse
import numpy as np

from backend import ai
from backend import model
import match

import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", type=int, default=100, help="number of matches")
    args = parser.parse_args()

    NUM_GAMES = args.n

    numbers = np.empty((ai.NUM, ai.NUM), dtype='float')
    numbers[:] = np.nan
    strings = np.empty((ai.NUM, ai.NUM), dtype='object')
    charts = [[[] for _ in range(ai.NUM)] for _ in range(ai.NUM)]

    for a in range(ai.NUM):
        for b in range(a+1):
            stats = match.play_multiple(a, b, NUM_GAMES)
            strings[a,b] = "{}/{}".format(stats[model.PLAYER_X], stats[model.PLAYER_O])
            charts[a][b] = [stats[model.PLAYER_O]/NUM_GAMES,
                            stats[model.PLAYER_X]/NUM_GAMES,
                            stats[model.DRAW]/NUM_GAMES]
            try:
                numbers[a, b] = stats[model.PLAYER_X] / stats[model.PLAYER_O]
            except:
                numbers[a, b] = float('Inf')
        for b in range(a+1, ai.NUM):
            charts[a][b] = [0, 0, 0]


    # print("\n --- Win/Loss ratios ---")
    # df = pd.DataFrame(numbers)
    # df = df.rename(lambda x: x + 1)
    # df = df.rename(columns=lambda x: x+1)
    # df = df.iloc[::-1]
    # print(df)

    print("\n --- Win/Loss ratios ---")
    df = pd.DataFrame(strings)
    # df = df.rename(lambda x: x + 1)
    # df = df.rename(columns=lambda x: x+1)
    # df = df.iloc[::-1]
    print(df)


    # print("\n --- [Loss, Win, Draw] ---")
    df = pd.DataFrame(charts)
    # df = df.rename(lambda x: x + 1)
    # df = df.rename(columns=lambda x: x+1)
    # print(df)

    plt.imshow(charts, interpolation='nearest')
