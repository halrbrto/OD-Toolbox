'''
Descrição: Pipeline de processamento das matrizes (limpeza, separação,
seleção, renomeação, separação de controles e empilhamento por tag).
'''
import os
import pandas as pd
from modules.mod_process import (clean_files, rename_matrix, separate_control, stack_lines)
from modules.mod_process import select_lin_col, separate_matrix

BASE = "data_process"

# Pastas de cada etapa
stages = {
    "data":                    "1_data",
    "clean":                   "2_clean_data",
    "matrix":                  "3_matrix_data",
    "selected":                "4_selected_matrix",
    "renamed":                 "5_renamed_matrix",
    "negative_control":        "6_negative_control_matrix",
    "without_control":         "7_matrix_without_control",
    "stack_control":           "8_stack_negative_control",
    "stack_matrix":            "9_stack_matrix_without_control",
}

# Monta os caminhos e cria as pastas que não existirem
paths = {name: os.path.join(BASE, folder) for name, folder in stages.items()}
for path in paths.values():
    os.makedirs(path, exist_ok=True)

# Execução do pipeline
clean_files(paths["data"], paths["clean"])
separate_matrix(paths["clean"], paths["matrix"])
select_lin_col(paths["matrix"], paths["selected"])
rename_matrix(paths["selected"], paths["renamed"])
separate_control(paths["renamed"], paths["negative_control"], paths["without_control"])

# Empilha as linhas dos arquivos {tag}_matrix{n}.csv de mesma tag
stack_lines(paths["negative_control"], paths["without_control"],
            paths["stack_control"], paths["stack_matrix"])
