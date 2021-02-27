import socket
import json
import time
from util import readjson

def sendonce(cofig_file, cfg_cd='utf-8'):
    config = readjson(cofig_file, cfg_cd)

    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    s.connect((config['addr'], config['port']))

    word = '离了谱了abc >?+_!@#$%$^&'

    s.send(bytes(word, encoding='utf-8'))
    recvs = s.recv(10240)
    print(recvs)

if __name__ == "__main__":
    for i in range(5):
        sendonce("../../config/stroke_serv.json")
        time.sleep(1)
    
    