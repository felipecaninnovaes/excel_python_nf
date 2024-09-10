import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def plotar_entrada_saida(entrada, saida):
    # Definindo o estilo do gráfico
    plt.style.use('ggplot')

    # Meses
    meses = list(entrada.keys())

    # Valores de entrada e saída
    valores_entrada = list(entrada.values())
    valores_saida = list(saida.values())

    # Configuração das barras
    largura = 0.35  # Largura das barras
    posicoes = range(len(meses))

    # Ajustando o tamanho da figura
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotando as barras
    barras_entrada = ax.bar(posicoes, valores_entrada, largura, label='Entrada')
    barras_saida = ax.bar([p + largura for p in posicoes], valores_saida, largura, label='Saída')

    # Adicionando os valores no topo das barras de entrada
    for barra in barras_entrada:
        altura = barra.get_height()
        ax.annotate(f'R$ {altura:,.2f}'.replace('.', 'X').replace(',', '.').replace('X', ','),  # Limitar a 2 casas decimais
                    xy=(barra.get_x() + barra.get_width() / 2, altura),
                    xytext=(0, 5),  # 5 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    # Adicionando os valores no topo das barras de saída
    for barra in barras_saida:
        altura = barra.get_height()
        ax.annotate(f'R$ {altura:,.2f}'.replace('.', 'X').replace(',', '.').replace('X', ','),  # Limitar a 2 casas decimais
                    xy=(barra.get_x() + barra.get_width() / 2, altura),
                    xytext=(0, 5),  # 5 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    # Configurações adicionais
    ax.set_xlabel('Meses', fontsize=12)
    ax.set_ylabel('Valores', fontsize=12)
    ax.set_title('Entrada e Saída por Mês', fontsize=14)
    ax.set_xticks([p + largura / 2 for p in posicoes])
    ax.set_xticklabels(meses, fontsize=10)
    ax.legend(loc='upper left', fontsize=12)

    # Adicionando uma grade
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Formatando os valores do eixo y como dinheiro
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'R$ {x:,.2f}'.replace('.', 'X').replace(',', '.').replace('X', ',')))

    # Ajustando a altura do gráfico para evitar sobreposição
    plt.tight_layout(pad=3.0)
    plt.show()