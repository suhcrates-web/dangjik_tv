import requests
from bs4 import BeautifulSoup

url = 'https://news.sbs.co.kr/news/endPage.do?news_id=N1006823518&'



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
    txt = txt.replace('\n','<br>').replace('<br> ','')
    return txt
