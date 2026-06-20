import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ======================================
# CONFIGURACIÓN
# ======================================

st.set_page_config(
    page_title="Figuras de Lissajous",
    page_icon="📈",
    layout="wide"
)

st.title("Figuras de Lissajous Interactivas")

st.markdown("""
Esta aplicación permite explorar cómo las amplitudes,
frecuencias, desfases y formas de onda modifican las
figuras de Lissajous.
""")

# ======================================
# SIDEBAR
# ======================================

st.sidebar.header("Parámetros")

Ax = st.sidebar.slider(
    "Amplitud Ax",
    1.0, 10.0, 3.0, 0.1
)

Ay = st.sidebar.slider(
    "Amplitud Ay",
    1.0, 10.0, 2.0, 0.1
)

wx = st.sidebar.slider(
    "Frecuencia ωx",
    1, 10, 3
)

wy = st.sidebar.slider(
    "Frecuencia ωy",
    1, 10, 2
)

delta = st.sidebar.slider(
    "Desfase δ (rad)",
    0.0,
    float(2*np.pi),
    float(np.pi/4),
    0.01
)

tipo = st.sidebar.selectbox(
    "Tipo de señal",
    ["Sinusoidal", "Triangular", "Cuadrada"]
)

# ======================================
# TIEMPO
# ======================================

t = np.linspace(0, 2*np.pi, 10000)

# ======================================
# GENERACIÓN DE SEÑALES
# ======================================

if tipo == "Sinusoidal":

    x = Ax * np.sin(wx * t)
    y = Ay * np.sin(wy * t + delta)

elif tipo == "Triangular":

    x = Ax * signal.sawtooth(wx * t, width=0.5)
    y = Ay * signal.sawtooth(wy * t + delta, width=0.5)

else:

    x = Ax * signal.square(wx * t)
    y = Ay * signal.square(wy * t + delta)

# ======================================
# FIGURA PRINCIPAL
# ======================================

fig, ax = plt.subplots(figsize=(6, 6))

ax.plot(x, y)

ax.set_title("Figura de Lissajous")
ax.set_xlabel("x(t)")
ax.set_ylabel("y(t)")
ax.grid(True)

ax.set_aspect('equal')

st.pyplot(fig)

# ======================================
# INFORMACIÓN
# ======================================

st.subheader("Parámetros actuales")

st.latex(
    rf"x(t)= {Ax:.1f}\,f({wx}t)"
)

st.latex(
    rf"y(t)= {Ay:.1f}\,f({wy}t+{delta:.2f})"
)

st.write(f"Razón de frecuencias: {wx}:{wy}")

# ======================================
# ANÁLISIS INVERSO
# ======================================

st.divider()

st.header("Análisis Inverso")

st.write("""
Presione el botón para generar una figura con parámetros ocultos.
Intente estimar:

- Ax
- Ay
- ωx
- ωy
- δ
""")

if "oculta_generada" not in st.session_state:
    st.session_state.oculta_generada = False

# --------------------------------------
# Generar nueva figura oculta
# --------------------------------------

if st.button("Generar figura oculta"):

    st.session_state.Ax = np.random.randint(1, 6)
    st.session_state.Ay = np.random.randint(1, 6)

    st.session_state.wx = np.random.randint(1, 6)
    st.session_state.wy = np.random.randint(1, 6)

    st.session_state.delta = np.random.choice([
        0,
        np.pi / 6,
        np.pi / 4,
        np.pi / 3,
        np.pi / 2
    ])

    st.session_state.oculta_generada = True

# --------------------------------------
# Mostrar figura oculta
# --------------------------------------

if st.session_state.oculta_generada:

    t2 = np.linspace(0, 2*np.pi, 10000)

    x2 = st.session_state.Ax * np.sin(
        st.session_state.wx * t2
    )

    y2 = st.session_state.Ay * np.sin(
        st.session_state.wy * t2
        + st.session_state.delta
    )

    # Figura más pequeña
    fig2, ax2 = plt.subplots(figsize=(3, 3))

    ax2.plot(x2, y2, linewidth=2)

    ax2.set_title("Figura Oculta")

    # Mantener ejes pero quitar cuadrícula
    ax2.grid(False)

    ax2.set_xlabel("x")
    ax2.set_ylabel("y")

    ax2.set_aspect('equal')

    st.pyplot(fig2)

    st.info(
        "Intente estimar Ax, Ay, ωx, ωy y δ observando únicamente la forma de la figura."
    )

    # ----------------------------------
    # Mostrar respuesta
    # ----------------------------------

    if st.button("Mostrar respuesta"):

        st.success(
            f"""
Ax = {st.session_state.Ax}

Ay = {st.session_state.Ay}

ωx = {st.session_state.wx}

ωy = {st.session_state.wy}

δ = {st.session_state.delta:.3f} rad
"""
        )