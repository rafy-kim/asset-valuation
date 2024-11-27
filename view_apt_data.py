import json
from dotenv import load_dotenv
import os
import MySQLdb
from MySQLdb.cursors import DictCursor
from draw_plot import draw_plot

load_dotenv()

# Connect to the database
connection = MySQLdb.connect(
  host=os.getenv("DATABASE_HOST"),
  user=os.getenv("DATABASE_USERNAME"),
  passwd=os.getenv("DATABASE_PASSWORD"),
  db=os.getenv("DATABASE"),
  autocommit=True,
)

try:
    cur = connection.cursor(DictCursor)

    ####
    apt_name = "디에이치아너힐즈"
    sql = "SELECT * FROM APTInfo WHERE name = %s"
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
            data[pt['date']] = round(pt['avg'], 2)
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
            data[pt['date']] = round(pt['avg'], 2)
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
            data[pt['date']] = round(pt['avg'], 2)
            # print(pt['date'], pt['avg'])
    dataset2 = dict(sorted(data.items()))

    print(dataset1)
    print(dataset2)

    draw_plot(f"{apt_name} - {PY}평", dataset1, dataset2)



except MySQLdb.Error as e:
    print("MySQL Error:", e)

finally:
    # Close the cursor and connection
    cur.close()
    connection.close()



