import streamlit as st
import pandas as pd
import altair as alt
from dotenv import load_dotenv
import os
from urllib.error import URLError
import pymysql
from pymysql.cursors import DictCursor

from get_apt_data import get_apt_data, get_apt_list

# st.set_page_config(page_title="아파트", page_icon="🏠")
ENV_LOAD = load_dotenv()

if ENV_LOAD:
    # Connect to the database
    connection = pymysql.connect(
      host=os.getenv("DATABASE_HOST"),
      user=os.getenv("DATABASE_USERNAME"),
      password=os.getenv("DATABASE_PASSWORD"),
      database=os.getenv("DATABASE"),
      ssl_verify_identity=True,
    )
else:
    connection = pymysql.connect(
        host=st.secrets["DATABASE_HOST"],
        user=st.secrets["DATABASE_USERNAME"],
        password=st.secrets["DATABASE_PASSWORD"],
        database=st.secrets["DATABASE"],
        ssl_verify_identity=True,
    )

st.markdown("# 아파트")
st.sidebar.header("아파트")
# st.write(
#     """This demo shows how to use `st.write` to visualize Pandas DataFrames.
# (Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
# )


@st.cache_data
def load_data(dataset1, dataset2):
    # 데이터프레임 생성
    # 데이터 프레임 생성
    df1 = pd.DataFrame(dataset1)
    df2 = pd.DataFrame(dataset2)
    # 'date'를 datetime 형식으로 변환
    df1['date'] = pd.to_datetime(df1['date'], format='%Y%m')
    df1 = df1.rename(columns={
        'date': 'Date',
        'avg': '매매가',
        'cnt': '매매 거래량'
    })
    df1['Date'] = df1['Date'].dt.date
    df2['date'] = pd.to_datetime(df2['date'], format='%Y%m')
    df2 = df2.rename(columns={
        'date': 'Date',
        'avg': '월세',
        'cnt': '월세 거래량'
    })
    df2['Date'] = df2['Date'].dt.date

    # df1 = pd.DataFrame(list(dataset1.items()), columns=['Date', 'Data'])
    # df1[['매매가', '매매 거래량']] = pd.DataFrame(df1['Data'].tolist(), index=df1.index)
    # df1.drop('Data', axis=1, inplace=True)
    # df2 = pd.DataFrame(list(dataset2.items()), columns=['Date', 'Data'])
    # df2[['월세', '월세 거래량']] = pd.DataFrame(df2['Data'].tolist(), index=df2.index)
    # df2.drop('Data', axis=1, inplace=True)
    #
    # # 데이터프레임을 날짜로 정렬
    # df1['Date'] = pd.to_datetime(df1['Date'], format='%Y%m')
    # df1['Date'] = df1['Date'].dt.date
    # df2['Date'] = pd.to_datetime(df2['Date'], format='%Y%m')
    # df2['Date'] = df2['Date'].dt.date
    # df1 = df1.sort_values(by='Date')
    # df2 = df2.sort_values(by='Date')

    # Date를 기준으로 병합
    # df3 = pd.merge(df1, df2, on='Date', how='inner')
    df3 = pd.merge(df1, df2, on='Date', how='outer')
    df3 = df3.sort_values(by='Date')

    # 결측치를 이전 달 값으로 채워넣기
    df3['매매가'] = df3['매매가'].astype(float).ffill()
    df3['월세'] = df3['월세'].astype(float).ffill()
    df3 = df3.fillna(0)

    # 'PER' 계산
    df3['PER'] = df3['매매가'] / (df3['월세'] * 12)

    return df3

try:
    cur = connection.cursor()
    apt = st.selectbox("Choose a APT", get_apt_list(cur))
    if not apt:
        st.error("Please select a APT.")
    else:
        # streamlit 앱 시작
        cur = connection.cursor(cursor=DictCursor)
        apt_name, apt_PY, dataset1, dataset2, dataset3 = get_apt_data(cur, apt)
        df = load_data(dataset1, dataset3)

        start_date, end_date = st.sidebar.select_slider(
            '조회하고 싶은 기간을 선택하세요',
            options=df["Date"].tolist(),
            value=(df["Date"].min(), df["Date"].max()))
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

        # 차트 그리기
        # Line Chart
        st.write(f"### {apt_name} - {apt_PY}평")
        line_chart1 = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("매매가:Q", title="매매가"),
            color=alt.value('red'),  # 첫 번째 데이터셋 색상
        )

        line_chart2 = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("PER:Q", title="PER"),
            color=alt.value('blue'),  # 두 번째 데이터셋 색상
        )

        # 수평선 추가
        hline1 = alt.Chart(df).mark_rule(color='orange', strokeWidth=1).encode(
            y="average(PER)",
        )
        hline2 = alt.Chart(pd.DataFrame({'y': [35]})).mark_rule(color='yellow', strokeWidth=1).encode(y='y:Q')
        hline3 = alt.Chart(pd.DataFrame({'y': [30]})).mark_rule(color='green', strokeWidth=1).encode(y='y:Q')

        # 차트에 수평선 추가
        base_chart = alt.layer(line_chart2, hline1, hline2, hline3).resolve_scale()
        # 전체 차트 그리기
        final_chart = alt.layer(line_chart1, base_chart).resolve_scale(y='independent')
        st.altair_chart(final_chart, use_container_width=True)

        df = df.set_index('Date')

        # 최근 6개월 매매가 평균
        st.write(f"- 최근 6개월 매매가 평균: {round(df[-6:].mean()['매매가']/10000, 1)}억원")

        # 최근 6개월 월세 평균
        st.write(f"- 최근 6개월 월세 평균: {int(df[-6:].mean()['월세'])}만원")

        # 최근 월세 시세를 통해 추정한 기대 매매가
        s_val = df[-6:].mean()['월세'] * 12 * 30
        e_val = df[-6:].mean()['월세'] * 12 * 35
        st.write(f"- 최근 월세 시세를 통해 추정한 기대 매매가: :blue[{round(s_val/10000, 1)}억원] ~ :blue[{round(e_val/10000, 1)}억원]")

        st.divider()

        st.dataframe(df, use_container_width=True)



except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )




