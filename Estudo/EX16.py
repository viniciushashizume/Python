# matrizes

def cria_matriz(num_linhas, num_colunas, valor):
    matriz = []
    for i in range(num_linhas):
        linha = []
        for j in range(num_colunas):
            linha.append(valor)
        matriz.append(linha)
    return matriz

def imprime_matriz(matriz):
    for linha in matriz:
        for elemento in linha:
            print(elemento, end=' ')
        print()

def insereelemento(matriz):
    print('Insira a posição que ira inserir o elemento:')
    l = int(input('Linha: \n'))
    c = int(input('Coluna \n'))
    elemento = input('Insira o elemento')
    matriz[l][c]=elemento

linhas = int(input('Insira o número de linhas: '))
colunas = int(input('Insira o número de colunas: '))

m = cria_matriz(linhas, colunas, 0)
imprime_matriz(m)
insereelemento(m)
imprime_matriz(m)
