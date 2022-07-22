import requests
import re
from bs4 import BeautifulSoup
from database import cursor, db

def giveme_lead(url, press, ind):
    # url='https://n.news.naver.com/mnews/article/366/0000829064'
    # data = {'sid':'105'}
    header = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7,ru;q=0.6',
        'cache-control': 'max-age=0',
        'cookie': 'NNB=HEGF2A3G5DMGE; VISIT_LOG_CLEAN=1; BMR=',
        'referer': 'http://127.0.0.1:5235/',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    temp = requests.get(url, headers=header)

    temp = BeautifulSoup(temp.content, 'html.parser')
    # print(temp)
    article = temp.find('div', {'id': 'dic_area'})
    if article == None:
        article = temp.find('div', {'id': 'articeBody'})

    ##꼬리표들 제거 ###

    bs = article.select('b')
    for b in bs:
        b.extract()

    strongs = article.find_all('strong')
    for strong in strongs:
        strong.extract()

    photos = article.find_all('span', class_='end_photo_org')
    for photo in photos:
        photo.extract()


    for br in article.find_all("br"):
        br.replace_with("\n")

    article = article.text
    article = article.replace('[서울경제]','')

    if press != '뉴시스':
        article = re.sub(r"\[.*\]",'',article)

    lead = article.strip().split('\n')[0]

    ## 통신의 경우 (수원=연합뉴스) 어쩌구 기자 =    뺴기
    if press in ['연합뉴스','뉴스1']:
        region = re.findall(r"(?<=\().*(?=\=.*\))", lead)
        if region != []:
            region = re.sub(r'\=.*', '', region[0])

            if region != '서울':
                lead += f"({region})"

        lead = re.sub(r'.*기자 =','',lead)

    if press in ['뉴시스']:
        region = re.findall(r"(?<=\[).*(?=\=.*\])", lead)
        if region != []:
            region = re.sub(r'\=.*', '', region[0])

            if region != '서울':
                lead += f"({region})"

        lead = re.sub(r'.*기자 =','',lead)

    lead = re.sub(r'\[.*\]','',lead)
    lead = lead.replace('습니다','다')

    cursor.execute(
        f"""update dangbun_stuffs.naver set writen = True where ind="{ind}" """
    )
    db.commit()

    return lead

