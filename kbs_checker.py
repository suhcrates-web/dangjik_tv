import requests, re, json
from bs4 import BeautifulSoup
from ast import literal_eval
from datetime import date, timedelta

def kbs_checker():
    result_txt = ''
    url = 'https://news.kbs.co.kr/api/getNewsList'

    data ={
    'currentPageNo': '1',
    'rowsPerPage': '50',
    'exceptPhotoYn': 'Y',
    'broadCode': '0001',
    'broadDate': f'{date.today().strftime("%Y%m%d") }',
    'needReporterInfo': 'Y',
    'orderBy': 'broadDate_desc,broadOrder_asc'
    }
    temp = requests.post(url, data = data)

    # temp = BeautifulSoup(temp.content, 'html.parser')
    temp = temp.content.decode('utf-8')
    temp = json.loads(temp)



    items = temp['data']   # kbs 는 json 안에 기사 전문이 들어있음.
    if items == []:
        # pass
        return "<br>오늘자 안 나옴<br><br>"

    item_dics = {}
    dan_n = 0
    n = 1
    for item in items:
        item_dics[n] = {}
        item_dics[n]['tit'] = item['newsTitle']
        item_dics[n]['content'] = item['newsContents']

        if '[단독]' in item_dics[n]['tit']:
            dan_n += 1
        n += 1


    result_txt += f"@KBS 9시뉴스 (단독 {dan_n}건)<br><br>"
    for item in item_dics.values():
        tit = item['tit']
        result_txt += f"-{tit}<br>"
        if '[단독]' in tit:
            result_txt += item['content'] + '<br>'

    result_txt = '<br>' + result_txt + '<br>'

    return result_txt