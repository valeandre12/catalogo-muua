import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

excel_path = os.path.join(BASE_DIR, "LIBRODEREGISTRO.xlsx")
csv_path = os.path.join(BASE_DIR, "LIBRODEREGISTRO.csv")

df = pd.read_excel(excel_path)

# limpiar nombres
df.columns = df.columns.str.strip()
#
# columnas útiles
columnas = [
    "Número de Registro",
    "Número de Inventario",
    "Número de Tenencia",
    "Colección",
    "Tipo de colección",
    "Área",
    "Subárea",
    "Grupo de Colección",
    "Fecha de ingreso",
    "Denominación del Objeto",
    "Forma",
    "Observaciones",
    "Categoría",
    "Avalúo",
    "Cultura",
    "Zona Arqueológica",
    "Nombre Sitio Arqueológico",
    "Corregimiento/inspección/vereda",
    "Ciudad",
    "Departamento",
    "País",
    "Periodo",
    "Cronología",
    "Materiales",
    "Materia Prima",
    "Unidad soporte",
    "Color",
    "Técnica elaboración",
    "Técnica decoración",
    "Técnica acabado",
    "Unidad medida lineal",
    "Alto",
    "Ancho",
    "Largo",
    "Profundidad",
    "Peso",
    "Ubicación Interna",
    "Montaje",
    "Ubicación Externa",
    "Fecha de revisión"
]

# filtrar columnas existentes
columnas_existentes = [
    c for c in columnas if c in df.columns
]

df = df[columnas_existentes]

# exportar
df.to_csv(
    csv_path,
    index=False
)

print("CSV creado en:")
print(csv_path)
print(f"Columnas exportadas: {len(columnas_existentes)}")
