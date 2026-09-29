'''
Descrição: Deletar todos os dados de cada pasta de destino, 
para que não haja conflito de dados.
'''
import pandas as pd
import os

BASE = "data_process"

# Pasta de dados brutos (só leitura, não precisa ser criada)
data = os.path.join(BASE, "1_data")

# Pastas de saída de cada etapa
stages = {
    "clean_files":             "2_clean_data",
    "matrix_files":            "3_matrix_data",
    "selected_matrix":         "4_selected_matrix",
    "renamed_matrix":          "5_renamed_matrix",
    "negative_control_matrix": "6_negative_control_matrix",
    "matrix_without_control":  "7_matrix_without_control",
}

# Monta os caminhos e cria as pastas que não existirem
paths = {name: os.path.join(BASE, folder) for name, folder in stages.items()}
for path in paths.values():
    os.makedirs(path, exist_ok=True)

clean_files             = paths["clean_files"]
matrix_files            = paths["matrix_files"]
selected_matrix         = paths["selected_matrix"]
renamed_matrix          = paths["renamed_matrix"]
negative_control_matrix = paths["negative_control_matrix"]
matrix_without_control  = paths["matrix_without_control"]

# Deletar todos os arquivos de cada pasta de destino
def delete_data_folders(folder):
    for file in os.listdir(folder):
        os.remove(os.path.join(folder, file))
        print(f"Deletado: {file}")

#delete_data_folders(data)
delete_data_folders(clean_files)
delete_data_folders(matrix_files)    
delete_data_folders(selected_matrix)
delete_data_folders(renamed_matrix)
delete_data_folders(negative_control_matrix)
delete_data_folders(matrix_without_control)
