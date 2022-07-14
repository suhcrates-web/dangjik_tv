

import requests, re
from bs4 import BeautifulSoup
from selenium_short import mbc_selenium_short,selenium_short
from datetime import date

# 단독기사 나올시 개별기사 추리기
def jtbc_article(url):
    temp = requests.get(url)
    temp = BeautifulSoup(temp.content, 'html.parser')
    # print(temp)
    articles = temp.findAll('div', {'class': 'article_content'})
    #
    txt = ''
    for article in articles:
        for br in article.find_all("br"):
            br.replace_with("\n")

        txt += article.text.strip()
        txt = txt.split('☞')[0]
        txt = txt.replace('\n', '<br>')
    return txt

def jtbc_checker():
    result_txt = ''
    url = 'https://news.jtbc.joins.com/Replay/news_replay.aspx?fcode=PR10000403'

    # temp = selenium_short(url)
    temp = requests.get(url)

    temp = BeautifulSoup(temp.content, 'html.parser')
    items = temp.find('div',{'class':'review_list'}).find('div',{'class':'bd'})


    items = items.findAll('li')
    item_dics = {}
    dan_n = 0
    n=1
    for item in items:
        item_dics[n] = {}
        item_dics[n]['tit'] = item.find('a',{'class':'title_cr'}).text
        item_dics[n]['link'] = item.find('a')['href']
        if '[단독]' in item_dics[n]['tit']:
            dan_n += 1
        n+=1


    result_txt +=f"@jtbc (단독 {dan_n}건)<br><br>"
    for item in item_dics.values():
        tit = item['tit']
        result_txt += f"-{tit}<br>"
        if '[단독]' in tit:
            result_txt += jtbc_article(item['link']) + '<br><br>'

    return result_txt
