'''
Descrição: Juntar as linhas de arquivos {tag}_matrix{n}.csv que
tenham a mesma tag, separadamente para controles e dados.
'''
import os
import re
from collections import defaultdict
import pandas as pd

PATTERN = re.compile(r"^(?P<tag>.+)_matrix(?P<n>[1-9]\d*)\.csv$")


def _stack_dir(input_dir, output_dir, sep=",", decimal=","):
    """Empilha, por tag, os arquivos {tag}_matrix{n}.csv de input_dir."""
    os.makedirs(output_dir, exist_ok=True)

    # 1) Agrupa os arquivos por tag: {tag: [(n, nome_do_arquivo), ...]}
    groups = defaultdict(list)
    for file in os.listdir(input_dir):
        m = PATTERN.match(file)
        if m is None:
            continue  # ignora arquivos fora do padrão
        groups[m.group("tag")].append((int(m.group("n")), file))

    # 2) Para cada tag, carrega na ordem de n e empilha as linhas
    for tag, items in groups.items():
        items.sort()  # ordena por n (numérico)
        dfs = [
            pd.read_csv(os.path.join(input_dir, f), index_col=0,
                        sep=sep, decimal=decimal)
            for _, f in items
        ]

        # Avisa se as colunas não forem idênticas (concat preencheria com NaN)
        cols_ref = set(dfs[0].columns)
        for (n, f), d in zip(items, dfs):
            if set(d.columns) != cols_ref:
                print(f"[aviso] {f}: colunas diferentes das de {items[0][1]}")

        stacked = pd.concat(dfs, axis=0)  # empilha as linhas

        # Avisa se houver rótulos de linha repetidos entre os arquivos
        if stacked.index.duplicated().any():
            print(f"[aviso] tag '{tag}': rótulos de linha duplicados após empilhar")

        out_path = os.path.join(output_dir, f"{tag}_stack.csv")
        stacked.to_csv(out_path, sep=sep, decimal=decimal)
        print(f"{tag}: {len(items)} arquivo(s) -> {stacked.shape[0]} linhas -> {out_path}")


def stack_lines(input_dir_ctrl, input_dir_matrix,
                output_stack_crtl, output_stack_matrix,
                sep=",", decimal=","):
    _stack_dir(input_dir_ctrl, output_stack_crtl, sep, decimal)
    _stack_dir(input_dir_matrix, output_stack_matrix, sep, decimal)