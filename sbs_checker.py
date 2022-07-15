import requests, re
from bs4 import BeautifulSoup
from selenium_short import mbc_selenium_short
from datetime import date


# 단독기사 나올시 개별기사 추리기
def sbs_article(url):
    temp = requests.get(url)
    temp = BeautifulSoup(temp.content, 'html.parser')

    article = temp.find('div', {'class': 'text_area'})
    txt = ''
    for br in article.find_all("br"):
        br.replace_with("\n")
    # print(article)
    txt = article.text.strip()
    txt = txt[:txt.find('(영상취재')+10]
    txt = txt.replace('\n', '<br>').replace('<br> ', '')
    return txt


def sbs_checker():
    result_txt = ''
    url = 'https://news.sbs.co.kr/news/programMain.do'
    temp = requests.get(url)

    temp = BeautifulSoup(temp.content, 'html.parser')

    items = temp.find('ul', {'class': 'snmd_vp_list'}).find_all('li', {'class': 'snmdvpl'})

    item_dics = {}
    dan_n = 0
    n = 1
    for item in items[1:-1]:
        item_dics[n] = {}
        item_dics[n]['tit'] = item.find('span', {'itemprop': 'headline'}).text

        link_temp = item.find('a', {'class': 'spml_cont'})['href']
        item_dics[n]['link'] = 'https://news.sbs.co.kr' + link_temp
        if '[단독]' in item_dics[n]['tit']:
            dan_n += 1
        n += 1

    result_txt += f"SBS 8시뉴스 (단독 {dan_n}건)<br><br>"
    for item in item_dics.values():
        tit = item['tit']
        result_txt += f"-{tit}<br>"
        if '[단독]' in tit:
            result_txt += sbs_article(item['link']) + '<br><br>'

    result_txt = '<br>' + result_txt + '<br>'
    return result_txt