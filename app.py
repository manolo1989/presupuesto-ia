
import streamlit as st
import pandas as pd
import joblib
import io

st.set_page_config(page_title="Estimador de Costo Real", layout="centered")

st.title("Estimador Inteligente de Costos Reales de Obra")
st.markdown("Sube tu archivo Excel con las columnas: 'Cantidad', 'PU (S/.)', 'Duración (días)', 'Ubicación'")

uploaded_file = st.file_uploader("Sube tu archivo .xlsx", type=["xlsx"])

if uploaded_file:
    df_pred = pd.read_excel(uploaded_file)

    st.subheader("Presupuesto cargado")
    st.dataframe(df_pred)

    modelo = joblib.load("modelo_costos_entrenado.pkl")
    columnas_requeridas = ['Cantidad', 'PU (S/.)', 'Duración (días)', 'Ubicación']
    df_pred["Costo Real (S/.) (Modelo)"] = modelo.predict(df_pred[columnas_requeridas])

    st.subheader("Resultados del modelo")
    st.dataframe(df_pred)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_pred.to_excel(writer, index=False, sheet_name='Resultados')
        writer.save()
    st.download_button(
        label="📥 Descargar Excel con resultados",
        data=output.getvalue(),
        file_name="resultado_prediccion.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
