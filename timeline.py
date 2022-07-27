import naver_start
from naver_routine import naver_routine
import time


while True:
    time.sleep(60)
    try:
        naver_routine()
    except Exception as e:
        print(e)


