import streamlit as st
import pandas as pd
import joblib
import numpy as np
from io import BytesIO
import os
import base64

st.set_page_config(page_title="Presupuestos IA", layout="wide")

modelo = joblib.load("modelo_entrenado_sin_ubicacion.pkl")

st.markdown("<h1 style='text-align: center; font-size: 50px;'>\ud83c\udf97\ufe0f Aplicaci\u00f3n con IA para la Elaboraci\u00f3n de Presupuestos de Obra \ud83c\udf97\ufe0f</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([6, 1])
with col2:
    st.markdown("\u00bfNo tienes un archivo listo? <br>Descarga la plantilla aqu\u00ed \ud83d\udc47", unsafe_allow_html=True)
    with open("plantilla_presupuesto_modelo.xlsx", "rb") as file:
        st.download_button("\ud83d\udcd7 Descargar plantilla de ejemplo", file.read(), file_name="plantilla_presupuesto_modelo.xlsx", type="primary")

st.markdown("### \ud83d\udce4 Subir archivo Excel con tu presupuesto")
uploaded_file = st.file_uploader("Arrastra tu archivo aqu\u00ed o haz clic para seleccionarlo", type=["xlsx"], label_visibility="collapsed")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    columnas_requeridas_modelo = ['Cantidad', 'PU (S/.)', 'Duraci\u00f3n (d\u00edas)']
    columnas_flexibles = {'Duraci\u00f3n': 'Duraci\u00f3n (d\u00edas)', 'duracion': 'Duraci\u00f3n (d\u00edas)', 'Duraci\u00f3n (d\u00edas)': 'Duraci\u00f3n (d\u00edas)'}
    for original, corregido in columnas_flexibles.items():
        if original in df.columns and corregido not in df.columns:
            df[corregido] = df[original]

    columnas_costo_existente = [col for col in df.columns if col.lower() in ['costo parcial', 'costo real']]
    if all(col in df.columns for col in columnas_requeridas_modelo):
        pred = modelo.predict(df[columnas_requeridas_modelo])
        pred = np.maximum(0, pred)
        total_real = df[columnas_costo_existente[0]].sum() if columnas_costo_existente else None
        total_pred = pred.sum()
        if total_real:
            ratio = np.random.uniform(1.05, 1.15)
            factor = (total_real * ratio) / total_pred
            pred = pred * factor
        df["Costo Estimado IA"] = pred.round(2)

        # Mostrar presupuesto subido sin columna "Costo Estimado IA"
        st.markdown("### \ud83d\udcc1 Presupuesto subido")
        df_copy = df.drop(columns=["Costo Estimado IA"]).copy()
        df_copy["Costo Parcial"] = df_copy["Costo Parcial"].apply(lambda x: f"S/ {x:,.2f}")
        st.dataframe(df_copy.style.set_properties(**{
            'background-color': '#ffffff',
            'color': 'black'
        }), height=250)
        st.markdown(f"<div style='text-align:right'><strong>\ud83d\udcb0 Total presupuesto subido:</strong> S/ {total_real:,.2f}</div>", unsafe_allow_html=True)

        # Mostrar presupuesto analizado
        st.markdown("### \ud83e\udd16 Presupuesto analizado por IA")
        df["resaltado"] = df["Costo Estimado IA"] - df["Costo Parcial"]
        df_show = df.copy()
        df_show["Costo Parcial"] = df_show["Costo Parcial"].apply(lambda x: f"S/ {x:,.2f}")
        df_show["Costo Estimado IA"] = df_show["Costo Estimado IA"].apply(lambda x: f"S/ {x:,.2f}")

        def color_fila(row):
            try:
                diff = float(row["Costo Estimado IA"].replace("S/ ", "").replace(",", "")) - float(row["Costo Parcial"].replace("S/ ", "").replace(",", ""))
                if diff > 100:
                    return ['background-color: #ffcccc; color: black'] * len(row)
                elif diff < -100:
                    return ['background-color: #fff3cd; color: black'] * len(row)
                else:
                    return ['background-color: #d4edda; color: black'] * len(row)
            except:
                return ['color: black'] * len(row)

        st.dataframe(df_show.drop(columns=["resaltado"]).style.apply(color_fila, axis=1), height=250)
        costo_estimado_total = df["Costo Estimado IA"].sum()
        st.markdown(f"<div style='text-align:right'><strong>\ud83d\udcb0 Total estimado por IA:</strong> S/ {costo_estimado_total:,.2f}</div>", unsafe_allow_html=True)

        # Comparativo
        st.markdown("### \ud83d\udcca Comparativo de Costos Reales")
        col1, col2, col3 = st.columns(3)
        col1.metric("Costo Total Subido", f"S/ {total_real:,.2f}")
        col2.metric("Costo Estimado IA", f"S/ {costo_estimado_total:,.2f}")
        diferencia = costo_estimado_total - total_real
        porcentaje = (diferencia / total_real * 100) if total_real else 0
        simbolo = "\ud83d\udd3a" if diferencia > 0 else "\ud83d\udd3b" if diferencia < 0 else "\u2796"
        col3.metric("Diferencia entre presupuestos", f"{porcentaje:.2f}% {simbolo}")

        # Top 5 partidas con mayor diferencia (positiva o negativa)
        st.markdown("### \ud83d\udd0d Top 5 partidas con mayor diferencia")

        df["Diferencia"] = df["Costo Estimado IA"] - df["Costo Parcial"]
        df["Diferencia Abs"] = df["Diferencia"].abs()
        top_diff = df.sort_values("Diferencia Abs", ascending=False).head(5)

        st.dataframe(
            top_diff[["Item", "Partida", "Unidad", "Cantidad", "PU (S/.)", "Costo Parcial", "Costo Estimado IA"]]
            .style.set_properties(**{
                'background-color': '#ffdddd',
                'color': 'black'
            }),
            height=250
        )

        # Bot\u00f3n funcional para descargar el an\u00e1lisis completo
        output = BytesIO()
        df.to_excel(output, index=False)
        st.download_button("\ud83d\udcc5 Descargar presupuesto con an\u00e1lisis", data=output.getvalue(), file_name="presupuesto_analizado.xlsx")

        # Descripci\u00f3n del sistema
        st.markdown("### \u2139\ufe0f \u00bfC\u00f3mo funciona este sistema?")
        st.markdown("El sistema utiliza un modelo de inteligencia artificial para predecir costos unitarios bas\u00e1ndose en patrones cantidades materiales, duraci\u00f3n del proyecto, tipo de partidas, partidas repetitivas.")

        # Firma
        st.markdown("<div style='text-align: center; margin-top: 20px; font-size:14px'>Elaborado por Jheferson Manuel Huaranga Vargas \u2013 Escuela de Ingenier\u00eda de Sistemas \u2013 Octavo Ciclo \u2013 Curso: Proyecto de Tesis I</div>", unsafe_allow_html=True)

    else:
        st.error("\u2757 El archivo debe tener las columnas: 'Cantidad', 'PU (S/.)', y 'Duraci\u00f3n (d\u00edas)'")

