import requests, re
from bs4 import BeautifulSoup
from selenium_short import mbc_selenium_short
from datetime import date

# 단독기사 나올시 개별기사 추리기
def tvchosun_article(url):
    temp = requests.get(url)
    temp = BeautifulSoup(temp.content, 'html.parser')

    articles = temp.findAll('div', {'class': 'article'})

    txt = ''
    for article in articles:
        for br in article.find_all("br"):
            br.replace_with("\n")

        txt += article.text.strip()
        txt = txt.replace('\n','<br>')
    return txt

def tvchosun_checker():
    result_txt = ''
    url = f'http://news.tvchosun.com/svc/vod/ospc_news_prog_pan.html?catid=2P&source=&indate={date.today().strftime("%Y%m%d")}'
    temp = requests.get(url)

    temp = BeautifulSoup(temp.content, 'html.parser')
    # print(temp)
    items = temp.findAll('p',{'class':'article_tit'})

    item_dics = {}
    dan_n = 0
    n=1
    for item in items:

        item_dics[n] = {}
        item_dics[n]['tit'] = item.text
        link_temp = item.find('a')['onclick']
        link = re.findall(r"""(?<=\(').*(?='\))""", link_temp)[0]
        item_dics[n]['link'] = link
        if '[단독]' in item_dics[n]['tit']:
            dan_n+=1
        n += 1

    result_txt += f"@tv조선 (단독 {dan_n}건)<br><br>"
    for item in item_dics.values():
        tit = item['tit']
        result_txt += f"-{tit}<br>"
        if '[단독]' in tit:
            result_txt += tvchosun_article(item['link']) + '<br>'

    return result_txt