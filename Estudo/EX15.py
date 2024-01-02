#Buscar em lista

lista = []

for i in range(3):
    num = input('Digite o numero ')
    lista.append(num)

busca = input('Qual valor deseja buscar')

if busca in lista:
    posicao = lista.index(busca)

print (lista)
print (posicao+1)