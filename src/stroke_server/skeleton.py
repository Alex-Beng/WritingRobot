import cv2
import numpy as np
from skimage.morphology import skeletonize


def uni2pnts(uni :str, font :dict):
    '''
    This function gets all contours control points of a unicode word.

    Args:
        uni (string): the input str of sigle unicode
        font (dict): the TTF font json-form object
    
    Returns:
        control pnts (list): list where all element are list. element containing 
                            control points list correspond to the contours one-to-one.
                            control point is the (x, y) form.
                            return None if TTF doesn't have the word
        rect size (tuple): tuple of two element, (x space, y space)
                           return None if TTF doesn't have the word
    '''
    if not uni in font['cmap']:
        return None, None
    if not font['cmap'][uni] in font['glyf'] or \
        not 'contours' in font['glyf'][font['cmap'][uni]]:
        return None, None
    glyf_key = font['cmap'][uni]

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
    return all_stroke_pnts, (x_max-x_min, y_max-y_min)

def pnts2skeleton(ploy_pnts, size, debug=False):
    '''
    This function gets the font skeleton point of its control points using lee's skeletonize method.

    Args:
        ploy_pnts (list): control points' list. control point is the (x, y) form
        size (tuple): tuple of two element, (x range, y range)
    
    Returns:
        skeleton points (list): skeleton points' list. coordinate keep the same with input.
    '''
    ploy_pnts = np.array(ploy_pnts)
    img = np.zeros(size, np.uint8)

    cv2.fillPoly(img, [ploy_pnts], (1))
    skeleton = skeletonize(img, method='lee')
    skeleton = skeleton.astype(np.uint8)
    return [list(i)[::-1] for i in np.nonzero(skeleton)]
