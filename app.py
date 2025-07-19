
import streamlit as st
import pandas as pd
import joblib
from io import BytesIO

# Configuración de la página
st.set_page_config(page_title="Estimador de Costos de Obra", layout="wide")

# Cargar el modelo entrenado
modelo = joblib.load("modelo_entrenado_sin_ubicacion.pkl")

# Encabezado principal
st.title("📐 Estimador Inteligente de Costos Reales de Obra")
st.markdown("Sube tu archivo Excel con las columnas: 'Cantidad', 'PU (S/.)', 'Duración (días)' y opcionalmente 'Costo Parcial' o 'Costo Real'.")

# Descargar plantilla de ejemplo
with open("plantilla_presupuesto_modelo.xlsx", "rb") as file:
    st.download_button("📥 Descargar plantilla de ejemplo", data=file, file_name="plantilla_presupuesto_modelo.xlsx", mime="application/vnd.ms-excel")

archivo = st.file_uploader("📤 Subir archivo Excel", type=["xlsx"])

if archivo is not None:
    df = pd.read_excel(archivo)
    st.markdown("### 🗂️ Presupuesto subido", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    columnas_requeridas = ['Cantidad', 'PU (S/.)', 'Duración (días)']
    columnas_costo_existente = [col for col in df.columns if col.lower() in ['costo parcial', 'costo real']]

    if all(col in df.columns for col in columnas_requeridas):
        df["Costo Estimado IA"] = modelo.predict(df[columnas_requeridas])

        # Mostrar resultados
        st.markdown("### 🧠 Presupuesto analizado por IA", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

        costo_ia_total = df["Costo Estimado IA"].sum()

        if columnas_costo_existente:
            columna_costo_real = columnas_costo_existente[0]
            costo_real_total = df[columna_costo_real].sum()
            diferencia = costo_ia_total - costo_real_total
            porcentaje_dif = (diferencia / costo_real_total * 100) if costo_real_total else 0
            simbolo = "🔺" if diferencia > 0 else "🔻" if diferencia < 0 else "➖"

            # Mostrar comparación visual
            st.markdown("---")
            st.markdown("### 📊 Comparativo de Costos Totales")
            col1, col2, col3 = st.columns(3)
            col1.metric("Costo Total Subido (S/.)", f"{costo_real_total:,.2f}")
            col2.metric("Costo Estimado IA (S/.)", f"{costo_ia_total:,.2f}")
            col3.metric("Diferencia (%)", f"{porcentaje_dif:.2f}% {simbolo}")

        # Descargar Excel con resultados
        output = BytesIO()
        df.to_excel(output, index=False, engine='xlsxwriter')
        st.download_button("📥 Descargar resultados", data=output.getvalue(), file_name="presupuesto_estimado.xlsx", mime="application/vnd.ms-excel")
    else:
        st.warning("❗ El archivo debe contener las columnas necesarias: 'Cantidad', 'PU (S/.)' y 'Duración (días)'")
