'''
    Author: Daniel Irizarry

    The approach:
        After looking at the video I noticed that the bead had a pretty
        distinct dark contrast compared to the top and bottom portions
        of the scene. I decided to use an edge detector to find the
        distinct horizontal lines of the bead approximation.

        In order so the algorithm is a little more robust, the location
        of the peak intensity pixel is captured and used as a reference
        for the width calculations. Essentially, I will only look at lines
        to the right of the intensity region for the width calculation.

        After restricting the computations, I took the canny binary output
        and summed the sub image along the rows of the image. The data was
        then split in half to yeild two distinct peaks in the count data
        localized around where a line should be and the max of both subIms
        was differenced as the width.

        NOTE: In order to get more consistent and robust thresholds, the
        OTSU thresholding method should be applied and would be if I were
        to revisit this specific project. Canny thresholds were manually
        adjusted due to this being a first order solution to this problem.
'''

import numpy as np
import cv2

#1D smoothing function
from scipy.signal import savgol_filter as sgf

#for easy frame visualization
import matplotlib.pyplot as plt

#defines for adjustable variabls
HIGH_THRESH = 40.0      # These were played around with
LOW_THRESH = 40.0/3.0   #
SIGMA = 1.6
KERN_SIZE = 5

#im: numpy array, raw video frame, this is RBG image
#prepIm: numpy array, prepared image ready for bead measurement
def prepareImage(im):
    #convert the frame to single channel
    prepIm = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

    #apply gaussian blur to eliminate high frequency noise
    #kernel size set to 5x5 and sigma set to 1.6 (noticed this give best results through experience)
    prepIm = cv2.GaussianBlur(prepIm, (KERN_SIZE, KERN_SIZE), SIGMA)
    xMax, yMax = np.where(prepIm == prepIm.max())

    return prepIm, xMax[0], yMax[0]

#im: numpy array, frame from weld video
#outputs: weldWidth, approximate width of weld bead in pixels
def measureWeldBead(im):
    edgeIm = cv2.Canny(im, LOW_THRESH, HIGH_THRESH)

    #convert to ture binary and sum along rows
    edgeIm[edgeIm==255] = 1
    rowSums = np.zeros(edgeIm.shape[0])
    print len(edgeIm[0])
    for i in range(0, edgeIm.shape[0]):
        rowSums[i] = np.sum(edgeIm[i])
    rowSums = sgf(rowSums, 5, 2)

    #split the dimension reduced data in half
    half = rowSums.shape[0]/2

    row1 = np.where(rowSums==rowSums[:half].max())[0][0]
    row2 = np.where(rowSums==rowSums[half:].max())[0][0]

    #plt.plot(rowSums, np.arange(len(rowSums)))
    #plt.show()
    #plt.imshow(edgeIm)
    #plt.show()
    return np.abs(row1-row2)

if __name__ == "__main__":
    print "Daniel Irizarry - The Best Candidate!"

    #open video file and pull the first frame
    video = cv2.VideoCapture("./videos/weld.mp4")
    ok, frame = video.read()
    widthOverTime = []

    #while we still get a valid frame
    while ok:

        prepIm, xMaxLoc, yMaxLoc = prepareImage(frame)

        #only send in a portion of the image where the weld track should be
        #a reasonable estimate is that it is in a 50 pixel window that
        #extends to the right of the image. The small y offset is to try to
        # eliminate the intense edge of the welding tip
        widthOverTime.append(measureWeldBead(prepIm[xMaxLoc-30:xMaxLoc+30, yMaxLoc+25:]))
        ok, frame = video.read()

    video.release()
    print widthOverTime
    print "AVERAGE WELD WIDTH IN PIXELS = ", np.mean(widthOverTime)
    plt.plot(np.array(widthOverTime), np.arange(len(widthOverTime)))
    plt.show()

    #widthInPixels = measureWeldBead(np.arange(1))
