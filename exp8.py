from database import db, cursor
import binascii, codecs

cursor.execute(
    """
    select date0, content from dangbun_stuffs.brods where brod = "mbc" 
    """
)

date0, content =  cursor.fetchall()[0]
print(date0.strftime("%Y년 %m월 %d일 // %H시 %M분"))
article = codecs.decode(content, 'utf-8')
