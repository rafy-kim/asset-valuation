import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

from get_apt_data import get_apt_data, get_apt_list

st.set_page_config(page_title="아파트 비교", page_icon="🏠🏠")

st.markdown("# 아파트 비교")
st.sidebar.header("아파트 비교")
# st.write(
#     """This demo shows how to use `st.write` to visualize Pandas DataFrames.
# (Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
# )


@st.cache_data
def load_data(dataset1, dataset2, dataset3):
    # 데이터프레임 생성
    df1 = pd.DataFrame(list(dataset1.items()), columns=['Date', 'Data'])
    df1[['매매가', '매매 거래량']] = pd.DataFrame(df1['Data'].tolist(), index=df1.index)
    df1.drop('Data', axis=1, inplace=True)
    df2 = pd.DataFrame(list(dataset2.items()), columns=['Date', 'Data'])
    df2[['전세', '전세 거래량']] = pd.DataFrame(df2['Data'].tolist(), index=df2.index)
    df2.drop('Data', axis=1, inplace=True)
    df3 = pd.DataFrame(list(dataset3.items()), columns=['Date', 'Data'])
    df3[['월세', '월세 거래량']] = pd.DataFrame(df3['Data'].tolist(), index=df3.index)
    df3.drop('Data', axis=1, inplace=True)

    # 데이터프레임을 날짜로 정렬
    df1['Date'] = pd.to_datetime(df1['Date'], format='%Y%m')
    df1['Date'] = df1['Date'].dt.date
    df2['Date'] = pd.to_datetime(df2['Date'], format='%Y%m')
    df2['Date'] = df2['Date'].dt.date
    df3['Date'] = pd.to_datetime(df3['Date'], format='%Y%m')
    df3['Date'] = df3['Date'].dt.date
    df1 = df1.sort_values(by='Date')
    df2 = df2.sort_values(by='Date')
    df3 = df3.sort_values(by='Date')

    # Date를 기준으로 병합
    # df3 = pd.merge(df1, df2, on='Date', how='inner')
    df_temp = pd.merge(df1, df2, on='Date', how='outer')
    df4 = pd.merge(df_temp, df3, on='Date', how='outer')
    df4 = df4.sort_values(by='Date')

    # 결측치를 이전 달 값으로 채워넣기
    df4['매매가'] = df4['매매가'].astype(float).ffill()
    df4['전세'] = df4['전세'].astype(float).ffill()
    df4['월세'] = df4['월세'].astype(float).ffill()
    df4 = df4.fillna(0)

    # 'PER' 계산
    df4['PER'] = df4['매매가'] / (df4['월세'] * 12)

    return df4

try:
    apts = st.multiselect("Choose a APT", get_apt_list())
    print(apts)
    # apt = st.selectbox("Choose a APT", get_apt_list())
    if not apts:
        st.error("Please select a APT.")
    else:
        data = []
        for apt in apts:
            # streamlit 앱 시작
            apt_name, apt_PY, dataset1, dataset2, dataset3 = get_apt_data(apt)
            df = load_data(dataset1, dataset2, dataset3)
            data.append({apt_name: df})

        date_list = []
        date_min, date_max = None, None
        for d in data:
            apt_df = list(d.values())[0]
            if not date_list:
                date_list = apt_df["Date"].tolist()
            else:
                date_list += apt_df["Date"].tolist()
                date_list = list(set(date_list))
                date_list.sort()
            if not date_min:
                date_min = apt_df["Date"].min()
            else:
                date_min = apt_df["Date"].min() if date_min > apt_df["Date"].min() else date_min
            if not date_max:
                date_max = apt_df["Date"].max()
            else:
                date_max = apt_df["Date"].max() if date_max < apt_df["Date"].max() else date_max
        print(date_list)
        print(date_min, date_max)
        start_date, end_date = st.sidebar.select_slider(
            '조회하고 싶은 기간을 선택하세요',
            options=date_list,
            value=(date_min, date_max))
        # df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]


        # print(data)
        # 차트 그리기
        st.write(f"### 매매가")
        charts = []
        for d in data:
            apt_name = list(d.keys())[0]
            apt_df = list(d.values())[0]
            apt_df = apt_df[(apt_df['Date'] >= start_date) & (apt_df['Date'] <= end_date)]
            apt_df['단지명'] = apt_name  # 각 아파트에 대한 데이터프레임에 단지명 추가
            line_chart = alt.Chart(apt_df).mark_line(point=True).encode(
                x=alt.X("Date:T", title="Date"),
                y=alt.Y("매매가:Q", title="매매가"),
                color="단지명:N",  # 각 아파트에 대한 데이터프레임을 사용하므로 색상 설정이 이곳으로 이동
            )
            charts.append(line_chart)

        price_chart = alt.layer(*charts).resolve_scale()
        st.altair_chart(price_chart, use_container_width=True)

        # 차트 그리기
        st.write(f"### 전세")
        charts = []
        for d in data:
            apt_name = list(d.keys())[0]
            apt_df = list(d.values())[0]
            apt_df = apt_df[(apt_df['Date'] >= start_date) & (apt_df['Date'] <= end_date)]
            apt_df['단지명'] = apt_name  # 각 아파트에 대한 데이터프레임에 단지명 추가
            line_chart = alt.Chart(apt_df).mark_line(point=True).encode(
                x=alt.X("Date:T", title="Date"),
                y=alt.Y("전세:Q", title="전세"),
                color="단지명:N",  # 각 아파트에 대한 데이터프레임을 사용하므로 색상 설정이 이곳으로 이동
            )
            charts.append(line_chart)

        price_chart = alt.layer(*charts).resolve_scale()
        st.altair_chart(price_chart, use_container_width=True)

        # 차트 그리기
        st.write(f"### 월세")
        charts = []
        for d in data:
            apt_name = list(d.keys())[0]
            apt_df = list(d.values())[0]
            apt_df = apt_df[(apt_df['Date'] >= start_date) & (apt_df['Date'] <= end_date)]
            apt_df['단지명'] = apt_name  # 각 아파트에 대한 데이터프레임에 단지명 추가
            line_chart = alt.Chart(apt_df).mark_line(point=True).encode(
                x=alt.X("Date:T", title="Date"),
                y=alt.Y("월세:Q", title="월세"),
                color="단지명:N",  # 각 아파트에 대한 데이터프레임을 사용하므로 색상 설정이 이곳으로 이동
            )
            charts.append(line_chart)

        price_chart = alt.layer(*charts).resolve_scale()
        st.altair_chart(price_chart, use_container_width=True)

        # 차트 그리기
        st.write(f"### PER")
        charts = []
        for d in data:
            apt_name = list(d.keys())[0]
            apt_df = list(d.values())[0]
            apt_df = apt_df[(apt_df['Date'] >= start_date) & (apt_df['Date'] <= end_date)]
            apt_df['단지명'] = apt_name  # 각 아파트에 대한 데이터프레임에 단지명 추가
            line_chart = alt.Chart(apt_df).mark_line(point=True).encode(
                x=alt.X("Date:T", title="Date"),
                y=alt.Y("PER:Q", title="PER"),
                color="단지명:N",  # 각 아파트에 대한 데이터프레임을 사용하므로 색상 설정이 이곳으로 이동
            )
            charts.append(line_chart)

        # 수평선 추가
        hline1 = alt.Chart(pd.DataFrame({'y': [35]})).mark_rule(color='yellow', strokeWidth=1).encode(y='y:Q')
        hline2 = alt.Chart(pd.DataFrame({'y': [30]})).mark_rule(color='green', strokeWidth=1).encode(y='y:Q')
        # 차트에 수평선 추가
        PER_chart = alt.layer(*charts, hline1, hline2).resolve_scale()
        # 전체 차트 그리기
        st.altair_chart(PER_chart, use_container_width=True)


        # df = df.set_index('Date')
        # df.index = df.index.date
        #
        # # 최근 6개월 매매가 평균
        # st.write(f"- 최근 6개월 매매가 평균: {round(df[-6:].mean()['매매가']/10000, 1)}억원")
        #
        # # 최근 6개월 월세 평균
        # st.write(f"- 최근 6개월 월세 평균: {int(df[-6:].mean()['월세'])}만원")
        #
        # # 최근 월세 시세를 통해 추정한 기대 매매가
        # s_val = df[-6:].mean()['월세'] * 12 * 30
        # e_val = df[-6:].mean()['월세'] * 12 * 35
        # st.write(f"- 최근 월세 시세를 통해 추정한 기대 매매가: :blue[{round(s_val/10000, 1)}억원] ~ :blue[{round(e_val/10000, 1)}억원]")

        st.divider()

        for d in data:
            apt_name = list(d.keys())[0]
            st.write(f"### {apt_name}")
            apt_df = list(d.values())[0]
            st.dataframe(apt_df, use_container_width=True)



except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )




