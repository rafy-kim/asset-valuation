import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 경로 설정 (예시: 나눔폰트)
font_path = '/System/Library/Fonts/AppleSDGothicNeo.ttc'  # 애플고딕 경로로 수정
# 폰트 설정
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)


def calculate_average_with_none(values):
    # None을 제외한 실제 값만 추출
    valid_values = [value for value in values if value is not None]

    # 리스트가 비어있는 경우 예외 처리
    if not valid_values:
        return None

    # 평균 계산
    average = sum(valid_values) / len(valid_values)
    return average


def draw_plot(title, dataset1, dataset2):
    # 데이터셋을 기반으로 X축과 Y축 데이터 추출 (소팅된 순서대로)
    x_values = sorted(set(dataset1.keys()) | set(dataset2.keys()))  # 소팅된 X값 리스트

    # dataset1의 값들을 저장하는 리스트
    y_values_dataset1 = []

    # dataset1과 dataset2의 비율을 저장하는 리스트
    y_values_ratio = []

    # dataset2의 값들을 저장하는 리스트
    y_values_dataset2 = []

    previous_value1 = None
    previous_value2 = None

    for x in x_values:
        value1 = dataset1.get(x)
        value2 = dataset2.get(x)

        # 이전 값이 없는 경우, 이전 값을 사용하고 현재 값을 업데이트
        if value1 is None and previous_value1 is not None:
            value1 = previous_value1
        if value2 is None and previous_value2 is not None:
            value2 = previous_value2

        # 이전 값 업데이트
        previous_value1 = value1
        previous_value2 = value2

        # dataset1과 dataset2의 값들 저장
        y_values_dataset1.append(value1)

        # 나눗셈 수행
        if value1 is not None and value2 is not None and value2 != 0:
            ratio = value1 / (value2 * 12)
        else:
            ratio = None
        y_values_ratio.append(ratio)

        # # dataset2의 값들 저장
        # y_values_dataset2.append(value2)

    # 평균 계산
    average_ratio = calculate_average_with_none(y_values_ratio)

    # 차트 생성 및 플로팅
    fig, ax1 = plt.subplots(figsize=(14, 5))  # 가로 10, 세로 6 크기로 조절

    # dataset1 그래프
    color = 'tab:red'
    ax1.set_xlabel('YYYYMM')
    ax1.set_ylabel('매매가', color=color)
    ax1.plot(x_values, y_values_dataset1, color=color, marker='o', label='매매가')

    # 두 번째 Y축을 만들어서 dataset2 그래프 플로팅
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('PER', color=color)
    ax2.plot(x_values, y_values_ratio, color=color, marker='o', label='PER')

    # # dataset1 / dataset2 비율 그래프
    # ax2.plot(x_values, y_values_ratio, color='g', marker='o', label='Dataset1 / Dataset2 Ratio')

    # 수평선으로 평균값 표시
    ax2.axhline(y=average_ratio, color='r', linestyle='--', label='PER 평균')
    ax2.axhline(y=35, color='g', linestyle='--', label='PER 35')
    ax2.axhline(y=30, color='b', linestyle='--', label='PER 30')

    # 범례 추가
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    # 제목 추가
    plt.title(title)

    # X축 눈금 간격 조절
    plt.xticks(rotation=45, ha='right')  # 눈금 레이블을 45도 기울여 표시하고, 오른쪽 정렬
    plt.xticks(range(0, len(x_values), len(x_values) // 10), x_values[::len(x_values) // 10])  # X축 눈금 조절

    # 그래프 표시
    plt.show()
