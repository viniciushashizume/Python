import torch
import random
import matplotlib.pyplot as plt

n_samples = 100 #tamanho da amostra
n_classes = 10 #numeros de 0 a 10 gerados
numbers = [random.randint(0, n_classes) for _ in range(n_samples)] #gera numeros aleatorios

print(numbers)
numbers_tensor = torch.tensor(numbers) #converte os numeros em um tensor 1x1 do torch
unique_numbers, counts = torch.unique(numbers_tensor, return_counts=True) #eixo x= numeros eixo y=contador de quantas vezes aparece
max_count = torch.max(counts) #retorna qual o indice de numero mais apareceu 
most_frequent_numbers = unique_numbers[counts == max_count] #retorna o numero que mais apareceu

#exibicao grafica do projeto
plt.bar(unique_numbers.tolist(), counts.tolist(), color='blue')
plt.xlabel('Números')
plt.ylabel('Ocorrências')
plt.show()
