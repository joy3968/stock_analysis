## 셀트리온 캔들 차트
# 캔들차트 기능은 mptplotlib.finance 모듈에 포함되었으나 matplotlib 에서 제거되면서
# mpl_finance 패키지로 이동되었다. 하지만 2019년 11월부터 mpl_finance 패키지는 폐기되고
# mplfinance 패키지로 바뀌었다.

# mplfinance 의 장점은 OHLC 데이터 컬럼과 날짜시간 인덱스(DatetimeIndex)를 포함한
# 데이터프레임만 있으면 기존에 사용자들이 수동으로 처리했던 데이터 변환 작업을 모두 자동화 해준다.

# [기본적인 사용법]
# mpf.plot(OHCL 데이터프레임 [, title=차트제목] [, type=차트형태] [, mav=이동평균선]
#               [, volume=거래량 표시여부] [, ylabel= y축 레이블])

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import mplfinance as mpf

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
        print(round(page / int(last_page) * 100,2), '% 완료')
    elif (int(last_page)+1-page) == 0:
        print(page, '페이지 읽는중...', int(last_page) - page, 'page 남음')
        print(round(page / int(last_page) * 100, 2), '% 완료')

# 차트 출력을 위해 데이터프레임 가공
df = df.dropna()
df = df.iloc[0:30] # 최근 데이터 30행 읽어온다.
# 한글 컬럼명을 영문 컬럼명으로 변경
df = df.rename(columns={'날짜':'Date', '시가':'Open', '고가':'High', '저가':'Low',
                        '종가':'Close', '거래량':'Volume'})
df = df.sort_values(by='Date') # 네이버 금융의 데이터가 내림차순 이어서 오름차순으로 변경
df.index = pd.to_datetime(df.Date)
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

# mplfinance로 캔들차트 그리기
# mpf.plot(df, title='Celltrion candle chart', type='candle')

# type 인수를 ohlc로 변경한다. 미국에서 개발된 라이브러리인 관계로
# type을 지정하지 않으면 기본값이 'ohlc'이다.
# mpf.plot(df, title='Celltrion candle chart', type='ohlc')


# 캔들 색상을 바꾸거나 차트 하단에 그래프를 추가하여 거래량을 표시할 수 있다.
# 이동평균선도 세 개 까지 지정하여 출력한다.

# kwargs 는 keyworld arguments 의 약자이며, 딕셔너리이다.
kwargs = dict(title = 'Celltrion customized chart', type='candle',
              mav=(2, 4, 6), volume=True, ylabel='ohlc candels')
# 마켓 색상은 스타일을 지정하는 필수 객체, 상승은 red, 하락은 blue
mc = mpf.make_marketcolors(up='r', down='b', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc)

# mplfinance로 캔들차트 그리기
mpf.plot(df, **kwargs, style=s)
