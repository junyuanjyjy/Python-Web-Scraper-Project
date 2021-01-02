from flask import Flask
import bs4 as bs
import urllib.request
import requests
import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

@app.route("/")
def index():
    source = [urllib.request.urlopen('https://finance.yahoo.com/quote/%5EGSPC?p=%5EGSPC').read(), urllib.request.urlopen('https://finance.yahoo.com/quote/MYR=X?p=MYR=X&.tsrc=fin-srch').read(), urllib.request.urlopen('https://finance.yahoo.com/quote/%5EKLSE?p=^KLSE&.tsrc=fin-srch').read(), urllib.request.urlopen('https://finance.yahoo.com/quote/%5ETNX?p=%5ETNX').read()]
    v = []
    for i in source:
        x = bs.BeautifulSoup(i,'html5lib')
        v.append(x)

    clas = "div span[class='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)']"
    cla = "div span[class='Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)']"
    cla2 = "div span[class='Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)']"

    quotes = []
    movements = []
    title = ['SP500','USDMYR','FBMKLCI','US10YRYIELD']
    for i in source:
        x = bs.BeautifulSoup(i,'html5lib')
        quote = x.select(clas)[0].text
        quotes.append(quote)
        try:
            movement = x.select(cla)[0].text
        except:
            movement = x.select(cla2)[0].text
        movements.append(movement)
    return render_template("index.html",quotes=quotes,movements=movements,title=title,len=len(title))

@app.route("/news")
def news():
    s = requests.get('http://www.theedgemarkets.com')
    source = s.text
    q = 'http://www.theedgemarkets.com'
    edge = bs.BeautifulSoup(source,'html5lib')
    head =[]
    yu = []
    stop = ['\n\n','\n\n(Updated)\n']
    for link in edge.find_all('div', class_='post-title'):
        head.append(link.text)
        for k in link.find_all('a'):
            yu.append(q + k['href'])
    head = head[1:]
    head = [word for word in head if word not in stop]
    return render_template("news.html",head=head,yu=yu,len=10)
