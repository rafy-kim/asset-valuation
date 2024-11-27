import json

from dotenv import load_dotenv
import os
import MySQLdb
from MySQLdb.cursors import DictCursor

from apt_value import get_APT_transactions, get_APT_info

# Load environment variables from the .env file
load_dotenv()

# Connect to the database
connection = MySQLdb.connect(
  host=os.getenv("DATABASE_HOST"),
  user=os.getenv("DATABASE_USERNAME"),
  passwd=os.getenv("DATABASE_PASSWORD"),
  db=os.getenv("DATABASE"),
  autocommit=True,
  # ssl_mode="VERIFY_IDENTITY",
  # See https://planetscale.com/docs/concepts/secure-connections#ca-root-configuration
  # to determine the path to your operating systems certificate file.
  # ssl={ "ca": "" }
)

try:
    # Create a cursor to interact with the database
    cur = connection.cursor(DictCursor)

    sql = "SELECT DISTINCT name, PY FROM APTInfo WHERE status = 0"
    cur.execute(sql)
    sql_result = cur.fetchall()
    for r in sql_result:
        ####
        apt_name = r['name']
        PY = r['PY']

        # 1은 매매, 2는 전세, 3은 월세
        # DEAL_TYPE = '3'
        deal_types = range(1, 4)
        for d in deal_types:
            DEAL_TYPE = str(d)

            sql = "SELECT * FROM APTInfo WHERE name = %s AND PY = %s AND DEAL_TYPE = %s AND status = 0"
            cur.execute(sql, (apt_name, PY, DEAL_TYPE,))
            # SELECT * FROM User WHERE createdAt BETWEEN DATE_ADD (NOW(), INTERVAL -1 DAY) AND NOW();
            res = cur.fetchone()
            price_trend = json.loads(res['price_trend'])
            data = []
            for key in price_trend.keys():
                data.extend(price_trend[key])
            print(data)
            data = sorted(data, key=lambda x: x['date'])
            print(data)
            cur.execute(
                f"UPDATE APTInfo SET price_trend  = '{json.dumps(data)}' WHERE id = '{res['id']}'")
            connection.commit()


except MySQLdb.Error as e:
    print("MySQL Error:", e)

finally:
    # Close the cursor and connection
    cur.close()
    connection.close()
