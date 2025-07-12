
import streamlit as st
import pandas as pd
import joblib

# Cargar el modelo entrenado
modelo = joblib.load("modelo_entrenado_sin_ubicacion.pkl")

# Título
st.title("🏗️Sistema de Prediccion de Presupuestos de Obra con IA")
st.markdown("Sube tu archivo Excel con las columnas: 'Cantidad', 'PU (S/.)', 'Duración (días)'")

# Subida de archivo
archivo = st.file_uploader("Sube tu archivo .xlsx", type=["xlsx"])

if archivo is not None:
    df_pred = pd.read_excel(archivo)
    st.subheader("Presupuesto cargado")
    st.dataframe(df_pred)

    columnas_requeridas = ['Cantidad', 'PU (S/.)', 'Duración (días)']

    if all(col in df_pred.columns for col in columnas_requeridas):
        df_pred["Costo Real (S/.) (Modelo)"] = modelo.predict(df_pred[columnas_requeridas])
        st.subheader("Resultados del modelo")
        st.dataframe(df_pred)

        # Descargar como Excel
        from io import BytesIO
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df_pred.to_excel(writer, index=False)
        writer.close()
        st.download_button("Descargar resultados", data=output.getvalue(), file_name="presupuesto_estimado.xlsx")
    else:
        st.warning("El archivo debe contener las columnas necesarias: 'Cantidad', 'PU (S/.)', 'Duración (días)'")
