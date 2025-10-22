"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel
import pandas as pd
import string
import re
def load_data(path):
    # Read file with wide enough columns
    df = pd.read_fwf(path, widths=[6, 12, 18, 200], skiprows=4, header=None)
    df.columns = ["cluster", "cantidad_de_palabras_clave", "porcentaje_de_palabras_clave", "principales_palabras_clave"]

    # Fill cluster numbers for continuation lines
    df["cluster"] = df["cluster"].ffill()

    # Group multiline entries per cluster
    df = (
        df.groupby("cluster", as_index=False)
        .agg({
            "cantidad_de_palabras_clave": "first",
            "porcentaje_de_palabras_clave": "first",
            "principales_palabras_clave": lambda x: " ".join(x.dropna().astype(str))
        })
    )

    # Clean numeric columns
    df["cantidad_de_palabras_clave"] = df["cantidad_de_palabras_clave"].astype(int)

    # Clean percentage text safely before converting
    df["porcentaje_de_palabras_clave"] = (
        df["porcentaje_de_palabras_clave"]
        .astype(str)
        .str.extract(r"([\d,\.]+)")[0]         # take only the number part
        .str.replace(",", ".", regex=False)
        .astype(float)
    )
    df["principales_palabras_clave"] = (
        df["principales_palabras_clave"]
        .str.replace(r"\s+", " ", regex=True)     # collapse multiple spaces
        .str.replace(r"\s+,", ",", regex=True)    # remove spaces before commas
        .str.replace(r",\s+", ", ", regex=True)   # normalize comma spacing
        .str.strip()                              # trim edges
        .str.rstrip(".")                          # remove trailing dot
    )
    return df

    

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    path="files/input/clusters_report.txt"
    
    df=load_data(path)
    print(df.principales_palabras_clave[0])
    return df
    