'''
Descrição: Selecionar colunas e linhas de cada matriz,
de acordo com a configuração definida em config.txt.
'''
import os
import pandas as pd
from .config_utils import load_bool_config

def select_lin_col(matrix_arquives, selected_matrix):
    os.makedirs(selected_matrix, exist_ok=True)

    # Configurações lidas do config.txt
    col_config = load_bool_config('col_select')
    lin_config = load_bool_config('lin_select')

    index_col = [i for i, select in enumerate(col_config) if select]
    index_lin = [i for i, select in enumerate(lin_config) if select]

    for file in os.listdir(matrix_arquives):

        # Carregar arquivo
        path = os.path.join(matrix_arquives, file)
        df = pd.read_csv(path)

        # Verifica se a configuração cabe na matriz
        if df.shape[1] != len(col_config) or df.shape[0] != len(lin_config):
            print(f"{file}: matriz {df.shape[0]}x{df.shape[1]}, mas config espera "
                  f"{len(lin_config)}x{len(col_config)}. Arquivo ignorado.")
            continue

        # Selecionar colunas e linhas
        df = df.iloc[index_lin, index_col]

        # Salvar
        path_save = os.path.join(selected_matrix, file)
        df.to_csv(path_save, index=False) 
        print(f"Processado: {file}")