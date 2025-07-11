
import streamlit as st
import pandas as pd
import joblib
import numpy as np
import datetime

# Cargar modelo entrenado con manejo de ubicaciones desconocidas
modelo = joblib.load("modelo_costos_entrenado_flexible.pkl")

st.title("Predicción de Costo Real por Partida")
st.write("Esta herramienta predice el costo real de cada partida de un presupuesto usando Machine Learning.")

# Subir archivo
archivo = st.file_uploader("📤 Sube tu archivo de presupuesto en Excel (.xlsx)", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)

    # Verificamos si ya tiene Costo Real
    tiene_costo_real = "Costo Real (S/.)" in df.columns

    # Columnas necesarias
    columnas_requeridas = ["Cantidad", "PU (S/.)", "Duración (días)", "Ubicación"]
    if all(col in df.columns for col in columnas_requeridas):

        # Copia para predicción
        df_pred = df.copy()

        if not tiene_costo_real:
            df_pred["Costo Real (S/.)"] = modelo.predict(df_pred[columnas_requeridas])
        else:
            df_pred["Costo Real (S/.) (Modelo)"] = modelo.predict(df_pred[columnas_requeridas])
            df_pred["Diferencia (%)"] = ((df_pred["Costo Real (S/.) (Modelo)"] - df_pred["Costo Real (S/.)"]) / df_pred["Costo Real (S/.)"]) * 100
            df_pred["Estado"] = np.where(df_pred["Diferencia (%)"] > 0, "🔴 SobreCosto", "🟢 Ahorro")

        st.subheader("📋 Presupuesto con Resultados")
        st.dataframe(df_pred)

        # Mostrar total estimado
        if not tiene_costo_real:
            total_estimado = df_pred["Costo Real (S/.)"].sum()
        else:
            total_estimado = df_pred["Costo Real (S/.) (Modelo)"].sum()
        st.success(f"💰 Costo Total Estimado del Proyecto: S/ {total_estimado:,.2f}")

        # Descargar resultados
        st.subheader("⬇ Descargar archivo con resultados")
        nombre_salida = f"presupuesto_con_resultados_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df_pred.to_excel(nombre_salida, index=False)
        with open(nombre_salida, "rb") as f:
            st.download_button("📥 Descargar Excel", f, file_name=nombre_salida)

    else:
        st.warning("Tu archivo debe tener las columnas: 'Cantidad', 'PU (S/.)', 'Duración (días)', 'Ubicación'")
