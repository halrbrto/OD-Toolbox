'''
Descrição: Limpa o ruído dos arquivos CSV,
removendo linhas e colunas desnecessárias, 
e renomeando as colunas restantes.
'''
import pandas as pd
import os

# Seleção da Pasta de Dados
folder = os.path.join("data_process/1_data")

# Pasta de destino dos arquivos limpos
clean_arquives = os.path.join("data_process/2_clean_data")

# Se a pasta de destino dos arquivos limpos não existir, cria a pasta
if not os.path.exists("data_process/2_clean_data"):
    os.makedirs("data_process/2_clean_data")

'''
Configuração de Colunas do Arquivo (Manual)
'''
Coluna_1 = 'A'
Coluna_2 = 'B'
Coluna_3 = 'C'
Coluna_4 = 'D'
Coluna_5 = 'E'
Coluna_6 = 'F'
Coluna_7 = 'G'
Coluna_8 = 'H'
def clean_files(folder, clean_arquives):
    for file in os.listdir(folder):
        # Carregamento do arquivo
        df = pd.read_csv(os.path.join(folder, file))
        # Deletar as 3 primeiras linhas do arquivo
        df = df.iloc[2:]
        # Deletar as duas primeiras colunas do arquivo
        df = df.iloc[:, 2:]
        # Deletar colunas a partir da coluna 7
        df = df.iloc[:, :8]
        # Deletar linhas com valores nulos
        df = df.dropna()
        # Renomeando as colunas
        df.columns = [Coluna_1, Coluna_2, Coluna_3, Coluna_4, Coluna_5, Coluna_6, Coluna_7, Coluna_8]

        # Salvando o arquivo com as colunas renomeadas
        df.to_csv(os.path.join(clean_arquives, file), index=False)

clean_files(folder, clean_arquives)