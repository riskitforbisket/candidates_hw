import numpy as np
import cv2

#im: numpy array, frame from weld video
#outputs: weldWidth, approximate width of weld bead in pixels
def measureWeldBead(im):
    print "Inside measure function"
    weldWidth = 0.0
    return weldWidth

if __name__ == "__main__":
    print "Daniel Irizarry - The Best!"
    widthInPixels = measureWeldBead(np.arange(1))
