## 웹에서 일별 시세 구하기
# 셀트리온 종목코드 : 068270
# https://finance.naver.com/item/sise.nhn?code=068270

# 셀트리온 일별 시세 데이터 가져오기
# 네이버 금융에서 일별 시세 페이지로 이동. 셀트리온 주가가 페이지당 10개씩
# 표시되어 있다. 첫 페이지의 주가는 최신 날짜 주가이다.

# BeautifulSoup 로 일별 시세 읽어오기
# 맨 뒤 페이지 구하기

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

url = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'
with urlopen(url) as doc:
    html = BeautifulSoup(doc, 'lxml')
    pgrr = html.find('td', class_='pgRR')
    # print(pgrr.a['href'])
    s = str(pgrr.a['href']).split('=')
    last_page = s[-1] # 마지막 페이지 가져오기
    # print(last_page)


# 뷰티풀 수프 생성자의 첫 번째 인수로 HTML/XML 페이지의 파일 경로나 URL을 넘겨주고, 두 번째인수로
# 웹 페이지를 파싱할 방식을 넘겨준다.

# find() 함수를 통해서 class 속성이 'pgRR'인 td 태그를 찾으면,
# 결과값은 'bs4.element.Tag' 타입으로 pgrr변수에 반환된다.
# 'pgRR'은 Page Right Right 즉, 맨 마지막 오른쪽 페이지를 의미한다.
# Find() 함수의 인수인 class 속성을 class_로 한 것은 파이썬에 이미 class라는 예약어가 존재하기 때문
# pgrr변수에 검색 결과가 담겨져 있으므로 prettify() 함수를 호출하여 출력하고, text 속성값을 출력한다.

# print(pgrr.prettify())
# print(pgrr.text)

## 전체 페이지 읽어오기
# 일별 시세의 전체 페이지 수를 구했으므로 첫 페이지부터 마지막 페이지까지 반복해서 일별 시세를
# 읽어온다. 일별 시세는 테이블 형태의(tabular) 데이터이므로 판다스의 read_html() 함수를
# 사용해서 한 페이지씩 읽어온 데이터를 데이터프레임에 추가하면 전체 페이지의 일별 시세 데이터를
# 구할 수 있다.

df = pd.DataFrame() #일별 시세를 저장할 데이터 프레임
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=068270'

for page in range(1, int(last_page)+1): # 1페이지 부터 마지막 페이지까지 반복
    page_url = '{}&page={}'.format(sise_url, page) # page 숫자를 이용하여 URL 페이지 수를 변경
    # print(page,' 읽는중...')
    df = df.append(pd.read_html(page_url, header=0)[0]) # read_html() 함수로 읽은 한 페이지 분량의 데이터를 df에 추가
    if page % 10 == 0:
        print(page, '페이지 읽는중...', int(last_page)-page, 'page 남음')

df = df.dropna() # 값이 빠진 행을 제거한다.

print(df)



