#Advinhar o numero
import random

aleatorio = random.randint(1,50)
print(aleatorio)

num = int(input('Digite o numero'))

while num != aleatorio:
    num = int(input('Digite o numero'))
    if num == aleatorio:
        print('Encontrou o numero')