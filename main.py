# -*- coding: utf-8 -*-
# @Time    : 2022/5/8 12:36
# @Author  : huni
# @Email   : zcshiyonghao@163.com
# @File    : main.py
# @Software: PyCharm
import re
import json
import rsa, base64
import requests
from fastapi import FastAPI, Form, Request
import uvicorn
import lzstring
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory = "static"), name = "static")
templates = Jinja2Templates(directory="templates")


@app.get("/h" ,response_class=HTMLResponse)
def getdate(request: Request):
    return templates.TemplateResponse('header_before.html', context = {'request': request})


@app.post("/h")
def turn(request: Request, data: str = Form(...)):
    s = f'''{data}'''
    pattern = '^(.*?): (.*?)$'
    output = '{'
    output += '\n'
    for line in s.splitlines():
        output += '\t'
        output += re.sub(pattern, '\'\\1\': \'\\2\',', line)
        output += '\n'
    output += "}"
    output = output.replace(",}", '}')
    return templates.TemplateResponse('output.html', context = {'request': request, 'output': output})


@app.get("/c")
def getdate(request: Request):
    return templates.TemplateResponse('cookie_before.html', context = {'request': request})


@app.post("/c")
def turn(request: Request, data: str = Form(...)):
    s = f'''{data}'''
    pattern = '^(.*?)=(.*?)$'
    output = '{'
    output += '\n'
    for line in s.split('; '):
        output += '\t'
        output += re.sub(pattern, '\'\\1\': \'\\2\',', line)
        output += '\n'
    output += "}"
    output = output.replace(",}", '}')
    return templates.TemplateResponse('output.html', context = {'request': request, 'output': output})


@app.get("/u")
def getdate(request: Request):
    return templates.TemplateResponse('unicode_before.html', context = {'request': request})


@app.post("/u")
def turn(request: Request, data: str = Form(...)):
    try:
        data = data.replace(r'\\', '\\')
        s = r'{}'.format(data)
        output = json.loads(f'"{s}"')
        return templates.TemplateResponse('output.html', context = {'request': request, 'output': output})
    except:
        return templates.TemplateResponse('output.html', context = {'request': request, 'output': '输入错误'})


@app.get("/p")
def getdate(request: Request):
    return templates.TemplateResponse('pwd_before.html', context = {'request': request})

@app.post("/p")
def turn(request: Request, data: str = Form(...)):
    _PRIVATE_KEY_PATH = 'static/rsa_private_key.pem'
    # privkey 直接放到内存
    with open(_PRIVATE_KEY_PATH, mode = 'rb') as f:
        _privkey = rsa.PrivateKey.load_pkcs1(f.read())
    try:
        data = data.replace(' ', '+')
        try:
            if type(data) == str: data = base64.b64decode(data)
            message = rsa.decrypt(data, _privkey)
        except rsa.pkcs1.DecryptionError:
            output = ''
        else:
            output = message.decode('utf-8')
        return templates.TemplateResponse('output.html', context = {'request': request, 'output': output})
    except:
        return templates.TemplateResponse('output.html', context = {'request': request, 'output': '输入错误'})



@app.get("/d")
def getdate(request: Request):
    return templates.TemplateResponse('data_before.html', context = {'request': request})

@app.post("/d")
def turn(request: Request, data: str = Form(...)):
    try:
        data = data.strip()
        rule_json = 'static/rule.json'
        with open(rule_json, mode='rb') as f:
            rule_json_list = f.read()
            rule_json_list = json.loads(rule_json_list)

        proxies ={
              "http": None,
              "https": None,
            }
        param = {
            'taskId': data
        }
        resp = {}
        if data.startswith('1'):

            resp = requests.get('https://mtax.kdzwy.com/taxtask/api/task/history', params=param, proxies=proxies).json()
            if not resp['data'].get('defaultRule'):
                resp['data']['defaultRule'] = rule_json_list
            if resp.get('code') in [301]:
                resp = requests.get('https://test1.kdzwy.com/taxtask/api/task/history', params=param, proxies=proxies).json()
                if not resp['data'].get('defaultRule'):
                    resp['data']['defaultRule'] = rule_json_list
        elif data.startswith('3'):
            resp = requests.get('https://tax.kdzwy.com/taxtask/api/task/history', params=param, proxies=proxies).json()
        else:
            pass
    except Exception as e:
        output = str(e)
    else:
        output = json.dumps(resp.get('data'), ensure_ascii=False) if (resp.get('code') == 200 and resp.get('msg') == 'success') else {}
    return templates.TemplateResponse('output.html', context={'request': request, 'output': output})

@app.get("/l")
def getdate(request: Request):
    return templates.TemplateResponse('lz_before.html', context = {'request': request})

@app.post("/l")
def turn(request: Request, data: str = Form(...)):
    try:
        output = lzstring.LZString().decompressFromBase64(data)

    except:
        output = {}

    return templates.TemplateResponse('output.html', context={'request': request, 'output': output})


@app.get("/t")
def getdate(request: Request):
    return templates.TemplateResponse('fy_before.html', context = {'request': request})

@app.post("/t")
def turn(request: Request, data: str = Form(...)):
    try:
        trans_type = 'auto2zh'
        zh = re.findall('[\u4e00-\u9fa5]', data)
        if zh:
            trans_type = 'auto2en'
        url = "http://api.interpreter.caiyunai.com/v1/translator"
        token = "s18sjx2ek2pl83j7861p"
        payload = {
            "source": data,
            "trans_type": trans_type,
            "request_id": "demo",
            "detect": True,
        }
        headers = {
            "content-type": "application/json",
            "x-authorization": "token " + token,
        }
        response = requests.request("POST", url, data = json.dumps(payload), headers = headers)
        output = json.loads(response.text)["target"]
    except:
        output = {}

    return templates.TemplateResponse('output.html', context={'request': request, 'output': output})




if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=20226, reload=True)
