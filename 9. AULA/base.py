#Verificando informações de roubo de carro pelo ponto de vista das cidades

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

#Preparando DADOS
try:
    print("Obtendo dados...")
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    #utf-8, iso-8859-1, latin1, cp1252
    df_ocorrecias = pd.read_csv(ENDERECO_DADOS, sep=";", encoding='iso-8859-1')
   
    #deliminitando variáveis
    df_roubo_veiculo = df_ocorrecias[['munic','roubo_veiculo']]
    
    #totalizando os roubos (agrupando por município)
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()
    
    #manter organizado dos maior pro menor
    df_roubo_veiculo = df_roubo_veiculo.sort_values(by='roubo_veiculo',ascending=False)
    
    # print(df_roubo_veiculo.head(10))

    
except Exception as e:
    print(f'Erro ao obter dados: {e}')

#MEDIDAS - KPI
try:
    # print("===Calculando as Medidas===")
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia = abs((media_roubo_veiculo-mediana_roubo_veiculo)/mediana_roubo_veiculo)
  
    # distancia ate 10% distribuição tem tendencia simetrica / 
    # até 25% a tendencia a distribuição apresentam uma certa assimetria - assimetria moderada - certa dispersão.... extremos estão influenciando no resultado
    # média deve ser descartada / dados assimetricos

    # print(f'\nMedidas de Tendência Central')
    # print("-"*30)
    # print(f'Média: {media_roubo_veiculo:.0f}\nMediana: {mediana_roubo_veiculo:.0f}')
    # print(f'Distância: {distancia:.0%}')


    #50% das cidades do estado teve roubos abaixo de 256 de 2003 até agora
    #o fato da media estar mto maior que a mediana é uma tendência que os extremos estão mto distantes
    #os dados não são simetricos e não tem padrão, são mto diversificados - dados assimétricos
    #nesse caso a média não poderá ser usada como medida de referência.

except Exception as e:
    print(f'Erro ao processar dados: {e}')

#
try:
    # print('\n===Processando os quartis===')

    q1 = np.quantile(array_roubo_veiculo,.25)
    q3 = np.quantile(array_roubo_veiculo,.75)
    
    # print(f'Quartis')
    # print("-"*30)
    # print(f'Q1: {q1:.0f}')
    # print(f'Mediana: {mediana_roubo_veiculo:.0f}')
    # print(f'Q3: {q3:.0f}')
    
    # 25% dos casos de roubo nos municipios do estado do RJ tem números até 48
    # 25% dos casos de roubo nos municipios do estado do RJ tiveram roubos acima de 1017
    
    #municípios com menos roubos
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]

    # print(f'\nMunicipios com menor índice de roubo')
    # print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=False))

    # print(f'\nMunicipios com Maior índice de roubo')
    # print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))

except Exception as e:
    print(f'Erro ao obter medidas descritivas: {e}')


try:
    # print('\n===Medidas de Dispersão===')
    # amplitude_total = (maximo - minimo)
    # Resultado mais próximo do mínimo indica baixa dispersão
    # Resultado zero indica que todos os dados são iguais
    # Resultado mais próximo do máximo indica alta dispesão
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo

    # print(f'Maior Valor: {maximo}')
    # print(f'Menor Valor: {minimo}')
    # print(f'Amplitude Total: {amplitude}')

except Exception as e:
    print(f'Erro ao calcular dispersão: {e}')

# IQR = Intervalo Interquartil
try:
    # print('\n===Calculando Outliers===')
    # iqr - é a amplitude dos dados mais centrais (50% entre 25% e 75%) de qq conjunto de dados
    # iqr = q3 - q1
    # mesmo ponto de observação da amplitude
    # ele ignora os extremos 
    # maximo e minimo estão fora do intervalo interquartil
    # não sofrem interferência
    # quanto mais próximo de q1 mais homogêneos são os dados
    # quanto mais próximo de q3, menos homog~eneos são os dados
    iqr = q3 - q1

    # limite inferior:
    # é uma medida que vai identificar como outliers, os valores abaixo dele
    limite_inferior = q1 - (1.5 * iqr)

    # limite superior
    # é uma medida que vai identificar como outliers, os valores acima dele
    limite_superior = q3 + (1.5 * iqr)

    # print(f'Limite Inferior: {limite_inferior}')
    # print(f'Limite Superior: {limite_superior}')
    # print(f'IQR: {iqr}')

    print(f'\n===Medidas===')
    print(f'Menor Valor: {minimo}')
    print(f'Limite Inferior: {limite_inferior:.0f}')
    print(f'Q1: {q1:.0f}')
    print(f'Mediana: {mediana_roubo_veiculo:.0f}')
    print(f'Q3: {q3:.0f}')
    print(f'Limite Superior: {limite_superior:.0f}')
    print(f'Maior Valor: {maximo}')
    print(f'IQR: {iqr}')


except Exception as e:
    print(f'Erro ao calcular outliers: {e}')


try:
    # outliers superiores
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    
    # outliers superiores
    df_roubo_veiculo_outliers_inferior = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]

    print(f'\n===Municípios - Outliers Inferiores===')
    print("="*40)
    if len(df_roubo_veiculo_outliers_inferior) == 0:
        print("Não existe Outliers Inferiores")
    else:
        print(df_roubo_veiculo_outliers_inferior.sort_values(by='roubo_veiculo', ascending=False))



    print(f'\n===Municípios - Outliers Superiores===')
    print("="*40)
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print("Não existe Outliers Superiores")
    else:
        print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))


#
except Exception as e:
    print(f'Erro ao calcular Outliers: {e}') 


# para ter outliers tem que ser acima do mínimo . no caso limite inferior não tem outliers

try:
    df_roubo_veiculo_maiores = df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False).head(10)
    plt.figure(figsize=(16,8))
    # Plotando o Gráfico Colunas
    # plt.bar(df_roubo_veiculo_maiores['munic'], df_roubo_veiculo_maiores['roubo_veiculo'])
    # plt.barh(df_roubo_veiculo_maiores['munic'], df_roubo_veiculo_maiores['roubo_veiculo'])
    # plt.bar(df_roubo_veiculo_maiores['munic'].head(10), df_roubo_veiculo_maiores['roubo_veiculo'].head(10))
    plt.bar(df_roubo_veiculo_maiores['munic'], df_roubo_veiculo_maiores['roubo_veiculo'])
    plt.title(f'Municípios com Maiores Roubos')
    plt.show()
     
except Exception as e:
    print(f"Erro ao gerar o gráfico: {e}")