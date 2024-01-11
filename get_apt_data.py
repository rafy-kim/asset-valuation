import json
from dotenv import load_dotenv
import streamlit as st
import os
# import pymysql
# from pymysql.cursors import DictCursor
# import MySQLdb
# from MySQLdb.cursors import DictCursor
# from draw_plot import draw_plot
conn = st.connection('mysql', type='sql')

# ENV_LOAD = load_dotenv()
#
# if ENV_LOAD:
#     conn = st.connection('mysql', type='sql')
#
#     # # Connect to the database
#     # connection = pymysql.connect(
#     #   host=os.getenv("DATABASE_HOST"),
#     #   user=os.getenv("DATABASE_USERNAME"),
#     #   password=os.getenv("DATABASE_PASSWORD"),
#     #   database=os.getenv("DATABASE"),
#     #   ssl_verify_identity=True,
#     # )
# else:
#     connection = pymysql.connect(
#         host=st.secrets["DATABASE_HOST"],
#         user=st.secrets["DATABASE_USERNAME"],
#         password=st.secrets["DATABASE_PASSWORD"],
#         database=st.secrets["DATABASE"],
#         ssl_verify_identity=True,
#     )


def get_apt_data(apt_name):
    try:
        # cur = connection.cursor(cursor=DictCursor)
        ####
        # apt_name = "헬리오시티"
        # sql = "SELECT * FROM APTInfo WHERE name = %s ORDER BY id DESC LIMIT 1"
        sql = "SELECT * FROM APTInfo WHERE name = :name ORDER BY id DESC LIMIT 1"
        res = conn.query(sql, ttl=600, params={"name": apt_name})
        # cur.execute(sql, (apt_name,))
        # res = cur.fetchone()
        ####
        PY = res['PY'][0]
        print(res['price_trend'][0])
        price_trend = json.loads(res['price_trend'][0])
        start_year = int(min(price_trend.keys()))
        end_year = int(max(price_trend.keys())) + 1
        ####

        # 1은 매매, 2는 전세, 3은 월세
        DEAL_TYPE = '1'
        # sql = "SELECT * FROM APTInfo WHERE name = %s AND PY = %s AND DEAL_TYPE = %s"
        # cur.execute(sql, (apt_name, PY, DEAL_TYPE,))
        # res = cur.fetchone()
        sql = "SELECT * FROM APTInfo WHERE name = :name AND PY = :py AND DEAL_TYPE = :deal_type"
        res = conn.query(sql, ttl=600, params={"name": apt_name, "py": PY, "deal_type": DEAL_TYPE})
        price_trend = json.loads(res['price_trend'][0])
        years = range(start_year, end_year)
        data = {}
        for y in years:
            YEAR = str(y)
            for pt in price_trend[YEAR]:
                data[pt['date']] = [round(pt['avg'], 2), pt['cnt']]
                # print(pt['date'], pt['avg'])
        dataset1 = dict(sorted(data.items()))

        DEAL_TYPE = '2'
        # sql = "SELECT * FROM APTInfo WHERE name = %s AND PY = %s AND DEAL_TYPE = %s"
        # cur.execute(sql, (apt_name, PY, DEAL_TYPE,))
        # res = cur.fetchone()
        sql = "SELECT * FROM APTInfo WHERE name = :name AND PY = :py AND DEAL_TYPE = :deal_type"
        res = conn.query(sql, ttl=600, params={"name": apt_name, "py": PY, "deal_type": DEAL_TYPE})
        price_trend = json.loads(res['price_trend'][0])
        data = {}
        for y in years:
            YEAR = str(y)
            for pt in price_trend[YEAR]:
                data[pt['date']] = [round(pt['avg'], 2), pt['cnt']]
                # print(pt['date'], pt['avg'])
        dataset2 = dict(sorted(data.items()))

        DEAL_TYPE = '3'
        # sql = "SELECT * FROM APTInfo WHERE name = %s AND PY = %s AND DEAL_TYPE = %s"
        # cur.execute(sql, (apt_name, PY, DEAL_TYPE,))
        # res = cur.fetchone()
        sql = "SELECT * FROM APTInfo WHERE name = :name AND PY = :py AND DEAL_TYPE = :deal_type"
        res = conn.query(sql, ttl=600, params={"name": apt_name, "py": PY, "deal_type": DEAL_TYPE})
        price_trend = json.loads(res['price_trend'][0])
        data = {}
        for y in years:
            YEAR = str(y)
            for pt in price_trend[YEAR]:
                data[pt['date']] = [round(pt['avg'], 2), pt['cnt']]
                # print(pt['date'], pt['avg'])
        dataset3 = dict(sorted(data.items()))
        return apt_name, PY, dataset1, dataset2, dataset3

        # draw_plot(f"{apt_name} - {PY}평", dataset1, dataset2)

    except:
        print("MySQL Error:")
        return '', 0, [], [], []

    finally:
        pass
        # Close the cursor and connection
        # TODO: 주석 해제 필요
        # cur.close()
        # connection.close()


# TODO: sqlalchemy로 SQL 부분 정리하기
def get_apt_list():
    # try:
    # cur = connection.cursor()
    ####
    # apt_name = "헬리오시티"
    sql = "SELECT DISTINCT name FROM APTInfo ORDER BY name ASC"
    # cur.execute(sql)
    # sql_result = cur.fetchall()
    sql_result = conn.query(sql, ttl=600)
    apt_names = sql_result['name'].tolist()
    # cleaned_list = [item[0] for item in sql_result]
    print(apt_names)
    return apt_names

        # draw_plot(f"{apt_name} - {PY}평", dataset1, dataset2)

    # except:
    #     print("MySQL Error:")
    #     return []
    #
    # finally:
    #     pass
    #     # Close the cursor and connection
    #     # TODO: 주석 해제 필요
    #     # cur.close()
    #     # connection.close()

