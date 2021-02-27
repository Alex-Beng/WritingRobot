import socket
import json
import threading


def readjson(file_path, cd):
    t_file = open(file_path, encoding=cd)
    t_dict = json.load(t_file)
    t_file.close()
    return t_dict

