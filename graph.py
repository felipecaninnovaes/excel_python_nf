import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def plotar_entrada_saida(entrada, saida):
    # Meses
    meses = list(entrada.keys())

    # Valores de entrada e saída
    valores_entrada = list(entrada.values())
    valores_saida = list(saida.values())

    # Configuração das barras
    largura = 0.35  # Largura das barras
    posicoes = range(len(meses))

    # Plotando as barras
    fig, ax = plt.subplots()
    barras_entrada = ax.bar(posicoes, valores_entrada, largura, label='Entrada')
    barras_saida = ax.bar([p + largura for p in posicoes], valores_saida, largura, label='Saída')

    # Adicionando rótulos e título
    ax.set_xlabel('Meses')
    ax.set_ylabel('Valores')
    ax.set_title('Entrada e Saída por Mês')
    ax.set_xticks([p + largura / 2 for p in posicoes])
    ax.set_xticklabels(meses)
    ax.legend()

    # Formatando os valores do eixo y como dinheiro
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'R$ {x:,.2f}'.replace('.', 'X').replace(',', '.').replace('X', ',')))

    # Mostrando o gráfico
    plt.show()
