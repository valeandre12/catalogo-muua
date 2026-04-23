import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide", page_title="Catálogo MUUA - Colección de Antropología")

st.title("🏛️ Catálogo MUUA - Colección de Antropología")

@st.cache_data
def load_data(path):
    # Usamos engine='openpyxl' para asegurar compatibilidad
    df = pd.read_excel(path, engine='openpyxl')
    df.columns = [c.strip() for c in df.columns]
    return df

def get_image(denominacion):
    denominacion = str(denominacion).lower()
    img_folder = "imagenes"
    if "vasija" in denominacion: return os.path.join(img_folder, "vasija.jpg")
    if "figura" in denominacion or "estatuilla" in denominacion: return os.path.join(img_folder, "figura.jpg")
    return os.path.join(img_folder, "default.jpg")

try:
    # 1. CARGA DE DATOS
    df = load_data("LIBRODEREGISTRO.xlsx") 
    
    # Manejo robusto de fechas para evitar el error del log
    if "Fecha de ingreso" in df.columns:
        # Convertimos a fecha ignorando errores y luego extraemos el año
        df['Año'] = pd.to_datetime(df["Fecha de ingreso"], errors='coerce').dt.year
        # Si el año es nulo, ponemos un 0 temporal para que no rompa el código
        df['Año'] = df['Año'].fillna(0).astype(int)

    # 2. BUSCADORES
    registro = st.text_input("Buscar por Número de Registro:")
    
    # Aseguramos que Cultura no tenga valores nulos para el filtro
    culturas_disponibles = df['Cultura'].dropna().unique().astype(str).tolist()
    lista_culturas = ["Todas"] + sorted(culturas_disponibles)
    cultura_sel = st.selectbox("Filtrar por Cultura", lista_culturas)

    # 3. LÓGICA DE FILTRADO
    df_filtrado = df.copy()
    if registro:
        df_filtrado = df_filtrado[df_filtrado['Número de Registro'].astype(str).str.contains(registro, case=False)]
    if cultura_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Cultura'] == cultura_sel]

    # 4. TABLA PRINCIPAL
    st.subheader("Información del Objeto")
    
    # Mostramos solo las columnas que existen para evitar errores
    columnas_a_mostrar = ["Número de Registro", "Año", "Denominación del Objeto", "Cultura", "Materiales"]
    columnas_reales = [c for c in columnas_a_mostrar if c in df_filtrado.columns]

    evento_seleccion = st.dataframe(
        df_filtrado[columnas_reales],
        use_container_width=True,
        on_select="rerun", 
        selection_mode="single-row"
    )

    # 5. FICHA TÉCNICA 
    seleccion = evento_seleccion.selection.rows
    if seleccion:
        indice_fila = seleccion[0]
        datos_objeto = df_filtrado.iloc[indice_fila]
        
        st.divider()
        col1, col2 = st.columns([1, 2])
        
        with col1:
            img_path = get_image(datos_objeto['Denominación del Objeto'])
            if os.path.exists(img_path):
                st.image(img_path, caption=datos_objeto['Denominación del Objeto'], use_container_width=True)
            else:
                st.image("https://via.placeholder.com/300?text=Sin+Imagen+Referencial", use_container_width=True)

        with col2:
            st.header(f"Ficha Técnica: {datos_objeto['Número de Registro']}")
            with st.container(border=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Denominación:** {datos_objeto.get('Denominación del Objeto', 'N/A')}")
                    st.write(f"**Cultura:** {datos_objeto.get('Cultura', 'N/A')}")
                    año_val = datos_objeto.get('Año', 0)
                    st.write(f"**Año de ingreso:** {año_val if año_val != 0 else 'N/A'}")
                with c2:
                    st.write(f"**Materiales:** {datos_objeto.get('Materiales', 'N/A')}")
                    st.write(f"**Zona:** {datos_objeto.get('Zona Arqueológica', 'N/A')}")
                    st.write(f"**País:** {datos_objeto.get('País', 'N/A')}")

except Exception as e:
    st.error(f"Hubo un problema al cargar los datos: {e}")
