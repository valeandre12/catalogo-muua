import streamlit as st
import pandas as pd
import os

st.set_page_config(
    layout="wide",
    page_title="Catálogo MUUA - Colección de Antropología"
)

st.title("🏛️ Catálogo MUUA - Colección de Antropología")


# ----------------------------
# CARGA ULTRA OPTIMIZADA
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(
        "LIBRODEREGISTRO.csv",
        usecols=[
            "Número de Registro",
            "Fecha de ingreso",
            "Denominación del Objeto",
            "Cultura",
            "Materiales",
            "Zona Arqueológica",
            "País"
        ]
    )

    df.columns = df.columns.str.strip()

    # fecha + año en una sola operación
    df["Fecha de ingreso"] = pd.to_datetime(df["Fecha de ingreso"], errors="coerce")
    df["Año"] = df["Fecha de ingreso"].dt.year

    return df


# ----------------------------
# IMAGENES
# ----------------------------
def get_image(denominacion):
    denominacion = str(denominacion).lower()
    img_folder = "imagenes"

    if "vasija" in denominacion:
        return os.path.join(img_folder, "vasija.jpg")
    if "figura" in denominacion or "estatuilla" in denominacion:
        return os.path.join(img_folder, "figura.jpg")

    return os.path.join(img_folder, "default.jpg")


# ----------------------------
# DATA LOAD
# ----------------------------
df = load_data()


# ----------------------------
# UI FILTROS
# ----------------------------
registro = st.text_input("Buscar por Número de Registro:")

lista_culturas = ["Todas"] + sorted(df["Cultura"].dropna().astype(str).unique())
cultura_sel = st.selectbox("Filtrar por Cultura", lista_culturas)


# ----------------------------
# FILTRADO (sin copy → menos RAM)
# ----------------------------
df_filtrado = df

if registro:
    df_filtrado = df_filtrado[
        df_filtrado["Número de Registro"].astype(str) == registro
    ]

if cultura_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Cultura"] == cultura_sel]


# ----------------------------
# LIMITAR RESULTADOS (CLAVE PARA RENDER)
# ----------------------------
df_filtrado = df_filtrado.head(200)  # ⚠️ modo demo / performance


# ----------------------------
# TABLA
# ----------------------------
st.subheader("Información del Objeto")

evento_seleccion = st.dataframe(
    df_filtrado[
        [
            "Número de Registro",
            "Año",
            "Denominación del Objeto",
            "Cultura",
            "Materiales"
        ]
    ],
    use_container_width=True,
    on_select="rerun",
    selection_mode="single-row"
)


# ----------------------------
# DETALLE
# ----------------------------
seleccion = evento_seleccion.selection.rows

if seleccion:
    datos_objeto = df_filtrado.iloc[seleccion[0]]

    st.divider()

    col1, col2 = st.columns([1, 2])

    with col1:
        img_path = get_image(datos_objeto["Denominación del Objeto"])

        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.image(
                "https://via.placeholder.com/300?text=Sin+Imagen",
                use_container_width=True
            )

    with col2:
        st.header(f"Ficha Técnica: {datos_objeto['Número de Registro']}")

        with st.container(border=True):
            c1, c2 = st.columns(2)

            with c1:
                st.write(f"**Denominación:** {datos_objeto['Denominación del Objeto']}")
                st.write(f"**Cultura:** {datos_objeto['Cultura']}")
                st.write(
                    f"**Año:** {int(datos_objeto['Año']) if pd.notna(datos_objeto['Año']) else 'N/A'}"
                )

            with c2:
                st.write(f"**Materiales:** {datos_objeto['Materiales']}")
                st.write(f"**Zona:** {datos_objeto['Zona Arqueológica']}")
                st.write(f"**País:** {datos_objeto['País']}")

else:
    st.warning("No hay objetos que coincidan con los filtros")