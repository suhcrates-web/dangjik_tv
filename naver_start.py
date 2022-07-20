from database import db, cursor
import requests
from bs4 import BeautifulSoup
import time
from database import db, cursor
import re
import binascii
from datetime import datetime

# cursor.execute(
#     """
#     drop table if exists dangbun_stuffs.naver;
#     """
# )
cursor.execute(
    """
    truncate dangbun_stuffs.naver;
    """
)

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

        ind = news_area.find('a',class_='news_tit')['onclick']
        ind = re.sub(r'.*g=\d*\.','',ind)
        ind = re.sub(r'&u=.*','',ind)
        ind = int(ind)


        good = True if "[단독]" in tit or "[속보]" in tit else False
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(press)
        print(link)
        print(tit)
        # cursor.execute(
        #     f"""
        #     insert into dangbun_stuffs.naver values ( NULL, "{ind}", "{now}" , "{tit_bin}", "{press}", "{link}", {naver_cp}, {good}
        #     )
        #     """
        # )

        dics[num]= {'ind':ind, 'time0':now, 'tit':tit, 'press' : press, 'link':link, 'naver_cp':naver_cp, 'good':good}
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
    cursor.execute(
        f"""
        insert into dangbun_stuffs.naver values ( NULL, "{ind}", "{now}" , b'{tit_bin}', "{press}", "{link}", {naver_cp}, {good}
        )
        """
    )
db.commit()