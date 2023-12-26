#Contador de palavras
import string

frase = str(input('Insira uma frase\n'))
palavras = frase.split()
cont = len(palavras)

print(cont)