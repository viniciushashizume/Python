import torch
import random
import matplotlib.pyplot as plt

# Parâmetros para geração dos números
n_samples = 100
n_classes = 10

# Gera uma lista grande de números aleatórios
numbers = [random.randint(0, n_classes) for _ in range(n_samples)]

print(numbers)
# Converte a lista para um tensor PyTorch
numbers_tensor = torch.tensor(numbers)

# Conta as ocorrências de cada número
unique_numbers, counts = torch.unique(numbers_tensor, return_counts=True)

# Encontra a maior contagem de ocorrências
max_count = torch.max(counts)

# Encontra todos os números com a maior incidência
most_frequent_numbers = unique_numbers[counts == max_count]

# Exibe os resultados
print(f"Números com maior incidência (ocorrências = {max_count.item()}): {most_frequent_numbers.tolist()}")

# Visualização das ocorrências
plt.bar(unique_numbers.tolist(), counts.tolist(), color='blue')
plt.xlabel('Números')
plt.ylabel('Ocorrências')
plt.title('Distribuição das Ocorrências')
plt.show()
