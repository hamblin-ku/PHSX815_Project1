# File:     monopoly_experiment.py
# Author:   Kurt Hamblin
# Description:  Utitlize the Monopoly class in Monopoly.py to:
#   (1) Simulate enough games using unbiased dice to arrive at (or close to) the true probability distribution
#   (2) simulate "experiment" games using biased dice to compare

from Random import Random
from Monopoly import Monopoly
import matplotlib
import numpy as np
import argparse
from celluloid import Camera
import matplotlib.pyplot as plt
import my_params

custom_params = my_params.params()
matplotlib.rcParams.update(custom_params)

# main function for this Python code
if __name__ == "__main__":
    
    # Set up parser to handle command line arguments
    # Run as 'python monopoly_experiment.py -h' to see all available commands
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", "-s", help="Seed number to use")
    parser.add_argument("--Nsides",  help="Number of sides on each die")
    parser.add_argument("--Ngames",  help="Number of games to simulate ")
    parser.add_argument("--Nturns",  help="Number of turns to roll for")
    parser.add_argument("--write","-w",  help="File to write output to", required = True)
    args = parser.parse_args()

    # default seed
    seed = 5555
    if args.seed:
        print("Set seed to %s" % args.seed)
        seed = args.seed
    random = Random(seed)
    
    # By default, roll 6 sided dice
    Nsides = 6
    if args.Nsides:
        print("Number sides per die: %s" % args.Nsides)
        Nsides = np.uint64(args.Nsides)
    # Simulate 50 turns by default
    Nturns = 50
    if args.Nturns:
        print("Number of turns: %s" % args.Nturns)
        Nturns = np.uint64(args.Nturns)
    # Simulate 100 games by default
    Ngames = 100
    if args.Ngames:
        print("Number of games: %s" % args.Ngames)
        Ngames = np.uint64(args.Ngames)
    # File to write experiment data to
    file_name = args.write
    
    # Create weights by pulling from normal distribution
    weights = abs(np.random.normal(size=Nsides))
    # The weigths need to sum to one, so normalize them
    weights /= weights.sum()
    print(f'Weights: {weights}')
    
    # Construct Monopoly Objects
    game_fair = Monopoly(Nsides=Nsides, weights = None)
    game_biased = Monopoly(Nsides = Nsides, weights = weights)
    
    # Simulate the games
    results_fair =  game_fair.play_games(Nturns = Nturns, Ngames = 10**1, norm = True)
    results_biased = game_biased.play_games(Nturns = Nturns, Ngames = Ngames, norm = True)

    # Save the normalized results
    np.savetxt('data/unbiased_dist.txt', results_fair, delimiter = ',')
    np.savetxt('data/'+file_name, results_biased, delimiter = ',')
    
