# coding:utf-8
import base64
import json
import traceback

from config import QQWRY_PATH, CHINA_AREA
from util.IPAddress import IPAddresss
import re
from util.compatibility import text_

from lxml import etree


class Html_Parser(object):
    def __init__(self):
        self.ips = IPAddresss(QQWRY_PATH)

    def parse(self, response, parser):
        '''

        :param response: 响应
        :param type: 解析方式
        :return:
        '''
        if parser['type'] == 'xpath':
            return self.XpathPraser(response, parser)
        elif parser['type'] == 'regular':
            return self.RegularPraser(response, parser)
        elif parser['type'] == 'module':
            return getattr(self, parser['moduleName'], None)(response, parser)
        elif parser['type'] == 'json':
            return self.json_Praser(response, parser)
        # elif parser['type'] == 'xmlList':
        #     return self.xmlList_Praser(response, parser)
        # elif parser['type'] == 'txtList':
        #     return self.txtList_Praser(response, parser)
        else:
            return None

    def AuthCountry(self, addr):
        '''
        用来判断地址是哪个国家的
        :param addr:
        :return:
        '''
        for area in CHINA_AREA:
            if text_(area) in addr:
                return True
        return False

    def XpathPraser(self, response, parser):
        '''
        针对xpath方式进行解析
        :param response:
        :param parser:
        :return:
        '''
        proxylist = []
        try:
            root = etree.HTML(response)
        except:
            root = etree.HTML(bytes(bytearray(response, encoding='utf-8')))

        proxys = root.xpath(parser['pattern'])
        for proxy in proxys:
            try:
                ip = proxy.xpath(parser['position']['ip'])[0].text
                port = proxy.xpath(parser['position']['port'])[0].text
                type = 0
                protocol = 0
                addr = self.ips.getIpAddr(self.ips.str2ip(ip.strip()))
                country = text_('')
                area = text_('')
                if text_('省') in addr or self.AuthCountry(addr):
                    country = text_('国内')
                    area = addr
                else:
                    country = text_('国外')
                    area = addr

            except Exception as e:
                exstr = traceback.format_exc()
                # print(f'{111}\n 异常堆栈1:{e}, 异常信息:{exstr}')
                continue

            # updatetime = datetime.datetime.now()
            # ip，端口，类型(0高匿名，1透明)，protocol(0 http,1 https http),country(国家),area(省市),updatetime(更新时间)
            # proxy ={'ip':ip,'port':int(port),'type':int(type),'protocol':int(protocol),'country':country,'area':area,'updatetime':updatetime,'speed':100}
            proxy = {
                'ip': ip.strip(),
                'port': int(port.strip()),
                'types': int(type),
                'protocol': int(protocol),
                'country': country,
                'area': area,
                'speed': 0,
            }
            # print('XpathPraser ', proxy)
            proxylist.append(proxy)
        return proxylist

    def json_Praser(self, response, parser):
        '''
        针对json方式进行解析
        :param response:
        :param parser:
        :return:
        '''
        proxylist = []
        # print(json.loads(response))
        # json.loads(r.text)
        datas = json.loads(response).get('data', -1)
        if datas == -1:
            datas = json.loads(response)['RESULT']
            for data in datas:
                ip = data['ip']
                port = data['port']
                type = 0
                protocol = 0
                addr = self.ips.getIpAddr(self.ips.str2ip(ip))
                country = text_('')
                area = text_('')
                if text_('省') in addr or self.AuthCountry(addr):
                    country = text_('国内')
                    area = addr
                else:
                    country = text_('国外')
                    area = addr

                proxy = {
                    'ip': ip,
                    'port': int(port),
                    'types': int(type),
                    'protocol': int(protocol),
                    'country': country,
                    'area': area,
                    'speed': 0,
                }
                proxylist.append(proxy)
        else:
            for data in datas:
                ip, port = data['ip'].split(':')
                type = 0
                protocol = 0
                addr = self.ips.getIpAddr(self.ips.str2ip(ip))
                country = text_('')
                area = text_('')
                if text_('省') in addr or self.AuthCountry(addr):
                    country = text_('国内')
                    area = addr
                else:
                    country = text_('国外')
                    area = addr

                proxy = {
                    'ip': ip,
                    'port': int(port),
                    'types': int(type),
                    'protocol': int(protocol),
                    'country': country,
                    'area': area,
                    'speed': 0,
                }
                proxylist.append(proxy)
        return proxylist

    def xmlList_Praser(self, response, parser):
        '''
        针对json方式进行解析
        :param response:
        :param parser:
        :return:
        '''
        proxylist = []

        datas = response.split('\n')
        for data in datas:
            if data:
                data = json.loads(data)
                ip = data['host']
                port = data['port']
                type = 0
                protocol = 0
                addr = self.ips.getIpAddr(self.ips.str2ip(ip))
                country = text_('')
                area = text_('')
                if text_('省') in addr or self.AuthCountry(addr):
                    country = text_('国内')
                    area = addr
                else:
                    country = text_('国外')
                    area = addr

                proxy = {
                    'ip': ip,
                    'port': int(port),
                    'types': int(type),
                    'protocol': int(protocol),
                    'country': country,
                    'area': area,
                    'speed': 0,
                }
                proxylist.append(proxy)

        return proxylist

    def txtList_Praser(self, response, parser):
        '''
        针对json方式进行解析
        :param response:
        :param parser:
        :return:
        '''
        proxylist = []

        datas = response.split('\n')
        for data in datas:
            if data:
                ip, port = data.split(':')
                type = 0
                protocol = 0
                addr = self.ips.getIpAddr(self.ips.str2ip(ip))
                country = text_('')
                area = text_('')
                if text_('省') in addr or self.AuthCountry(addr):
                    country = text_('国内')
                    area = addr
                else:
                    country = text_('国外')
                    area = addr

                proxy = {
                    'ip': ip,
                    'port': int(port),
                    'types': int(type),
                    'protocol': int(protocol),
                    'country': country,
                    'area': area,
                    'speed': 0,
                }
                proxylist.append(proxy)

        return proxylist

    def RegularPraser(self, response, parser):
        '''
        针对正则表达式进行解析
        :param response:
        :param parser:
        :return:
        '''
        proxylist = []
        pattern = re.compile(parser['pattern'])
        matchs = pattern.findall(response)
        if matchs != None:
            for match in matchs:
                try:
                    ip = match[parser['position']['ip']]
                    port = match[parser['position']['port']]
                    # 网站的类型一直不靠谱所以还是默认，之后会检测
                    type = 0
                    # if parser['postion']['protocol'] > 0:
                    # protocol = match[parser['postion']['protocol']]
                    # if protocol.lower().find('https')!=-1:
                    #         protocol = 1
                    #     else:
                    #         protocol = 0
                    # else:
                    protocol = 0
                    addr = self.ips.getIpAddr(self.ips.str2ip(ip))
                    country = text_('')
                    area = text_('')
                    # print(ip,port)
                    if text_('省') in addr or self.AuthCountry(addr):
                        country = text_('国内')
                        area = addr
                    else:
                        country = text_('国外')
                        area = addr
                except Exception as e:
                    continue

                proxy = {
                    'ip': ip,
                    'port': port,
                    'types': type,
                    'protocol': protocol,
                    'country': country,
                    'area': area,
                    'speed': 100,
                }

                proxylist.append(proxy)
            return proxylist


    def CnproxyPraser(self, response, parser):
        proxylist = self.RegularPraser(response, parser)
        chardict = {
            'v': '3',
            'm': '4',
            'a': '2',
            'l': '9',
            'q': '0',
            'b': '5',
            'i': '7',
            'w': '6',
            'r': '8',
            'c': '1',
        }

        for proxy in proxylist:
            port = proxy['port']
            new_port = ''
            for i in range(len(port)):
                if port[i] != '+':
                    new_port += chardict[port[i]]
            new_port = int(new_port)
            proxy['port'] = new_port
        return proxylist

    def proxy_listPraser(self, response, parser):
        proxylist = []
        pattern = re.compile(parser['pattern'])
        matchs = pattern.findall(response)
        if matchs:
            for match in matchs:
                try:
                    ip_port = base64.b64decode(
                        match.replace("Proxy('", "").replace("')", "")
                    )
                    ip = ip_port.split(':')[0]
                    port = ip_port.split(':')[1]
                    type = 0
                    protocol = 0
                    addr = self.ips.getIpAddr(self.ips.str2ip(ip))
                    country = text_('')
                    area = text_('')
                    if text_('省') in addr or self.AuthCountry(addr):
                        country = text_('国内')
                        area = addr
                    else:
                        country = text_('国外')
                        area = addr
                except Exception as e:
                    continue
                proxy = {
                    'ip': ip,
                    'port': int(port),
                    'types': type,
                    'protocol': protocol,
                    'country': country,
                    'area': area,
                    'speed': 100,
                }
                proxylist.append(proxy)
            return proxylist

    def plus_listPraser(self, response, parser):
        proxylist = []
        pattern = re.compile(parser['pattern'])
        matchs = pattern.findall(response)
        if matchs:
            for match in matchs:
                try:
                    ip_port = ':'.join(match)
                    ip = ip_port.split(':')[0]
                    port = ip_port.split(':')[1]
                    type = 0
                    protocol = 0
                    addr = self.ips.getIpAddr(self.ips.str2ip(ip))
                    country = text_('')
                    area = text_('')

                    if text_('省') in addr or self.AuthCountry(addr):
                        country = text_('国内')
                        area = addr
                    else:
                        country = text_('国外')
                        area = addr
                except Exception as e:
                    continue
                proxy = {
                    'ip': ip,
                    'port': int(port),
                    'types': type,
                    'protocol': protocol,
                    'country': country,
                    'area': area,
                    'speed': 100,
                }
                proxylist.append(proxy)
            return proxylist
