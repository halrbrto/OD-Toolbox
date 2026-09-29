'''
Descrição: Selecionar colunas e linhas de cada matriz, 
de acordo com a configuração definida.
'''
import os
import pandas as pd

def select_lin_col(matrix_arquives,selected_matrix):
    '''
     CONFIGURAÇÃO DAS COLUNAS (Manual)
     Obs: é interessante aqui criar uma chama de arquivo .txt
     com as configurações de seleção para evitar mexer no módulo.
    '''
    Col_1 = False
    Col_2 = True
    Col_3 = True
    Col_4 = True
    Col_5 = True
    Col_6 = True
    Col_7 = False
    Col_8 = False
    Col_9 = False

    '''
    # CONFIGURAÇÃO DAS LINHAS
    '''
    Lin_1 = True
    Lin_2 = True
    Lin_3 = True
    Lin_4 = False
    Lin_5 = False
    Lin_6 = False

    if not os.path.exists(selected_matrix):
        os.makedirs(selected_matrix)
    # Lista com as configurações das colunas
    col_config = [Col_1,Col_2,Col_3,Col_4,Col_5,Col_6,Col_7,Col_8,Col_9]

    # Lista com as configurações das linhas
    lin_config = [Lin_1,Lin_2,Lin_3,Lin_4,Lin_5,Lin_6]

    for file in os.listdir(matrix_arquives):

        # Carregar arquivo
        path = os.path.join(matrix_arquives, file)
        df = pd.read_csv(path)

        # Selecionar colunas
        index_col = [i for i, select in enumerate(col_config) if select]
        df = df.iloc[:, index_col]

        # Selecionar linhas
        index_lin = [i for i, select in enumerate(lin_config) if select]
        df = df.iloc[index_lin]

        # Salvar
        path_save = os.path.join(selected_matrix, file)
        df.to_csv(path_save, index=False)
        print(f"Processado: {file}")
