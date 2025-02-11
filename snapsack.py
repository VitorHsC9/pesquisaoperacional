# Vitor Hugo Sousa Campos
# 20221011090051

import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# --- Parâmetros do Problema ---
itens = {
    1: {"peso": 4, "valor": 10, "cor": "red"},
    2: {"peso": 2, "valor": 6, "cor": "blue"},
    3: {"peso": 6, "valor": 11, "cor": "green"},
    4: {"peso": 3, "valor": 6, "cor": "yellow"},
    5: {"peso": 5, "valor": 9, "cor": "orange"},
    6: {"peso": 7, "valor": 12, "cor": "purple"},
}
peso_maximo = 17
num_itens = len(itens)

# --- Parâmetros do Algoritmo Genético ---
tamanho_populacao = 50
taxa_crossover = 0.7
taxa_mutacao = 0.01
num_geracoes = 150 
tamanho_torneio = 3
elitismo = True
num_elitismo = 2 if elitismo else 0




def gerar_cromossomo():
    return [random.randint(0, 1) for _ in range(num_itens)]

def calcular_fitness(cromossomo):
    peso_total = 0
    valor_total = 0
    for i, gene in enumerate(cromossomo):
        if gene == 1:
            peso_total += itens[i + 1]["peso"]
            valor_total += itens[i + 1]["valor"]
    if peso_total > peso_maximo:
        return 0  # Penalidade
    return valor_total

def selecao_torneio(populacao, tamanho_torneio):
    torneio = random.sample(populacao, tamanho_torneio)
    return max(torneio, key=calcular_fitness)

def crossover_um_ponto(pai1, pai2):
    ponto_corte = random.randint(1, num_itens - 1)
    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
    return filho1, filho2

def mutacao(cromossomo, taxa_mutacao):
    for i in range(len(cromossomo)):
        if random.random() < taxa_mutacao:
            cromossomo[i] = 1 - cromossomo[i]
    return cromossomo


# --- Funções de Visualização ---

def visualizar_mochila(cromossomo, geracao, fitness, melhor_fitness_global, ax):
    """Visualiza o estado da mochila em um determinado cromossomo e geração."""

    ax.clear()  
    ax.set_xlim(0, 18) 
    ax.set_ylim(0, 10) 
    ax.set_title(f"Geração: {geracao+1} - Fitness: {fitness:.2f} (Melhor: {melhor_fitness_global:.2f})")

 
    mochila = patches.Rectangle((0, 0), peso_maximo, 8, linewidth=2, edgecolor='black', facecolor='lightgray')
    ax.add_patch(mochila)


    x_atual = 0  
    for i, gene in enumerate(cromossomo):
        if gene == 1:
            item = itens[i + 1]
            retangulo = patches.Rectangle((x_atual, 1), item["peso"], item["valor"]/2,  # Ajuste a altura se precisar
                                        linewidth=1, edgecolor='black', facecolor=item["cor"], label=f"Item {i+1}")
            ax.add_patch(retangulo)
            ax.text(x_atual + item["peso"] / 2, 1 + item["valor"]/2 + 0.5, f"Item {i+1}\nR${item['valor']:.2f}",
                    ha='center', va='bottom', fontsize=8, color='black')
            x_atual += item["peso"]

            if x_atual > peso_maximo:
                ax.text(8,5, "Peso Excedido!", color='red',fontsize=12, ha='center')



    ax.set_xlabel("Peso (kg)")
    ax.set_ylabel("Valor (escala)")
   
    ax.set_xticks(range(0, peso_maximo + 1))  
    ax.grid(True, axis='x', linestyle='--')  


def visualizar_evolucao_fitness(melhores_fitness, ax):
    """Gráfico da evolução do melhor fitness ao longo das gerações."""
    ax.plot(melhores_fitness)
    ax.set_xlabel("Geração")
    ax.set_ylabel("Melhor Fitness")
    ax.set_title("Evolução do Melhor Fitness")
    ax.grid(True)


def algoritmo_genetico_visual(tamanho_populacao, taxa_crossover, taxa_mutacao, num_geracoes, tamanho_torneio):

    # Inicializa a população
    populacao = [gerar_cromossomo() for _ in range(tamanho_populacao)]

    # Armazena o melhor fitness de cada geração
    melhores_fitness = []
    melhor_fitness_global = 0 #Melhor fitness de todas as gerações.

 
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6)) 
    plt.ion() 

    for geracao in range(num_geracoes):
        fitness_populacao = [calcular_fitness(cromossomo) for cromossomo in populacao]

        # Elitismo
        if elitismo:
            elite = sorted(populacao, key=calcular_fitness, reverse=True)[:num_elitismo]

        nova_populacao = []
        if elitismo:
            nova_populacao.extend(elite)

        while len(nova_populacao) < tamanho_populacao:
            pai1 = selecao_torneio(populacao, tamanho_torneio)
            pai2 = selecao_torneio(populacao, tamanho_torneio)
            if random.random() < taxa_crossover:
                filho1, filho2 = crossover_um_ponto(pai1, pai2)
            else:
                filho1, filho2 = pai1[:], pai2[:]
            filho1 = mutacao(filho1, taxa_mutacao)
            filho2 = mutacao(filho2, taxa_mutacao)
            nova_populacao.extend([filho1, filho2])

        populacao = nova_populacao[:tamanho_populacao]

        # Melhor fitness da geração atual
        melhor_fitness = max(fitness_populacao)
        melhores_fitness.append(melhor_fitness)
        melhor_cromossomo = populacao[fitness_populacao.index(melhor_fitness)]

        # Atualiza o melhor fitness global
        if melhor_fitness > melhor_fitness_global:
            melhor_fitness_global = melhor_fitness


       
        visualizar_mochila(melhor_cromossomo, geracao, melhor_fitness, melhor_fitness_global, ax1)
        visualizar_evolucao_fitness(melhores_fitness, ax2)
        plt.pause(0.1) 


    # --- Melhor Solução (após o loop) ---
    fitness_final = [calcular_fitness(cromossomo) for cromossomo in populacao]
    melhor_cromossomo = populacao[fitness_final.index(max(fitness_final))]
    itens_selecionados = [i + 1 for i, gene in enumerate(melhor_cromossomo) if gene == 1]
    peso_total_final = sum(itens[item]["peso"] for item in itens_selecionados)
    valor_total_final = sum(itens[item]["valor"] for item in itens_selecionados)

    print(f"\nMelhor Solução:")
    print(f"Itens Selecionados: {itens_selecionados}")
    print(f"Peso Total: {peso_total_final} kg")
    print(f"Valor Total: R$ {valor_total_final:.2f}")

    plt.ioff()  
    plt.show() 

    return melhor_cromossomo, melhor_fitness


melhor_cromossomo, melhor_fitness = algoritmo_genetico_visual(tamanho_populacao, taxa_crossover, taxa_mutacao, num_geracoes, tamanho_torneio)