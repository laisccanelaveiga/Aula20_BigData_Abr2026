import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

try:
    print("Obtendo dados...")
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_estelionato = pd.read_csv(ENDERECO_DADOS, sep=";",encoding='iso-8859-1')
    df_estelionato = df_estelionato[['mes_ano', 'estelionato']]
    df_estelionato = df_estelionato.groupby('mes_ano', as_index=False)['estelionato'].sum()
    df_estelionato = df_estelionato.sort_values(by='mes_ano', ascending=False)
    # print(df_estelionato.head(10))

except Exception as e:
    print(f'Erro ao obter dados: {e}')

#MEDIDAS
try:
    array_estelionato = np.array(df_estelionato['estelionato'])
    media_estelionato = np.mean(array_estelionato)
    mediana_estelionato = np.median(array_estelionato)
    distancia = abs((media_estelionato-mediana_estelionato)/mediana_estelionato)
    q1 = np.quantile(array_estelionato, .25)
    q3 = np.quantile(array_estelionato, .75)
    maiores = np.max(array_estelionato)
    menores = np.min(array_estelionato)
    amplitude = maiores - menores
    iqr = q3 - q1
    limite_inferior = q1 - (1.5 * iqr)
    limite_superior = q3 + (1.5 * iqr)



except Exception as e:
    print(f'Erro ao processar medidadas: {e}')


#ANALISANDO RESULTADOS
try:
    print('=========Resultados=========')
    print(f'Média: {media_estelionato:.0f}')
    print(f'Mediana: {mediana_estelionato:.0f}')
    print(f'Amplitude Total: {amplitude}')
    print(f'Distância: {distancia:.0%}')
    print(f'Menor valor: {menores:.0f}')
    print(f'Limite Inferior: {limite_inferior:.0f}')
    print(f'Q1: {q1:.0f}')
    print(f'Limite Superior: {limite_superior:.0f}')
    print(f'Maior valor: {maiores:.0f}')
    print(f'Q3: {q3:.0f}')
    print(f'IQR: {iqr:.0f}')

except Exception as e:
    print(f'Erro apresentar medidas: {e}')


try:
    df_estelionato_maiores = df_estelionato[df_estelionato['estelionato'] > q3]
    df_estelionato_menores = df_estelionato[df_estelionato['estelionato'] < q1]
    df_outliers_superior = df_estelionato[df_estelionato['estelionato'] > limite_superior]

    print('========= Maiores Casos de Estelionato =========')
    print(df_estelionato_maiores.sort_values(by='estelionato', ascending=False).head(15))
    
    print('========= Menores Casos de Estelionato =========')
    print(df_estelionato_menores.sort_values(by='estelionato', ascending=True).head(15))
    
    print('========= Outliers Superior =========')
    print(df_outliers_superior.sort_values(by='estelionato', ascending=False).head(15))
    
    print('========= Análise Geral =========')
    print("""
    A média está bem acima da mediana — uma distância de 49% entre elas —, o que indica 
    que o conjunto de dados é assimétrico e sem padrão uniforme. 
    A amplitude total de 14.846 confirma alta dispersão: há meses com volumes muito baixos 
    e outros com picos expressivos de estelionato. 
    No geral, os dados são heterogêneos e exigem atenção a outliers antes de qualquer conclusão.
    ---A análise dos outliers reforça essa assimetria: o limite superior calculado foi de 6.958,
    O pico histórico ocorreu em março de 2026, com 15.563 casos, mais que o dobro do limite superior.
    Isso indica uma tendência estrutural de crescimento no volume de estelionato ao longo dos anos,
    e não episódios isolados. Os dados mais recentes (2024-2026) concentram os maiores índices,
    sugerindo que o problema se intensificou de forma consistente no período analisado.---
    """)


except Exception as e:
    print(f'Erro a demonstrar os resultados: {e}')


try:
    # df_estelionato_maiores = df_estelionato_maiores.sort_values(by='estelionato', ascending=False).head(10)
    # plt.figure(figsize=(16,8))
    # plt.bar(df_estelionato_maiores['mes_ano'], df_estelionato_maiores['estelionato'])
    # plt.title(f'Ranking Top 10')
    # plt.show()
    
    plt.subplots(2,2, figsize=(18,10))

    # Posição 1 
    plt.subplot(2, 2, 1)    
    # showfliers=False para tirar o outliers
    plt.boxplot(array_estelionato, vert=False, showmeans=True )
    plt.title('BoxPlot da Distribuição')

    # Posição 2
    plt.subplot(2, 2, 2)
    plt.text(0.1, 0.9, f'Média: {media_estelionato:.0f}')
    plt.text(0.1, 0.8, f'Distância: {distancia:.0%}')
    plt.text(0.1, 0.7, f'Limite Inferior: {limite_inferior:.0f}')
    plt.text(0.1, 0.6, f'Mínimo: {menores:.0f}')
    plt.text(0.1, 0.5, f'Q1: {q1:.0f}')
    plt.text(0.1, 0.4, f'Mediana: {mediana_estelionato:.0f}')
    plt.text(0.1, 0.3, f'Q3: {q3:.0f}')
    plt.text(0.1, 0.2, f'Limite Superior: {limite_superior:.0f}')
    plt.text(0.1, 0.1, f'Máximo: {maiores:.0f}')
    plt.text(0.1, 0.0, f'Amplitude Total: {amplitude:.0f}')
    plt.axis('off')
    plt.title('Resumo Estatístico')

    # Posição 3
    plt.subplot(2, 2, 3)
    df_outliers_superior = (
        df_outliers_superior
        .sort_values(by='estelionato', ascending=True)
        .head(10)
        .sort_values(by='estelionato', ascending=False)
    )
    plt.bar(
        df_outliers_superior['mes_ano'],
        df_outliers_superior['estelionato']
    )
    plt.xticks(rotation=45, ha='right')
    deslocamento = max(df_outliers_superior['estelionato']) * 0.02
    for i, valor in enumerate(df_outliers_superior['estelionato']):
            plt.text(
                i, #posição Y
                valor, #posição X
                f'{valor:,}',
                ha='center'
            )
    plt.title('Períodos c/ Outliers Superiores')

    # # Posição 4 - Outliers Inferiores ou Menores
    plt.subplot(2, 2, 4)
    
    df_estelionato_menores = (
        df_estelionato_menores
        .sort_values(by='estelionato', ascending=True)
        .head(10)
        .sort_values(by='estelionato', ascending=False)
    )
    plt.barh(
        df_estelionato_menores['mes_ano'],
        df_estelionato_menores['estelionato']
        )
    deslocamento = max(df_estelionato_menores['estelionato']) * 0.02

    # Rótulo de Dados
    for i, valor in enumerate(df_estelionato_menores['estelionato']):
        plt.text(
            valor, #posição X
            i, #posição Y
            f'{valor:,}',
            ha='left'
        )
    plt.title('Períodos c/ Menores Estelionato')




    plt.show()

except Exception as e:
    print(f'Erro ao gerar Gráfico: {e}')
