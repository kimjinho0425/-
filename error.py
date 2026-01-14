import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 사용자 입력 받기
n = st.slider('반복 횟수 (n)', 10, 1000, 50)
alpha = st.slider('절대오차 가중치 (α)', 0.0, 2.0, 1.0)  # alpha는 절대오차 가중치
# beta는 이제 필요없으므로 제거됨

# 오차 계산
e = 0.5  # 절대오차 (°C)
p = 0.02  # 비율오차 (2%)
A = 100  # 초기 값 (습도 센서 초기값)

# 절대오차 계산 (등차수열)
E_absolute = np.array([e * n for n in range(1, n + 1)])

# 비율오차 계산 (등비수열)
E_relative = A * ((1 + p)**np.arange(1, n + 1) - 1)

# 복합 오차 계산 (절대오차 + 비율오차)
E_total = E_absolute + E_relative  # 더하는 형태로 복합 오차 계산

# 결과 출력
st.write(f"최종 절대오차: {E_absolute[-1]:.2f} °C")
st.write(f"최종 비율오차: {E_relative[-1]:.2f} %")
st.write(f"최종 복합오차: {E_total[-1]:.2f}")

# 그래프 시각화
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(range(1, n + 1), E_absolute, label='Absolute Error', color='blue')
ax.plot(range(1, n + 1), E_relative, label='Relative Error', color='red')
ax.plot(range(1, n + 1), E_total, label='Total Error', color='purple')

ax.set_title('Error Accumulation Comparison')
ax.set_xlabel('Number of repetitions (n)')
ax.set_ylabel('Error size')
ax.set_yscale('log')  # Log scale
ax.legend()

# 그래프 출력
st.pyplot(fig)
