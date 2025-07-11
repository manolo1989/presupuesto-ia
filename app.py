
import streamlit as st
import pandas as pd
import joblib

# Cargar modelo
modelo = joblib.load("modelo_costos_entrenado.pkl")

st.title("Sistema Inteligente para Estimar Costo Real de Presupuestos de Obra")

archivo = st.file_uploader("Sube tu archivo Excel con partidas", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)

    st.subheader("Vista previa del presupuesto cargado")
    st.dataframe(df.head())

    if all(col in df.columns for col in ["Cantidad", "PU (S/.)", "Duración (días)"]):
        X = df[["Cantidad", "PU (S/.)", "Duración (días)"]]
        df["Costo Real (S/.) (Modelo)"] = modelo.predict(X)

        st.subheader("Resultados con estimación del modelo")
        st.dataframe(df[["Item", "Partida", "Costo Real (S/.) (Modelo)"]].head())

        st.download_button("Descargar resultados", data=df.to_excel(index=False), file_name="presupuesto_estimado.xlsx")
    else:
        st.error("Tu archivo debe tener las columnas: Cantidad, PU (S/.) y Duración (días)")
