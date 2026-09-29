'''
Descrição: Deletar todos os dados de cada pasta de destino, 
para que não haja conflito de dados.
'''
import pandas as pd
import os

# Seleção da Pasta de Dados
folder = os.path.join("data_process/1_data")

# Pasta de destino dos arquivos limpos
clean_arquives = os.path.join("data_process/2_clean_data")

# Pasta de destino dos arquivos de matrizes separadas
matrix_arquives = os.path.join("data_process/3_matrix_data")

# Pasta de destino dos arquivos de matrizes selecionadas
selected_matrix = os.path.join("data_process/4_selected_matrix")

# Deletar todos os arquivos de cada pasta de destino
def delete_data_folders(folder):
    for file in os.listdir(folder):
        os.remove(os.path.join(folder, file))
        print(f"Deletado: {file}")

#delete_data_folders(folder)
delete_data_folders(clean_arquives)
delete_data_folders(matrix_arquives)    
delete_data_folders(selected_matrix)

