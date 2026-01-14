import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 올바른 경로로 업로드된 폰트 파일 경로 설정
font_path = "/mnt/data/D8B30F8C-97C9-4E6D-A499-810A6B22D631.ttf"  # 업로드한 파일 경로로 수정
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

# 사용자 입력 받기
n = st.slider('반복 횟수 (n)', 10, 1000, 50)
alpha = st.slider('절대오차 가중치 (α)', 0.0, 2.0, 1.0)
beta = st.slider('비율오차 가중치 (β)', 0.0, 2.0, 0.5)

# 오차 계산
e = 0.5  # 절대오차 (°C)
p = 0.02  # 비율오차 (2%)
A = 100  # 초기 값 (습도 센서 초기값)

# 절대오차 계산 (등차수열)
E_absolute = np.array([n * e for n in range(1, n + 1)])

# 비율오차 계산 (등비수열)
E_relative = A * ((1 + p)**np.arange(1, n + 1) - 1)

# 복합 오차 계산
E_total = alpha * E_absolute + beta * E_relative

# 시각화
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(range(1, n + 1), E_absolute, label='절대오차', color='blue')
ax.plot(range(1, n + 1), E_relative, label='비율오차', color='red')
ax.plot(range(1, n + 1), E_total, label='복합 오차', color='purple')

ax.set_title('오차 누적 비교')
ax.set_xlabel('반복 횟수 (n)')
ax.set_ylabel('오차 크기')
ax.set_yscale('log')  # 로그 스케일
ax.legend()

# 그래프 출력
st.pyplot(fig)

# 값 표시
st.write(f"최종 절대오차: {E_absolute[-1]:.2f} °C")
st.write(f"최종 비율오차: {E_relative[-1]:.2f} %")
st.write(f"최종 복합오차: {E_total[-1]:.2f}")
