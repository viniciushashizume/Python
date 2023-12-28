#Gerador de jogo    

import random

lista_aleatoria = []
lista_aposta = []
lista_acertos = []
acerto = 0

for i in range(6):
    num_aleatorio = random.randint(1,60)
    lista_aleatoria.append(num_aleatorio)

print(lista_aleatoria)
    
for i in range(6):
    num=int(input(f"Insira o numero {i+1} "))
    lista_aposta.append(num)

lista_aleatoria.sort()
lista_aposta.sort()

for num in lista_aposta:
    if num in lista_aleatoria:
        acerto+=1 
        lista_acertos.append(num)

lista_acertos.sort()

print(lista_aleatoria)
print(lista_aposta)
print(acerto)
print(lista_acertos)
    
