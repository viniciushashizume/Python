#Entrada para listas

lista = []

elementos = int(input('Quantos elementos deseja inserir '))

for i in range(elementos):
    num = int(input('Qual valor deseja imprimir '))
    lista.append(num)

#for i in lista: 
print('lista:', lista)