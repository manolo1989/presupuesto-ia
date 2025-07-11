
import streamlit as st
import pandas as pd
import joblib
import io

st.set_page_config(page_title="Estimador de Costo Real", layout="centered")

st.title("Sistema Inteligente para Estimar Costo Real de Presupuestos de Obra")
st.markdown("Sube tu archivo Excel con partidas")

uploaded_file = st.file_uploader("Drag and drop file here", type=["xlsx"])

if uploaded_file:
    df_pred = pd.read_excel(uploaded_file)

    st.subheader("Vista previa del presupuesto cargado")
    st.dataframe(df_pred)

    columnas_requeridas = ['Cantidad', 'PU (S/.)', 'Duración (días)', 'Ubicación']
    modelo = joblib.load("modelo_costos_entrenado.pkl")

    df_pred["Costo Real (S/.) (Modelo)"] = modelo.predict(df_pred[columnas_requeridas])

    st.subheader("Resultados con estimación del modelo")
    st.dataframe(df_pred[["Item", "Partida", "Costo Real (S/.) (Modelo)"]])

    # Crear archivo Excel en memoria para descarga
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_pred.to_excel(writer, index=False, sheet_name='Resultados')
        writer.save()
    processed_data = output.getvalue()

    st.download_button(
        label="📥 Descargar resultados",
        data=processed_data,
        file_name="resultados_modelo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
