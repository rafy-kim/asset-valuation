# 샘플 Python 스크립트입니다.

# ⌃R을(를) 눌러 실행하거나 내 코드로 바꿉니다.
# 클래스, 파일, 도구 창, 액션 및 설정을 어디서나 검색하려면 ⇧ 두 번을(를) 누릅니다.


import requests

service_key = "fYFEUoGn3%2F8sQSQTmroyIKSmd0OwscfuRo6c8NMy2Eo3k%2BV8A65BUJb9VCx%2F%2F4gI0N5NbEzvcRA%2FzmNkVzl9dg%3D%3D"
LAWD_CD = "11110"
DEAL_YMD = "201512"

# url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptRent'
# params = {'serviceKey': 'fYFEUoGn3%2F8sQSQTmroyIKSmd0OwscfuRo6c8NMy2Eo3k%2BV8A65BUJb9VCx%2F%2F4gI0N5NbEzvcRA%2FzmNkVzl9dg%3D%3D', 'LAWD_CD': '11110', 'DEAL_YMD': '201512' }
#
# response = requests.get(url, params=params)
# print(response)
# print(response.content)

url = f'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptRent?serviceKey={service_key}&LAWD_CD={LAWD_CD}&DEAL_YMD={DEAL_YMD}&type=json'
response = requests.get(url)
print(response.content)

def print_hi(name):
    # 스크립트를 디버그하려면 하단 코드 줄의 중단점을 사용합니다.
    print(f'Hi, {name}')  # 중단점을 전환하려면 ⌘F8을(를) 누릅니다.


# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
    print_hi('PyCharm')

# https://www.jetbrains.com/help/pycharm/에서 PyCharm 도움말 참조
