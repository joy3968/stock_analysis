## read_html() 함수로 읽기

# 판다스의 reaed_html()함수를 사용하려면 html5lib 나 lxml 라이브러리를 설치해야 한다.
# read_html() 함수는 인수로 받는 경로의 HTML 파일 내부에 존재하는 Table 태그를
# 분석하여 데이터프레임으로 변환해준다. read_html() 함수는 결괏값으로 데이터프레임 객체를
# 원소로 가지는 리스트를 반환한다.

import pandas as pd
krx_list = pd.read_html('상장법인목록.xls')
# print(krx_list[0])

# 출력된 데이터프레임은 현재 2378개 종목이 상장되어 있다. 6자리 종목코드가 앞자리 0이 사라져있다.
# map() 함수를 사용해 보정한다. 종목코드 기준으로 오름차순 정렬을 한다.

krx_list[0].종목코드 = krx_list[0].종목코드.map('{:06d}'.format) #6자리 수 중 빈자리 0으로 채움
krx_list[0] = krx_list[0].sort_values(by='종목코드') # 종목코드를 기준으로 오름차순 정렬
print(krx_list[0])

## 파일 경로를 URL로 대신할 수 있다.
# krx_list = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13')
# krx_list[0].종목코드 = krx_list[0].종목코드.map('{:06d}'.format) #6자리 수 중 빈자리 0으로 채움
# krx_list[0] = krx_list[0].sort_values(by='종목코드') # 종목코드를 기준으로 오름차순 정렬
# print(krx_list[0])

# ## 다른방식
# df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13')[0]
# df['종목코드'] = df['종목코드'].map('{:06d}'.format) # 6자리 수 중 빈자리 0으로 채움
# df = df.sort_values(by='종목코드') # 오름차순 정렬
# print(df)