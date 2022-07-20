from database import cursor
import codecs

objs = []
cursor.execute(
    """
    select time0, title, press, url from dangbun_stuffs.naver where naver_cp = 1 and good = 1
    """
)
for article in cursor.fetchall()[::-1]:
    objs.append({
        'time0': article[0],
        'title': codecs.decode(article[1], 'utf-8') ,
        'press': article[2],
        'url': article[3],
    })

print(objs)