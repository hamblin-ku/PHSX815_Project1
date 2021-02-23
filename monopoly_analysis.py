# imports of external packages to use in our code
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse
import my_params
from Random import Random



def make_plot(data):
    #imort custom matplotlib parameters from file
    custom_params = my_params.params()
    mpl.rcParams.update(custom_params)
    
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(myx, 50, density=True, facecolor='g', alpha=0.75)
    ax.set_xlabel('x')
    ax.set_ylabel('Probability')
    ax.set_title('Uniform Random Number')

    
# main function for this Python code
if __name__ == "__main__":
    
    # CODE to analyze outputs from monopoly_sim.py
    # maybe compile into animation where turn # increases over time
    # allow user to see probability of landing on any tile given the current turn #
