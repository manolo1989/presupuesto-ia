
import streamlit as st
import pandas as pd
import joblib
import numpy as np
import datetime

# Cargar el modelo entrenado con OrdinalEncoder
modelo = joblib.load("modelo_costos_entrenado_ordinal.pkl")

st.title("📊 Predicción de Costo Real por Partida")
st.write("Carga tu archivo Excel con partidas de obra para predecir el costo real usando Machine Learning.")

archivo = st.file_uploader("📤 Sube tu archivo de presupuesto (.xlsx)", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)

    columnas_requeridas = ["Cantidad", "PU (S/.)", "Duración (días)", "Ubicación"]
    tiene_costo_real = "Costo Real (S/.)" in df.columns

    if all(col in df.columns for col in columnas_requeridas):
        df_pred = df.copy()

        if not tiene_costo_real:
            df_pred["Costo Real (S/.)"] = modelo.predict(df_pred[columnas_requeridas])
        else:
            df_pred["Costo Real (S/.) (Modelo)"] = modelo.predict(df_pred[columnas_requeridas])
            df_pred["Diferencia (%)"] = ((df_pred["Costo Real (S/.) (Modelo)"] - df_pred["Costo Real (S/.)"]) / df_pred["Costo Real (S/.)"]) * 100
            df_pred["Estado"] = np.where(df_pred["Diferencia (%)"] > 0, "🔴 SobreCosto", "🟢 Ahorro")

        st.subheader("📋 Resultado del Análisis")
        st.dataframe(df_pred)

        # Mostrar total estimado
        total = df_pred.filter(like="Costo Real").select_dtypes(include=["number"]).sum().sum()
        st.success(f"💰 Costo Total Estimado: S/ {total:,.2f}")

        # Descargar resultado
        nombre_salida = f"resultado_presupuesto_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df_pred.to_excel(nombre_salida, index=False)
        with open(nombre_salida, "rb") as f:
            st.download_button("📥 Descargar Excel con resultados", f, file_name=nombre_salida)

    else:
        st.warning("Tu archivo debe contener las columnas: 'Cantidad', 'PU (S/.)', 'Duración (días)', 'Ubicación'")
