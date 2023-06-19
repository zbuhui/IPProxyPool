# coding:utf-8
from gevent import monkey
monkey.patch_all()

import sys
import time
import gevent

from gevent.pool import Pool
from multiprocessing import Queue, Process, Value
from api.apiServer import start_api_server
from config import THREADNUM, parserList, UPDATE_TIME, MINNUM, MAX_CHECK_CONCURRENT_PER_PROCESS, MAX_DOWNLOAD_CONCURRENT
from db.DataStore import store_data, sqlhelper
from spider.HtmlDownloader import Html_Downloader
from spider.HtmlPraser import Html_Parser
from validator.Validator import validator, getMyIP, detect_from_db


'''
这个类的作用是描述爬虫的逻辑
'''


def startProxyCrawl(queue, db_proxy_num, myip):
    crawl = ProxyCrawl(queue, db_proxy_num, myip)
    crawl.run()


class ProxyCrawl(object):
    proxies = set()

    def __init__(self, queue, db_proxy_num, myip):
        self.crawl_pool = Pool(THREADNUM) # 5
        self.queue = queue
        self.db_proxy_num = db_proxy_num # Value('i', 0)
        self.myip = myip


    def run(self):
        while True:
            self.proxies.clear()
            str = 'IPProxyPool----->beginning'
            sys.stdout.write(str + "\r\n")
            sys.stdout.flush()
            proxylist = sqlhelper.select() # 获取数据库中所有的ip

            spawns = []
            for proxy in proxylist:
                spawns.append(gevent.spawn(detect_from_db, self.myip, proxy, self.proxies))
                if len(spawns) >= MAX_CHECK_CONCURRENT_PER_PROCESS: # CHECK_PROXY时每个进程的最大并发
                    gevent.joinall(spawns)
                    spawns = []
            gevent.joinall(spawns)
            self.db_proxy_num.value = len(self.proxies)
            str = 'IPProxyPool----->db exists ip:%d' % len(self.proxies)

            if len(self.proxies) < MINNUM: # 当有效的ip值小于一个时 需要启动爬虫进行爬取
                str += '\r\nIPProxyPool----->>>>>>>>now ip num < MINNUM,start crawling...'
                sys.stdout.write(str + "\r\n")
                sys.stdout.flush()
                spawns = []
                for p in parserList:
                    # 带时间戳
                    if '{}' in p['urls'][0]:
                        import datetime
                        from datetime import timezone
                        tz = timezone(datetime.timedelta(hours=8))
                        timestamp = datetime.datetime.now(tz).strftime('%a %b %d %Y %H:%M:%S GMT%z (中国标准时间)')
                        p['urls'][0] = p['urls'][0].format(timestamp)
                    spawns.append(gevent.spawn(self.crawl, p))
                    if len(spawns) >= MAX_DOWNLOAD_CONCURRENT:
                        gevent.joinall(spawns)
                        spawns= []
                gevent.joinall(spawns)
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                str += '\r\nIPProxyPool----->>>>>>>>now ip num meet the requirement,wait UPDATE_TIME...'
                sys.stdout.write(str + "\r\n")
                sys.stdout.flush()
            print('sleep UPDATE_TIME')
            time.sleep(UPDATE_TIME)

    def crawl(self, parser):
        # print('spider start...')
        html_parser = Html_Parser()
        for url in parser['urls']:
            print('当前解析:',url)
            response = Html_Downloader.download(url)
            if response is not None:
                # print('开始解析...')
                proxylist = html_parser.parse(response, parser)
                # print('解析结果:',proxylist)
                if proxylist is not None:
                    for proxy in proxylist:
                        proxy_str = '%s:%s' % (proxy['ip'], proxy['port'])
                        if proxy_str not in self.proxies:
                            self.proxies.add(proxy_str)
                            while True:
                                if self.queue.full():
                                    time.sleep(0.2)
                                else:
                                    self.queue.put(proxy)
                                    break


if __name__ == "__main__":
    DB_PROXY_NUM = Value('i', 0)
    q1 = Queue()
    q2 = Queue()
    p0 = Process(target=start_api_server)
    p1 = Process(target=startProxyCrawl, args=(q1, DB_PROXY_NUM))
    p2 = Process(target=validator, args=(q1, q2))
    p3 = Process(target=store_data, args=(q2, DB_PROXY_NUM))

    p0.start()
    p1.start()
    p2.start()
    p3.start()

    # spider = ProxyCrawl()
    # spider.run()
