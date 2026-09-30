'''
Descrição: Renomear as colunas de cada matriz,
de acordo com a configuração definida.
'''
import os
import pandas as pd
from .config_utils import load_config

def rename_matrix(selected_matrix, renamed_matrix):
    os.makedirs(renamed_matrix, exist_ok=True)

    col_names = load_config('col_names')

    for file in os.listdir(selected_matrix):
        if not file.endswith(".csv"):
            continue

        # decimal=',' faz o pandas ler "0,1259" como número (0.1259)
        df = pd.read_csv(os.path.join(selected_matrix, file), decimal=',')

        if len(df.columns) != len(col_names):
            print(f"{file}: {len(df.columns)} colunas, mas {len(col_names)} nomes. Arquivo ignorado.")
            continue

        df.columns = col_names

        df.to_csv(os.path.join(renamed_matrix, file), index=False, decimal=',')