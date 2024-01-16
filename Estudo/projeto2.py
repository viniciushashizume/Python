#jogo da velha

def cria_matriz(num_linhas, num_colunas, valor):
    matriz=[]
    for i in range(num_linhas):
        linha = []
        for i in range(num_colunas):
            linha.append(valor)
        matriz.append(linha)
    return matriz

def imprime_matriz(matriz):
    for linha in matriz:
        for elemento in linha:
            print(elemento, end='')
        print()

def insereelemento(matriz):
    i = int(input('Insira a linha que deseja jogoar'))
    j = int(input('Insira a coluna que deseja jogar'))
    if i < 0 or i > 2 or j < 0 or j > 2:
        print('Posição inválida! As coordenadas devem estar entre 0 e 2.')
        return False
    if(matriz[i][j]==0):
        valor = int(input('Insira o valor que ira jogar 1- para O ou 2- para X'))
        if (valor == 1 or valor ==2):
            matriz[i][j]= valor
            return True
        else:
            print('Use apenas 1 ou 2')
            return False
    else:
        print('Posicao ja utilizada!')
        return False
    

m=cria_matriz(3, 3, 0)
vitoria = False

while True:
    imprime_matriz(m)
    
    if((m[0][0]==1 and m[0][1]==1 and m[0][2]==1) or (m[1][0] ==1 and m[1][1]==1 and m[1][2] ==1) or (m[2][0]==1 and m[2][1]==1 and m[2][2]==1) or (m[0][0]==1 and m[1][0]==1 or m[2][0]==1) or (m[0][1]==1 and m[1][1]==1 and m[1][2]==1) or (m[2][0]==1 and m[2][1]==1 and m[2][2]==1)):
        print('jogador 1 venceu')
        break
    if((m[0][0]==2 and m[0][1]==2 and m[0][2]==2) or (m[1][0] ==2 and m[1][1]==2 and m[1][2] ==2) or (m[2][0]==2 and m[2][1]==2 and m[2][2]==2) or (m[0][0]==2 and m[1][0]==2 or m[2][0]==2) or (m[0][1]==2 and m[1][1]==2 and m[1][2]==2) or (m[2][0]==2 and m[2][1]==2 and m[2][2]==2)):
        print('jogador 2 venceu')
        break
    insereelemento(m)


