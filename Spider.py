# -*- coding: utf-8 -*-

import urllib2, re, HTMLParser
from BeautifulSoup import BeautifulSoup

class UrlSpider:
    __userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36'
    __headers = {'User-Agent': __userAgent}
    def __init__(self, target):
        self.target = target
    def __one(self):
        ret = []
        url = 'http://wufazhuce.com/'
        req = urllib2.Request(url, headers = self.__headers)
        res = urllib2.urlopen(req).read()
        res = re.search(r'http://wufazhuce.com/one/vol.(\d+)', res)
        ret.append('http://wufazhuce.com/one/vol.' + res.groups()[0])
        return ret
    def __douban(self):
        url = 'http://thing.douban.com/'
        req = urllib2.Request(url, headers = self.__headers)
        res = urllib2.urlopen(req).read()
        res = re.findall(r'on=(\d+)"', res)
        ret = []
        for u in res:
            ret.append('http://www.douban.com/note/' + u + '/')
        return list(ret)
    def __zhihu(self):
        url = 'http://daily.zhihu.com/'
        req = urllib2.Request(url, headers = self.__headers)
        res = urllib2.urlopen(req).read()
        res = re.findall(r'<a href="http://daily.zhihu.com/story/(\d+)', res)
        ret = []
        for u in res:
            ret.append('http://daily.zhihu.com/story/' + u)
        return list(ret)
    def __jiandan(self):
        url = 'http://jandan.net/new'
        req = urllib2.Request(url, headers = self.__headers)
        res = urllib2.urlopen(req).read()
        res = re.findall(r'http://jandan.net/201.*html', res)
        return list(res)
    def collect(self):
        if self.target == 'one':
                return self.__one()
        elif self.target == 'douban':
                return self.__douban()
        elif self.target == 'zhihu':
                return self.__zhihu()
        elif self.target == 'jiandan':
                return self.__jiandan()
        else :
            print('Target is not existed!')
            return None
    
class ContSpider:
    __userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36'
    __headers = {'User-Agent': __userAgent}
    def __init__(self, url):
        self.url = url
        if url.find('wufazhuce.com') != -1:
            self.target = 'one'
        elif url.find('www.douban.com') != -1:
            self.target = 'douban'
        elif url.find('daily.zhihu.com') != -1:
            self.target = 'zhihu'
        elif url.find('jandan.net') != -1:
            self.target = 'jiandan'
        else :
            self.target = None
            
    def __replaceImgs(self, content):
        imgs = re.findall(r'\[img\](.*)\[/img\]', content)
        for img in imgs:
            _url = 'http://getlink.sinaapp.com/ext?url=' + img
            _img = urllib2.urlopen(_url).read()
            content = content.replace(img, _img)
        return content
    def __message(self, content, url, name):
        return '[font=微软雅黑]' + content +\
               '\n\n\n\n\n转自：[url=%s]「%s」[/url][/font]' % (url, name)
    def __one(self):
        name = 'ONE·一个'
        req = urllib2.Request(url, headers = self.__headers)
        req = urllib2.Request(url = self.url, headers = self.__headers)
        res = urllib2.urlopen(req).read()
        soup = BeautifulSoup(res)
        res = res.replace('<br />', '\n')
        res = res.replace('\r', '').replace('\n\n', '\n')
        soup = soup.find('div', {'class': 'one-cuestion'})
        title = soup.findAll('h4')
        subject = title[0].getText().encode('utf8')
        author = title[1].getText().encode('utf8')
        content = soup.findAll('div', {'class': 'cuestion-contenido'})
        h = HTMLParser.HTMLParser()
        ask = h.unescape(content[0].getText()).encode('utf8')
        ans = h.unescape(content[1].getText()).encode('utf8')
        content = '[quote]' + ask + '[/quote]\n' + '[b]' + author + '[/b]\n' + ans
        message = self.__message(content, 'http://wufazhuce.com/', name)
        return subject + ' | ' + name , message
        
    def __douban(self):
        name = '豆瓣·事情'
        req = urllib2.Request(url = self.url, headers = self.__headers)
        res = urllib2.urlopen(req).read()
        subject = re.search(r'<title>([\w\W]*)</title>', res).groups()[0]
        subject = subject.strip()
        res = res.replace('<img src="', '[img]').replace('" alt=', '[/img]<span id=')
        res = res.replace('<br>', '\n')
        soup = BeautifulSoup(res)
        soup = soup.find('div', {'class': 'note', 'id': 'link-report'})
        content = soup.getText()
        content = content.replace('[/img]', '[/img]\n').replace('[img]', '\n[img]')
        h = HTMLParser.HTMLParser()
        content = h.unescape(content).encode('utf8')
        content = self.__replaceImgs(content)
        message = self.__message(content, 'http://thing.douban.com/', name)
        return subject + ' | ' + name , message
    
    def __zhihu(self):
        name = '知乎日报'
        req = urllib2.Request(url = self.url, headers = self.__headers)
        res = urllib2.urlopen(req).read()
        res = res.replace('<img class="content-image" src="', '\n[img]')
        res = res.replace('" alt="" />', '[/img]\n')
        res = res.replace('<strong>', '[b]').replace('</strong>', '[/b]')
        res = res.replace('<ul>', '[list]').replace('</ul>', '[/list]')
        res = res.replace('<ol>', '[list=1]').replace('</ol>', '[/list]')
        res = res.replace('<li>', '[*]').replace('</li>', '')
        res = res.replace('<p>', '').replace('</p>', '\n')
        res = res.replace('<br />', '\n')
        res = res.replace('\r', '').replace('\n\n', '\n')
        soup = BeautifulSoup(res)
        subject = soup.find('h1', {'class': 'headline-title'}).getText().encode('utf8')
        content = soup.find('div', {'class': 'content'}).getText()
        h = HTMLParser.HTMLParser()
        content = h.unescape(content).encode('utf8')
        content = self.__replaceImgs(content)
        message = self.__message(content, 'http://daily.zhihu.com/', name)
        return subject + ' | ' + name , message
    
    def __jiandan(self):
        name = '煎蛋'
        req = urllib2.Request(url = self.url, headers = self.__headers)
        res = urllib2.urlopen(req).read()
        subject = re.search(r'<title>(.*)</title>', res).groups()[0]
        res = res.replace('<img src="', '[img]').replace('" alt="' + subject + '" />', '[/img]')
        res = res.replace('<strong>', '[b]').replace('</strong>', '[/b]')
        res = res.replace('<br />', '\n')
        res = res.replace('\r', '').replace('\n\n', '\n')
        soup = BeautifulSoup(res)
        soup = soup.find('div', {'class': 'post f'}).findAll('p')
        content = ''
        for p in soup[:-1]:
            content += p.getText().encode('utf8') + '\n'
        content = self.__replaceImgs(content)
        message = self.__message(content, 'http://jandan.net/', name)
        return subject + ' | ' + name , message
    def collect(self):
        if self.target == 'one':
                return self.__one()
        elif self.target == 'douban':
                return self.__douban()
        elif self.target == 'zhihu':
                return self.__zhihu()
        elif self.target == 'jiandan':
                return self.__jiandan()
        else :
            print('Target is not existed!')
            return None
