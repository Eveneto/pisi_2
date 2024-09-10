from random import random, randint, shuffle, sample
import tsplib95 as tsplib

def carregar_cidades(file_path):
    tsp = tsplib.load(file_path)
    return {i: coord for i, coord in enumerate(tsp.node_coords.values())}

def gerar_populacao_inicial(cidades, n_pop=20):
    return [shuffle(list(cidades.keys())) or list(cidades.keys()) for _ in range(n_pop)]

def calcular_distancia_total(caminho, cidades):
    return sum(((cidades[caminho[i]][0] - cidades[caminho[i+1]][0])**2 + 
                (cidades[caminho[i]][1] - cidades[caminho[i+1]][1])**2)**0.5
               for i in range(len(caminho) - 1))

def avaliar_populacao(populacao, cidades):
    return [calcular_distancia_total(ind, cidades) for ind in populacao]

def selecao_por_torneio(populacao, aptidoes, k):
    selecionados = []
    for _ in range(2):
        competidores = sample(range(len(populacao)), k)
        aptidoes_torneio = [aptidoes[i] for i in competidores]
        melhor = competidores[aptidoes_torneio.index(min(aptidoes_torneio))]
        selecionados.append(populacao[melhor])
    return selecionados

def cruzamento_pmx(p1, p2):
    filho = [None] * len(p1)
    ponto1, ponto2 = sorted([randint(0, len(p1) - 1) for _ in range(2)])
    filho[ponto1:ponto2+1] = p1[ponto1:ponto2+1]
    
    mapa = {p1[i]: p2[i] for i in range(ponto1, ponto2+1) if p2[i] not in filho}
    
    for i in range(len(filho)):
        if filho[i] is None:
            gene = p2[i]
            while gene in mapa:
                gene = mapa[gene]
            filho[i] = gene
    return filho

def cruzamento_e_mutacao(populacao, aptidoes, cidades, taxa_cruzamento, taxa_mutacao, tamanho_torneio):
    nova_populacao = []
    for _ in range(len(populacao) // 2):
        pais = selecao_por_torneio(populacao, aptidoes, tamanho_torneio)
        if random() < taxa_cruzamento:
            filhos = [cruzamento_pmx(pais[0], pais[1]), cruzamento_pmx(pais[1], pais[0])]
        else:
            filhos = pais
        
        filhos = [mutar_individuo(filho, taxa_mutacao, cidades) for filho in filhos]
        nova_populacao.extend(filhos)
    return nova_populacao

def mutar_individuo(individuo, taxa_mutacao, cidades):
    if random() < taxa_mutacao:
        c1, c2 = sample(range(len(cidades)), 2)
        individuo[c1], individuo[c2] = individuo[c2], individuo[c1]
    return individuo

def evoluir(cidades, taxa_cruzamento, taxa_mutacao, tamanho_torneio, n_geracoes):
    populacao = gerar_populacao_inicial(cidades)
    aptidoes = avaliar_populacao(populacao, cidades)

    for _ in range(n_geracoes):
        nova_populacao = cruzamento_e_mutacao(populacao, aptidoes, cidades, taxa_cruzamento, taxa_mutacao, tamanho_torneio)
        aptidoes_novas = avaliar_populacao(nova_populacao, cidades)
        populacao, aptidoes = selecao_elitista(populacao, nova_populacao, aptidoes, aptidoes_novas)

    melhor_rota = populacao[aptidoes.index(min(aptidoes))]
    melhor_custo = min(aptidoes)
    
    return melhor_rota, melhor_custo

def selecao_elitista(populacao_atual, nova_populacao, aptidoes_atual, aptidoes_novas):
    populacao_combinada = populacao_atual + nova_populacao
    aptidoes_combinadas = aptidoes_atual + aptidoes_novas
    sobreviventes = sorted(zip(populacao_combinada, aptidoes_combinadas), key=lambda x: x[1])[:len(populacao_atual)]
    return [ind for ind, _ in sobreviventes], [apt for _, apt in sobreviventes]

def main():
    cidades = carregar_cidades("pisi_2\wi29.tsp")
    taxa_cruzamento = 0.8
    taxa_mutacao = 0.01
    tamanho_torneio = 4
    n_geracoes = 10000
    
    melhor_rota, menor_custo = evoluir(cidades, taxa_cruzamento, taxa_mutacao, tamanho_torneio, n_geracoes)
    print(f"A melhor rota encontrada foi: {melhor_rota} com custo {menor_custo} dronômetros.")
for i in range(30):
    main()
