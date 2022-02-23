import os
import requests
from requests_toolbelt.downloadutils import stream

url = 'https://cvideo.yanhekt.cn/vod-lxx/2021/11/18/7341626/1/video1.mp4'
filepath = os.path.join('D:/Downloads/test1.mp4')

headers = {
    'Host': 'cvideo.yanhekt.cn',
    'Connection': 'close',
    'User-Agent': '',
    'Origin': 'https://www.yanhekt.cn',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'video',
    'Referer': 'https://www.yanhekt.cn/',
    'Range': 'bytes=0-',
}

proxies = {
    "http": None,
    "https": None,
}

res = requests.get(url, headers=headers, proxies=proxies, stream=True)

with open(filepath, 'wb') as fd:
    stream.stream_response_to_file(res, path=fd)
