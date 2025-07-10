
# 📊 Sistema Inteligente de Ajuste de Presupuestos de Obra

Este sistema permite subir un archivo Excel con un presupuesto estimado de construcción y, mediante una simulación de inteligencia artificial, ajusta automáticamente los precios unitarios. Está pensado para ayudar a las constructoras a prever desviaciones en costos antes de ejecutar una obra.

## 🚀 Funcionalidades

- Subida de archivos Excel (.xlsx) con presupuestos.
- Análisis automático de precios unitarios.
- Generación de nuevos precios ajustados por IA (simulada con variación aleatoria entre 5% y 15%).
- Cálculo del costo parcial ajustado por cada partida.
- Visualización interactiva de los datos.
- Descarga del nuevo archivo con los precios ajustados.

## 🛠 Requisitos

Este proyecto utiliza:
- Python
- Streamlit
- Pandas
- Numpy
- Openpyxl

Instala los requisitos con:

```
pip install -r requirements.txt
```

## 📂 Estructura de entrada esperada

El archivo Excel debe contener las siguientes columnas:

- `Partida`
- `Unidad`
- `Cantidad`
- `Precio Unitario Estimado (S/.)`

## 🌐 Ver en línea

Puedes probar la aplicación directamente desde Streamlit Cloud:

[👉 Ir a la app](https://TU-ENLACE.streamlit.app)

> Reemplaza "TU-ENLACE" con el nombre que elegiste al desplegar.

## 🧑‍💻 Autor

Desarrollado por [manolo1989](https://github.com/manolo1989) como parte de un proyecto de tesis de pregrado.

---

¡Gracias por visitar este repositorio! Cualquier sugerencia o mejora es bienvenida.
