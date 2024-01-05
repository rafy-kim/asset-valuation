import json
from dotenv import load_dotenv
import streamlit as st
import os
import pymysql
from pymysql.cursors import DictCursor
# import MySQLdb
# from MySQLdb.cursors import DictCursor
# from draw_plot import draw_plot

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


def get_apt_data(apt_name):
    try:
        cur = connection.cursor(cursor=DictCursor)
        ####
        # apt_name = "헬리오시티"
        sql = "SELECT * FROM APTInfo WHERE name = %s ORDER BY id DESC LIMIT 1"
        cur.execute(sql, (apt_name,))
        res = cur.fetchone()
        ####
        PY = res['PY']
        price_trend = json.loads(res['price_trend'])
        start_year = int(min(price_trend.keys()))
        end_year = int(max(price_trend.keys())) + 1
        ####

        # 1은 매매, 2는 전세, 3은 월세
        DEAL_TYPE = '1'
        sql = "SELECT * FROM APTInfo WHERE name = %s AND PY = %s AND DEAL_TYPE = %s"
        cur.execute(sql, (apt_name, PY, DEAL_TYPE,))
        res = cur.fetchone()
        print(res['name'], res['PY'], res['DEAL_TYPE'])

        price_trend = json.loads(res['price_trend'])
        years = range(start_year, end_year)
        data = {}
        for y in years:
            YEAR = str(y)
            for pt in price_trend[YEAR]:
                data[pt['date']] = [round(pt['avg'], 2), pt['cnt']]
                # print(pt['date'], pt['avg'])
        dataset1 = dict(sorted(data.items()))

        DEAL_TYPE = '2'
        sql = "SELECT * FROM APTInfo WHERE name = %s AND PY = %s AND DEAL_TYPE = %s"
        cur.execute(sql, (apt_name, PY, DEAL_TYPE,))
        res = cur.fetchone()
        price_trend = json.loads(res['price_trend'])
        data = {}
        for y in years:
            YEAR = str(y)
            for pt in price_trend[YEAR]:
                data[pt['date']] = [round(pt['avg'], 2), pt['cnt']]
                # print(pt['date'], pt['avg'])
        dataset2 = dict(sorted(data.items()))

        DEAL_TYPE = '3'
        sql = "SELECT * FROM APTInfo WHERE name = %s AND PY = %s AND DEAL_TYPE = %s"
        cur.execute(sql, (apt_name, PY, DEAL_TYPE,))
        res = cur.fetchone()
        price_trend = json.loads(res['price_trend'])
        data = {}
        for y in years:
            YEAR = str(y)
            for pt in price_trend[YEAR]:
                data[pt['date']] = [round(pt['avg'], 2), pt['cnt']]
                # print(pt['date'], pt['avg'])
        dataset2 = dict(sorted(data.items()))
        return f"{apt_name} - {PY}평", dataset1, dataset2

        # draw_plot(f"{apt_name} - {PY}평", dataset1, dataset2)

    except pymysql.Error as e:
        print("MySQL Error:", e)
        return '', [], []

    finally:
        pass
        # Close the cursor and connection
        # TODO: 주석 해제 필요
        # cur.close()
        # connection.close()



