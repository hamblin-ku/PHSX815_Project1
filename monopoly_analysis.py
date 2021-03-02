# File:     monopoly_analysis.py
# Author:   Kurt Hamblin
# Description:  Analyze outputs from the monopoly simulation in monopoly_experiment.py

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse
from Random import Random
from celluloid import Camera
import matplotlib
from scipy.stats import chisquare

# Import my custom matplotlib config and activate it
import my_params
custom_params = my_params.params()
matplotlib.rcParams.update(custom_params)

# This function makes the animation with the package 'celluloid'
def make_animation(data_left, data_right, fname):
    fig, (ax1, ax2) = plt.subplots(nrows= 1, ncols=2, figsize = (10, 3), sharey = True)
    ax1.set_xlim([-1,40])
    ax2.set_xlim([-1,40])
    ax1.set_ylim([0, 0.25])
    ax1.set_xlabel('Board Tile')
    ax2.set_xlabel('Board Tile')
    ax1.set_ylabel('Probability')
    
    #Start the camera object
    camera = Camera(fig)
    
    # These are the x values for all the tiles by the color we want to plot them by
    # We will manually define the colors for the values not in the dict, but those in the dict can be indexed by the respective color key
    x_vals = np.arange(40)
    x_else = [7, 22, 36, 2, 17, 33, 4, 20, 38, 0]
    x_locs = {"brown": [1, 3], "skyblue": [6, 8, 9], "fuchsia": [11, 13, 14], "orange": [16, 18, 19], "red": [21, 23, 24],
                "yellow": [26, 27, 29],  "forestgreen": [31, 32, 34], "mediumblue": [37, 39], "black": [5, 15, 25, 35], "slategrey": [12, 28]}
    keys = list( x_locs.keys() )
    
    # Iterate through each row (correspondign to a turn) in the data and construct the plot
    for i, turn in enumerate(data_left):
        ax1.bar(x_else, turn[x_else], color = 'none', edgecolor = 'k', hatch = '/')
        ax1.bar(10, turn[10], color = 'lightgrey', edgecolor = 'k', hatch = 'XXX')
        for key in keys:
            ax1.bar(x_locs[key], turn[x_locs[key]], color = key)
        ax1.text(2/40, .88, 'Unbiased Dice', transform= ax1.transAxes , color='k', fontsize = 16)
        ax1.text(32/40, .88, 'Turn {0}'.format(i+1), transform= ax1.transAxes , color='k', fontsize = 16)
        ax1.set_xticks([0, 5, 10, 15, 20, 25, 30, 35, 40])
        ax1.set_xticks([], minor=True)
        
        ax2.bar(x_else, data_right[i][x_else], color = 'none', edgecolor = 'k', hatch = '/')
        ax2.bar(10, data_right[i][10], color = 'lightgrey', edgecolor = 'k', hatch = 'XXX')
        for key in keys:
            ax2.bar(x_locs[key], data_right[i][x_locs[key]], color = key)
        ax2.text(2/40, .88, 'Biased Dice', transform= ax2.transAxes , color='k', fontsize = 16)
        ax2.text(32/40, .88, 'Turn {0}'.format(i+1), transform= ax2.transAxes , color='k', fontsize = 16)
        ax2.set_xticks([0, 5, 10, 15, 20, 25, 30, 35, 40])
        ax2.set_xticks([], minor=True)
        
        # Take a snapshot for the animation
        camera.snap()
    
    # Complete the animation and save it
    animation = camera.animate(interval= 600, repeat = True, repeat_delay = 500)
    animation.save('docs/'+fname,  writer = 'imagemagick')

    
# main function for this Python code
if __name__ == "__main__":

    # Set up parser to handle command line arguments
    # Run as 'python monopoly_analysis.py -h' to see all available commands
    parser = argparse.ArgumentParser()
    parser.add_argument("--Read_From", "-r", help="File to read numbers from", required = True)
    parser.add_argument("--Ngames",  help="Number of games used to simulate imported data", required = True)
    args = parser.parse_args()
    
    Ngames = np.uint64(args.Ngames)
    fname = args.Read_From
    
    results = np.loadtxt('data/'+fname, delimiter = ',')
    expected_dist = np.loadtxt('data/unbiased_dist.txt', delimiter = ',')
    
    # create the animation
    make_animation(data_left = expected_dist, data_right = results, fname='total.gif')

    
    #we must convert from the normalized distributions to the expected
    expected_dist =  expected_dist[-1]*Ngames
    obs_dist = results[-1]*Ngames
    
    # Remove index 30 (go to jail tile) since it always has value 0
    expected_dist = np.delete(expected_dist, 30)
    obs_dist = np.delete(obs_dist, 30)
    
    # Figure to compare the final probability distributions
    fig, ax = plt.subplots()
    x_plot = np.concatenate([np.arange(30), np.arange(31,40)])
    ax.bar(x_plot, obs_dist/Ngames, color = 'b', alpha = 0.6, label = 'observed')
    ax.bar(x_plot, expected_dist/Ngames, color = 'r', alpha = 0.6, label = 'expected')
    ax.set_xlabel('Board Tile')
    ax.legend(loc='upper right')
    ax.set_ylabel('Probability')
    fig.savefig('docs/dist_compare2.pdf')
    
    # Perform the chi-squared test
    chisq, p = chisquare(f_obs = obs_dist,f_exp = expected_dist)
    print('Chisq: %.3f \np-value: %.3e' % (chisq, p))

    plt.show()

