import socket
import json
import threading
import cv2
import numpy as np
from util import readjson, viz_pnts
from skeleton import uni2pnts, pnts2skeleton
from stroke_path import get_max_continue, StrokePath


def stroke_server(sock: socket.socket, font: dict):
    while True:
        data = sock.recv(10240)
        if not data:
            sock.close()
            return

        req = str(data, encoding='utf-8')
        all_strokes = [[], []]
        rect_size = None
        for word in req:
            uni = str(ord(word))
            print(word)
            stroke_control_pnts, rect_size = uni2pnts(uni, font)
            if stroke_control_pnts is None:
                continue
            print(rect_size)
            img = np.zeros(rect_size, np.uint8)
            for stroke_control_pnt in stroke_control_pnts:
                stroke_ske_pnts = pnts2skeleton(stroke_control_pnt, rect_size, True)

                stroke_ske_path = StrokePath(stroke_ske_pnts, rect_size)
                
                viz_pnts(rect_size,
                         stroke_ske_path.points, 
                         stroke_ske_path.path, False, img)
                
                all_strokes[0] += stroke_ske_path.points[0]
                all_strokes[1] += stroke_ske_path.points[1]
        # viz result
        # viz_pnts(rect_size, all_strokes)

        res = str(all_strokes)
        print(len(res))
        sock.send(bytes(res, encoding='utf-8'))
        # sock.close()


def main(font_file, cofig_file, font_cd='utf-8', cfg_cd='utf-8') -> int:
    # font json
    font = readjson(font_file, font_cd)
    config = readjson(cofig_file, cfg_cd)

    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # in case CTRLC

    s.bind((config['addr'], config['port']))
    s.listen(socket.SOMAXCONN)
    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=stroke_server, args=[sock, font])
        t.start()


if __name__ == "__main__":
    
    # exit()
    main(
        "../../config/font/fangsong_gb2312.json",
        "../../config/stroke_serv.json")
