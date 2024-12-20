import pandas as pd
import streamlit as st
from PIL import Image
import os

# Configurar título de la aplicación
st.image("CROWN.jpg")
st.title("Catálogo de Partes MRO Crown Qro1")

# Cargar el archivo Excel
@st.cache_data
def cargar_datos(archivo):
    return pd.read_excel(archivo)

# Ruta de la carpeta de imágenes
carpeta_imagenes = "IMG"

# Generar la columna de rutas de imágenes
def generar_ruta_imagen(df, carpeta):
    df['Ruta Imagen'] = df['Número de material externo largo'].apply(
        lambda x: os.path.join(carpeta, f"{x}.jpg")
    )
    return df

# Cargar la base de datos
archivo_excel = "EXPORT.XLSX"  # Asegúrate de que el archivo esté en el mismo directorio
df = cargar_datos(archivo_excel)
df = generar_ruta_imagen(df, carpeta_imagenes)

# Barra de búsqueda
consulta = st.text_input("Buscar una parte (ejemplo: 'sensor'):")

# Filtrar resultados
if consulta:
    resultados = df[df.apply(lambda row: consulta.lower() in str(row).lower(), axis=1)]
else:
    resultados = df

# Parámetros de paginación
resultados_por_pagina = 25
num_paginas = (len(resultados) + resultados_por_pagina - 1) // resultados_por_pagina
pagina_actual = st.number_input(
    "Página", min_value=1, max_value=num_paginas, value=1, step=1
)

# Determinar el rango de datos para la página actual
inicio = (pagina_actual - 1) * resultados_por_pagina
fin = inicio + resultados_por_pagina
resultados_paginados = resultados.iloc[inicio:fin]

# Mostrar resultados paginados
st.write(f"### Mostrando página {pagina_actual} de {num_paginas}")

for _, fila in resultados_paginados.iterrows():
    # Mostrar datos de la fila
    st.write(f"**Número de material:** {fila['Número de material externo largo']}")
    st.write(f"**Descripción:** {fila.get('Descripción de material', 'Sin descripción')}")
    
    # Mostrar la imagen
    ruta_imagen = fila['Ruta Imagen']
    if os.path.exists(ruta_imagen):
        img = Image.open(ruta_imagen)
        st.image(img, caption=fila['Número de material externo largo'], use_container_width=True)
    else:
        st.warning(f"No se encontró la imagen para: {fila['Número de material externo largo']}")