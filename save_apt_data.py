import json

from dotenv import load_dotenv
import os
import MySQLdb
from MySQLdb.cursors import DictCursor
from supabase import create_client, Client
from apt_value import get_APT_transactions, get_APT_info
from get_apt_data import extract_and_save_year, extract_address  # year 추출 함수 import

# Load environment variables from the .env file
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
# # Connect to the database
# connection = MySQLdb.connect(
#   host=os.getenv("DATABASE_HOST"),
#   user=os.getenv("DATABASE_USERNAME"),
#   passwd=os.getenv("DATABASE_PASSWORD"),
#   db=os.getenv("DATABASE"),
#   autocommit=True,
#   # ssl_mode="VERIFY_IDENTITY",
#   # See https://planetscale.com/docs/concepts/secure-connections#ca-root-configuration
#   # to determine the path to your operating systems certificate file.
#   # ssl={ "ca": "" }
# )

try:
    # Create a cursor to interact with the database
    # cur = connection.cursor(DictCursor)

    ####
    apt_name = "잠실올림픽아이파크"
    PY = '26'
    apt_info = get_APT_info(apt_name)
    
    # description에서 year와 address 추출
    year = extract_and_save_year(apt_info['desc'])
    address = extract_address(apt_info['desc'])
    
    s_yy = apt_info['desc'].split('/')[1].split('년')[0].strip()
    if len(s_yy) == 2:
        if s_yy[0] in ['0', '1', '2']:
            yyyy = '20' + s_yy
        else:
            yyyy = '19' + s_yy
        start_year = int(yyyy) + 1
    elif len(s_yy) == 4:
        start_year = int(s_yy) + 1
    else:
        print(f"s_yy 값이 이상해요: {s_yy}")

    # 1은 매매, 2는 전세, 3은 월세
    deal_types = range(1, 4)
    for d in deal_types:
        DEAL_TYPE = str(d)
        ####
        years = range(start_year, 2024)
        for y in years:
            YEAR = str(y)
            amount = get_APT_transactions(apt_info, PY, YEAR, DEAL_TYPE)
            print(amount)
            if not amount:
                continue
            amount = sorted(amount, key=lambda x: x['date'])
            print(amount)

            response = supabase.table('APTInfo').select('*').eq('name', apt_name).eq('PY', PY).eq('DEAL_TYPE', DEAL_TYPE).limit(1).execute()
            res = response.data
            if res:
                res = res[0]
                price_trend = json.loads(res['price_trend'])
                print(amount[-1]['date'])
                date_exists = any(d['date'] == amount[-1]['date'] for d in price_trend)
                if date_exists:
                    print(f'{amount[-1]["date"]} 이미 존재함')
                else:
                    price_trend.extend(amount)
                    response = supabase.table('APTInfo').update({
                        'price_trend': json.dumps(price_trend),
                        'year': year  # year 필드도 함께 업데이트
                    }).eq('id', res['id']).execute()
                    print("업데이트 완료!!")

            else:
                print('최초 생성')
                response = supabase.table('APTInfo').insert({
                    'name': apt_info['name'], 
                    'PY': PY, 
                    'DEAL_TYPE': DEAL_TYPE, 
                    'seq': apt_info['seq'], 
                    'description': apt_info['desc'], 
                    'price_trend': json.dumps(amount),
                    'status': 1,
                    'year': year,
                    'address': address  # address 필드 추가
                }).execute()

except MySQLdb.Error as e:
    print("MySQL Error:", e)

finally:
    print("Finished")
