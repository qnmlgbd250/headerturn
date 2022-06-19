# -*- coding: utf-8 -*-
# @Time    : 2022/5/8 12:36
# @Author  : huni
# @Email   : zcshiyonghao@163.com
# @File    : main.py
# @Software: PyCharm
import re
import json
import rsa, base64
from fastapi import FastAPI, Form, Request
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))
app.mount("/static", StaticFiles(directory = "static"), name = "static")


@app.get("/h")
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
            print('[error]: Decryption failed')
            output = ''
        else:
            output = message.decode('utf-8')
        return templates.TemplateResponse('output.html', context = {'request': request, 'output': output})
    except:
        return templates.TemplateResponse('output.html', context = {'request': request, 'output': '输入错误'})


if __name__ == '__main__':
    uvicorn.run('main:app', host = "0.0.0.0", port = 20225, reload = True)
