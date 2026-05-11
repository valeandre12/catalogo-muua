import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide", page_title="Catálogo MUUA - Colección de Antropología")

st.title("🏛️ Catálogo MUUA - Colección de Antropología")

@st.cache_data
def load_data(path):
    df = pd.read_excel(path)
    df.columns = [c.strip() for c in df.columns]
    
    # Procesar fechas de forma robusta
    if "Fecha de ingreso" in df.columns:
        df['Fecha de ingreso'] = pd.to_datetime(df["Fecha de ingreso"], format='%d/%m/%Y', errors='coerce')
        df['Año'] = df['Fecha de ingreso'].dt.year.astype('Int64')
    else:
        df['Año'] = None
    
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
    
    if "Fecha de ingreso" in df.columns:
        df['Año'] = pd.to_datetime(df["Fecha de ingreso"], errors='coerce').dt.year

    # 2. BUSCADORES (Exactamente como los tenías al principio)
    registro = st.text_input("Buscar por Número de Registro:")
    lista_culturas = ["Todas"] + sorted(df['Cultura'].dropna().unique().astype(str).tolist())
    cultura_sel = st.selectbox("Filtrar por Cultura", lista_culturas)

    # 3. LÓGICA DE FILTRADO
    df_filtrado = df.copy()
    if registro:
        df_filtrado = df_filtrado[df_filtrado['Número de Registro'].astype(str) == registro]
    if cultura_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Cultura'] == cultura_sel]

    df_filtrado = df_filtrado.reset_index(drop=True)

    # 4. TABLA PRINCIPAL
    st.subheader("Información del Objeto")
    
    evento_seleccion = st.dataframe(
        df_filtrado[["Número de Registro", "Año", "Denominación del Objeto", "Cultura", "Materiales"]],
        use_container_width=True,
        on_select="rerun", 
        selection_mode="single-row"
        key="Tabla_antropologia"
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
                    st.write(f"**Denominación:** {datos_objeto['Denominación del Objeto']}")
                    st.write(f"**Cultura:** {datos_objeto['Cultura']}")
                    st.write(f"**Año de ingreso:** {int(datos_objeto['Año']) if not pd.isna(datos_objeto['Año']) else 'N/A'}")
                with c2:
                    st.write(f"**Materiales:** {datos_objeto['Materiales']}")
                    st.write(f"**Zona:** {datos_objeto['Zona Arqueológica']}")
                    st.write(f"**País:** {datos_objeto['País']}")
    else:
        st.warning("No hay objetos que coincidan con los filtros seleccionados")

except Exception as e:
    st.error(f"Error: {e}")
