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

def viz_pnts(size, pnts, path=None):
    img = np.zeros(size, np.uint8)

    if path is None:
        for i in range(len(pnts[0])):
            img[pnts[0][i], pnts[1][i]] = 255
    else:
        for i in path:
            img[pnts[0][i], pnts[1][i]] = 255
            timg = cv2.transpose(img)
            timg = cv2.flip(timg, 0)
            cv2.imshow("ya", timg)
            cv2.waitKey(1)
    img = cv2.transpose(img)
    img = cv2.flip(img, 0)
    cv2.imshow("ya", img)
    cv2.waitKey()
    cv2.destroyAllWindows()
