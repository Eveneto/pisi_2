import numpy as np
from collections import Counter

# Classe que implementa o Algoritmo Genético (GA)
class AG:
    def __init__(self, num_individuos, num_geracoes, taxa_mutacao, taxa_cruzamento):
        # Inicializa os parâmetros do AG
        self.num_individuos = num_individuos  # Número de indivíduos na população
        self.num_geracoes = num_geracoes  # Número de gerações
        self.taxa_mutacao = taxa_mutacao  # Taxa de mutação
        self.taxa_cruzamento = taxa_cruzamento  # Taxa de cruzamento

    def calcular_distancia(self, p1, p2):
        # Calcula a distância Manhattan entre dois pontos (p1 e p2)
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def inicializar_populacao(self, num_pontos):
        # Inicializa a população com rotas sequenciais e faz mutações para gerar diversidade
        populacao = []
        for i in range(self.num_individuos):
            individuo = list(range(1, num_pontos))  # Ignora o ponto inicial/final (0)
            individuo = self.mutacao_deterministica(individuo)
            populacao.append(individuo)
        return populacao

    def mutacao_deterministica(self, individuo):
        # Aplica mutação permutando dois elementos de maneira determinística
        for i in range(len(individuo)):
            if i < len(individuo) - 1:
                # Simples troca de posições vizinhas (sem usar random)
                individuo[i], individuo[i + 1] = individuo[i + 1], individuo[i]
        return individuo

    def cruzamento_deterministico(self, pai1, pai2):
        # Implementa cruzamento sem usar random, de forma determinística
        ponto_corte = len(pai1) // 2  # Divide a rota ao meio
        filho = pai1[:ponto_corte] + [gene for gene in pai2 if gene not in pai1[:ponto_corte]]
        return filho

    def calcular_fitness(self, individuo, pontos):
        # Calcula o custo total (distância) da rota do indivíduo
        rota = [0] + individuo + [0]  # Adiciona o ponto inicial e final (0)
        return sum(self.calcular_distancia(pontos[rota[i]], pontos[rota[i+1]]) for i in range(len(rota) - 1))

    def selecionar_pais(self, populacao, fitness):
        # Seleção de pais de forma determinística: escolher os dois melhores
        indices_melhores = np.argsort(fitness)[:2]  # Seleciona os dois melhores indivíduos
        return populacao[indices_melhores[0]], populacao[indices_melhores[1]]

    def encontrar_melhor_rota(self, pontos):
        num_pontos = len(pontos)
        populacao = self.inicializar_populacao(num_pontos)
        melhor_rota = None
        menor_custo = float('inf')

        for geracao in range(self.num_geracoes):
            fitness = [self.calcular_fitness(individuo, pontos) for individuo in populacao]

            # Atualiza a melhor rota e custo
            for i in range(len(populacao)):
                if fitness[i] < menor_custo:
                    menor_custo = fitness[i]
                    melhor_rota = populacao[i]

            # Seleção de pais
            pai1, pai2 = self.selecionar_pais(populacao, fitness)

            # Gerar nova população através de cruzamento e mutação
            nova_populacao = []
            while len(nova_populacao) < self.num_individuos:
                filho = self.cruzamento_deterministico(pai1, pai2)
                if np.random.rand() < self.taxa_mutacao:
                    filho = self.mutacao_deterministica(filho)
                nova_populacao.append(filho)

            populacao = nova_populacao

        return melhor_rota, menor_custo

def ler_tsp(arquivo):
    # Lê o arquivo TSP e extrai os pontos
    with open(arquivo, 'r') as f:
        linhas = f.readlines()

    pontos = {}
    for linha in linhas:
        if linha.strip() == 'EOF':
            break
        if linha.strip() and not linha.startswith(('NAME', 'TYPE', 'COMMENT', 'DIMENSION', 'EDGE_WEIGHT_TYPE', 'NODE_COORD_SECTION')):
            partes = linha.split()
            indice = int(partes[0])
            x = float(partes[1])
            y = float(partes[2])
            pontos[indice - 1] = (x, y)  # Subtrai 1 para ajustar ao índice zero

    return pontos

def indices_para_letras(indices):
    letras = ['R', 'A', 'B', 'C', 'D']
    return [letras[i] for i in indices]

# Exemplo de uso
arquivo_tsp = 'alg_genetico/matriz.tsp'
pontos = ler_tsp(arquivo_tsp)  # Lê os pontos a partir do arquivo TSP
pontos_lista = [pontos[i] for i in sorted(pontos.keys())]  # Organiza os pontos na ordem dos índices

# Loop para executar o AG e contar as rotas
rotas = []
for i in range(1000):
    ag = AG(num_individuos=10, num_geracoes=100, taxa_mutacao=0.1, taxa_cruzamento=0.8)
    melhor_rota, menor_custo = ag.encontrar_melhor_rota(pontos_lista)
    # Converte a rota encontrada em uma string para facilitar a visualização
    rota_str = ' '.join(indices_para_letras(melhor_rota))
    rotas.append(rota_str)
    print(f'Execução {i+1}:')
    print('Melhor rota:', rota_str)
    print('Menor custo:', menor_custo)
    print('---')

# Contar a frequência de cada rota
contador_rotas = Counter(rotas)
rota_mais_frequente = contador_rotas.most_common(1)[0]

print('Rotas encontradas e suas frequências:')
for rota, frequencia in contador_rotas.items():
    print(f'Rota: {rota}, Frequência: {frequencia}')

print('---')
print(f'Rota mais frequente: {rota_mais_frequente[0]}, Frequência: {rota_mais_frequente[1]}')
