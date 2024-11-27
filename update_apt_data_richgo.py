import json
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
import os
import MySQLdb
from MySQLdb.cursors import DictCursor
from supabase import create_client, Client

from apt_value import get_APT_transactions, get_APT_info

# Load environment variables from the .env file
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


try:
    # TODO: 리치고 실거래 업뎃
    # payload = {"danjiId": "a9ylRld", "pyeongType": 34, "tradeType": "Rent", "limit": 1000, "offset": 0}
    # url = "https://api-m.richgo.ai/api/data/danji/molit/history?"
    # headers = {
    #     'Referer': 'https://m.richgo.ai/',
    #     'Content-Type': 'application/json'  # 추가된 부분: JSON 형식임을 명시
    # }
    # r = requests.post(url, headers=headers, json=payload)
    #
    # print(r.status_code)
    # print(r.text)
    #
    # if r.status_code == 200:  # 상태 코드가 200일 때만 JSON을 파싱
    #     data = r.json()['result']['items']
    #     for d in data:
    #         print(d)
    # else:
    #     print(f"Error: {r.status_code}")

    # Create a cursor to interact with the database
    response = supabase.table('APTInfo').select('name, PY, seq, description', count='exact').gt("id", 251).eq('status', 1).execute()
    for r in response.data:
        ####
        apt_name = r['name']
        PY = r['PY']
        print(f"{apt_name} - {PY}")

        apt_info = {
            'desc': r['description'],
            'seq': r['seq'],
            'name': r['name'],
        }

        query_url = f"https://api-m.richgo.ai/api/data/search?s={apt_name}&danji=true&officetel=true&region=true&goodnews=true&education=true&parcel=true&limit=10"
        headers = {
            'Referer': f'https://m.richgo.ai/'
        }
        r = requests.get(query_url, headers=headers)

        r_id = r.json()['result']['apartList'][0]['danjiId']
        print(r_id)

        # TODO: 주석 해제 필요
        response = supabase.table('APTInfo').update({'r_id': r_id}).eq('name', apt_name).execute()
        print("업데이트 완료!!")


except MySQLdb.Error as e:
    print("MySQL Error:", e)

finally:
    # Close the cursor and connection
    # cur.close()
    # connection.close()

    print('Finished')
