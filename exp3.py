from selenium import webdriver

url = 'https://imnews.imbc.com/replay/2022/nwdesk/article/6387118_35744.html'
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-gpu")
# driver = webdriver.Chrome('./chromedriver', options=options)
driver = webdriver.Chrome('C:/stamp/chromedriver', options=options)
driver.get(url)
html = driver.page_source
print(html)

#드라이버로 크롬 브라우저 제어해서 url 제어시키면 이 페이지에 있는 자바스크립트가 움직인다. 그 자바스크립트가 이 기사의 텍스트를 가져오게 된다.
#걍 get 만 하면 자바스크립특 가동을 안한다.