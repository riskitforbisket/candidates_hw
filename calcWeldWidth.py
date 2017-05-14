'''
    Author: Daniel Irizarry

    BONUS_NOTE:
        This program finds the bead with in pixels. IF you desire the output
        in millimeters I would use this instantaneous field of view projection.
        This also assumes the camera has been calibrated and run through a
        dewarping algorithm to remove any lense distortion.

        UnitsDependingOnRangeMeasurement = fieldofView/focalPlaneArraySize \
                * (np.pi/180.0) * cameraDistanceToWeldingPoint

    CALIBRATION VARIABLES:


    The Problem:
        Calculate welding bead width

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

###############################################################################
#for interval datalogger
#yanked from SO: http://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds

import time
from threading import Event, Thread

class RepeatedTimer:

    """Repeat `function` every `interval` seconds."""

    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.start = time.time()
        self.event = Event()
        self.thread = Thread(target=self._target)
        self.thread.start()

    def _target(self):
        while not self.event.wait(self._time):
            self.function(*self.args, **self.kwargs)

    @property
    def _time(self):
        return self.interval - ((time.time() - self.start) % self.interval)

    def stop(self):
        self.event.set()
        self.thread.join()
###############################################################################

#defines for adjustable variabls
HIGH_THRESH = 40.0      # These were played around with
LOW_THRESH = 40.0/3.0   #
SIGMA = 1.6
KERN_SIZE = 5
OUT_FILENAME_ALL = "widthPerFrame.csv"
OUT_FILENAME_20HZ = "widthPerFrame20HZ.csv"
TIME_DELTA = 0.05 #20Hz

#container for data
widthOverTime = []
loggedData = []
cumulativeTime = 0.0

#function to log data
def logData():
    global cumulativeTime
    cumulativeTime += 0.05
    loggedData.append((cumulativeTime, widthOverTime[-1]))
    return

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
    for i in range(0, edgeIm.shape[0]):
        rowSums[i] = np.sum(edgeIm[i])
    rowSums = sgf(rowSums, 5, 2)

    #split the dimension reduced data in half
    half = rowSums.shape[0]/2

    row1 = np.where(rowSums==rowSums[:half].max())[0][0]
    row2 = np.where(rowSums==rowSums[half:].max())[0][0]

    #debug visuals
    #plt.plot(rowSums, np.arange(len(rowSums)))
    #plt.show()
    #plt.imshow(edgeIm)
    #plt.show()
    return np.abs(row1-row2)

if __name__ == "__main__":
    print "Daniel Irizarry - The Best Candidate!"

    #container for data
    widthOverTime = []
    cumulativeTime = 0

    #open video file and pull the first frame
    video = cv2.VideoCapture("./videos/weld.mp4")
    ok, frame = video.read()

    #open file for data logging per frame
    fp = open(OUT_FILENAME_ALL, "w")
    fpHz = open(OUT_FILENAME_20HZ, "w")
    print>>fp,"time,width"
    print>>fpHz,"time,width"

    #while we still get a valid frame
    count = 0

    #start datalogger and begin the frame processing
    datalogger = RepeatedTimer(0.05, logData)

    #loop and process frames, no timing limits
    while ok:

        #prepFrame
        prepIm, xMaxLoc, yMaxLoc = prepareImage(frame)

        #only send in a portion of the image where the weld track should be
        #a reasonable estimate is that it is in a 50 pixel window that
        #extends to the right of the image. The small y offset is to try to
        # eliminate the intense edge of the welding tip
        widthOverTime.append(measureWeldBead(prepIm[xMaxLoc-30:xMaxLoc+30, yMaxLoc+25:]))
        print>>fp,str(count) + "," + str(widthOverTime[count])
        ok, frame = video.read()
        count += 1

    #stop logger, write logged data to file, release video resources, close file.
    datalogger.stop()
    for data in loggedData:
        print>>fpHz,str(data[0]) + "," + str(data[1])
    video.release()
    fp.close()
    fpHz.close()

    #visualize the measurements over time
    print "AVERAGE WELD WIDTH IN PIXELS = ", np.mean(widthOverTime)
    plt.plot(np.array(widthOverTime), np.arange(len(widthOverTime)))
    plt.title("Bead Width In Pixels")
    plt.show()
