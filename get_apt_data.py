import json
import streamlit as st
# import MySQLdb
# from MySQLdb.cursors import DictCursor
# from draw_plot import draw_plot
from supabase import create_client, Client
import os
from dotenv import load_dotenv

ENV_LOAD = load_dotenv()
if ENV_LOAD:
    # Connect to the database
    # connection = pymysql.connect(
    #   host=os.getenv("DATABASE_HOST"),
    #   user=os.getenv("DATABASE_USERNAME"),
    #   password=os.getenv("DATABASE_PASSWORD"),
    #   database=os.getenv("DATABASE"),
    #   ssl_verify_identity=True,
    # )
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)

else:
    # connection = pymysql.connect(
    #     host=st.secrets["DATABASE_HOST"],
    #     user=st.secrets["DATABASE_USERNAME"],
    #     password=st.secrets["DATABASE_PASSWORD"],
    #     database=st.secrets["DATABASE"],
    #     ssl_verify_identity=True,
    # )
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)


def get_apt_data(apt_name):
    ####
    # apt_name = "헬리오시티"
    # sql = "SELECT * FROM APTInfo WHERE name = %s ORDER BY id DESC LIMIT 1"
    # cur.execute(sql, (apt_name,))
    # res = cur.fetchone()
    response = supabase.table('APTInfo').select('PY').eq('name', apt_name).limit(1).single().execute()
    res = response.data

    ####
    PY = res['PY']
    # price_trend = json.loads(res['price_trend'])
    # start_year = int(min(price_trend.keys()))
    # end_year = int(max(price_trend.keys())) + 1
    ####

    # 1은 매매, 2는 전세, 3은 월세
    DEAL_TYPE = '1'
    # sql = "SELECT * FROM APTInfo WHERE name = %s AND PY = %s AND DEAL_TYPE = %s"
    # cur.execute(sql, (apt_name, PY, DEAL_TYPE,))
    # res = cur.fetchone()
    response = supabase.table('APTInfo').select('*').eq('name', apt_name).eq('PY', PY).eq('DEAL_TYPE',
                                                                                                         DEAL_TYPE).limit(1).single().execute()
    res = response.data

    dataset1 = json.loads(res['price_trend'])
    # print(res['name'], res['PY'], res['DEAL_TYPE'])
    #
    # price_trend = json.loads(res['price_trend'])
    # years = range(start_year, end_year)
    # data = {}
    # for y in years:
    #     YEAR = str(y)
    #     for pt in price_trend[YEAR]:
    #         data[pt['date']] = [round(pt['avg'], 2), pt['cnt']]
    #         # print(pt['date'], pt['avg'])
    # dataset1 = dict(sorted(data.items()))

    DEAL_TYPE = '2'
    # sql = "SELECT * FROM APTInfo WHERE name = %s AND PY = %s AND DEAL_TYPE = %s"
    # cur.execute(sql, (apt_name, PY, DEAL_TYPE,))
    # res = cur.fetchone()
    response = supabase.table('APTInfo').select('*').eq('name', apt_name).eq('PY', PY).eq('DEAL_TYPE',
                                                                                                         DEAL_TYPE).limit(1).single().execute()
    res = response.data

    dataset2 = json.loads(res['price_trend'])
    # data = {}
    # for y in years:
    #     YEAR = str(y)
    #     for pt in price_trend[YEAR]:
    #         data[pt['date']] = [round(pt['avg'], 2), pt['cnt']]
    #         # print(pt['date'], pt['avg'])
    # dataset2 = dict(sorted(data.items()))

    DEAL_TYPE = '3'
    # sql = "SELECT * FROM APTInfo WHERE name = %s AND PY = %s AND DEAL_TYPE = %s"
    # cur.execute(sql, (apt_name, PY, DEAL_TYPE,))
    # res = cur.fetchone()
    response = supabase.table('APTInfo').select('*').eq('name', apt_name).eq('PY', PY).eq('DEAL_TYPE',
                                                                                                         DEAL_TYPE).limit(1).single().execute()
    res = response.data

    dataset3 = json.loads(res['price_trend'])
    # data = {}
    # for y in years:
    #     YEAR = str(y)
    #     for pt in price_trend[YEAR]:
    #         data[pt['date']] = [round(pt['avg'], 2), pt['cnt']]
    #         # print(pt['date'], pt['avg'])
    # dataset3 = dict(sorted(data.items()))
    return apt_name, PY, dataset1, dataset2, dataset3


# TODO: sqlalchemy로 SQL 부분 정리하기
def get_apt_list():
    ####
    # apt_name = "헬리오시티"
    # query = "SELECT DISTINCT name FROM APTInfo ORDER BY name ASC"
    # cur.execute(sql)
    # sql_result = cur.fetchall()
    data = supabase.table('APTInfo').select('name').execute().data
    cleaned_list = sorted({d['name'] for d in data})
    # cleaned_list = [item[0] for item in sql_result]
    # print(cleaned_list)
    return cleaned_list
