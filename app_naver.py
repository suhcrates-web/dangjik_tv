from flask import Flask, render_template, url_for, request, redirect, jsonify
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from database import cursor, db
import binascii, codecs
import time
import mysql.connector
import requests
from giveme_lead import giveme_lead

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' ##
# db = SQLAlchemy(app)

@app.route('/donga/dangbun/naver/', methods=['get'])
def naver_check_0():
    return redirect('/donga/dangbun/naver/only')


@app.route('/donga/dangbun/naver/<what0>', methods=['get'])
def naver_check(what0):
    config = {
        'user': 'root',
        'password': 'Seoseoseo7!',
        'host': 'localhost',
        # 'database':'shit',
        'port': '3306'
    }

    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    objs = []
    if what0 == 'all':
        cursor.execute(
            """
            select time0, title, press, url, ind, writen, naver_cp from dangbun_stuffs.naver 
            """
            # and good = 1
        )
    elif what0 =='only' or '':
        cursor.execute(
            """
            select time0, title, press, url, ind, writen, naver_cp from dangbun_stuffs.naver where naver_cp = 1 and good = 1
            """
        )
    for article in cursor.fetchall()[::-1]:
        objs.append({
            'time0': article[0].strftime("%H:%M"),
            'title': codecs.decode(article[1], 'utf-8'),
            'press': article[2],
            'url': article[3],
            'ind': article[4],
            'writen': 'writen' if article[5] else 'None',
            'cp': article[6],
        })
    return render_template('bot_v3.html', objs=objs)


## 요약작성 ##
@app.route('/donga/dangbun/naver/write', methods = ['POST','GET'])
def write():
    if request.method == 'POST':
        url = request.form['url']
        press = request.form['press']
        title = request.form['title']
        ind = request.form['ind']
        lead = giveme_lead(url, press, ind)
        if '[속보]' in title:
            text = f"@{press}/{title} {url}"
        else:
            text = f"@{press}/{title} = {lead} {url}"
        return text


##실수로 들어왔을때 ##
@app.route('/donga/dangbun/', methods = ['POST','GET'])
def mistake_2_1():
    return redirect('http://testbot.ddns.net:5234/donga/dangbun/')


if __name__ == "__main__":
    # serve(app, host = '0.0.0.0', port = '3389', threads=1)
    with open('C:/stamp/port.txt', 'r') as f:
        port = f.read().split(',')[0]  # 노트북 5232, 데스크탑 5231
        # port = port[0]
    # print(port)
    # host = '0.0.0.0'
    if port == '5232':
        port ='5235'
        host = '172.30.1.58'
        host = '0.0.0.0'

    elif port == '5231':
        port = '5235'
        host = '0.0.0.0'
    # port = 5233
    # 172.30.1.53
    # 0.0.0.0
    app.run(host=host, port=port, debug=True)
