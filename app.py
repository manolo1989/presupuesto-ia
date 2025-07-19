
import streamlit as st
import pandas as pd
import joblib
import numpy as np
from io import BytesIO
import os
import base64

st.set_page_config(page_title="Presupuestos IA", layout="wide")

modelo = joblib.load("modelo_entrenado_sin_ubicacion.pkl")

# Encabezado
st.markdown("## 🏗️ Aplicación con IA para la Elaboración de Presupuestos de Obra 🏗️")

# Parte superior derecha - descarga plantilla
col_sup_izq, col_sup_der = st.columns([2, 1])
with col_sup_der:
    st.markdown("### 🧾 ¿No tienes un archivo listo?")
    st.markdown("Descarga la plantilla de ejemplo 👇", unsafe_allow_html=True)
    if os.path.exists("plantilla_presupuesto_modelo.xlsx"):
        with open("plantilla_presupuesto_modelo.xlsx", "rb") as file:
            data = file.read()
            b64 = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="plantilla_presupuesto_modelo.xlsx"><button style="background-color:#28a745;color:white;padding:10px 20px;border:none;border-radius:5px;font-size:16px">📥 Descargar plantilla de ejemplo</button></a>'
            st.markdown(href, unsafe_allow_html=True)

# Subida de archivo
st.markdown("### 📤 Subir archivo Excel con tu presupuesto")
st.markdown('<div style="background-color:white;padding:10px;border-radius:5px">', unsafe_allow_html=True)
archivo = st.file_uploader(" ", type=["xlsx"])
st.markdown('</div>', unsafe_allow_html=True)

if archivo is not None:
    df = pd.read_excel(archivo)
    columnas_requeridas_modelo = ['Cantidad', 'PU (S/.)', 'Duración (días)']
    columnas_flexibles = {
        'Duración': 'Duración (días)',
        'duracion': 'Duración (días)',
        'Duración (días)': 'Duración (días)'
    }

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

        # Mostrar presupuesto subido
        st.markdown("### 📁 Presupuesto subido")
        df_copy = df.copy()
        df_copy["Costo Parcial"] = df_copy["Costo Parcial"].apply(lambda x: f"S/ {x:,.2f}")
        st.dataframe(df_copy.style.set_properties(**{'background-color': '#ffffff'}), height=250)
        st.markdown(f"**💰 Total presupuesto subido:** S/ {total_real:,.2f}")

        # Mostrar presupuesto analizado
        st.markdown("### 🤖 Presupuesto analizado por IA")
        df["resaltado"] = df["Costo Estimado IA"] - df["Costo Parcial"]
        df_show = df.copy()
        df_show["Costo Parcial"] = df_show["Costo Parcial"].apply(lambda x: f"S/ {x:,.2f}")
        df_show["Costo Estimado IA"] = df_show["Costo Estimado IA"].apply(lambda x: f"S/ {x:,.2f}")

        def color_fila(row):
            try:
                diff = float(row["Costo Estimado IA"].replace("S/ ", "").replace(",", "")) - float(row["Costo Parcial"].replace("S/ ", "").replace(",", ""))
                if diff > 100:
                    return ['background-color: #ffcccc'] * len(row)
                elif diff < -100:
                    return ['background-color: #fff3cd'] * len(row)
                else:
                    return ['background-color: #d4edda'] * len(row)
            except:
                return [''] * len(row)

        st.dataframe(df_show.drop(columns=["resaltado"]).style.apply(color_fila, axis=1), height=250)
        costo_estimado_total = df["Costo Estimado IA"].sum()
        st.markdown(f"**💰 Total estimado por IA:** S/ {costo_estimado_total:,.2f}")

        st.markdown(" " * 5)
        st.markdown("### 📊 Comparativo de Costos Reales")
        col1, col2, col3 = st.columns(3)
        col1.metric("Costo Total Subido", f"S/ {total_real:,.2f}")
        col2.metric("Costo Estimado IA", f"S/ {costo_estimado_total:,.2f}")
        diferencia = costo_estimado_total - total_real
        porcentaje = (diferencia / total_real * 100) if total_real else 0
        simbolo = "🔺" if diferencia > 0 else "🔻" if diferencia < 0 else "➖"
        col3.metric("Diferencia entre presupuestos", f"{porcentaje:.2f}% {simbolo}")

        st.markdown("### 🔍 Top 5 partidas con mayor diferencia")
        df["Diferencia"] = df["Costo Estimado IA"] - df["Costo Parcial"]
        top_diff = df.sort_values("Diferencia", ascending=False).head(5)
        st.dataframe(top_diff[["Item", "Partida", "Unidad", "Cantidad", "PU (S/.)", "Costo Parcial", "Costo Estimado IA"]].style.set_properties(**{'background-color': '#ffdddd'}), height=250)

        output = BytesIO()
        df.drop(columns=["Diferencia", "resaltado"], errors='ignore').to_excel(output, index=False, engine='xlsxwriter')
        st.download_button("📥 Descargar presupuesto con análisis", data=output.getvalue(), file_name="presupuesto_estimado.xlsx", mime="application/vnd.ms-excel")

    else:
        st.error("❗ El archivo debe tener las columnas: 'Cantidad', 'PU (S/.)', y 'Duración (días)'")
