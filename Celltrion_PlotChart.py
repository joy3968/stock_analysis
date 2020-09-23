## OHLC와 캔들차트

# 셀트리온 종가 차트
# OHLC(시가, 고가, 저가, 종가)를 하나의 캔들로 나타내야 하기 때문에 라이브러리를 사용하더라도 복잡하다.
# 따라서 캔들 차트를 그리기에 앞서 종가만으로 가격 변동을 표시한다.

# 셀트리온의 최근 30개 종가 데이터를 이용하여 차트를 표시한다. 보통 일주일에 5일 개장하므로
# 약 한달 반 정도 데이터에 해당한다. x축은 날짜 컬럼의 데이터, y축은 종가 컬럼의 데이터를 사용하여 그린다.

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from matplotlib import pyplot as plt

url = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'

with urlopen(url) as doc:
    html = BeautifulSoup(doc, 'lxml')
    pgrr = html.find('td', class_='pgRR')
    # print(pgrr.a['href'])
    s = str(pgrr.a['href']).split('=')
    last_page = s[-1] # 마지막 페이지 가져오기


# 전체 페이지 읽어오기
df = pd.DataFrame() #일별 시세를 저장할 데이터 프레임
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=068270'

for page in range(1, int(last_page)+1): # 1페이지 부터 마지막 페이지까지 반복
    page_url = '{}&page={}'.format(sise_url, page) # page 숫자를 이용하여 URL 페이지 수를 변경
    # print(page,' 읽는중...')
    df = df.append(pd.read_html(page_url, header=0)[0]) # read_html() 함수로 읽은 한 페이지 분량의 데이터를 df에 추가
    if page % 10 == 0:
        print(page, '페이지 읽는중...', int(last_page)-page, 'page 남음')

# 차트 출력을 위해 데이터프레임 구하기
df = df.dropna()
df = df.iloc[0:30] # 최근 데이터 30행 읽어온다.
df = df.sort_values(by='날짜') # 네이버 금융의 데이터가 내림차순이어서 오름차순으로 변경

# 날짜, 종가 컬럼으로 차트 그리기
plt.title('Celltrion (close)')
plt.xticks(rotation=45) # x축 레이블의 날짜가 겹쳐서 45도 회전하여 표시한다.
plt.plot(df['날짜'], df['종가'], 'co-') # x축은 날짜 데이터, y축은 종가 데이터, co는 좌표를 cyen 원, -는 실선이다.
plt.grid(color='gray', linestyle='--')
plt.show()