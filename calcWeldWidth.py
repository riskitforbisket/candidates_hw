import numpy as np
import cv2

#for easy frame visualization
import matplotlib.pyplot as plt

#im: numpy array, raw video frame
#prepIm: numpy array, prepared image ready for bead measurement
def prepareImage(im):

    return prepIm


#im: numpy array, frame from weld video
#outputs: weldWidth, approximate width of weld bead in pixels
def measureWeldBead(im):
    print "Inside measure function"
    weldWidth = 0.0
    return weldWidth

if __name__ == "__main__":
    print "Daniel Irizarry - The Best!"

    #open video file and pull the first frame
    video = cv2.VideoCapture("./videos/weld.mp4")
    ok, frame = video.read()

    #while we still get a valid frame
    while ok:
        ok, frame = video.read()
        print frame.shape
        plt.imshow(frame)
        plt.show()

    widthInPixels = measureWeldBead(np.arange(1))
