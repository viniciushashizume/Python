import torch
import random
import matplotlib.pyplot as plt


n_samples = 10
n_hours = 24 #horas do dia
n_minutes = 60 #minutos
times = [f"{random.randint(12, 16):02}:{random.randint(0, n_minutes - 1):02}" for _ in range(n_samples)] #gera horario aleatorio
#:02 (garante que a formatação de horas tera obrigatoriamente 2 valores)
#gera um numero randomico entre 0 e 23

# Contagem das ocorrências de cada horário usando um dicionário comum
time_counts = {}

for time in times:
    if time in time_counts:
        time_counts[time] += 1
    else:
        time_counts[time] = 1

#conversao dos horarios gerados para tensores do pytorch
unique_times = list(time_counts.keys())
counts = torch.tensor(list(time_counts.values()))

#maior contagem de ocorrências
max_count = torch.max(counts)

#horarios com maior incidencia
mais_frequentes = [unique_times[i] for i in torch.where(counts == max_count)[0].tolist()]

#visualização grafica
plt.bar(unique_times, counts.tolist())
plt.xlabel('Horarios')
plt.ylabel('Ocorrências')
plt.show()
