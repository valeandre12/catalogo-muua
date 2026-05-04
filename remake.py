import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

excel_path = os.path.join(BASE_DIR, "LIBRODEREGISTRO.xlsx")
csv_path = os.path.join(BASE_DIR, "LIBRODEREGISTRO.csv")

df = pd.read_excel(excel_path)

df = df[
    [
        "Número de Registro",
        "Fecha de ingreso",
        "Denominación del Objeto",
        "Cultura",
        "Materiales",
        "Zona Arqueológica",
        "País"
    ]
]

df.to_csv(csv_path, index=False)

print("CSV creado en:", csv_path)