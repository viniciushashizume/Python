#Verificador de palindromo


#i=0
#palavra = input('Digite a palavra ')
#palavra_reversa = ''.join(reversed(palavra))
#tam = len(palavra)
#if tam == len(palavra_reversa):
#   for letra in palavra:
 #       for letra2 in palavra_reversa:
  #          if letra == letra2: 
   #             palavra2 = letra[i]
    #    i+=1
#if palavra2 == palavra:
 #   print('As palavras sao palindromos')##

palavra = input('Digite a palavra ')
palavra_reversa = ''.join(reversed(palavra))

if palavra == palavra_reversa:
    print("As palavras sao palindromos ")
else:
    print('As palavras nao sao palindromos ')