# -*- coding: utf-8 -*-
# @Time    : 2022/5/8 12:36
# @Author  : huni
# @Email   : zcshiyonghao@163.com
# @File    : main.py
# @Software: PyCharm
import re
import json
from fastapi import FastAPI,Form,Request
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/h")
def getdate(request: Request):
    return templates.TemplateResponse('header_before.html',context = {'request':request})


@app.post("/h")
def turn(request: Request,data: str = Form(...)):
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
    return templates.TemplateResponse('output.html',context = {'request':request,'output':output})

@app.get("/c")
def getdate(request: Request):
    return templates.TemplateResponse('cookie_before.html',context = {'request':request})


@app.post("/c")
def turn(request: Request,data: str = Form(...)):
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
    return templates.TemplateResponse('output.html',context = {'request':request,'output':output})

@app.get("/u")
def getdate(request: Request):
    return templates.TemplateResponse('unicode_before.html',context = {'request':request})


@app.post("/u")
def turn(request: Request,data: str = Form(...)):
    s = r'{}'.format(data)
    output = json.loads(f'"{s}"')
    return templates.TemplateResponse('output.html',context = {'request':request,'output':output})


if __name__ == '__main__':
    uvicorn.run('main:app', host = "0.0.0.0", port = 20225, reload = True)
