import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

from get_apt_data import get_apt_data, get_apt_list

st.set_page_config(page_title="아파트", page_icon="🏠")

st.markdown("# 아파트")
st.sidebar.header("아파트")
# st.write(
#     """This demo shows how to use `st.write` to visualize Pandas DataFrames.
# (Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
# )


@st.cache_data
def load_data(dataset1, dataset2):
    # 데이터프레임 생성
    # df1 = pd.DataFrame(list(dataset1.items()), columns=['Date', ['매매가', '매매 거래량']])
    # df2 = pd.DataFrame(list(dataset2.items()), columns=['Date', ['월세', '월세 거래량']])
    df1 = pd.DataFrame(list(dataset1.items()), columns=['Date', 'Data'])
    df1[['매매가', '매매 거래량']] = pd.DataFrame(df1['Data'].tolist(), index=df1.index)
    df1.drop('Data', axis=1, inplace=True)
    df2 = pd.DataFrame(list(dataset2.items()), columns=['Date', 'Data'])
    df2[['월세', '월세 거래량']] = pd.DataFrame(df2['Data'].tolist(), index=df2.index)
    df2.drop('Data', axis=1, inplace=True)

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
    df3 = df3.fillna(0)

    # 'PER' 계산
    df3['PER'] = df3['매매가'] / (df3['월세'] * 12)

    return df3

try:
    apt = st.selectbox("Choose a APT", get_apt_list())
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
        apt_name, apt_PY, dataset1, dataset2, dataset3 = get_apt_data(apt)
        df = load_data(dataset1, dataset3)

        # class_data = [5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 35, 37, 39, 41, 43, 45, 47, 49, 51, 54, 56,
        #               58, 60, 62, 64, 66, 68, 70, 72, 74, 77, 79, 81, 83, 85, 88, 90, 92]
        # # 결과 출력
        # # print(time.time() - stime)
        #
        # start_class_num, end_class_num = st.select_slider(
        #     '문제 출제 범위를 정해주세요',
        #     options=class_data,
        #     value=(min(class_data), max(class_data)))
        # # st.write('You selected wavelengths between', start, 'and', end)
        # # TODO: 현재 푼 문제 수 / 출제 가능한 문제 수 표시
        # cur = conn.cursor()
        # sql = f"SELECT COUNT(*) FROM studyEnglish WHERE class_num >= {start_class_num} AND class_num <= {end_class_num}"

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
        df.index = df.index.date

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




