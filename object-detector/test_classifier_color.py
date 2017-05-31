# Import the required modules
from skimage.transform import pyramid_gaussian
from skimage.io import imread
from skimage.feature import hog
from sklearn.externals import joblib
import cv2
import argparse as ap
from nms import nms
from config import *




#new
import selectivesearch
from skimage import  transform

def sliding_window(image, window_size, step_size):
    '''
    This function returns a patch of the input image `image` of size equal
    to `window_size`. The first image returned top-left co-ordinates (0, 0)
    and are increment in both x and y directions by the `step_size` supplied.
    So, the input parameters are -
    * `image` - Input Image
    * `window_size` - Size of Sliding Window
    * `step_size` - Incremented Size of Window

    The function returns a tuple -
    (x, y, im_window)
    where
    * x is the top-left x co-ordinate
    * y is the top-left y co-ordinate
    * im_window is the sliding window image
    '''
    for y in xrange(0, image.shape[0], step_size[1]):
        for x in xrange(0, image.shape[1], step_size[0]):
            yield (x, y, image[y:y + window_size[1], x:x + window_size[0]])

if __name__ == "__main__":
    # Parse the command line arguments
    # file_dot = open('..\data\Locations.txt', 'w')
    # file_dot.write('1: ')
    parser = ap.ArgumentParser()
    parser.add_argument('-i', "--image", help="Path to the test image", required=True)
    parser.add_argument('-d','--downscale', help="Downscale ratio", default=1.25,
            type=int)
    parser.add_argument('-v', '--visualize', help="Visualize the sliding window",
            action="store_true")
    args = vars(parser.parse_args())

    clf = joblib.load(model_path)

    detections = []
    # Read the image
    im = imread(args["image"])
    min_wdw_sz = (100, 40)
    step_size = (10, 10)
    downscale = args['downscale']
    visualize_det = args['visualize']


    #selective search
    img_lbl, regions = selectivesearch.selective_search(
        im, scale=500, sigma=0.9, min_size=10)

    candidates = set()
    for r in regions:
        # excluding same rectangle (with different segments)
        if r['rect'] in candidates:
            continue
        # excluding regions smaller than 2000 pixels
        if r['size'] < 2000:
            continue
        # distorted rects
        x, y, w, h = r['rect']
        if w / h > 3 or h / w > 1:
            continue
        candidates.add(r['rect'])
    candidates_window = []
    gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)


    for x, y, w, h in candidates:
        candidates_window.append(gray[y:y + h, x:x + w])
    image = 0
    for (x, y, w, h) in candidates:
        im_window = transform.resize(candidates_window[image],(40,100))
        # cv2.imshow("warp",im_window)
        cv2.waitKey()
        image+=1
        cd = []
        fd = hog(im_window, orientations, pixels_per_cell, cells_per_block, visualize, normalize)
        pred = clf.predict(fd)
        if pred == 1:
            print  "Detection:: Location -> ({}, {})".format(x, y)
            detections.append((x, y, clf.decision_function(fd),
                               w,
                               h))
            cd.append(detections[-1])



    # Display the results before performing NMS
    clone = gray.copy()
    for (x_tl, y_tl, _, w, h) in detections:
        # Draw the detections
        cv2.rectangle(gray, (x_tl, y_tl), (x_tl+w, y_tl+h), (0, 0, 0), thickness=2)
    cv2.imshow("Raw Detections before NMS", gray)
    cv2.waitKey()

    # Perform Non Maxima Suppression
    detections = nms(detections, threshold)

    # Display the results after performing NMS
    for (x_tl, y_tl, _, w, h) in detections:
        # Draw the detections
        cv2.rectangle(clone, (x_tl, y_tl), (x_tl+w,y_tl+h), (0, 0, 0), thickness=2)
        # file_dot.write('({} {})'.format(y_tl, x_tl))
    cv2.imshow("Final Detections after applying NMS", clone)

    cv2.waitKey()
