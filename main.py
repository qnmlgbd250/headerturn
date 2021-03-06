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
        return templates.TemplateResponse('output.html', context = {'request': request, 'output': '????????????'})


@app.get("/p")
def getdate(request: Request):
    return templates.TemplateResponse('pwd_before.html', context = {'request': request})

@app.post("/p")
def turn(request: Request, data: str = Form(...)):
    _PRIVATE_KEY_PATH = 'static/rsa_private_key.pem'
    # privkey ??????????????????
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
        return templates.TemplateResponse('output.html', context = {'request': request, 'output': '????????????'})



@app.get("/d")
def getdate(request: Request):
    return templates.TemplateResponse('data_before.html', context = {'request': request})

@app.post("/d")
def turn(request: Request, data: str = Form(...)):
    try:
        param = {
            'taskId': data
        }
        resp = {}
        if data.startswith('1'):
            resp = requests.get('https://mtax.kdzwy.com/taxtask/api/task/history', params=param).json()
        elif data.startswith('3'):
            resp = requests.get('https://tax.kdzwy.com/taxtask/api/task/history', params=param).json()
        else:
            pass
    except Exception as e:
        output = str(e)
    else:
        output = json.dumps(resp.get('data'),ensure_ascii=False) if (resp.get('code') == 200 and resp.get('msg') == 'success') else {}
    return templates.TemplateResponse('output.html', context = {'request': request, 'output': output})





if __name__ == '__main__':
    uvicorn.run('main:app', host = "0.0.0.0", port = 20225, reload = True)
