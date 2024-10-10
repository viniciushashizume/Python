import pandas as pd
import torch
import matplotlib.pyplot as plt
import seaborn as sns

# Passo 1: Ler o CSV
df = pd.read_csv('sensor_data.csv', parse_dates=['timestamp'])
print(df.head())

# Passo 2: Extrair a hora do timestamp
df['hour'] = df['timestamp'].dt.hour  # Extrair apenas a hora como número inteiro

# Passo 3: Agrupar por hora e contar as leituras
hourly_counts = df.groupby('hour')['distance'].count().reset_index()
hourly_counts.columns = ['hour', 'count']

# Passo 4: Converter para tensores
features = torch.tensor(hourly_counts['count'].values, dtype=torch.float32)

# Passo 5: Visualizar os dados
plt.figure(figsize=(10, 6))
sns.barplot(x='hour', y='count', data=hourly_counts, palette='viridis')
plt.title('Análise de Leituras por Hora')
plt.xlabel('Hora do Dia')
plt.ylabel('Número de Leituras')
plt.xticks(hourly_counts['hour'])  # Definir rótulos do eixo x como horas inteiras
plt.grid()

# Passo 6: Salvar a imagem
plt.savefig('horas.png')
plt.show()
