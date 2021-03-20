import socket
import json
import threading
from util import readjson
from skeleton import uni2pnts, pnts2skeleton


def stroke_server(sock: socket.socket, font: dict):
    data = sock.recv(10240)
    if not data:
        return

    req = str(data, encoding='utf-8')
    res = ''
    for word in req:
        uni = str(ord(word))
        stroke_pnts, rect_size = uni2pnts(uni, font)
        if stroke_pnts is None:
            continue
        for stroke_pnt in stroke_pnts:
            stroke = pnts2skeleton(stroke_pnt, rect_size, True)

            t_res = str(stroke)
            res += t_res
    print(res)
    sock.send(bytes(res, encoding='utf-8'))
    sock.close()
    return


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
