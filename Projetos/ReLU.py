import numpy as np

def ReLU(input):
    return np.maximum(0, input)

array = np.array([], dtype=int)
i=0
while True:
    try:
        num = int(input('Insira um numero no vetor: '))
        num = ReLU(num)
        array = np.insert(array, i, num)
        i+=1
        print(f'Array atual: {array}')
    except ValueError:
        print("Por favor, insira um número válido.")
    if len(array) >= 5:
        break
print(f'Array final: {array}')