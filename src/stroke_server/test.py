import socket
import json
import time
import math
from util import readjson
from skeleton import viz_pnts
from tsp_solver.greedy import solve_tsp

def distance(x1, y1, x2, y2):
    '''
    This fucntion calculates the  Euclidian distance between 2 points

    Args:
        x1 (float): X value of the first point
        y1 (float): Y value of the first point
        x2 (float): X value of the second point
        y2 (float): Y value of the secons point

    Returns:
        dist (float): Euclidian distance between point 1 and 2
    '''
    dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return dist


def getajmat(points):
    pnt_nums = len(points[0])
    r  = [[0 for x in range(pnt_nums)] for y in range(pnt_nums)]

    for p1 in range(pnt_nums):
        for p2 in range(pnt_nums):
            x1, y1= points[0][p1], points[1][p1]
            x2, y2= points[1][p2], points[1][p2]
            r[p1][p2]=distance(x1,y1,x2,y2)

    return r


def sendonce(cofig_file, cfg_cd='utf-8'):
    config = readjson(cofig_file, cfg_cd)
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    s.connect((config['addr'], config['port']))

    while True:
        # word = '离了谱了abc >?+_!@#$%$^&'
        word = input("type what u fucking want to write: ")
        for sig_wd in word:
            print("???", sig_wd)
            s.send(bytes(sig_wd, encoding='utf-8'))
            recvs = s.recv(10240000)
            t_str = str(recvs, encoding='utf-8')
            t_list = json.loads(t_str)
            # viz_pnts((255, 255), t_list)
            print(len(t_list[0]))
            r = getajmat(t_list)
            b_t = time.time()
            path = solve_tsp(r, optim_steps=10)
            e_t = time.time()
            print(f'tsp cost {e_t-b_t}')
            print(len(recvs), len(t_list[0]))
            viz_pnts((255, 255), t_list, path)
    s.close()
if __name__ == "__main__":
    for i in range(5):
        sendonce("../../config/stroke_serv.json")
        time.sleep(1)
    
    