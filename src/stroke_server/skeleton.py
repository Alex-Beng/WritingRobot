import cv2
import numpy as np
from skimage.morphology import skeletonize


# unicode to path points
# input: sigle unicode 
# output: poly points(rebase if needed), and the glyf-rect
# reture None if not have
def uni2pnts(uni :str, font :dict):
    if not uni in font['cmap']:
        return None, None
    if not font['cmap'][uni] in font['glyf'] or \
        not 'contours' in font['glyf'][font['cmap'][uni]]:
        return None, None
    glyf_key = font['cmap'][uni]
    print(glyf_key)

    x_min = font['head']['xMin']
    y_min = font['head']['yMin']
    x_max = font['head']['xMax']
    y_max = font['head']['yMax']

    contours = font['glyf'][glyf_key]['contours']
    all_stroke_pnts = []
    for contour in contours:
        res_pnts = []
        for pnt_dict in contour:
            t_x = pnt_dict['x']
            t_y = pnt_dict['y']
            if x_min < 0:
                t_x -= x_min
            if y_min < 0:
                t_y -= y_min
            res_pnts.append([t_x, t_y])
        all_stroke_pnts.append(res_pnts)
    return all_stroke_pnts, (y_max-y_min, x_max-x_min)

     
# poly points(contours) to its skeleton
# coor keep the same
# assume the pnt have become 0-base
# size: [0] x, [1] y.
def pnts2skeleton(ploy_pnts, size, debug=False):
    ploy_pnts = np.array(ploy_pnts)
    img = np.zeros(size, np.uint8)

    cv2.fillPoly(img, [ploy_pnts], (1))
    skeleton = skeletonize(img, method='lee')
    skeleton = skeleton.astype(np.uint8)
    return np.nonzero(skeleton)
    
# use tsp alg to plan path based on skeleton
# coor keep the same
def tsp_pnts(ske_pnts):
    
    return

if __name__ == "__main__":
    pass