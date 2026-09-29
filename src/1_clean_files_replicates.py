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

# Seleção da Pasta de Dados
folder = os.path.join("1_data")

# Pasta de destino dos arquivos limpos
clean_arquives = os.path.join("2_clean_data")

# Pasta de destino dos arquivos de matrizes separadas
matrix_arquives = os.path.join("3_matrix_data")

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

def separate_matrix(clean_arquives, matrix_arquives):

    # Percorrer os arquivos da pasta
    for file in os.listdir(clean_arquives):

        # Processar somente arquivos CSV
        if not file.endswith(".csv"):
            continue

        # Carregamento do arquivo
        caminho = os.path.join(clean_arquives, file)
        df = pd.read_csv(caminho)

        # Resetar o índice
        df = df.reset_index(drop=False)

        # Separar em matrizes de 6 linhas
        for i in range(0, len(df), 6):

            # Criar uma matriz 6 x 8
            matrix = df.iloc[i:i+6, :]

            # Número da matriz
            numero_matrix = i // 6 + 1

            # Resetar o índice
            matrix = matrix.reset_index(drop=False)


            # Deletar colunas level_0, index
            matrix = matrix.drop(columns=['level_0', 'index'], errors='ignore')
    
            # Nome do arquivo de saída
            nome_saida = file.replace(
                ".csv",
                f"_matrix{numero_matrix}.csv"
            )

            # Caminho completo
            caminho_saida = os.path.join(
                matrix_arquives,
                nome_saida
            )
            # Excluir linha 8 vazia
            matrix = matrix.dropna(how='any', axis=0)

            # Salvar
            matrix.to_csv(caminho_saida,index=True)

separate_matrix(clean_arquives, matrix_arquives)