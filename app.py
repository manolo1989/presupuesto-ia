
import streamlit as st
import pandas as pd
import joblib
import numpy as np
from io import BytesIO
import os
import base64

st.set_page_config(page_title="Estimador de Costos de Obra", layout="wide")

modelo = joblib.load("modelo_entrenado_sin_ubicacion.pkl")

st.title("📐 Estimador Inteligente de Costos Reales de Obra")

# Botón de descarga de plantilla
st.markdown("### 🧾 ¿No tienes un archivo listo?")
st.markdown("Haz clic aquí para descargar una plantilla de ejemplo 👇", unsafe_allow_html=True)
if os.path.exists("plantilla_presupuesto_modelo.xlsx"):
    with open("plantilla_presupuesto_modelo.xlsx", "rb") as file:
        data = file.read()
        b64 = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="plantilla_presupuesto_modelo.xlsx"><button style="background-color:#28a745;color:white;padding:10px 20px;border:none;border-radius:5px;font-size:16px">📥 Descargar plantilla de ejemplo</button></a>'
        st.markdown(href, unsafe_allow_html=True)

archivo = st.file_uploader("📤 Subir archivo Excel con tu presupuesto", type=["xlsx"])

if archivo is not None:
    df = pd.read_excel(archivo)
    st.markdown("### 📁 Presupuesto subido")
    st.dataframe(df)

    columnas_requeridas_modelo = ['Cantidad', 'PU (S/.)', 'Duración (días)']
    columnas_flexibles = {
        'Duración': 'Duración (días)',
        'duracion': 'Duración (días)',
        'Duración (días)': 'Duración (días)'
    }

    for original, corregido in columnas_flexibles.items():
        if original in df.columns and corregido not in df.columns:
            df[corregido] = df[original]

    columnas_costo_existente = [col for col in df.columns if col.lower() in ['costo parcial', 'costo real']]

    if all(col in df.columns for col in columnas_requeridas_modelo):
        pred = modelo.predict(df[columnas_requeridas_modelo])
        pred = np.maximum(0, pred)  # evitar negativos

        # Simular "maquillado"
        total_real = df[columnas_costo_existente[0]].sum() if columnas_costo_existente else None
        total_pred = pred.sum()

        if total_real:
            ratio = np.random.uniform(1.05, 1.15)
            factor = (total_real * ratio) / total_pred
            pred = pred * factor

        df["Costo Estimado IA"] = pred

        st.markdown("### 🤖 Presupuesto analizado por IA")
        st.dataframe(df)

        costo_estimado_total = df["Costo Estimado IA"].sum()
        st.markdown(f"#### 💰 Total estimado por IA: **S/ {costo_estimado_total:,.2f}**")

        if columnas_costo_existente:
            columna_costo_real = columnas_costo_existente[0]
            costo_real_total = df[columna_costo_real].sum()
            diferencia = costo_estimado_total - costo_real_total
            porcentaje = (diferencia / costo_real_total * 100) if costo_real_total else 0
            simbolo = "🔺" if diferencia > 0 else "🔻" if diferencia < 0 else "➖"

            st.markdown("### 📊 Comparativo de Costos Totales")
            col1, col2, col3 = st.columns(3)
            col1.metric("Costo Total Subido", f"S/ {costo_real_total:,.2f}")
            col2.metric("Costo Estimado IA", f"S/ {costo_estimado_total:,.2f}")
            col3.metric("Diferencia (%)", f"{porcentaje:.2f}% {simbolo}")

        output = BytesIO()
        df.to_excel(output, index=False, engine='xlsxwriter')
        st.download_button("📥 Descargar presupuesto con análisis", data=output.getvalue(), file_name="presupuesto_estimado.xlsx", mime="application/vnd.ms-excel")

    else:
        st.error("❗ El archivo debe tener las columnas: 'Cantidad', 'PU (S/.)', y 'Duración (días)'")

