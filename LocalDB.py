# -*- coding: utf-8 -*-

import os, json

class LocalDB:
    def __init__(self, dbpath, limit):
        self.dbpath = dbpath
        self.limit = limit
    def __read(self):
        f = open(self.dbpath, 'r')
        data = f.readline()
        f.close()
        return data
    def __write(self, data):
        f = open(self.dbpath, 'w')
        f.write(data)
        f.close()
    def isExist(self, item):
        if not os.path.exists(self.dbpath):
            return False
        res = json.loads(self.__read())
        if item in res:
            return True
        else :
            return False
    def push(self, item):
        res = []
        if os.path.exists(self.dbpath):
            res = json.loads(self.__read())
        res.append(item)
        if len(res) > self.limit:
            res = res[len(res)/2:]
        self.__write(json.dumps(res))
