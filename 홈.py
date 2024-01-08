import streamlit as st

st.set_page_config(
    page_title="홈",
    page_icon="📊",
)

st.write("# 매크로 지표들 (예정)")

st.sidebar.success("메뉴를 골라주세요")

st.markdown(
    """
    ### 경기
    - (미국) 장단기 금리차
    - (국내) 경상수지 
    
    ### 주식
    - 미국 - 버핏 지수
    - 한국 - 버핏 지수
    - Fear and Greed Index
        
    ### 부동산
    - PIR
    - PER 
    
    ### 암호화폐
    - Fear and Greed Index
    - 김치 프리미엄 
    
"""
)
