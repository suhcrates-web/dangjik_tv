from selenium import webdriver
from bs4 import BeautifulSoup
import re

def selenium_short(url):
# url = 'https://imnews.imbc.com/replay/2022/nwdesk/article/6387118_35744.html'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("disable-gpu")
    # driver = webdriver.Chrome('./chromedriver', options=options)
    driver = webdriver.Chrome('C:/stamp/chromedriver', options=options)
    driver.get(url)
    html0 = driver.page_source
    html0 = BeautifulSoup(html0, 'html.parser')
    return html0


def mbc_selenium_short(url):
    temp = selenium_short(url)

    news_txt = temp.find('div', {'class': 'news_txt'})
    news_txt = re.sub(r"MBC 뉴스는 24시간.*", '', news_txt.text)
    news_txt = news_txt.replace("        ", '').replace('\n\n\n', '').replace("        ", '')
    news_txt = re.sub(r'영상편집:.*', '', news_txt)
    news_txt = news_txt.replace('\n','<br>')
    return news_txt.strip()