
import streamlit as st
import pandas as pd
import joblib
from io import BytesIO
import os

# Configurar página
st.set_page_config(page_title="Estimador de Costos de Obra", layout="wide")

# Cargar modelo entrenado
modelo = joblib.load("modelo_entrenado_sin_ubicacion.pkl")

# Encabezado
st.title("📐 Estimador Inteligente de Costos Reales de Obra")

# Descargar plantilla con estilo llamativo
st.markdown("### 🧾 ¿No tienes un archivo listo?")
st.markdown("Haz clic aquí para descargar una plantilla de ejemplo 👇", unsafe_allow_html=True)
if os.path.exists("plantilla_presupuesto_modelo.xlsx"):
    with open("plantilla_presupuesto_modelo.xlsx", "rb") as file:
        st.download_button(
            "🟢 Descargar plantilla de ejemplo",
            data=file,
            file_name="plantilla_presupuesto_modelo.xlsx",
            mime="application/vnd.ms-excel"
        )

# Subir archivo
archivo = st.file_uploader("📤 Subir archivo Excel con tu presupuesto", type=["xlsx"])

if archivo is not None:
    df = pd.read_excel(archivo)
    st.markdown("### 🗂️ Presupuesto subido", unsafe_allow_html=True)
    st.dataframe(df.style.set_properties(**{'background-color': '#1f1f1f', 'color': 'white'}), use_container_width=True)

    columnas_requeridas = ['Cantidad', 'PU (S/.)', 'Duración']
    columnas_costo_existente = [col for col in df.columns if col.lower() in ['costo parcial', 'costo real']]

    if all(col in df.columns for col in columnas_requeridas):
        df["Costo Estimado IA"] = modelo.predict(df[columnas_requeridas])
        st.markdown("### 🧠 Presupuesto analizado por IA", unsafe_allow_html=True)
        st.dataframe(df.style.set_properties(**{'background-color': '#fff3cd', 'color': 'black'}), use_container_width=True)

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

        # Descargar resultados
        output = BytesIO()
        df.to_excel(output, index=False, engine='xlsxwriter')
        st.download_button("📥 Descargar presupuesto con análisis", data=output.getvalue(), file_name="presupuesto_estimado.xlsx", mime="application/vnd.ms-excel")

    else:
        st.error("❗ El archivo debe tener las columnas: 'Cantidad', 'PU (S/.)', y 'Duración'")
