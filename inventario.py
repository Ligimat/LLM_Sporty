import pandas as pd
import os

def cargar_inventario(filepath):
    # Carga el archivo Excel y devuelve una lista de máquinas
    df = pd.read_excel(filepath)
    lista = list(df["MAQUINA"])
    return lista


ruta_relativa = os.path.join('docs', 'inventario.xlsx')

# Cargar el inventario usando la ruta relativa
inventario_df = cargar_inventario(ruta_relativa)
