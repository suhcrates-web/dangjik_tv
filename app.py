from flask import Flask, render_template, url_for, request, redirect, jsonify
from datetime import datetime, timedelta
from jonghap import jonghap
from database import cursor, db
from mbc_checker import mbc_checker
from jtbc_checker import jtbc_checker
from tvchosun_checker import tvchosun_checker
from mbn_checker import mbn_checker
from kbs_checker import kbs_checker
from sbs_checker import sbs_checker
from sql_toolbox import time_checker
import binascii, codecs

checkers_dic = {'mbc': mbc_checker,
                'jtbc':jtbc_checker,
                'tvchosun':tvchosun_checker,
                'mbn':mbn_checker,
                'kbs':kbs_checker,
                'sbs':sbs_checker}

app = Flask(__name__)


@app.route(f'/donga/dangbun/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route(f'/donga/dangbun/<brod>/', methods=['GET'])
def index_brod(brod):
    cursor.execute(
        f"""
        select date0, content from dangbun_stuffs.brods where brod = "{brod}" 
        """
    )

    date0, content = cursor.fetchall()[0]
    date0 = date0.strftime("%Y년 %m월 %d일 // %H시 %M분")
    article = codecs.decode(content, 'utf-8')

    return render_template('sihwang.html', article=article, now=date0, id_0='asdf', state='asdf', state_m='asdf', brod= brod)



@app.route('/donga/dangbun/<brod>/post', methods=['POST'])
def si_post(brod):
    if request.method == 'POST':


        cmd = request.form['cmd']
        state = request.form['state']
        version = request.form['version']
        if state == '2':
            magam = True
        else:
            magam = False

        if cmd == 'giveme':
            if version == '1':
                jong_time = 'jonghap_time'
            elif version == '2':
                jong_time = 'jonghap_time2'

            now = datetime.today()
            ago = time_checker(brod) or (now- timedelta(minutes=3))
            # ago = datetime.strptime(ago, '%Y-%m-%d %H:%M:%S')
            if (now - ago) < timedelta(minutes=2):  # 2분미만
                message = "다른 사람이 생성중이거나 최근 생성 2분 미만입니다…좀만 기다려보세요"
                cmd = 'not_yet'
                time = ''
            else:

                message = checkers_dic[brod]()
                cursor.execute(
                    f"""update dangbun_stuffs.brods set date0 = "{now}" where brod="{brod}" """
                )
                cursor.execute(
                    f"""update dangbun_stuffs.brods set content = b'{bin(int(binascii.hexlify(message.encode('utf-8')), 16))[2:]}' where brod="{brod}" """
                )
                db.commit()
                cmd = 'ok'

        return {"message": message, "cmd": cmd, "time": now.strftime("%Y년 %m월 %d일 // %H시 %M분")}



#잘못들어갈때
@app.route(f'/donga/dangbun/naver/', methods=['GET'])
def index():
    return redirect('http://testbot.ddns.net:5235/donga/dangbun/naver/only')



if __name__ == "__main__":
    # serve(app, host = '0.0.0.0', port = '3389', threads=1)
    with open('C:/stamp/port.txt', 'r') as f:
        port = f.read().split(',')[0]  # 노트북 5232, 데스크탑 5231
        # port = port[0]
    # print(port)
    # host = '0.0.0.0'
    if port == '5232':
        host = '172.30.1.58'
        host = '0.0.0.0'

    elif port == '5231':
        port = '5234'
        host = '0.0.0.0'
    # port = 5233
    # 172.30.1.53
    # 0.0.0.0
    app.run(host=host, port=port, debug=True)
