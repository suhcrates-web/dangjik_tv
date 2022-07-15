import requests, re
from bs4 import BeautifulSoup
from datetime import date, timedelta


# 단독기사 나올시 개별기사 추리기
def mbn_article(url):
    temp = requests.get(url)
    temp = BeautifulSoup(temp.content, 'html.parser')

    article = temp.find('div', {'class': 'txt'}).p
    txt = ''
    # for article in articles:
    #     print([article])
    #
    for br in article.find_all("br"):
        br.replace_with("\n")
    article = article.text.replace('\r','').replace('\n\n','\n')

    # txt += article.text.strip()
    # txt = txt.replace('\n','<br>')
    # print(txt)
    article = '<br>' + article.replace('\n','<br>') + '<br>'
    return article


def mbn_checker():
    url = 'https://www.mbn.co.kr/lib/module/getProgramReviewList_A.v2.php'

    li_list = []
    download_whole = True


    today0 = date.today()

    while  download_whole ==True:
        download_today = True
        page_n = 1
        while download_today == True:
            data  = {
            'progCode': '552',
            'menuCode': '2636',
            'currentDate': today0.strftime("%Y%m%d"),
            'page': page_n,
            }
            temp = requests.post(url, data= data)

            temp = BeautifulSoup(temp.content, 'html.parser')

            li_temp = temp.findAll('li')
            if li_temp == []:

                download_today=False

            li_list += li_temp
            page_n +=1
        if li_list == [] :
            today0 -= timedelta(days=1)
        else:
            download_whole = False


    item_dics = {}
    dan_n = 0
    n = 1
    for item in li_list:

        item_dics[n] = {}
        item_dics[n]['tit'] = item.find('a', {'class':'tlt'}).text
        link = item.find('a', {'class': 'tlt'})['href']
        item_dics[n]['link'] = 'https://www.mbn.co.kr/'+link
        if '[단독]' in item_dics[n]['tit']:
            dan_n += 1
        n += 1

    result_txt = ''
    result_txt += f"@mbn 뉴스7 (단독 {dan_n}건)<br><br>"
    for item in item_dics.values():
        tit = item['tit']
        result_txt += f"-{tit}<br>"
        if '[단독]' in tit:
            result_txt += mbn_article(item['link']) #+ '<br>'
            # pass
    return result_txt
