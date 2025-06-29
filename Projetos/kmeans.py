import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

# Funções para as novas métricas de avaliação (mantidas iguais)
def tanimoto_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    mag_sq1 = np.dot(vec1, vec1)
    mag_sq2 = np.dot(vec2, vec2)
    return dot_product / (mag_sq1 + mag_sq2 - dot_product)

def average_tanimoto_similarity(X, labels, centers):
    total_similarity = 0
    for i in range(X.shape[0]):
        center_of_point = centers[labels[i]]
        total_similarity += tanimoto_similarity(X.iloc[i].values, center_of_point)
    return total_similarity / X.shape[0]

def average_inner_product(X, labels, centers):
    total_inner_product = 0
    for i in range(X.shape[0]):
        center_of_point = centers[labels[i]]
        total_inner_product += np.dot(X.iloc[i].values, center_of_point)
    return total_inner_product / X.shape[0]

# 1. Criar o DataFrame (mantido igual)
data = {
    'Dia': [f'D{i}' for i in range(1, 15)],
    'Tempo': ['Sol', 'Sol', 'Nublado', 'Chuva', 'Chuva', 'Chuva', 'Nublado', 'Sol', 'Sol', 'Chuva', 'Sol', 'Nublado', 'Nublado', 'Chuva'],
    'Temperatura': ['Quente', 'Quente', 'Quente', 'Mediana', 'Frio', 'Frio', 'Frio', 'Mediana', 'Frio', 'Mediana', 'Mediana', 'Mediana', 'Quente', 'Mediana'],
    'Umidade': ['Alta', 'Alta', 'Alta', 'Alta', 'Normal', 'Normal', 'Normal', 'Alta', 'Normal', 'Normal', 'Normal', 'Alta', 'Normal', 'Alta'],
    'Vento': ['Fraco', 'Forte', 'Fraco', 'Fraco', 'Fraco', 'Forte', 'Forte', 'Fraco', 'Fraco', 'Fraco', 'Forte', 'Forte', 'Fraco', 'Forte']
}
df = pd.DataFrame(data)

# 2. Pré-processamento (mantido igual)
df_encoded = df.copy()
for column in ['Tempo', 'Temperatura', 'Umidade', 'Vento']:
    le = LabelEncoder()
    df_encoded[column] = le.fit_transform(df[column])
X = df_encoded[['Tempo', 'Temperatura', 'Umidade', 'Vento']]

# 3. Clusterização (mantido igual)
kmeans_2 = KMeans(n_clusters=2, random_state=42, n_init=20)
df['cluster_k2'] = kmeans_2.fit_predict(X)
centers_k2 = kmeans_2.cluster_centers_
tanimoto_k2 = average_tanimoto_similarity(X, kmeans_2.labels_, centers_k2)
inner_prod_k2 = average_inner_product(X, kmeans_2.labels_, centers_k2)

kmeans_3 = KMeans(n_clusters=3, random_state=42, n_init=20)
df['cluster_k3'] = kmeans_3.fit_predict(X)
centers_k3 = kmeans_3.cluster_centers_
tanimoto_k3 = average_tanimoto_similarity(X, kmeans_3.labels_, centers_k3)
inner_prod_k3 = average_inner_product(X, kmeans_3.labels_, centers_k3)

# 4. PCA para visualização (mantido igual)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# --- NOVO: Projetar os centróides no espaço PCA ---
centroids_pca_k2 = pca.transform(centers_k2)  # Centróides para k=2
centroids_pca_k3 = pca.transform(centers_k3)  # Centróides para k=3

# 5. Gerar os gráficos (com centróides adicionados)
plt.style.use('seaborn-v0_8-whitegrid')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
fig.suptitle('Simulação K-means', fontsize=18, fontweight='bold')

# --- Gráfico para k=2 ---
colors_k2 = cm.get_cmap('viridis', kmeans_2.n_clusters)
ax1.scatter(X_pca[:, 0], X_pca[:, 1], c=df['cluster_k2'], cmap=colors_k2, s=100, alpha=0.8, edgecolor='k')
# Plotar centróides (k=2)
ax1.scatter(centroids_pca_k2[:, 0], centroids_pca_k2[:, 1], marker='X', s=200, c='red', label='Centróides', edgecolor='k', linewidth=1.5)
ax1.set_title(f'k = 2\nProduto Interno Médio: {inner_prod_k2:.2f}\nTanimoto Médio: {tanimoto_k2:.2f}', fontsize=14)
ax1.set_xlabel('Componente Principal 1', fontsize=12)
ax1.set_ylabel('Componente Principal 2', fontsize=12)
ax1.legend()
for i, txt in enumerate(df['Dia']):
    ax1.text(X_pca[i, 0]+0.05, X_pca[i, 1]+0.05, txt, fontsize=9, ha='center')

# --- Gráfico para k=3 ---
colors_k3 = cm.get_cmap('plasma', kmeans_3.n_clusters)
ax2.scatter(X_pca[:, 0], X_pca[:, 1], c=df['cluster_k3'], cmap=colors_k3, s=100, alpha=0.8, edgecolor='k')
# Plotar centróides (k=3)
ax2.scatter(centroids_pca_k3[:, 0], centroids_pca_k3[:, 1], marker='X', s=200, c='red', label='Centróides', edgecolor='k', linewidth=1.5)
ax2.set_title(f'k = 3\nProduto Interno Médio: {inner_prod_k3:.2f}\nTanimoto Médio: {tanimoto_k3:.2f}', fontsize=14)
ax2.set_xlabel('Componente Principal 1', fontsize=12)
ax2.legend()
for i, txt in enumerate(df['Dia']):
    ax2.text(X_pca[i, 0]+0.05, X_pca[i, 1]+0.05, txt, fontsize=9, ha='center')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("kmeans_tenis_com_centroides.png")
plt.show()