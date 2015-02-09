# -*- coding: utf-8 -*-

class Domain:
    def __init__(self, hostname, protocol = 'http', port = 80):
        self.hostname = hostname
        self.protocol = protocol
        self.port = port
    def rootUrl(self):
        url = self.protocol + '://' + self.hostname + \
              ('' if self.port == 80 else ':' + str(self.port)) + '/'
        return url
    def fullUrl(self, extUrl):
        if extUrl[0] == '/':
            return rootUrl(self) + extUrl[1:]
        else :
            return extUrl
    def urlWithParams(self, path = '', params = {}):
        pd = ''
        for key in params:
            pd += key + '=' + params[key] + '&'
        if pd == '':
            return self.rootUrl() + path
        else :
            return self.rootUrl() + path + '?' + pd[:-1]
