# 🏗️ Aplicación de Predicción de Costos Reales - Presupuesto Inteligente

Esta aplicación permite predecir el **Costo Real por partida** de un proyecto de construcción usando **Machine Learning (Regresión Lineal)** entrenado con presupuestos históricos simulados.

Desarrollada en Python con **Streamlit** y **scikit-learn**, ideal para estudiantes de ingeniería, arquitectos o profesionales del sector construcción.

---

## 🚀 ¿Qué hace la app?

- 📤 Permite subir un archivo Excel con tu presupuesto (cantidad, precio unitario, ubicación, duración)
- 🤖 Predice automáticamente el `Costo Real (S/.)` por partida usando un modelo entrenado
- 📊 Compara si hubo ahorro (🟢) o sobrecosto (🔴)
- 💰 Muestra el **Costo Total Estimado del Proyecto**
- 📥 Descarga un nuevo Excel con los resultados

---

## 📂 Archivos del repositorio

| Archivo                      | Descripción |
|-----------------------------|-------------|
| `app.py`                    | Código principal de la app Streamlit |
| `modelo_costos_entrenado.pkl` | Modelo de Machine Learning entrenado |
| `requirements.txt`          | Paquetes necesarios para ejecutar en Streamlit Cloud |

---

## 📦 Requisitos

- Python 3.9 o superior
- Streamlit (se instala con `requirements.txt`)

---

## 📡 Publicación en Streamlit Cloud

1. Crea una cuenta en https://streamlit.io/cloud
2. Conecta tu GitHub
3. Crea un nuevo repositorio con los 3 archivos mencionados
4. En Streamlit Cloud, selecciona el repo y lanza la app

---

## 📞 Contacto

Desarrollado como parte de un proyecto de tesis de pregrado en Perú.  
**Tema:** Aplicación de Inteligencia Artificial para el diseño de un sistema inteligente de presupuestos de obra.