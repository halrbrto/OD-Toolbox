'''
Descrição: este script serve para extrair as
horas de cada observação do experimento pela tag
e plotar as métricas de cada observação em função do tempo.
'''
import os
import matplotlib.pyplot as plt
import pandas as pd


def tag_to_datetime(tag):
    """Converte a tag VX_{dia}_{mes}_{ano}_{hora}H em Timestamp."""
    parts = tag.split("_")  # ex.: ['V0', '03', '10', '2026', '9H']
    day, month, year, hour = parts[1], parts[2], parts[3], parts[4][:-1]
    return pd.to_datetime(f"{year}-{month}-{day} {hour}:00")


def plot_curve(folder, output_path=None):
    """
    Lê os CSVs <tag>.csv da pasta, calcula a hora de cada observação
    (horas decorridas desde V0) e plota média ± desvio padrão por coluna.
    folder: pasta com os CSVs (ex.: data_analysis/3_remove_negative_control).
    output_path: se informado, salva a figura nesse caminho.
    Retorna (médias, desvios): DataFrames com índice em horas.
    """
    obs = []
    for name in os.listdir(folder):
        if not name.endswith(".csv"):
            continue
        tag = os.path.splitext(name)[0]
        df = pd.read_csv(os.path.join(folder, name), index_col=0, decimal=",")
        df = df.apply(pd.to_numeric, errors="coerce")
        obs.append((tag_to_datetime(tag), df))

    if not obs:
        raise FileNotFoundError(f"Nenhum .csv em {folder}")

    obs.sort(key=lambda x: x[0])  # ordem cronológica
    t0 = obs[0][0]

    hours = [(dt - t0).total_seconds() / 3600 for dt, _ in obs]
    means = pd.DataFrame([df.loc["Média"] for _, df in obs], index=hours)
    stds = pd.DataFrame([df.loc["Desvio padrão"] for _, df in obs], index=hours)

    fig, ax = plt.subplots(figsize=(8, 5))
    for col in means.columns:
        ax.errorbar(means.index, means[col], yerr=stds[col],
                    fmt="-o", capsize=3, label=col)

    ax.set_xlabel("Tempo (h)")
    ax.set_ylabel("Média (controle negativo descontado)")
    ax.legend(title="Coluna")
    fig.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=300)
    plt.show()

    return means, stds


plot_curve("data_analysis/3_remove_negative_control")