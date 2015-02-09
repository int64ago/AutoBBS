# -*- coding: utf-8 -*-

import os, json

class UrlFIFO:
    def __init__(self, fifopath):
        self.fifopath = fifopath
    def __read(self):
        f = open(self.fifopath, 'r')
        data = f.readline()
        f.close()
        return data
    def __write(self, data):
        f = open(self.fifopath, 'w')
        f.write(data)
        f.close()
    def get(self):
        if not os.path.exists(self.fifopath):
            return 'no_url'
        res = json.loads(self.__read())
        if len(res) == 0:
            return 'no_url'
        url = res[0]
        self.__write(json.dumps(res[1:]))
        return url
    def put(self, item):
        res = []
        if os.path.exists(self.fifopath):
            res = json.loads(self.__read())
        res.append(item)
        self.__write(json.dumps(res))
