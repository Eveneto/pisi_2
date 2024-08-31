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
        # Calcula a distância Manhattan entre dois pontos (p1 e p2)
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def calcular_probabilidade(self, i, j, feromonio, visibilidade, visitados):
        # Calcula a probabilidade de uma formiga se mover do ponto i para o ponto j
        numerador = (feromonio[i][j] ** self.alfa) * (visibilidade[i][j] ** self.beta)
        # Calcula o denominador somando as probabilidades de todos os pontos não visitados
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
                    # Calcula as probabilidades de ir para os pontos não visitados
                    probabilidades = [self.calcular_probabilidade(i, j, feromonio, visibilidade, visitados) for j in range(num_pontos) if j not in visitados]
                    # Escolhe o próximo ponto com base nas probabilidades
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

def ler_matriz(arquivo):
    # Lê a matriz a partir de um arquivo
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
    matriz = [linha.strip().split() for linha in linhas]
    return matriz

def encontrar_pontos(matriz):
    # Encontra os pontos de entrega e o ponto de origem na matriz
    pontos = {}
    for i, linha in enumerate(matriz):
        for j, valor in enumerate(linha):
            if valor != '0':  # Considera apenas valores diferentes de '0'
                pontos[valor] = (i, j)  # Adiciona o ponto com suas coordenadas
    return pontos

# Exemplo de uso
arquivo = 'colonia_formigas/matriz.txt'
matriz = ler_matriz(arquivo)  # Lê a matriz do arquivo
pontos = encontrar_pontos(matriz)  # Encontra os pontos de interesse
pontos_lista = [pontos['R']] + [pontos[p] for p in 'ABCD']  # Lista de pontos na ordem inicial

# Loop para executar o ACO 30 vezes e contar as rotas
rotas = []
for i in range(30):
    aco = ACO(num_formigas=10, num_iteracoes=100, alfa=1.0, beta=2.0, evaporacao=0.5, Q=100)
    melhor_rota, menor_custo = aco.encontrar_melhor_rota(pontos_lista)
    # Converte a rota encontrada em uma string para facilitar a visualização
    rota_str = ' '.join('ABCD'[i-1] for i in melhor_rota)
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
