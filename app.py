
import streamlit as st
import pandas as pd
import joblib
from io import BytesIO

st.set_page_config(page_title="Predicción de Presupuestos de Obra", layout="wide", page_icon="📊")

st.markdown("## 📊 Sistema de Predicción de Presupuestos de Obra con IA")
st.markdown("Cargue su archivo Excel para predecir el Precio Unitario (PU) o simular el costo real de sus partidas.")
st.markdown("---")

# Estilos personalizados
st.markdown(
    """
    <style>
    body {
        background-color: #0E1117;
        color: white;
    }
    .stDataFrame tbody tr td {
        background-color: #222;
        color: white;
    }
    .metric-label {
        font-size: 20px !important;
    }
    .metric-container {
        background-color: #1a1a1a;
        border-radius: 10px;
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

archivo = st.file_uploader("📤 Suba su archivo Excel aquí", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)
    modelo = joblib.load("modelo_pu.pkl")

    df_copy = df.copy()
    df_copy["PU (S/.)"] = df_copy["PU (S/.)"].fillna(0)

    df_pred = df_copy[df_copy["PU (S/.)"] == 0]
    df_ok = df_copy[df_copy["PU (S/.)"] > 0]

    if not df_pred.empty:
        st.markdown("### 🟢 Presupuesto cargado (faltan PU)")
        st.dataframe(df_pred.style.set_properties(**{'background-color': '#0a4', 'color': 'white'}))

        df_pred_input = df_pred[["Partida", "Unidad", "Cantidad"]]
        df_pred["PU (S/.)"] = modelo.predict(df_pred_input)
        df_pred["Costo Estimado"] = df_pred["Cantidad"] * df_pred["PU (S/.)"]

        st.markdown("### 🟡 Resultado de predicción")
        st.dataframe(df_pred.style.set_properties(**{'background-color': '#cc0', 'color': 'black'}))

        total_estimado = df_pred["Costo Estimado"].sum()
        st.markdown("### 💰 Resumen General del Presupuesto")
        st.metric("Presupuesto Estimado por IA (S/.)", f"{total_estimado:,.2f}")

        # Exportar Excel
        output = BytesIO()
        df_pred.to_excel(output, index=False)
        st.download_button("📥 Descargar resultado estimado", output.getvalue(), "resultado_estimado.xlsx", "application/vnd.ms-excel")

    elif not df_ok.empty:
        st.markdown("### 🟢 Presupuesto cargado (ya tiene PU)")
        df_ok["Costo Estimado"] = df_ok["Cantidad"] * df_ok["PU (S/.)"]
        st.dataframe(df_ok.style.set_properties(**{'background-color': '#0a4', 'color': 'white'}))

        st.markdown("### 🟡 Simulación de Costo Real Estimado")
        df_simulado = df_ok.copy()
        df_simulado["PU Simulado"] = modelo.predict(df_simulado[["Partida", "Unidad", "Cantidad"]])
        df_simulado["Costo Estimado IA"] = df_simulado["Cantidad"] * df_simulado["PU Simulado"]
        st.dataframe(df_simulado.style.set_properties(**{'background-color': '#cc0', 'color': 'black'}))

        total_cargado = df_simulado["Costo Estimado"].sum()
        total_estimado = df_simulado["Costo Estimado IA"].sum()
        diferencia = ((total_estimado - total_cargado) / total_cargado) * 100 if total_cargado else 0

        st.markdown("### 💰 Resumen Comparativo")
        col1, col2, col3 = st.columns(3)
        col1.metric("Presupuesto Cargado (S/.)", f"{total_cargado:,.2f}")
        col2.metric("Presupuesto Estimado por IA (S/.)", f"{total_estimado:,.2f}")
        col3.metric("Diferencia (%)", f"{diferencia:.2f}%")

        # Descargar resultado completo
        output = BytesIO()
        df_simulado.to_excel(output, index=False)
        st.download_button("📥 Descargar comparación completa", output.getvalue(), "comparacion_presupuesto.xlsx", "application/vnd.ms-excel")

    else:
        st.warning("⚠️ No se encontraron datos válidos para analizar.")
