#Jogo da forca

palavra = str(input("Teste: "))

condicao = True

while condicao:
    letra = input('Insira uma letra')
    i=0
    for letras in palavra:
        if letra == letras:
            acertou[i]=letra
        i+=1
