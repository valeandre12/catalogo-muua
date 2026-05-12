import streamlit as st
import pandas as pd
import os
import gc

st.set_page_config(
    layout="wide",
    page_title="Catálogo MUUA - Colección de Antropología"
)

st.title("🏛️ Catálogo MUUA - Colección de Antropología")


# ----------------------------
# CARGA OPTIMIZADA
# ----------------------------
@st.cache_data(ttl=3600)
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
        ],
        dtype={
            "Número de Registro": "string",
            "Cultura": "string",
            "Materiales": "string",
            "Zona Arqueológica": "string",
            "País": "string",
            "Denominación del Objeto": "string"
        },
        low_memory=False
    )

    df.columns = df.columns.str.strip()

    df["Fecha de ingreso"] = pd.to_datetime(
        df["Fecha de ingreso"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    df["Año"] = df["Fecha de ingreso"].dt.year.astype("Int16")

    # liberar memoria
    df = df.drop(columns=["Fecha de ingreso"])

    gc.collect()

    return df


# ----------------------------
# IMÁGENES
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
# DATA
# ----------------------------
df = load_data()

# limitar memoria global
df = df.head(300)


# ----------------------------
# FILTROS
# ----------------------------
registro = st.text_input("Buscar por Número de Registro:")

lista_culturas = ["Todas"] + sorted(
    df["Cultura"].dropna().unique()
)

cultura_sel = st.selectbox(
    "Filtrar por Cultura",
    lista_culturas
)

df_filtrado = df

if registro:
    df_filtrado = df_filtrado[
        df_filtrado["Número de Registro"] == registro
    ]

if cultura_sel != "Todas":
    df_filtrado = df_filtrado[
        df_filtrado["Cultura"] == cultura_sel
    ]

# limitar render
df_filtrado = df_filtrado.head(200)

# reset index IMPORTANTE
df_filtrado = df_filtrado.reset_index(drop=True)


# ----------------------------
# TABLA
# ----------------------------
st.subheader("Información del Objeto")

if not df_filtrado.empty:

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
        selection_mode="single-row",
        key="tabla_museo"
    )

    # ----------------------------
    # SELECCIÓN
    # ----------------------------
    seleccion = evento_seleccion.selection.rows

    if seleccion:

        indice_fila = seleccion[0]

        datos_objeto = df_filtrado.iloc[indice_fila]

        st.divider()

        col1, col2 = st.columns([1, 2])

        with col1:

            img_path = get_image(
                datos_objeto["Denominación del Objeto"]
            )

            if os.path.exists(img_path):

                st.image(
                    img_path,
                    caption=datos_objeto["Denominación del Objeto"],
                    use_container_width=True
                )

            else:

                st.image(
                    "https://via.placeholder.com/300?text=Sin+Imagen",
                    use_container_width=True
                )

        with col2:

            st.header(
                f"Ficha Técnica: {datos_objeto['Número de Registro']}"
            )

            with st.container(border=True):

                c1, c2 = st.columns(2)

                with c1:

                    st.write(
                        f"**Denominación:** {datos_objeto['Denominación del Objeto']}"
                    )

                    st.write(
                        f"**Cultura:** {datos_objeto['Cultura']}"
                    )

                    st.write(
                        f"**Año:** {datos_objeto['Año']}"
                    )

                with c2:

                    st.write(
                        f"**Materiales:** {datos_objeto['Materiales']}"
                    )

                    st.write(
                        f"**Zona:** {datos_objeto['Zona Arqueológica']}"
                    )

                    st.write(
                        f"**País:** {datos_objeto['País']}"
                    )

    else:
        st.info(
            "💡 Haz clic en una fila para ver la ficha técnica."
        )

else:
    st.warning(
        "No hay objetos que coincidan con los filtros."
    )