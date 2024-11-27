import json
from statistics import mean

import requests
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

# payload = {'key1': 'value1', 'key2': 'value2'}
# r = requests.get('https://exam.com/get', params=payload)


def convert_to_int(s):
    if s == '':
        return 0
    i = 0
    s = s.replace(',', '')
    if '억' in s:
        i += int(s.split('억 ')[0]) * 10000
        if s.split('억 ')[1]:
            i += int(s.split('억 ')[1])
    else:
        i += int(s)
    return i

def get_key(secret):
    key_bytes = secret.encode('utf-8')
    length = len(key_bytes)

    if length < 16:
        adjusted_key = key_bytes.ljust(16, b'\0')
    elif 16 < length < 24:
        adjusted_key = key_bytes.ljust(24, b'\0')
    elif 24 < length < 32:
        adjusted_key = key_bytes.ljust(32, b'\0')
    elif length >= 32:
        adjusted_key = key_bytes[:32]
    else:
        adjusted_key = key_bytes

    return adjusted_key

def decrypt(encrypted_text, secret):
    key = get_key(secret)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_bytes = base64.b64decode(encrypted_text)
    decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
    return decrypted_bytes.decode('utf-8')

def fetch_and_parse_key(url):
    # Fetch the URL
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful

    # Search for the getKey pattern in the response text
    pattern = r'getKey\("(\d+)"\)'
    match = re.search(pattern, response.text)

    if match:
        secret = match.group(1)
        return secret
    else:
        print("Pattern not found in the response.")
        return None

def get_APT_info(apt_name):
    """
    :param apt_name: 아파트 이름
    :param PY: 평형
    :param YEAR: 거래된 년도
    :param DEAL_TYPE: 1은 매매, 2는 전세, 3은 월세
    :return: [{'date': '202212', 'avg': 294.15384615384613, 'min': 230.0, 'max': 380.0, 'cnt': 13}, ...]
    """
    apt_info = {}
    seq = ''
    r = requests.get(f'https://asil.kr/json/getAptname_ver_3_4.jsp?os=pc&aptname={apt_name}')
    tmp = r.json()[0]
    if tmp['name'] == apt_name:
        seq = tmp['seq']
        apt_info = {
            'desc': tmp['desc'],
            'seq': tmp['seq'],
            'name': tmp['name'],
        }
        print(apt_info)
        return apt_info
    else:
        print(f"이름이 동일하지 않아요: {apt_name} != {tmp['name']}")
        return 0


# ASIL은 데이터 암호화 해독 필요
def get_APT_transactions(apt_info, PY, YEAR, DEAL_TYPE):
    """
    :param apt_info: 아파트 apt_info {name, seq, desc}
    :param PY: 평형
    :param YEAR: 거래된 년도
    :param DEAL_TYPE: 1은 매매, 2는 전세, 3은 월세
    :return: [{'date': '202212', 'avg': 294.15384615384613, 'min': 230.0, 'max': 380.0, 'cnt': 13}, ...]
    """
    seq = apt_info['seq']
    headers = {'Referer': f'https://asil.kr/app/price_detail_ver_3_9.jsp?os=pc&user=0&building=apt&apt={seq}&evt={PY}py&year={YEAR}&deal={DEAL_TYPE}'}
    # TODO: sido = 11 (서울) / 41 (경기도) 주소 참조해서 변수로 바꿀 것
    if '경기' in apt_info['desc']:
        sido = 41
    else:
        sido = 11
    req_url = f"https://asil.kr/app/data/apt_price_m2_newver_6.jsp?sido={sido}&dealmode={DEAL_TYPE}&building=apt&seq={seq}&m2=&py={PY}&py_type=&isPyQuery=true&year={YEAR}&u=0&start=0&count=1000&dong_name=&order="
    # print(req_url)
    r = requests.get(req_url, headers=headers)
    data = r.json()[0]['val']
    print(data)

    url = f"https://asil.kr/app/apt_info.jsp?os=pc&apt={seq}"
    secret = fetch_and_parse_key(url)
    if secret:
        print(f"Extracted secret: {secret}")
    else:
        print("Failed to extract the secret.")

    amount = []
    for m in data:
        # 여기서 m['val']은 월간 거래 내역
        # print(m['yyyymm'])
        m_data = m['val']
        m_amount = []
        for d in m_data:
            # 여기서 m['val']은 일간 거래 내역
            # print(d['day'])
            d_data = d['val']
            for r in d_data:
                if r['reg_gbn'] == "1":
                    # 직거래는 noise가 되므로 저장하지 않음
                    continue

                # print(r['money'], r['rent'])
                d_money = decrypt(r['money'], secret)
                d_rent = decrypt(r['rent'], secret)
                # print(d_money, d_rent)

                r_money = convert_to_int(d_money)
                # print(r_money, r['rent'])
                # r['money'].split()
                if DEAL_TYPE == '3':
                    a = r_money / 10000 * 40 + int(d_rent)
                else:
                    a = r_money
                m_amount.append(a)
        if m_amount:
            amount.append({
                'date': m['yyyymm'],
                'avg': mean(m_amount),
                'min': min(m_amount),
                'max': max(m_amount),
                'cnt': len(m_amount)
            })
    return amount


# 리치고에서 데이터 가져오는 것으로 변경
def get_APT_transactions_richgo(apt_info, PY, YEAR, DEAL_TYPE):
    """
    :param apt_info: 아파트 apt_info {name, seq, desc}
    :param PY: 평형
    :param YEAR: 거래된 년도
    :param DEAL_TYPE: 1은 매매, 2는 전세, 3은 월세
    :return: [{'date': '202212', 'avg': 294.15384615384613, 'min': 230.0, 'max': 380.0, 'cnt': 13}, ...]
    """

    idx = int(DEAL_TYPE) - 1
    trade_type = ["Meme", "Jeonse", "Rent"][idx]

    r_id = apt_info['r_id']
    payload = {"danjiId": r_id, "pyeongType": PY, "tradeType": trade_type, "limit": 1000, "offset": 0}
    url = "https://api-m.richgo.ai/api/data/danji/molit/history?"
    headers = {
        'Referer': 'https://m.richgo.ai/',
        'Content-Type': 'application/json'  # 추가된 부분: JSON 형식임을 명시
    }
    r = requests.post(url, headers=headers, json=payload)

    if r.status_code != 200:  # 상태 코드가 200일 때만 JSON을 파싱
        print(f"Error: {r.status_code}")
        return False


    data = r.json()['result']['items']

    amount_dict = {}
    for d in data:
        yyyy = d['y'].split('.')[0]
        if int(yyyy) < int(YEAR):
            print(yyyy)
            break

        mm = d['y'].split('.')[1]
        yyyymm = yyyy + mm
        if yyyymm not in amount_dict:
            amount_dict[yyyymm] = []

        if DEAL_TYPE == 1:
            if d['tt'] == "직거래":
                # 직거래는 noise가 되므로 저장하지 않음
                print("직거래는 Pass")
                continue
        # r['money'].split()
        if DEAL_TYPE == '3':
            a = d['d'] / 10000 * 40 + d['p']
        else:
            a = d['p']
        amount_dict[yyyymm].append(a)
        # if yyyymm not in amount_dict:
        #     amount_dict[yyyymm] = {
        #         'tot': d['p'],
        #         'min': d['p'],
        #         'max': d['p'],
        #         'cnt': 1
        #     }
        # else:
        #     amount_dict[yyyymm]['tot'] += d['p']
        #     amount_dict[yyyymm]['min'] = min(d['p'], amount_dict[yyyymm]['min'])
        #     amount_dict[yyyymm]['max'] = max(d['p'], amount_dict[yyyymm]['max'])
        #     amount_dict[yyyymm]['cnt'] += 1


        # if m_amount:
        #     amount.append({
        #         'date': m['yyyymm'],
        #         'avg': mean(m_amount),
        #         'min': min(m_amount),
        #         'max': max(m_amount),
        #         'cnt': len(m_amount)
        #     })

    amount = []
    for date, values in amount_dict.items():
        avg = sum(values) / len(values)
        max_value = max(values)
        min_value = min(values)
        cnt = len(values)

        new_entry = {
            'avg': avg,
            'cnt': cnt,
            'max': max_value,
            'min': min_value,
            'date': date
        }
        amount.append(new_entry)

    return amount

