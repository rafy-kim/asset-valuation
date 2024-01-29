import json
import streamlit as st
# import MySQLdb
# from MySQLdb.cursors import DictCursor
# from draw_plot import draw_plot


def get_apt_data(cur, apt_name):
    ####
    # apt_name = "헬리오시티"
    sql = "SELECT * FROM APTInfo WHERE name = %s ORDER BY id DESC LIMIT 1"
    cur.execute(sql, (apt_name,))
    res = cur.fetchone()
    ####
    PY = res['PY']
    # price_trend = json.loads(res['price_trend'])
    # start_year = int(min(price_trend.keys()))
    # end_year = int(max(price_trend.keys())) + 1
    ####

    # 1은 매매, 2는 전세, 3은 월세
    DEAL_TYPE = '1'
    sql = "SELECT * FROM APTInfo WHERE name = %s AND PY = %s AND DEAL_TYPE = %s"
    cur.execute(sql, (apt_name, PY, DEAL_TYPE,))
    res = cur.fetchone()
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
    sql = "SELECT * FROM APTInfo WHERE name = %s AND PY = %s AND DEAL_TYPE = %s"
    cur.execute(sql, (apt_name, PY, DEAL_TYPE,))
    res = cur.fetchone()
    dataset2 = json.loads(res['price_trend'])
    # data = {}
    # for y in years:
    #     YEAR = str(y)
    #     for pt in price_trend[YEAR]:
    #         data[pt['date']] = [round(pt['avg'], 2), pt['cnt']]
    #         # print(pt['date'], pt['avg'])
    # dataset2 = dict(sorted(data.items()))

    DEAL_TYPE = '3'
    sql = "SELECT * FROM APTInfo WHERE name = %s AND PY = %s AND DEAL_TYPE = %s"
    cur.execute(sql, (apt_name, PY, DEAL_TYPE,))
    res = cur.fetchone()
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
def get_apt_list(cur):
    ####
    # apt_name = "헬리오시티"
    sql = "SELECT DISTINCT name FROM APTInfo ORDER BY name ASC"
    cur.execute(sql)
    sql_result = cur.fetchall()
    cleaned_list = [item[0] for item in sql_result]
    # print(cleaned_list)
    return cleaned_list
