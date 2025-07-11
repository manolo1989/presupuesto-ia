
# 🧱 Estimador Inteligente de Costos de Obra

Esta aplicación permite estimar el **Costo Real (S/.)** de cada partida de obra usando **Machine Learning**, entrenado con proyectos reales.

---

## 📂 ¿Qué necesitas para usarlo?

1. Subir un archivo Excel (.xlsx) con las siguientes columnas obligatorias:
   - `Partida` → Descripción de la actividad (ej. Excavación, Encofrado, Tarrajeo)
   - `Duración (días)` → Duración total del proyecto (ej. 120, 180)
   - `Fecha de Inicio` → Fecha del inicio del proyecto (ej. 2021-06-15)

📌 **Ejemplo de estructura:**

| Partida                  | Duración (días) | Fecha de Inicio |
|--------------------------|-----------------|------------------|
| Excavación en zanja      | 180             | 2020-05-10       |
| Tarrajeo de muros        | 180             | 2020-05-10       |

---

## 🤖 ¿Cómo funciona?

- El modelo está entrenado para identificar patrones en el **tipo de partida**, la duración de la obra y el año de inicio.
- Usa **Regresión Lineal** con codificación automática para predecir el **Costo Real (S/.)**.

---

## 📊 Resultado

Una vez subido el archivo, obtendrás:
- Una nueva columna: `Costo Real (S/.) (Modelo)`
- Botón para **descargar los resultados** en Excel

---

## 🛠️ Tecnologías

- Python
- Streamlit
- scikit-learn
- pandas
- xlsxwriter

---

## 📦 Archivos del proyecto

- `app.py` → Código principal de la aplicación
- `modelo_con_partida_duracion_fecha.pkl` → Modelo entrenado
- `requirements.txt` → Librerías necesarias

---

## 📈 Demo

Puedes ejecutar la aplicación localmente o subirla a [Streamlit Cloud](https://streamlit.io/cloud).

---
Desarrollado por: *Tesis Pregrado - Aplicación IA en Presupuestos*
