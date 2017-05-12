'''
    Author: Daniel Irizarry

    The Problem:
        Generate a STL file from any given multivariable expression.

    The approach:

'''

import numpy as np
import cv2

#1D smoothing function
from scipy.signal import savgol_filter as sgf

#for easy frame visualization
import matplotlib.pyplot as plt

if __name__ == "__main__":

    print "Daniel Irizarry - The Best!"
