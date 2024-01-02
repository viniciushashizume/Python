#Pedra papel ou tesoura

import random

def escolha_jogador():
    escolha = input('Qual opção? \nPedra \nPapel \nTesoura \n')
    return escolha.capitalize()

def escolha_computador():
    escolhas = ['Pedra', 'Papel', 'Tesoura']
    return random.choice(escolhas)


escolha1 = escolha_jogador()
escolha2= escolha_computador()

print('Escolha do jogador: {escolha1}', escolha1)
print('Escolha do computador {escolha2}', escolha2)

if escolha1 == 'Pedra' and escolha2 == 'Tesoura':
    print('\nO jogador ganhou')

if escolha1 == 'Papel' and escolha2 == 'Pedra':
    print('\nO jogador ganhou')

if escolha1 == 'Tesoura' and escolha2 == 'Papel':
    print('\nO jogador ganhou')

if escolha2 == 'Pedra' and escolha1 == 'Tesoura':
    print('\nO computador ganhou')

if escolha2 == 'Papel' and escolha1 == 'Pedra':
    print('\nO computador ganhou')

if escolha2 == 'Tesoura' and escolha1 == 'Papel':
    print('\nO computador ganhou')

