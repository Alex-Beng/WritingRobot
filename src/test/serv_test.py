import socket
import json
import time
import math

import sys
sys.path.append("../")
from stroke_server.util import readjson, viz_pnts
from tsp_solver.greedy import solve_tsp


def sendonce(cofig_file, cfg_cd='utf-8'):
    config = readjson(cofig_file, cfg_cd)
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    s.connect((config['addr'], config['port']))

    while True:
        word = input("type what u fucking want to write: ")
        for sig_wd in word:
            s.send(bytes(sig_wd, encoding='utf-8'))
            recvs = s.recv(10240000)
            t_str = str(recvs, encoding='utf-8')
            t_list = json.loads(t_str)

            # min_idx = min(range(len(t_list[0])), key= lambda k: t_list[0][k]**2+t_list[1][k]**2)
            # min_path = sorted(range(len(t_list[0])), key= lambda k: t_list[0][k]**2+t_list[1][k]**2)
            # print(min_idx)
            # path = None
            path = range(len(t_list[0]))
            # path = min_path

            # viz_pnts((255, 255), t_list)
            # print(len(t_list[0]))
            # r = getajmat(t_list)
            # b_t = time.time()
            # path = solve_tsp(r, optim_steps=10)
            # e_t = time.time()
            # print(f'tsp cost {e_t-b_t}')
            # print(len(recvs), len(t_list[0]))
            viz_pnts((255, 255), t_list, path)
    s.close()
if __name__ == "__main__":
    for i in range(5):
        sendonce("../../config/stroke_serv.json")
        time.sleep(1)
    
    