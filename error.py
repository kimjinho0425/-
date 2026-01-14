import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 사용자 입력 받기
n = st.slider('반복 횟수 (n)', 10, 1000, 50)

# 센서에 맞는 가중치 설정 (절대 오차 및 비율 오차)
alpha = st.slider('온도 절대오차 가중치 (α)', 0.0, 2.0, 1.0)  # 온도 절대오차 가중치
beta = st.slider('습도 비율오차 가중치 (β)', 0.0, 2.0, 1.0)  # 습도 비율오차 가중치
gamma = st.slider('압력 절대오차 가중치 (γ)', 0.0, 2.0, 1.0)  # 압력 절대오차 가중치

# 오차 계산 (온도, 습도, 압력 센서)
e = 0.5  # 절대오차 (°C)
p = 0.02  # 비율오차 (2%)
A = 100  # 초기 값 (습도 센서 초기값)

# 온도 센서: 절대오차 (선형 증가)
E_temperature_absolute = np.array([e * n for n in range(1, n + 1)])  # 온도 센서 절대 오차

# 습도 센서: 비율오차 (지수 증가)
E_humidity_relative = A * ((1 + p)**np.arange(1, n + 1) - 1)  # 습도 센서 비율 오차

# 압력 센서: 절대오차 (선형 증가)
E_pressure_absolute = np.array([e * n for n in range(1, n + 1)])  # 압력 센서 절대 오차

# 복합 오차 계산 (각 센서의 절대 오차 + 비율 오차 * 가중치)
E_temperature_total = (alpha * E_temperature_absolute)  # 온도 센서
E_humidity_total = (beta * E_humidity_relative)  # 습도 센서
E_pressure_total = (gamma * E_pressure_absolute)  # 압력 센서

# 결과 출력
st.write(f"최종 온도 절대오차: {E_temperature_absolute[-1]:.2f} °C")
st.write(f"최종 습도 비율오차 (절대값): {E_humidity_relative[-1]:.2f} units")
st.write(f"최종 압력 절대오차: {E_pressure_absolute[-1]:.2f} hPa")
st.write(f"최종 온도 복합오차: {E_temperature_total[-1]:.2f}")
st.write(f"최종 습도 복합오차: {E_humidity_total[-1]:.2f}")
st.write(f"최종 압력 복합오차: {E_pressure_total[-1]:.2f}")

# 그래프 시각화
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(range(1, n + 1), E_temperature_absolute, label='Temperature Absolute Error', color='blue')
ax.plot(range(1, n + 1), E_humidity_relative, label='Humidity Relative Error', color='red')
ax.plot(range(1, n + 1), E_pressure_absolute, label='Pressure Absolute Error', color='green')

ax.plot(range(1, n + 1), E_temperature_total, label='Temperature Total Error', color='purple')
ax.plot(range(1, n + 1), E_humidity_total, label='Humidity Total Error', color='orange')
ax.plot(range(1, n + 1), E_pressure_total, label='Pressure Total Error', color='yellow')

ax.set_title('Sensor Error Accumulation Comparison')
ax.set_xlabel('Number of repetitions (n)')
ax.set_ylabel('Error size')

# 로그 스케일로 표시
ax.set_yscale('log')  # Log scale for better visualization of large differences
ax.legend()

# 그래프 출력
st.pyplot(fig)
