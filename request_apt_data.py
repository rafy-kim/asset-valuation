# 1-1. 데이터 가져오기
import requests
import datetime
import xml.etree.ElementTree as ET
import pandas as pd
import chardet

url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?"
service_key = "fYFEUoGn3%2F8sQSQTmroyIKSmd0OwscfuRo6c8NMy2Eo3k%2BV8A65BUJb9VCx%2F%2F4gI0N5NbEzvcRA%2FzmNkVzl9dg%3D%3D"
base_date = "202001"
gu_code = '11215'  ## 법정동 코드 5자리라면, 구 단위로 데이터를 확보하는 것. 11215 = 광진구

payload = "LAWD_CD=" + gu_code + "&" + \
          "DEAL_YMD=" + base_date + "&" + \
          "serviceKey=" + service_key + "&"


def get_items(response):
    root = ET.fromstring(response.content)
    item_list = []
    for child in root.find('body').find('items'):
        elements = child.findall('*')
        data = {}
        for element in elements:
            tag = element.tag.strip()
            text = element.text.strip()
            # print tag, text
            data[tag] = text
        item_list.append(data)
    return item_list


# res = requests.get(url + payload)
# print(res)
#
# items_list = get_items(res)
# items = pd.DataFrame(items_list)
# # items.head()
# print(items.head())


# code_file = "국토교통부_전국 법정동_20240513.csv"
# # # 파일의 인코딩 감지
# # with open(code_file, 'rb') as f:
# #     result = chardet.detect(f.read())
# #     detected_encoding = result['encoding']
# #
# # # 감지된 인코딩으로 파일 읽기
# # code = pd.read_csv(code_file, sep='\t', encoding=detected_encoding)
# # print(detected_encoding)
#
# df = pd.read_csv(code_file, sep=',', encoding='EUC-KR')
# #
# # 첫 몇 줄 출력하여 열 개수 확인
# print(df.head())
# print(df.columns)
# print(len(df.columns))
#
# df = df[df['삭제일자'].isna()]
#
# df['법정동코드'] = df['법정동코드'].astype(str)
# df['법정동코드'] = df['법정동코드'].str[:5]
#
# # 시도명과 시군구명을 합친 새로운 컬럼 생성
# df['법정동명'] = df['시도명'] + " " + df['시군구명'].fillna('')
#
# df = df[['법정동코드', '법정동명']]
# df = df.drop_duplicates()
# #
# # print(df.head())
# print(df)

csv_file_path = 'unique_values.csv'
df = pd.read_csv(csv_file_path, sep=',')

print(df)

# 법정동코드의 끝 3자리가 '000'인 행을 필터링
df['법정동코드'] = df['법정동코드'].astype(str)
# df_filtered = df[df['법정동코드'].str[-3:] == '000']
df_filtered = df[df['법정동코드'].str[-3:] != '000']

# 결과 확인
print(df_filtered)

# CSV 파일로 저장
file_path = 'filtered_code.csv'
df_filtered.to_csv(file_path, index=False, encoding='utf-8')


