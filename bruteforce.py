# Vitor Hugo Sousa Campos
# 20221011090051


itens = {
    1: {"peso": 4, "valor": 10},
    2: {"peso": 2, "valor": 6},
    3: {"peso": 6, "valor": 11},
    4: {"peso": 3, "valor": 6},
    5: {"peso": 5, "valor": 9},
    6: {"peso": 7, "valor": 12},
}
peso_maximo = 17
num_itens = len(itens)



def calcular_valor_e_peso(combinacao, itens):  # Passa 'itens' como argumento
    """Calcula o valor total e o peso total de uma combinação de itens."""
    peso_total = 0
    valor_total = 0
    for i in range(len(combinacao)):
        if combinacao[i] == 1:  # Se o item está na combinação
            peso_total += itens[i + 1]["peso"]  # Usa i+1 para acessar o item correto
            valor_total += itens[i + 1]["valor"]
    return valor_total, peso_total

# --- Força Bruta ---

def forca_bruta(itens, peso_maximo):
    """Resolve o problema da mochila por força bruta, sem usar bibliotecas como itertools."""

    melhor_valor = 0
    melhor_combinacao = []
    n = len(itens)

    # Gerar todas as combinações possíveis usando representação binária
    for i in range(2**n):  # Itera por todos os números de 0 a 2^n - 1
        combinacao = []
        temp = bin(i)[2:].zfill(n)  # Converte para binário e preenche com zeros à esquerda
        
        for bit in temp:
             combinacao.append(int(bit))

        valor, peso = calcular_valor_e_peso(combinacao, itens) # Passa 'itens'

        # Verifica se a combinação é válida e se é a melhor encontrada
        if peso <= peso_maximo and valor > melhor_valor:
            melhor_valor = valor
            melhor_combinacao = combinacao

    # Decodifica a melhor combinação (obtém os índices dos itens)
    itens_selecionados = [i + 1 for i, gene in enumerate(melhor_combinacao) if gene == 1]
    return itens_selecionados, melhor_valor


# --- Execução e Resultados ---

melhor_combinacao, melhor_valor = forca_bruta(itens, peso_maximo)

print(f"Melhor Combinação (Força Bruta): {melhor_combinacao}")
peso_total = sum(itens[item]["peso"] for item in melhor_combinacao) #Soma o peso baseado na lista de itens
print(f"Peso Total: {peso_total} kg")
print(f"Valor Total: R$ {melhor_valor:.2f}")