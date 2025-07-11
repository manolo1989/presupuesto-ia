
# Sistema Inteligente para Estimar Costos Reales de Presupuestos de Obra

Este proyecto permite cargar un archivo Excel con partidas de obra y obtener una estimación del costo real usando un modelo de Machine Learning entrenado con datos simulados.

## 🔧 Cómo usar

1. Clona este repositorio en tu máquina o súbelo a Streamlit Cloud.
2. Asegúrate de tener instalado `streamlit`, `pandas`, `scikit-learn`, `joblib`, y `openpyxl`.
3. Ejecuta la aplicación con:

```bash
streamlit run app.py
```

4. Sube tu archivo Excel que contenga las columnas:
   - `Cantidad`
   - `PU (S/.)`
   - `Duración (días)`

El sistema mostrará una predicción del **Costo Real (S/.)** para cada partida.

## 📁 Archivos del proyecto

- `app.py`: Código principal de la aplicación.
- `requirements.txt`: Lista de librerías necesarias.
- `modelo_costos_entrenado.pkl`: Modelo de regresión lineal entrenado.
- `config.toml`: Configuración visual de la app (opcional).

## 🌐 Despliegue en Streamlit Cloud

Puedes subir este repositorio directamente a Streamlit Cloud y publicar tu app de forma gratuita.

---

Proyecto de tesis basado en simulación de presupuestos reales con IA.
