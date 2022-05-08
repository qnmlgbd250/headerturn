# -*- coding: utf-8 -*-
# @Time    : 2022/5/8 12:36
# @Author  : huni
# @Email   : zcshiyonghao@163.com
# @File    : main.py
# @Software: PyCharm
import re
from fastapi import FastAPI,Form,Request
import uvicorn
from fastapi.templating import Jinja2Templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")
@app.get("/")
def getdate(request: Request):
    return templates.TemplateResponse('before.html',context = {'request':request})


@app.post("/turn")
def turn(request: Request,data: str = Form(...)):
    s = f'''{data}'''
    pattern = '^(.*?): (.*?)$'
    headers = '{'
    for line in s.splitlines():
        headers += re.sub(pattern, '\'\\1\': \'\\2\',', line)
    headers += "}"
    return templates.TemplateResponse('after.html',context = {'request':request,'headers':headers})



if __name__ == '__main__':
    uvicorn.run('main:app', host = "localhost", port = 20225, reload = True)
