import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(layout="wide")

# Título principal actualizado
st.markdown("<h1 style='text-align: center; font-size: 60px;'>🏗️ Prototipo con IA para la Elaboración de Presupuestos de Obra de Construcción 🏗️</h1>", unsafe_allow_html=True)

# Botón descargar plantilla de ejemplo
col1, col2 = st.columns([6, 1])
with col2:
    st.markdown("¿No tienes un archivo listo? <br>Descarga la plantilla aquí 👇", unsafe_allow_html=True)
    with open("plantilla_presupuesto_modelo.xlsx", "rb") as file:
        st.download_button("📗 Descargar plantilla de ejemplo", file.read(), file_name="plantilla_presupuesto_modelo.xlsx", type="primary")

# Subida de archivo
st.markdown("### 📤 Subir archivo Excel con tu presupuesto")
uploaded_file = st.file_uploader("Arrastra tu archivo aquí o haz clic en 'Buscar archivos'", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    columnas_requeridas = ["Item", "Nombre del Proyecto", "Ubicación", "Duración (días)", "Fecha de Inicio",
                           "Partida", "Unidad", "Cantidad", "PU (S/.)", "Costo Parcial"]

    if all(col in df.columns for col in columnas_requeridas):
        modelo = joblib.load("modelo_entrenado_sin_ubicacion.pkl")

        df["Costo Estimado IA"] = modelo.predict(df[["Cantidad", "PU (S/.)", "Duración (días)"]])
        df["Costo Estimado IA"] = df["Costo Estimado IA"].apply(lambda x: round(x, 2))

        # Estilizado de la tabla IA antes del renombramiento
        def color_fila(row):
            if row["Costo Estimado IA"] > row["Costo Parcial"] * 1.1:
                return ["background-color: #ffcccc"] * len(row)
            elif row["Costo Estimado IA"] < row["Costo Parcial"] * 0.9:
                return ["background-color: #fff2cc"] * len(row)
            else:
                return [""] * len(row)

        st.markdown("### 📁 Presupuesto subido")
        st.dataframe(df[columnas_requeridas].style.set_properties(**{
            'background-color': 'white', 'color': 'black'
        }), height=250)

        st.markdown(f"<p style='text-align: right; font-weight: bold;'>💰 Total presupuesto subido: S/ {round(df['Costo Parcial'].sum(),2):,.2f}</p>", unsafe_allow_html=True)

        st.markdown("### 🤖 Presupuesto analizado por IA")
        st.dataframe(df[columnas_requeridas + ["Costo Estimado IA"]].style.apply(color_fila, axis=1), height=250)

        st.markdown(f"<p style='text-align: right; font-weight: bold;'>💰 Total estimado por IA: S/ {round(df['Costo Estimado IA'].sum(),2):,.2f}</p>", unsafe_allow_html=True)

        # Comparativo
        st.markdown("### 🧾 Comparativo de Costos Reales")
        diferencia = ((df["Costo Estimado IA"].sum() - df["Costo Parcial"].sum()) / df["Costo Parcial"].sum()) * 100
        col1, col2, col3 = st.columns(3)
        col1.metric("Costo Total Subido", f"S/ {round(df['Costo Parcial'].sum(),2):,.2f}")
        col2.metric("Costo Estimado IA", f"S/ {round(df['Costo Estimado IA'].sum(),2):,.2f}")
        col3.metric("Diferencia entre presupuestos", f"{diferencia:.2f}%", delta="")

        # Top 5 partidas con mayor diferencia
        st.markdown("### 🔍 Top 5 partidas con mayor diferencia")
        df["Diferencia Abs"] = abs(df["Costo Estimado IA"] - df["Costo Parcial"])
        top_dif = df.sort_values(by="Diferencia Abs", ascending=False).head(5)
        st.dataframe(top_dif[["Item", "Partida", "Unidad", "Cantidad", "PU (S/.)", "Costo Parcial", "Costo Estimado IA"]]
                     .style.set_properties(**{
                         'background-color': '#ffcccc', 'color': 'black'
                     }), height=220)

        # Botón rojo grande centrado
        st.markdown("<div style='text-align: center; margin-top: 20px;'>"
                    "<button style='background-color: red; color: white; padding: 12px 24px; font-size: 18px; border: none; border-radius: 8px;'>"
                    "📥 Descargar presupuesto con análisis</button></div>", unsafe_allow_html=True)

        # Explicación del sistema
        st.markdown("### ℹ️ ¿Cómo funciona este sistema?")
        st.markdown("""<p style='font-size: 18px;'>
        El sistema utiliza un modelo de inteligencia artificial para predecir costos unitarios basándose en la cantidad, precio unitario base y duración.
        Este análisis permite detectar partidas con sobrecostos o subvalorizaciones dentro del presupuesto original.
        </p>""", unsafe_allow_html=True)

        # Firma final
        st.markdown("<p style='font-size: 16px; font-weight: bold; text-align: center;'>"
                    "Elaborado por Jheferson Manuel Huaranga Vargas – Escuela de Ingeniería de Sistemas – Octavo Ciclo – Curso: Proyecto de Tesis I"
                    "</p>", unsafe_allow_html=True)
    else:
        st.warning("El archivo cargado no tiene todas las columnas requeridas.")

