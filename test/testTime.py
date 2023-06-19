import datetime
import json
from datetime import timezone

# 设置时区为中国标准时间
import requests

tz = timezone(datetime.timedelta(hours=8))

# 获取当前时间并转换为指定时区
now = datetime.datetime.now(tz)

# 格式化时间戳，包含时区偏移量和"中国标准时间"
timestamp = now.strftime('%a %b %d %Y %H:%M:%S GMT%z (中国标准时间)')

# print(timestamp)

url = f'https://www.docip.net/data/free.json?t={timestamp}'

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'Hm_lvt_b404b9b1dcf7fb4fa7057cf1e34f6bf8=1686805189; Hm_lpvt_b404b9b1dcf7fb4fa7057cf1e34f6bf8=1686806408',
    'DNT': '1',
    'Host': 'www.docip.net',
    'Pragma': 'no-cache',
    'Referer': 'https://www.docip.net/',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    # 'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
}

r = requests.get(url, headers=headers)
r.text
print(r.json())
# ip_port = r.json()['data'][0]['ip']
