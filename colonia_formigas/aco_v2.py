import numpy as np
import random
from collections import Counter

# Classe que implementa o Algoritmo de Colônia de Formigas (ACO)
class ACO:
    def __init__(self, num_formigas, num_iteracoes, alfa, beta, evaporacao, Q):
        # Inicializa os parâmetros do ACO
        self.num_formigas = num_formigas  # Número de formigas na colônia
        self.num_iteracoes = num_iteracoes  # Número de iterações do algoritmo
        self.alfa = alfa  # Parâmetro que controla a influência do feromônio
        self.beta = beta  # Parâmetro que controla a influência da visibilidade
        self.evaporacao = evaporacao  # Taxa de evaporação do feromônio
        self.Q = Q  # Constante que determina a quantidade de feromônio depositado

    def inicializar_feromonio(self, num_pontos):
        # Inicializa a matriz de feromônio com valores iguais a 1
        return np.ones((num_pontos, num_pontos))

    def calcular_distancia(self, p1, p2):
        # Calcula a distância euclidiana entre dois pontos (p1 e p2)
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def calcular_probabilidade(self, i, j, feromonio, visibilidade, visitados):
        # Calcula a probabilidade de uma formiga se mover do ponto i para o ponto j
        numerador = (feromonio[i][j] ** self.alfa) * (visibilidade[i][j] ** self.beta)
        denominador = sum(
            (feromonio[i][k] ** self.alfa) * (visibilidade[i][k] ** self.beta)
            for k in range(len(feromonio)) if k not in visitados
        )
        return numerador / denominador

    def atualizar_feromonio(self, feromonio, formigas, distancias):
        # Atualiza os níveis de feromônio na matriz
        num_pontos = len(feromonio)
        for i in range(num_pontos):
            for j in range(num_pontos):
                # Aplica a evaporação do feromônio
                feromonio[i][j] *= (1 - self.evaporacao)
                # Adiciona o feromônio depositado pelas formigas na aresta (i, j)
                for k in range(self.num_formigas):
                    if j in formigas[k]:
                        feromonio[i][j] += self.Q / distancias[k]

    def encontrar_melhor_rota(self, pontos):
        # Encontra a melhor rota usando o Algoritmo de Colônia de Formigas (ACO)
        num_pontos = len(pontos)
        feromonio = self.inicializar_feromonio(num_pontos)
        visibilidade = np.zeros((num_pontos, num_pontos))
        
        # Calcula a visibilidade (1 / distância) entre todos os pares de pontos
        for i in range(num_pontos):
            for j in range(num_pontos):
                if i != j:
                    visibilidade[i][j] = 1 / self.calcular_distancia(pontos[i], pontos[j])

        melhor_rota = None
        menor_custo = float('inf')

        for _ in range(self.num_iteracoes):
            formigas = []  # Armazena as rotas encontradas por cada formiga
            distancias = []  # Armazena o custo de cada rota

            for _ in range(self.num_formigas):
                rota = [0]  # Começa a rota no ponto inicial (0)
                visitados = set(rota)  # Conjunto de pontos visitados

                while len(rota) < num_pontos:
                    i = rota[-1]  # Último ponto visitado
                    probabilidades = [self.calcular_probabilidade(i, j, feromonio, visibilidade, visitados) for j in range(num_pontos) if j not in visitados]
                    j = random.choices([j for j in range(num_pontos) if j not in visitados], probabilidades)[0]
                    rota.append(j)
                    visitados.add(j)
                rota.append(0)  # Volta ao ponto inicial para completar o ciclo
                formigas.append(rota)
                # Calcula o custo da rota (distância total)
                distancias.append(sum(self.calcular_distancia(pontos[rota[k]], pontos[rota[k+1]]) for k in range(len(rota) - 1)))

            # Atualiza o feromônio com base nas rotas e custos encontrados
            self.atualizar_feromonio(feromonio, formigas, distancias)

            # Verifica a melhor rota encontrada na iteração atual
            for i in range(self.num_formigas):
                if distancias[i] < menor_custo:
                    menor_custo = distancias[i]
                    melhor_rota = formigas[i]

        return melhor_rota[1:-1], menor_custo  # Retorna a melhor rota (sem o ponto inicial e final repetidos) e o custo

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

# Exemplo de uso
arquivo_tsp = 'pisi_2\wi29.tsp'
pontos = ler_tsp(arquivo_tsp)  # Lê os pontos a partir do arquivo TSP
pontos_lista = [pontos[i] for i in sorted(pontos.keys())]  # Organiza os pontos na ordem dos índices

# Loop para executar o ACO 30 vezes e contar as rotas
rotas = []
for i in range(30):
    aco = ACO(num_formigas=10, num_iteracoes=100, alfa=1.0, beta=2.0, evaporacao=0.5, Q=100)
    melhor_rota, menor_custo = aco.encontrar_melhor_rota(pontos_lista)
    rota_str = ' '.join(map(str, melhor_rota))
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
