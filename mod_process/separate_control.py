'''
Descrição: Por definição, a primeira linha (ou coluna)
é a série de controle negativo, e deve ser removida
e analisada separadamente. 
'''
import os
import pandas as pd

def separate_control(input_dir, output_ctrl_dir, output_matrix_dir):
    
    for file in os.listdir(input_dir):
        if not file.endswith(".csv"):
            continue

        # Carregamento do arquivo (primeira coluna = rótulos das linhas)
        df = pd.read_csv(os.path.join(input_dir, file), index_col=0)

        # Primeira linha = controle negativo
        controle = df.iloc[[0]]

        # Matriz sem o controle negativo
        df_without_crtl = df.iloc[1:]

        # Salvar os dois resultados
        controle.to_csv(os.path.join(output_ctrl_dir, file))
        df_without_crtl.to_csv(os.path.join(output_matrix_dir, file))
