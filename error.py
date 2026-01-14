import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# User input for number of repetitions and error weights
n = st.slider('Number of repetitions (n)', 10, 1000, 50)
alpha = st.slider('Weight for absolute error (α)', 0.0, 2.0, 1.0)
beta = st.slider('Weight for relative error (β)', 0.0, 2.0, 0.5)

# Error values
e = 0.5  # Absolute error (°C)
p = 0.02  # Relative error (2%)
A = 100  # Initial value (for relative error)

# Calculating errors
absolute_error = np.array([n * e for n in range(1, n + 1)])
relative_error = A * ((1 + p)**np.arange(1, n + 1) - 1)

# Total combined error (weighted sum)
total_error = alpha * absolute_error + beta * relative_error

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(range(1, n + 1), absolute_error, label='Absolute Error', color='blue')
ax.plot(range(1, n + 1), relative_error, label='Relative Error', color='red')
ax.plot(range(1, n + 1), total_error, label='Total Error', color='purple')

ax.set_title('Error Accumulation Comparison')
ax.set_xlabel('Number of repetitions (n)')
ax.set_ylabel('Error size')
ax.set_yscale('log')  # Log scale
ax.legend()

# Display the plot
st.pyplot(fig)

# Display values
st.write(f"Final Absolute Error: {absolute_error[-1]:.2f} °C")
st.write(f"Final Relative Error: {relative_error[-1]:.2f} %")
st.write(f"Final Total Error: {total_error[-1]:.2f}")
