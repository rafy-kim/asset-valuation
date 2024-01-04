import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError
import matplotlib.pyplot as plt

from get_apt_data import get_apt_data

st.set_page_config(page_title="APT Valuation", page_icon="🏠")

st.markdown("# APT Valuation")
st.sidebar.header("APT Valuation")
# st.write(
#     """This demo shows how to use `st.write` to visualize Pandas DataFrames.
# (Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
# )


@st.cache_data
def load_data(dataset1, dataset2):
    # 데이터프레임 생성
    df1 = pd.DataFrame(list(dataset1.items()), columns=['Date', '매매가'])
    df2 = pd.DataFrame(list(dataset2.items()), columns=['Date', '월세'])

    # 데이터프레임을 날짜로 정렬
    df1['Date'] = pd.to_datetime(df1['Date'], format='%Y%m')
    df2['Date'] = pd.to_datetime(df2['Date'], format='%Y%m')
    df1 = df1.sort_values(by='Date')
    df2 = df2.sort_values(by='Date')

    # Date를 기준으로 병합
    # df3 = pd.merge(df1, df2, on='Date', how='inner')
    df3 = pd.merge(df1, df2, on='Date', how='outer')
    df3 = df3.sort_values(by='Date')

    # 결측치를 이전 달 값으로 채워넣기
    df3['매매가'] = df3['매매가'].astype(float).ffill()
    df3['월세'] = df3['월세'].astype(float).ffill()

    # 'PER' 계산
    df3['PER'] = df3['매매가'] / (df3['월세'] * 12)

    return df3

try:
    apt = st.selectbox("Choose a APT", ["타워팰리스1차", "디에이치아너힐즈", "마포래미안푸르지오", "헬리오시티", "잠실엘스"])
    if not apt:
        st.error("Please select a APT.")
    else:
        # data = df.loc[countries]
        # data /= 1000000.0
        # st.write("### Gross Agricultural Production ($B)", data.sort_index())
        #
        # data = data.T.reset_index()
        # data = pd.melt(data, id_vars=["index"]).rename(
        #     columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        # )
        # chart = (
        #     alt.Chart(data)
        #     .mark_area(opacity=0.3)
        #     .encode(
        #         x="year:T",
        #         y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
        #         color="Region:N",
        #     )
        # )
        # st.altair_chart(chart, use_container_width=True)

        # streamlit 앱 시작
        title, dataset1, dataset2 = get_apt_data(apt)
        df3 = load_data(dataset1, dataset2)

        # 차트 그리기
        # Line Chart
        st.write(f"### {title}")
        line_chart1 = alt.Chart(df3).mark_line(point=True).encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("매매가:Q", title="매매가"),
            color=alt.value('red'),  # 첫 번째 데이터셋 색상
        )

        line_chart2 = alt.Chart(df3).mark_line(point=True).encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("PER:Q", title="PER"),
            color=alt.value('blue'),  # 두 번째 데이터셋 색상
        )

        # 수평선 추가
        hline1 = alt.Chart(df3).mark_rule(color='orange', strokeWidth=1).encode(
            y="average(PER)",
        )
        hline2 = alt.Chart(pd.DataFrame({'y': [35]})).mark_rule(color='yellow', strokeWidth=1).encode(y='y:Q')
        hline3 = alt.Chart(pd.DataFrame({'y': [30]})).mark_rule(color='green', strokeWidth=1).encode(y='y:Q')

        # 차트에 수평선 추가
        base_chart = alt.layer(line_chart2, hline1, hline2, hline3).resolve_scale()
        # 전체 차트 그리기
        final_chart = alt.layer(line_chart1, base_chart).resolve_scale(y='independent')
        st.altair_chart(final_chart, use_container_width=True)

        df3 = df3.set_index('Date')
        df3.index = df3.index.date

        # 최근 6개월 매매가 평균
        st.write(f"- 최근 6개월 매매가 평균: {round(df3[-6:].mean()['매매가']/10000, 1)}억원")

        # 최근 6개월 월세 평균
        st.write(f"- 최근 6개월 월세 평균: {int(df3[-6:].mean()['월세'])}만원")

        # 최근 월세 시세를 통해 추정한 기대 매매가
        s_val = df3[-6:].mean()['월세'] * 12 * 30
        e_val = df3[-6:].mean()['월세'] * 12 * 35
        st.write(f"- 최근 월세 시세를 통해 추정한 기대 매매가: :blue[{round(s_val/10000, 1)}억원] ~ :blue[{round(e_val/10000, 1)}억원]")

        st.divider()

        st.dataframe(df3, use_container_width=True)



except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )




