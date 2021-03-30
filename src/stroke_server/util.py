import socket
import json
import threading
import cv2
import numpy as np
import copy


def readjson(file_path, cd):
    t_file = open(file_path, encoding=cd)
    t_dict = json.load(t_file)
    t_file.close()
    return t_dict

def viz_pnts(size, pnts, path=None, blocking=True, img=None):
    '''
    This function visualize the 0-base TTF coooridate system's point in opencv

    Args:
        size (tuple): the viz rect size
        pnts (list): two elements' list, xs' list and ys' list
        paht (list): pnts idxs' list, the path of points
        blocking (bool): whether block when imshowing the final result
        img (np.array): 
    '''
    def rot90(img):
        timg = cv2.transpose(img)
        timg = cv2.flip(timg, 0)
        return timg
    
    if not img:
        img = np.zeros(size, np.uint8)

    if path is None:
        for i in range(len(pnts[0])):
            img[pnts[0][i], pnts[1][i]] = 255
    else:
        for i in path:
            img[pnts[0][i], pnts[1][i]] = 255
            timg = rot90(img)
            cv2.imshow("viz points", timg)
            cv2.waitKey(20)
    
    timg = rot90(img)
    cv2.imshow("viz points", timg)
    if blocking:
        cv2.waitKey()
    else:
        cv2.waitKey(5000)
    cv2.destroyAllWindows()
