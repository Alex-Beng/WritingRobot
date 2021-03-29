import socket
import json
import threading
from util import readjson, viz_pnts
from skeleton import uni2pnts, pnts2skeleton
from stroke_path import get_max_continue

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
            stroke_pnts, rect_size = uni2pnts(uni, font)
            print(rect_size)
            if stroke_pnts is None:
                continue
            for stroke_pnt in stroke_pnts:
                stroke = pnts2skeleton(stroke_pnt, rect_size, True)

                min_idx = sorted(range(len(stroke[0])), key= lambda k: stroke[0][k]-stroke[1][k])
                t_stroke = [[stroke[0][i] for i in min_idx], [stroke[1][i] for i in min_idx]]
                stroke = t_stroke

                path = get_max_continue(stroke)
                t_stroke = [[stroke[0][i] for i in path], [stroke[1][i] for i in path]]
                stroke = t_stroke
                
                # for i in range(len(stroke[0])):
                all_strokes[0] += stroke[0]
                all_strokes[1] += stroke[1]
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
