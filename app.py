
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Predicción de Presupuestos", layout="wide", page_icon="📊")

st.markdown("## 📊 Sistema de Predicción de Presupuestos de Obra")
st.markdown("Cargue su archivo Excel para predecir el Precio Unitario (PU) o simular el costo real de sus partidas.")
st.markdown("---")

# Colores y estilos
st.markdown(
    """
    <style>
    body {
        background-color: #0E1117;
        color: white;
    }
    .css-1d391kg {
        background-color: #1E1E1E;
    }
    .stDataFrame tbody tr td {
        background-color: #222;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Subida de archivo
archivo = st.file_uploader("Suba su archivo Excel aquí", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)
    modelo = joblib.load("modelo_pu.pkl")

    df_copy = df.copy()
    df_copy["PU (S/.)"] = df_copy["PU (S/.)"].fillna(0)

    # Filtrar las que necesitan predicción
    df_pred = df_copy[df_copy["PU (S/.)"] == 0]

    if not df_pred.empty:
        st.markdown("### 🟢 Presupuesto cargado (faltan PU)")
        st.dataframe(df_pred.style.set_properties(**{'background-color': '#0a4', 'color': 'white'}))

        # Predecir PU
        df_pred_input = df_pred[["Partida", "Unidad", "Cantidad"]]
        df_pred["PU (S/.)"] = modelo.predict(df_pred_input)

        df_pred["Costo Estimado"] = df_pred["Cantidad"] * df_pred["PU (S/.)"]

        st.markdown("### 🟡 Resultado de predicción")
        st.dataframe(df_pred.style.set_properties(**{'background-color': '#cc0', 'color': 'black'}))

    else:
        st.markdown("### 🟢 Presupuesto cargado (ya tiene PU)")
        st.dataframe(df_copy.style.set_properties(**{'background-color': '#0a4', 'color': 'white'}))

        df_copy["Costo Estimado"] = df_copy["Cantidad"] * df_copy["PU (S/.)"]

        st.markdown("### 🟡 Simulación de Costo Real Estimado")
        st.dataframe(df_copy.style.set_properties(**{'background-color': '#cc0', 'color': 'black'}))
