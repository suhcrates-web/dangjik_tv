import requests
from bs4 import BeautifulSoup
import time

page = 1
download = True
while download==True:
    url =f'https://search.naver.com/p/crd/rd?m=1&px=271&py=1650&sx=271&sy=554&p=hWPdysp0YihssFKJTndssssssD4-322517&q=%5B%EB%8B%A8%EB%8F%85%5D+%7C+%5B%EC%86%8D%EB%B3%B4%5D&ie=utf8&rev=1&ssc=tab.news.all&f=news&w=news&s=p0rw0vpWLYlcekQoydvswA%3D%3D&time=1658294496464&a=nws.paging&r={page}&u=https%3A%2F%2Fsearch.naver.com%2Fsearch.naver%3Fwhere%3Dnews%26sm%3Dtab_pge%26query%3D%255B%25EB%258B%25A8%25EB%258F%2585%255D%2520%257C%2520%255B%25EC%2586%258D%25EB%25B3%25B4%255D%26sort%3D1%26photo%3D0%26field%3D0%26pd%3D0%26ds%3D%26de%3D%26mynews%3D0%26office_type%3D0%26office_section_code%3D0%26news_office_checked%3D%26nso%3Dso%3Add%2Cp%3Aall%2Ca%3Aall%26start%3D{page}1'
    # url =f'https://search.naver.com/p/crd/rd/'

    data = {
        'm': '1',
        'px': '271',
        'py': '1652',
        'sx': '271',
        'sy': '556',
        'p': 'hWPgZwp0YiRssbmP5ihssssssvZ-139023',
        'q': '[단독] | [속보]',
        'ie': 'utf8',
        'rev': '1',
        'ssc': 'tab.news.all',
        'f': 'news',
        'w': 'news',
        's': '5DKotjx2J62GzDYFCcDV3A==',
        'time': '1658295069281',
        'a': 'nws.paging',
        'r': page,
        # 'u': 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%5B%EB%8B%A8%EB%8F%85%5D%20%7C%20%5B%EC%86%8D%EB%B3%B4%5D&sort=1&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:all,a:all&start=21'
    }

    temp = requests.get(url)
    temp = BeautifulSoup(temp.content, 'html.parser')
    # print(temp)

    news_areas = temp.find_all('div', {'class':'news_area'})

    for news_area in news_areas:

        infos = news_area.find_all('a', class_='info')
        info_list = []
        for info in infos:
            if 'press' in info['class']:
                press = info.text.replace('언론사 선정','')
            else:
                info_list.append(info)

        doit = True if info_list != [] else False

        if doit:
            link = info_list[0]['href']
            tit = news_area.find('a',class_='news_tit')['title']
            # if "[단독]" in tit or "[속보]" in tit:
            print(press)
            print(link)
            print(tit)

    print(f"{page}")
    page +=1
    time.sleep(5)
