# -*- coding: utf-8 -*-

import time
from Domain import Domain
from AutoBBS import AutoBBS
from LocalDB import LocalDB
from UrlFIFO import UrlFIFO
from Spider import UrlSpider, ContSpider

hour = int(time.strftime('%H',time.localtime(time.time())))
domain = Domain(hostname = 'bbs.uestc.edu.cn')
autobbs = AutoBBS(domain = domain, userName = 'xxoo', passWord = 'ooxx')
autobbs.login()
path = '.'
localdb = LocalDB(path + '/dbpath', 1000)
urlfifo = UrlFIFO(path + '/fifo')

if hour == 2 or hour == 4 or hour == 6:
    res = []
    for select in ['one', 'zhihu', 'douban', 'jiandan']:
        urlspider = UrlSpider(select)
        res += urlspider.collect()
    for r in res:
        if localdb.isExist(r) == False:
            localdb.push(r)
            urlfifo.put(r)
if hour >= 7 and hour <= 23:
    url = urlfifo.get()
    if url != 'no_url':
        contspider = ContSpider(url)
        sub, msg = contspider.collect()
        autobbs.new('25', sub, msg)
