import re
a = '(인천=연합뉴스) 김상연 기자 = 성기홍 연합뉴스 사장이 21일 오전 인천시 연수구 송도컨벤시아에서 열린 제3회 인천국제해양포럼(IIOF 2022)에서 축사하고 있다. 이 행사는 수도권 최대 규모의 해양 비즈니스 포럼으로 이날부터 22일까지 이틀간 열린다. 2022.7.21'

region = re.findall(r"(?<=\().*(?=\=.*\))",a)
region = re.sub(r'\=.*','',region[0])
print(region)