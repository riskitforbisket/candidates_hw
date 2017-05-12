import numpy as np
import cv2

#for easy frame visualization
import matplotlib.pyplot as plt

#im: numpy array, raw video frame, this is RBG image
#prepIm: numpy array, prepared image ready for bead measurement
def prepareImage(im):
    #convert the frame to single channel
    prepIm = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

    #apply gaussian blur to eliminate high frequency noise
    #kernel size set to 7x7 and sigma set to 1.6 (noticed this give best results through experience)
    prepIm = cv2.GaussianBlur(prepIm, (7,7), 1.6)
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
        prepIm = prepareImage(frame)
        plt.imshow(prepIm)
        plt.show()

    widthInPixels = measureWeldBead(np.arange(1))
