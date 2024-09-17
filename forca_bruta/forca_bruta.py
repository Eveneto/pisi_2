def permutar(lista): 
    if len(lista) <= 1: 
        return [lista]
    
    aux_list = []

    for indice, elemento in enumerate(lista): 
        restantes = lista[:indice] + lista[indice+1:] 
        for p in permutar(restantes):
            aux_list.append([elemento] + p)
    return aux_list

def calcular_distancia(lista): 
    distancias = [] 
    for indice in range(len(lista) - 1):
        dij = 0
        di = abs(coordenadas[lista[indice]][0] - coordenadas[lista[indice+1]][0])
        dj = abs(coordenadas[lista[indice]][1] - coordenadas[lista[indice+1]][1])
        dij += di + dj
        distancias.append(dij)
    return sum(distancias)

pontos_de_entrega = []
entrada = open("matriz.txt", 'r')

i, j = [int(x) for x in entrada.readline().split()]

coordenadas = {}

for l in range(i):
    linha = entrada.readline().split() 
    for c in range(j):
        if linha[c] != 'R' and linha[c] != '0': 
            pontos_de_entrega.append(linha[c])
        if linha[c] != '0':
            coordenadas[linha[c]] = (l, c)

entrada.close() 

rotas_permutadas = permutar(pontos_de_entrega)

resultados = {}
for rota in rotas_permutadas:
    rota = ['R'] + rota + ['R']
    distancia = calcular_distancia(rota)
    resultados[''.join(rota)] = distancia

melhor_rota = min(resultados, key=resultados.get)
custo = resultados[melhor_rota]



print(f"MELHOR ROTA: {melhor_rota[1:-1]}\nCUSTO:{custo} dronômetros.")
