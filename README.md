# Sistema de Predicción de Presupuestos de Obra

Este proyecto permite cargar un archivo Excel con partidas de obra y obtener:
- Predicción del Precio Unitario (PU) si está vacío.
- Simulación del Costo Real si se proporciona un PU.

## Estructura del Proyecto

- `app.py`: Aplicación principal de Streamlit.
- `modelo_pu.pkl`: Modelo de regresión entrenado para predecir el PU.
- `plantilla_presupuesto_modelo.xlsx`: Archivo base de ejemplo para cargar tus datos.
- `requirements.txt`: Librerías necesarias.

## Cómo usarlo

1. Instala los requerimientos: `pip install -r requirements.txt`
2. Ejecuta la app con: `streamlit run app.py`
3. Carga tu archivo Excel y revisa los resultados con colores diferenciados.

