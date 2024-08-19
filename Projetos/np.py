import numpy as np

array = np.array([], dtype=int)
i=0
while True:
    try:
        num = (int(input('insira um número no vetor: ')))
        i = int(input('Em que posicao deseja inserir: '))
        array = np.insert(array, i, num)
        i+=1
    except:
        pass
    if (len(array)>=3):
         break
        
print(array)