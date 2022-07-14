import requests
from bs4 import BeautifulSoup

url = 'https://news.jtbc.joins.com/article/article.aspx?news_id=NB12065990&pDate=20220712'

def jtbc_article(url):
    temp = requests.get(url)
    temp = BeautifulSoup(temp.content, 'html.parser')
    # print(temp)
    articles = temp.findAll('div', {'class':'article_content'})
    #
    txt = ''
    for article in articles:
        for br in article.find_all("br"):
            br.replace_with("\n")

        txt+= article.text.strip()
    return txt.split('☞')[0]