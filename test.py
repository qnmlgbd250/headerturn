# -*- coding: utf-8 -*-
# @Time    : 2022/5/25 21:13
# @Author  : huni
# @Email   : zcshiyonghao@163.com
# @File    : test.py
# @Software: PyCharm
# import re
#
# s = '''accept-encoding: gzip, deflate, br
# accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
# cookie: buvid3=D1AA6BE3-40D6-BF4D-4494-4D70B80DADFA86367infoc; i-wanna-go-back=-1; _uuid=A1012C47E-7C95-19A4-10473-578D7E36B9BD86965infoc; buvid4=A54765BF-039D-BBA4-875C-F32749CBEEC689313-022050312-IqFDZutdi3vuh8dgtqypSw%3D%3D; sid=9hmrbcc4; fingerprint=9e85a8411db3d8474b9133c61de9c69c; buvid_fp_plain=undefined; DedeUserID=91384060; DedeUserID__ckMd5=7e0b00d6b02226e9; SESSDATA=01fe9e9d%2C1667105406%2Ca90dc*51; bili_jct=6be285e04d28db4511d9a416af7a5694; buvid_fp=6f3ed06e237d728c432c361475458bed; rpdid=|(u)~Y)Yl)R)0J'uYlullJRum; LIVE_BUVID=AUTO7216515534356996; b_ut=5; CURRENT_BLACKGAP=0; hit-dyn-v2=1; nostalgia_conf=-1; CURRENT_QUALITY=80; PVID=1; blackside_state=0; bp_video_offset_91384060=663450891124211800; b_lsid=A5F8D1C3_180FB1C1D48; b_timer=%7B%22ffp%22%3A%7B%22333.1007.fp.risk_D1AA6BE3%22%3A%22180FB1C1F6D%22%2C%22444.41.fp.risk_D1AA6BE3%22%3A%22180FB1C2EBF%22%2C%22333.788.fp.risk_D1AA6BE3%22%3A%22180FB1C4045%22%7D%7D; CURRENT_FNVAL=80; innersign=0
# referer: https://www.bilibili.com/
# sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="101", "Microsoft Edge";v="101"
# sec-ch-ua-mobile: ?0
# sec-ch-ua-platform: "Windows"
# sec-fetch-dest: script
# sec-fetch-mode: no-cors
# sec-fetch-site: same-origin
# user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53'''
#
# pattern = '^(.*?)=(.*?)$' if len(re.findall('(.*?)=(.*?)',s)) >= len(re.findall('(.*?): (.*?)',s)) else '^(.*?): (.*?)$'
# headers = '{'
# headers += '\n'
# for line in s.split('; '):
#     headers += '\t'
#     headers += re.sub(pattern, '\'\\1\': \'\\2\',', line)
#     headers += '\n'
# headers += "}"
# headers = headers.replace(",}", '}')
#
# print(headers)

s = str(r'\u4e24\u6b21\u8f93\u5165\u7684\u5bc6\u7801\u4e0d\u4e00\u81f4')
import json
print(json.loads(f'"{s}"'))
