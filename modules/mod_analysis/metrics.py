'''
Descrição: este script serve para calcular as métricas
de cada matriz empilhada pelo pré-processo.

As métricas de cada coluna são: média, desvio padrão,
variância, coeficiente de variação.
'''
import os
import pandas as pd


def calc_metrics(input_dir, output_dir, sep=",", decimal=",", ddof=1,
                 index_col=None, decimals=4, var_decimals=8):
    """
    decimals:     casas decimais de média, desvio padrão e CV (None = sem arredondar).
    var_decimals: casas decimais da variância (None = sem arredondar). Precisa ser
                  maior que `decimals`, pois a variância de dados na escala de 0,1
                  é da ordem de 1e-5 e viraria 0,0 com 4 casas.
    """
    os.makedirs(output_dir, exist_ok=True)

    def arredonda(serie, casas):
        return serie if casas is None else serie.round(casas)

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
        # (calculado com valores sem arredondar)
        cv = desvio / media.where(media != 0) * 100

        # Arredonda só na saída, cada métrica com sua precisão
        metrics = pd.DataFrame({
            "Média": arredonda(media, decimals),
            "Desvio padrão": arredonda(desvio, decimals),
            "Variância": arredonda(variancia, var_decimals),
            "CV (%)": arredonda(cv, decimals),
        }).T  # transposta: métricas nas linhas, colunas originais nas colunas

        name = os.path.splitext(file)[0]
        out_path = os.path.join(output_dir, f"{name}_metrics.csv")
        metrics.to_csv(out_path, sep=sep, decimal=decimal)
        print(f"{file} -> {out_path}")