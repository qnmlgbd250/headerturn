# -*- coding: utf-8 -*-
# @Time    : 2022/5/8 15:19
# @Author  : huni
# @Email   : zcshiyonghao@163.com
# @File    : 11111111111.py
# @Software: PyCharm
import re

headers = """accept: */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
origin: https://www.bilibili.com
referer: https://www.bilibili.com/
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="101", "Microsoft Edge";v="101"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-site
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39

"""

pattern = '^(.*?): (.*?)$'
f = '{'
for line in headers.splitlines():  # 反向引用
    f += re.sub(pattern, '\'\\1\': \'\\2\',', line)
f += "}"
print(f, type(f))

