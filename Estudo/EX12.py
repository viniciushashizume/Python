#Pedra papel ou tesoura com funcoes
import random

def escolha_computador():
    
    opcoes_computador = ['Pedra', 'Papel', 'Tesoura']
    escolha_comp = random.choice(opcoes_computador)
    return escolha_comp

def verificador(jogador, computador):
    if jogador == 'Pedra' and computador == 'Tesoura' or jogador == 'Papel' and computador == 'Pedra' or jogador == 'Tesoura' and computador == 'Papel' :
        return 'O jogador ganhou'
    elif computador == 'Pedra' and jogador == 'Tesoura' or computador == 'Papel' and jogador == 'Pedra' or computador == 'Tesoura' and jogador == 'Papel' :
        return 'O computador ganhou'
    else: 
        return 'Empate'

def rps():
    escolha_jogador = input('')
    computador = escolha_computador()
    resultado = verificador(escolha_jogador, computador)
    print(resultado)

rps()



