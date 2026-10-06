'''
Descrição: Deletar todos os dados de cada pasta de destino, 
para que não haja conflito de dados.
'''
import pandas as pd
import os

BASE1 = "data_process"
BASE2 = "data_analysis"
# Pasta de dados brutos (só leitura, não precisa ser criada)
data1 = os.path.join(BASE1, "1_data")
data2 = os.path.join(BASE2, "1_data")

# Pastas de saída de cada etapa
stages1 = {
    "clean_files":             "2_clean_data",
    "matrix_files":            "3_matrix_data",
    "selected_matrix":         "4_selected_matrix",
    "renamed_matrix":          "5_renamed_matrix",
    "negative_control_matrix": "6_negative_control_matrix",
    "matrix_without_control":  "7_matrix_without_control",
    "stack_control":           "8_stack_negative_control",
    "stack_matrix":            "9_stack_matrix_without_control",
}

stages2 = {
    "metrics_control": "1_metrics_negative_control",
    "metrics_matrix":  "2_metrics_matrix",
    # "boxplot_control": "3_boxplot_negative_control",  
    # "plate_test":      "4_plate_test",
}

# Monta os caminhos e cria as pastas que não existirem
paths1 = {name: os.path.join(BASE1, folder) for name, folder in stages1.items()}
paths2 = {name: os.path.join(BASE2, folder) for name, folder in stages2.items()}

for path in paths1.values():
    os.makedirs(path, exist_ok=True)

for path in paths2.values():
    os.makedirs(path, exist_ok=True)

# stage1
clean_files             = paths1["clean_files"]
matrix_files            = paths1["matrix_files"]
selected_matrix         = paths1["selected_matrix"]
renamed_matrix          = paths1["renamed_matrix"]
negative_control_matrix = paths1["negative_control_matrix"]
matrix_without_control  = paths1["matrix_without_control"]
stack_control           = paths1["stack_control"]
stack_matrix            = paths1["stack_matrix"]

# stage2
metrics_control = paths2["metrics_control"]
metrics_matrix = paths2["metrics_matrix"]

# Deletar todos os arquivos de cada pasta de destino
def delete_data_folders(folder):
    for file in os.listdir(folder):
        os.remove(os.path.join(folder, file))
        print(f"Deletado: {file}")

#delete_data_folders(data)
# stage1
delete_data_folders(clean_files)
delete_data_folders(matrix_files)    
delete_data_folders(selected_matrix)
delete_data_folders(renamed_matrix)
delete_data_folders(negative_control_matrix)
delete_data_folders(matrix_without_control)
delete_data_folders(stack_control)
delete_data_folders(stack_matrix)
# stage2
delete_data_folders(metrics_control)
delete_data_folders(metrics_matrix)