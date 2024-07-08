import random

lista = ["turma","falso","claro","legal"]
termo = random.choice(lista)
chances = 5
game_over = False

while not game_over:
    print(f'Chances restantes {chances}')
    palavra = input("Digite uma palavra de até 5 letras: ").lower()
    
    
    if len(palavra) > 5:
        print("A palavra deve ter no máximo 5 letras.")
        continue
    
    chances -= 1
    
    if palavra == termo:
        print('Você acertou!')
        game_over = True
        break
    else:
        for i, (char1, char2) in enumerate(zip(palavra, termo)):
            if char1 == char2:
                print(f'Você acertou a posição da letra correspondente na posição {i+1}: {char1}')
            else:
                print(f'Os caracteres na posição {i} são diferentes: {char1} != []')
    
    if chances == 0:
        print("Você perdeu!")
        game_over = True
