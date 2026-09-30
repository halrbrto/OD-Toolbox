'''
Descrição: Pipeline de análise das matrizes empilhadas pelo pré-processo.
Entrada: pastas 8 e 9 de data_process. Saída: pastas dentro de data_analysis.
'''
import os
from modules.mod_analysis import calc_metrics

BASE_IN = "data_process"
BASE_OUT = "data_analysis"

# Entradas: últimas duas etapas do pré-processamento
inputs = {
    "stack_control": os.path.join(BASE_IN, "8_stack_negative_control"),
    "stack_matrix":  os.path.join(BASE_IN, "9_stack_matrix_without_control"),
}

# Pastas de saída de cada etapa da análise
stages = {
    "metrics_control": "1_metrics_negative_control",
    "metrics_matrix":  "2_metrics_matrix",
    # "boxplot_control": "3_boxplot_negative_control",
    # "plate_test":      "4_plate_test",
}
outputs = {name: os.path.join(BASE_OUT, folder) for name, folder in stages.items()}

# Confere se as entradas existem e têm CSVs (evita rodar em pasta vazia)
for name, path in inputs.items():
    if not os.path.isdir(path):
        raise FileNotFoundError(f"Pasta de entrada não encontrada: {path} "
                                f"(rode o exec.py antes)")
    if not any(f.endswith(".csv") for f in os.listdir(path)):
        raise FileNotFoundError(f"Nenhum .csv em {path}")

for path in outputs.values():
    os.makedirs(path, exist_ok=True)

# Execução da análise
# Métricas por coluna (média, desvio padrão, variância, CV)
calc_metrics(inputs["stack_control"], outputs["metrics_control"])
calc_metrics(inputs["stack_matrix"],  outputs["metrics_matrix"])

# Analisar controle Negativo (Box-Plot)

# Teste de placas:
# Analisar variação de replicata (Gráfico de linhas Vs. Replicatas)
# Mostrar variação de cada placa