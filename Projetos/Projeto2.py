#Advinhar o numero
import random

num_gerado = random.randint(0,100)


acerto = False

while not acerto:
    num_escolhido = int(input('Escolha um numero de 0 a 100: '))
    if 0 <= num_escolhido <= 100:
        if num_escolhido == num_gerado:
            print('Você acertou!')
            acerto = True
        elif num_escolhido > num_gerado:
            print('O numero escolhido é maior do que o numero a ser advinhado')
        elif num_escolhido < num_gerado:
            print('O numero escolhido é menor do que o numero a ser advinhado')
    else: 
        print('Escolha um número entre 0 e 100')


print(num_escolhido)