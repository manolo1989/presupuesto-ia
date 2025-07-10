
import streamlit as st
import pandas as pd
import numpy as np
import io

st.set_page_config(page_title="Ajuste Inteligente de Presupuesto", layout="wide")
st.title("📊 Sistema de Ajuste de Presupuesto con Simulación IA")

st.markdown("Sube un archivo Excel con tu presupuesto estimado para analizarlo y obtener un nuevo presupuesto ajustado automáticamente.")

uploaded_file = st.file_uploader("Selecciona tu archivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        df["Precio Unitario Estimado (S/.)"] = pd.to_numeric(df["Precio Unitario Estimado (S/.)"], errors="coerce")
        df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors="coerce")

        ajuste_percent = np.random.uniform(0.05, 0.15, size=len(df))
        df["Precio Unitario Ajustado (S/.)"] = np.round(df["Precio Unitario Estimado (S/.)"] * (1 + ajuste_percent), 2)
        df["Costo Parcial Ajustado (S/.)"] = np.round(df["Cantidad"] * df["Precio Unitario Ajustado (S/.)"], 2)

        st.success("✅ Análisis completado. Revisa los datos abajo.")
        st.dataframe(df, use_container_width=True)

        output = io.BytesIO()
        df.to_excel(output, index=False)
        st.download_button("📥 Descargar archivo ajustado", output.getvalue(), file_name="presupuesto_ajustado.xlsx")

    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
