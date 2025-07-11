
import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# Estilos personalizados
st.markdown("""
<style>
    body {
        background-color: #f2f2f2;
    }
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
    }
    h1 {
        color: #f7b733;
        text-align: center;
        font-size: 36px;
    }
    .stButton>button {
        background-color: #f7b733;
        color: black;
        font-weight: bold;
        border-radius: 8px;
        padding: 8px 20px;
    }
    .stDownloadButton>button {
        background-color: #393e46;
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Cargar modelo entrenado
modelo = joblib.load("modelo_con_partida_duracion_fecha.pkl")

# Título
st.markdown("<h1>🧱 Estimador de Costos de Obra</h1>", unsafe_allow_html=True)
st.markdown("#### Estima el costo real por partida según duración del proyecto y fecha de inicio")

# Subida de archivo
archivo = st.file_uploader("📂 Sube tu archivo Excel (.xlsx)", type=["xlsx"])

if archivo is not None:
    df_pred = pd.read_excel(archivo)
    st.markdown("### 📋 Presupuesto Cargado")
    st.dataframe(df_pred)

    # Extraer el año de la fecha de inicio
    df_pred["Año de Inicio"] = pd.to_datetime(df_pred["Fecha de Inicio"]).dt.year

    columnas_requeridas = ["Partida", "Duración (días)", "Año de Inicio"]
    if all(col in df_pred.columns for col in columnas_requeridas):
        df_pred["Costo Real (S/.) (Modelo)"] = modelo.predict(df_pred[columnas_requeridas])
        st.markdown("### 🧮 Resultados del Modelo")
        st.dataframe(df_pred)

        # Descargar
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_pred.to_excel(writer, index=False)
        st.download_button("📥 Descargar Resultados", data=output.getvalue(), file_name="presupuesto_estimado.xlsx")
    else:
        st.error("⚠️ Tu archivo debe tener las columnas: 'Partida', 'Duración (días)', 'Fecha de Inicio'")
