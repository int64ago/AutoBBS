# -*- coding: utf-8 -*-

import urllib, urllib2, cookielib, re, md5, time

class Utils:
    @staticmethod
    def getMD5Of(src):
        m = md5.new()
        m.update(src)
        return m.hexdigest()
    @staticmethod
    def getTime():
        return int(time.time())

class AutoBBS:
    __userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36'

    def __init__(self, domain, userName, passWord, proxyHandler = {}):
        self.domain = domain
        self.__userName = userName
        self.__passWord = passWord
        cj = cookielib.CookieJar()
        self.__opener = urllib2.build_opener(urllib2.ProxyHandler(proxyHandler),
                                             urllib2.HTTPCookieProcessor(cj))
        
    def __get(self, url, headers):
        request = urllib2.Request(url = url, headers = headers)
        res = self.__opener.open(request)
        return res.getcode(), res.info(), res.geturl(), res.read()
    
    def __post(self, url, headers, data):
        data = urllib.urlencode(data)
        request = urllib2.Request(url = url, headers = headers, data = data)
        res = self.__opener.open(request)
        return res.getcode(), res.info(), res.geturl(), res.read()
    
    def login(self):
        headers = {'User-Agent': self.__userAgent}
        params = {'mod': 'logging', 'action': 'login'}
        url = self.domain.urlWithParams('member.php', params)
        res = self.__get(url, headers)
        
        loginhash = re.search(r'loginhash=(\w+)', res[3])
        params = {'mod': 'logging', 'action': 'login',
                  'loginsubmit': 'yes', 'inajax': '1',
                  'loginhash': loginhash.groups()[0]}
        url = self.domain.urlWithParams('member.php', params)
        formhash = re.search(r'formhash=(\w+)', res[3])
        data = {'formhash': formhash.groups()[0], 'referer': self.domain.rootUrl(),
                'questionid': '0', 'answer': '', 'loginsubmit': 'true',
                'username': self.__userName,
                'password': Utils.getMD5Of(self.__passWord)}
        self.__post(url, headers, data)
        url = self.domain.rootUrl()
        res = self.__get(url, headers)
        if res[3].find('访问我的空间'):
            print('Login OK!')
            self.__formhash = re.search(r'formhash=(\w+)', res[3]).groups()[0]
        else :
            print('Login failed!')
    
    def reply(self, fid, tid, msg):
        headers = {'User-Agent': self.__userAgent}
        params = {'mod': 'post', 'action': 'reply',
                  'replysubmit': 'yes', 'infloat': 'yes',
                  'handlekey': 'fastpost', 'inajax': '1',
                  'fid': fid, 'tid': tid}
        url = self.domain.urlWithParams('forum.php', params)
        data = {'message': msg, 'posttime': Utils.getTime(),
                'usesig': '0', 'subject': '', 'formhash': self.__formhash}
        res = self.__post(url, headers, data)
        if res[3].find('成功'):
            print('Reply OK!')
        else :
            print('Reply failed!')
    def new(self, fid, subject, message):
        headers = {'User-Agent': self.__userAgent}
        params = {'mod': 'post', 'action': 'newthread', 'topicsubmit': 'yes', 'fid': fid}
        url = self.domain.urlWithParams('forum.php', params)
        data = {'formhash': self.__formhash, 'posttime': Utils.getTime(),
                'wysiwyg': '1', 'typeid': '323', 'subject': subject,
                'message': message, 'allownoticeauthor': '0', 'usesig': '1'}
        res = self.__post(url, headers, data)
'''
from Domain import Domain
domain = Domain(hostname = 'bbs.stuhome.net')
autobbs = AutoBBS(domain = domain, userName = '', passWord = '')
autobbs.login()
'''
