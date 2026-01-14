import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sensor Error Weighting", layout="centered")

st.title("Sensor Error Model (Temperature / Humidity / Pressure)")
st.caption("Only 3 component errors + 1 total error are plotted.")

# -------------------------
# Inputs
# -------------------------
n = st.slider("Number of steps (n)", 1, 1000, 50)

st.subheader("Sensor parameters")
e_temp = st.number_input("Temperature absolute error per step (e_T)", value=0.5, min_value=0.0, step=0.1)
e_press = st.number_input("Pressure absolute error per step (e_P)", value=0.5, min_value=0.0, step=0.1)

H0 = st.number_input("Humidity baseline (H0)", value=50.0, min_value=0.0, step=1.0)
p_hum = st.number_input("Humidity relative error rate per step (p_H)", value=0.02, min_value=0.0, step=0.005, format="%.3f")

st.subheader("Weights (reliability / importance)")
alpha = st.slider("α (Temperature weight)", 0.0, 3.0, 1.0, 0.1)
beta  = st.slider("β (Humidity weight)", 0.0, 3.0, 1.0, 0.1)
gamma = st.slider("γ (Pressure weight)", 0.0, 3.0, 1.0, 0.1)

show_log = st.checkbox("Use log scale (optional)", value=False)

# -------------------------
# Model (one error type per sensor)
# -------------------------
# Temperature: absolute error (linear)
# E_T(n) = e_T * n
# Pressure: absolute error (linear)
# E_P(n) = e_P * n
# Humidity: relative error -> expressed as absolute magnitude (exponential)
# E_H(n) = H0 * ((1 + p_H)^n - 1)

k = np.arange(1, n + 1)

E_T = e_temp * k
E_P = e_press * k
E_H = H0 * ((1 + p_hum) ** k - 1)

# Apply weights
W_T = alpha * E_T
W_H = beta  * E_H
W_P = gamma * E_P

# Total = sum of the three (ONLY ONE total)
E_total = W_T + W_H + W_P

# -------------------------
# Formulas shown on the site
# -------------------------
st.subheader("Formulas used")
st.latex(r"E_T(n)=e_T\cdot n \quad \text{(Temperature: absolute, linear)}")
st.latex(r"E_H(n)=H_0\left((1+p_H)^n-1\right) \quad \text{(Humidity: relative -> absolute magnitude, exponential)}")
st.latex(r"E_P(n)=e_P\cdot n \quad \text{(Pressure: absolute, linear)}")
st.latex(r"\text{Total}(n)=\alpha E_T(n)+\beta E_H(n)+\gamma E_P(n)")

# Quick table-like summary (simple + clean)
st.markdown(
    f"""
**Error type by sensor**
- Temperature: **Absolute error** (linear)
- Humidity: **Relative error** (exponential), displayed as **absolute magnitude**
- Pressure: **Absolute error** (linear)
"""
)

# -------------------------
# Final values (clean)
# -------------------------
st.subheader("Final errors at step n")
col1, col2 = st.columns(2)
with col1:
    st.metric("Temperature (weighted)", f"{W_T[-1]:.4f}")
    st.metric("Humidity (weighted)", f"{W_H[-1]:.4f}")
    st.metric("Pressure (weighted)", f"{W_P[-1]:.4f}")
with col2:
    st.metric("TOTAL (sum of three)", f"{E_total[-1]:.4f}")
    st.caption("TOTAL = Temperature + Humidity + Pressure (after weights)")

# -------------------------
# Plot (ONLY 3 components + 1 total)
# -------------------------
st.subheader("Graph")
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(k, W_T, label="Temperature error (weighted)")
ax.plot(k, W_H, label="Humidity error (weighted)")
ax.plot(k, W_P, label="Pressure error (weighted)")
ax.plot(k, E_total, label="TOTAL error (sum)", linewidth=3)

ax.set_xlabel("Step (n)")
ax.set_ylabel("Error magnitude")
ax.set_title("Linear vs Exponential Growth + Total Sum")

if show_log:
    ax.set_yscale("log")

ax.legend()
st.pyplot(fig)
