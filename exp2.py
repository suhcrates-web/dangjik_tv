import requests,re
from selenium_short import selenium_short
from bs4 import BeautifulSoup

url = 'https://imnews.imbc.com/replay/2022/nwdesk/article/6387118_35744.html'

def mbc_selenium_short(url):
    temp = selenium_short(url)

    temp = BeautifulSoup(temp, 'html.parser')

    report =  temp.find('div',{'class':'report'})
    article =  temp.find('div',{'class':'article'})

    news_txt = temp.find('div', {'class':'news_txt'})
    news_txt = re.sub(r"MBC 뉴스는 24시간.*",'',news_txt.text)
    news_txt = news_txt.replace("        ",'').replace('\n\n\n','').replace("        ",'')
    news_txt = re.sub(r'영상편집:.*','',news_txt)
    print([news_txt.strip()])
