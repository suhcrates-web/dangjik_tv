import requests
from bs4 import BeautifulSoup
from selenium_short import mbc_selenium_short

def mbc_checker():
    result_txt = ''
    url = 'https://imnews.imbc.com/replay/2022/nwdesk/'
    temp = requests.get(url)

    temp = BeautifulSoup(temp.content, 'html.parser')

    items = temp.findAll('li',{'class':'item'})


    item_dics = {}
    dan_n = 0
    n=1
    for item in items:

        item_dics[n]={}
        item_dics[n]['tit'] = item.find('span', {'class': 'tit'}).text
        item_dics[n]['link'] = item.find('a')['href']

        if '[단독]' in item_dics[n]['tit']:
            dan_n+=1
        n += 1

    result_txt += f"@MBC뉴스 (단독 {dan_n}건)<br><br>"
    for item in item_dics.values():
        tit = item['tit']
        result_txt += f"-{tit} <br>"
        if '[단독]' in tit:
            result_txt += mbc_selenium_short(item['link']) + '<br><br>'
    return result_txt