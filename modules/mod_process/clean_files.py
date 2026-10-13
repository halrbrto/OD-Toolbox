'''
Descrição: Limpa o ruído dos arquivos CSV,
removendo linhas e colunas desnecessárias, 
e renomeando as colunas restantes.

Esta versão aplica a limpeza para todas as replicatas
de leitura de uma mesma amostra, gerando arquivos limpos 
e matrizes separadas.
'''
import pandas as pd
import os


def read_any_csv(path, **kwargs):
    '''
    Lê CSV exportado por diferentes programas:
    - Google Drive: UTF-8, separado por vírgula
    - LibreOffice (Texto Unicode): UTF-16, separado por tabulação
    '''
    # Detecta UTF-16 pelo BOM; senão, assume UTF-8
    with open(path, 'rb') as f:
        bom = f.read(2)
    encoding = 'utf-16' if bom in (b'\xff\xfe', b'\xfe\xff') else 'utf-8-sig'

    # sep=None + engine='python' detecta vírgula ou tabulação sozinho
    return pd.read_csv(path, encoding=encoding, sep=None,
                       engine='python', **kwargs)


def clean_files(folder, clean_arquives):
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

    for file in os.listdir(folder):
        # Carregamento do arquivo (aceita UTF-8/vírgula e UTF-16/tabulação)
        df = read_any_csv(os.path.join(folder, file))
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

        # Salvando o arquivo com as colunas renomeadas (sempre UTF-8, vírgula)
        df.to_csv(os.path.join(clean_arquives, file), index=False)

def separate_matrix(clean_arquives, matrix_arquives):

    for file in os.listdir(clean_arquives):

        # Verificar se o arquivo é um CSV
        if not file.endswith(".csv"):
            continue

        # Aqui pd.read_csv basta: são arquivos gerados pelo clean_files
        df = pd.read_csv(os.path.join(clean_arquives, file))

        # Separar em matrizes de 6 linhas
        for i in range(0, len(df), 6):
            # Criar uma matriz individual com 6 linhas
            matrix = df.iloc[i:i+6, :]
            numero_matrix = i // 6 + 1

            # Excluir linhas vazias
            matrix = matrix.dropna(how='any', axis=0)

            name_exit = file.replace(".csv", f"_matrix{numero_matrix}.csv")
            path_exit = os.path.join(matrix_arquives, name_exit)

            matrix.to_csv(path_exit, index=False)