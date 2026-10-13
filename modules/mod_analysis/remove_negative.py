'''
Descrição: este script serve para remover o valor
do controle negativo de cada matriz empilhada 
pelo pré-processo.
'''
import os
import pandas as pd

def extract_tag(tag_name):
    """Retorna a tag VX_{data}_{hora} (ex.: V0_03_10_2026_9H), ou None."""
    parts = os.path.splitext(tag_name)[0].split("_")
    for i, part in enumerate(parts):
        if part.startswith("V") and part[1:].isdigit():
            for j in range(i + 1, len(parts)):
                p = parts[j]
                if p.endswith("H") and p[:-1].isdigit():
                    return "_".join(parts[i:j + 1])
            return None  # achou VX, mas não achou a hora
    return None

def load_folder(folder):
    """Lê todos os *_metrics.csv da pasta e devolve {tag: DataFrame}."""
    data = {}
    for name in sorted(os.listdir(folder)):
        if not name.endswith("_metrics.csv"):
            continue
        tag = extract_tag(name)
        if tag is None:
            print(f"Warning: no tag in {name}, skipped.")
            continue
        df = pd.read_csv(os.path.join(folder, name), index_col=0, decimal=",")
        data[tag] = df.apply(pd.to_numeric, errors="coerce")
    return data


def removal_control(control, matrix, output_folder):
    """
    control, matrix: dicionários {tag: DataFrame} (saída de load_folder).
    output_folder: pasta onde os CSVs corrigidos serão salvos, um por tag (<tag>.csv).
    Retorna {tag: DataFrame} com a matriz já descontada.
    """
    os.makedirs(output_folder, exist_ok=True)

    for tag in sorted(set(control) ^ set(matrix)):
        print(f"Warning: tag {tag} exists in only one of the folders, skipped.")

    results = {}
    for tag in sorted(set(control) & set(matrix)):
        df_m = matrix[tag].copy()
        mean_c = control[tag].loc["Média"]

        # Colunas da matriz sem par no controle
        unpaired = [c for c in df_m.columns if c not in mean_c.index]
        if unpaired:
            print(f"Warning: {tag}: columns without a match in control: {unpaired}")

        # coluna[matriz] - coluna[controle], alinhado pelo nome da coluna
        df_m.loc["Média"] = (df_m.loc["Média"] - mean_c.reindex(df_m.columns)).round(4)

        path = os.path.join(output_folder, f"{tag}.csv")
        df_m.to_csv(path, decimal=",", encoding="utf-8")
        results[tag] = df_m
        print(f"Saved: {path}")

    return results