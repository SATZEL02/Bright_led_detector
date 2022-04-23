import numpy as np
import cv2
import argparse
# ---- Useful functions ----


def display_img(img, delay=1000):
    """
    One liner that displays the given image on screen
    """
    cv2.namedWindow("V", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("V", img)
    cv2.waitKey(50)


def to_gray(img):
    """
    Converts the input in grey levels
    Returns a one channel image
    """
    greyi=0
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    while(greyi<=9):
            greyi +=1 
            grey_name = "C:/Users/Dev/OneDrive/Documents/GitHub/Led_detector/grey/" + str(greyi) + '.jpg'
            try:
                cv2.imwrite(grey_name, gray)
            except:
                print('x')
    return gray

def grey_histogram(img, nBins=64):
    """
    Returns a one dimension histogram for the given image
    The image is expected to have one channel, 8 bits depth
    nBins can be defined between 1 and 255 
    """
    hist_size = [nBins]
    h_ranges = [0, 256]
    hist = cv2.calcHist(img,[0],None,hist_size, h_ranges)
    return hist


def extract_bright(grey_img, histogram=False):
    """
    Extracts brightest part of the image.
    Expected to be the LEDs (provided that there is a dark background)
    Returns a Thresholded image
    histgram defines if we use the hist calculation to find the best margin
    """
    # Searches for image maximum (brightest pixel)
    # We expect the LEDs to be brighter than the rest of the image
    [minVal, maxVal, minLoc, maxLoc] = cv2.minMaxLoc(grey_img)
    # print("Brightest pixel val is %d" % (maxVal))
    # We retrieve only the brightest part of the image
    # Here is use a fixed margin (80%), but you can use hist to enhance this one
    if 1:
        # Histogram may be used to wisely define the margin
        # We expect a huge spike corresponding to the mean of the background
        # and another smaller spike of bright values (the LEDs)
        hist = grey_histogram(grey_img, nBins=64)
        [hminValue, hmaxValue, hminIdx, hmaxIdx] = cv2.minMaxLoc(hist)
        margin = 244  # statistics to be calculated using hist data

    thresh = int(margin) # in pix value to be extracted
    threshi = 0
    # thresh = 255
    print("Threshold is defined as %d" % (thresh))

    ret,thresh_img = cv2.threshold(grey_img,thresh,255, cv2.THRESH_BINARY)
    while(threshi<=9):
            threshi +=1 
            thresh_name = "C:/Users/Dev/OneDrive/Documents/GitHub/Led_detector/thresh/" + str(threshi) + '.jpg'
            try:
                cv2.imwrite(thresh_name, thresh_img)
            except:
                print('x')
    return thresh_img

def pointDist(a, b):
  return np.linalg.norm(np.subtract(a, b))

def find_leds(thresh_img):
    """
    Given a binary image showing the brightest pixels in an image, 
    returns a result image, displaying found leds in a rectangle
    """
    contours,heirarcy= cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = list( map(lambda c: cv2.approxPolyDP(c, 4, True), contours) )
    points = [ (i, tuple(pt)) for i, c in enumerate(contours) for [pt] in c ]
    checkedContours = set()
    outputi = 0
    for i, c in enumerate(contours):
        checkedContours.add(i)
        cv2.drawContours(img, [c], -1, (0,255,0), 2)
        pts = [pt[1] for pt in points if pt[0] not in checkedContours]
        if not pts: break
        for [pt] in c:
            nearest = min(pts, key=lambda b: pointDist(pt, b))
            if pointDist(pt, nearest) <= 15:
                cv2.line(img, tuple(pt), tuple(nearest), (0, 255, 0), 3)
    while(outputi<=9):
            outputi +=1 
            out_name = "C:/Users/Dev/OneDrive/Documents/GitHub/Led_detector/output/" + str(outputi) + '.jpg'
            try:
                cv2.imwrite(out_name, img)
            except:
                print('x')
    return img


if __name__ == '__main__':
    url = 'ipwebcam address/video'
    video_file = cv2.VideoCapture(0)
    ap = argparse.ArgumentParser()
    args = vars(ap.parse_args())
    cpt =0


    while (True):
    # Capture the video frame by frame
        ret, frame = video_file.read()
        frame = frame[1] if args.get("video", False) else frame
        img = frame
        while (cpt<=9):
            cpt += 1
            input_name = "C:/Users/Dev/OneDrive/Documents/GitHub/Led_detector/input/" + str(cpt) + '.jpg'
            try:
                cv2.imwrite(input_name, img)
            except:
                print('x')
        ####
        # Starts image processing here
        ####
        # Turns to one channel image
        grey_img = to_gray(img)

        thresh_img = extract_bright(grey_img)

        # We want to extract the elements left, and count their number
        led_img = find_leds(thresh_img)
        display_img(led_img, delay=1000)