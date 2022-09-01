import requests
from bs4 import BeautifulSoup
import time
# from database import db, cursor
import mysql.connector
import re
import binascii
from datetime import datetime, date

config = {
    'user' : 'root',
    'password': 'Seoseoseo7!',
    'host':'localhost',
    # 'database':'shit',
    'port':'3306'
}

db = mysql.connector.connect(**config)
cursor = db.cursor()


cursor.execute(
    """
    select min(time0) from dangbun_stuffs.naver
    """
)
min_time = cursor.fetchall()[0][0] or datetime(2022,1,1)

if min_time.date() != datetime.today().date():

    cursor.execute(
        """
        drop table if exists dangbun_stuffs.naver;
        """
    )
else:
    pass


# cursor.execute(
#     """
#     truncate dangbun_stuffs.naver;
#     """
# )

cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS dangbun_stuffs.naver(
        num int not null auto_increment,
        ind varchar(30),
        time0 timestamp,
        title blob,
        press varchar(30),
        url varchar(200),
        naver_cp boolean,
        good boolean,
        sokbo boolean,
        writen boolean default False,
        primary key(num, ind)
        );
        """
    )


page = 0
download = True
dics = {}
num = 1

# while download==True:
for _ in range(3):
    url =f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%5B%EB%8B%A8%EB%8F%85%5D%20%7C%20%5B%EC%86%8D%EB%B3%B4%5D&sort=1&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:all,a:all&start={page}1'

    data = {
        'where': 'news',
'sm': 'tab_pge',
'query': '[단독] | [속보]',
'sort': '1',
'photo': '0',
'field': '0',
'pd': '0',
'ds': '',
'de': '',
'mynews': '0',
'office_type': '0',
'office_section_code': '0',
'news_office_checked':  '',
'nso': 'so:dd,p:all,a:all',
'start': page*10 + 1
    }

    temp = requests.get(url)
    temp = BeautifulSoup(temp.content, 'html.parser')
    # print(temp)

    news_areas = temp.find_all('div', {'class':'news_area'})

    for news_area in news_areas:

        infos = news_area.find_all('a', class_='info')
        info_list = []
        for info in infos:
            if 'press' in info['class']:
                press = info.text.replace('언론사 선정','')
            else:
                info_list.append(info)

        naver_cp =  True if info_list != [] else False

        link = info_list[0]['href'] if naver_cp else None

        tit = news_area.find('a',class_='news_tit')['title']
        # tit_bin = bin(int(binascii.hexlify(tit.encode('utf-8')), 16))[2:]
        print(press)
        print(link)
        print(tit)
        ind = news_area.find('a',class_='news_tit')['onclick']
        ind = re.sub(r'.*g=\d*\.','',ind)
        ind = re.sub(r'&u=.*','',ind)
        print(ind)
        ind = int(ind)
        print("======================")


        good = True if "[단독]" in tit else False
        sokbo = True if "[속보]" in tit else False
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print(press)
        # print(link)
        # print(tit)
        # cursor.execute(
        #     f"""
        #     insert into dangbun_stuffs.naver values ( NULL, "{ind}", "{now}" , "{tit_bin}", "{press}", "{link}", {naver_cp}, {good}
        #     )
        #     """
        # )

        dics[num]= {'ind':ind, 'time0':now, 'tit':tit, 'press' : press, 'link':link, 'naver_cp':naver_cp, 'good':good, 'sokbo':sokbo}
        num +=1
    db.commit()
    print(f"{page}")
    page +=1
    download = False
    if page <3:
        time.sleep(5)

####mysql 입력구간 ###
# print(dics.values())
for article in list(dics.values())[::-1]:
    # print(article)
    ind = article['ind']
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tit = article['tit']
    tit_bin = bin(int(binascii.hexlify(tit.encode('utf-8')), 16))[2:]
    press = article['press']
    link = article['link']
    naver_cp = article['naver_cp']
    good = article['good']
    sokbo = article['sokbo']
    cursor.execute(
        f"""
        insert into dangbun_stuffs.naver values ( NULL, "{ind}", "{now}" , b'{tit_bin}', "{press}", "{link}", {naver_cp}, {good}, {sokbo}, False
        )
        """
    )
db.commit()