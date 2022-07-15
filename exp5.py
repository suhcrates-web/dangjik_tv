import requests
from bs4 import BeautifulSoup

url = 'https://www.mbn.co.kr/vod/programView/1303482'



# 단독기사 나올시 개별기사 추리기
def mbn_article(url):
    temp = requests.get(url)
    temp = BeautifulSoup(temp.content, 'html.parser')

    txt = temp.find('div', {'class': 'txt'}).p
    # txt = ''
    # for article in articles:
    #     for br in article.find_all("br"):
    #         br.replace_with("\n")
    #
    #     txt += article.text.strip()
    #     txt = txt.replace('\n','<br>')
    return txt
