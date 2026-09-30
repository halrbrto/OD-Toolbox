'''
Descrição: este script serve para calcular as métricas
de cada matriz empilhada pelo pré-processo.

As métricas de cada coluna são: média, desvio padrão,
variância, coeficiente de variação.
'''
import os
import pandas as pd


def calc_metrics(input_dir, output_dir, sep=",", decimal=",", ddof=1,
                 index_col=None, decimals=4):
    """
    ...
    decimals: número de casas decimais na saída (None = sem arredondar).
    """
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if not file.endswith(".csv"):
            continue

        df = pd.read_csv(os.path.join(input_dir, file),
                         index_col=index_col, sep=sep, decimal=decimal)

        # Só colunas numéricas entram no cálculo
        num = df.select_dtypes(include="number")
        ignoradas = set(df.columns) - set(num.columns)
        if ignoradas:
            print(f"[aviso] {file}: colunas não numéricas ignoradas: {sorted(ignoradas)}")

        media = num.mean()
        desvio = num.std(ddof=ddof)
        variancia = num.var(ddof=ddof)
        # CV em %; se a média for 0, vira NaN em vez de inf
        cv = desvio / media.where(media != 0) * 100

        metrics = pd.DataFrame({
            "Média": media,
            "Desvio padrão": desvio,
            "Variância": variancia,
            "CV (%)": cv,
        }).T  # transposta: métricas nas linhas, colunas originais nas colunas

        if decimals is not None:
            metrics = metrics.round(decimals)  # arredonda só na saída

        name = os.path.splitext(file)[0]
        out_path = os.path.join(output_dir, f"{name}_metrics.csv")
        metrics.to_csv(out_path, sep=sep, decimal=decimal)
        print(f"{file} -> {out_path}")