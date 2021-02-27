import socket
import json
import threading
from util import readjson


def stroke_server(sock: socket.socket, font: dict):
    data = sock.recv(10240)
    if not data:
        return

    req = str(data, encoding='utf-8')

    for word in req:
        uni = str(ord(word))
        if uni in font['cmap']:
            word_name = font['cmap'][uni]
            
            print(word_name, uni)
        else:
            print(ord(word))
        pass
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
        "../../config/font/arial.json",
        "../../config/stroke_serv.json")
