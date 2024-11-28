import pandas as pd
import torch
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('sensor_data.csv', parse_dates=['tempo'])
print(df.head())

df['hour'] = df['tempo'].dt.hour

hourly_counts = df.groupby('hour')['distance'].count().reset_index()
hourly_counts.columns = ['hour', 'count']

features = torch.tensor(hourly_counts['count'].values, dtype=torch.float32)

plt.figure(figsize=(10, 6))
sns.barplot(x='hour', y='count', data=hourly_counts, palette='viridis')
plt.title('Análise de Leituras por Hora')
plt.xlabel('Hora do Dia')
plt.ylabel('Número de Leituras')
plt.xticks(hourly_counts['hour']) 
plt.grid()

plt.savefig('horas.png')
plt.show()
