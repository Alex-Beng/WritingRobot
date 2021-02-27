import cv2
import numpy as np
from skimage.morphology import skeletonize


# poly points(contours) to its skeleton
# coor keep the same
# assume the pnt have become 0-base
# size: [0] x, [1] y.
def pnts2skeleton(ploy_pnts, size, debug=False):
    ploy_pnts = np.array(ploy_pnts)
    img = np.zeros(size, np.uint8)

    cv2.fillPoly(img, [ploy_pnts], (1))
    skeleton = skeletonize(img, method='lee')
    skeleton = skeleton.astype(np.uint8)*255
    _, contours, _, = cv2.findContours(skeleton, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    contour = contours[0]
    pnt_num = contour.shape[0]
    pnt_num = int(pnt_num)
    half_pnt_num = pnt_num//2

    half_contour = contour[:half_pnt_num, :, :]
    half_contour = half_contour.reshape(-1, 2)    
    if debug:
        result_img = np.zeros(size, np.uint8)        
        for pnt in half_contour:
            result_img[pnt[1], pnt[0]] = 255
        cv2.imshow("res", result_img)
        cv2.waitKey()
