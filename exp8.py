from database import db, cursor
import binascii, codecs

a = '@MBC뉴스 (단독 2건)'
a = bin(int(binascii.hexlify(a.encode('utf-8')), 16))[2:]
brod = 'mbc'
cursor.execute(
                    f"""update dangbun_stuffs.brods set content = b'{a}' where brod="{brod}" """
                )
db.commit()


cursor.execute(
    """
    select content from dangbun_stuffs.brods where brod = "mbc" 
    """
)

temp = codecs.decode(cursor.fetchall[0][0], 'utf-8')

print(temp)