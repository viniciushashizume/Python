import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import MinMaxScaler

# Carregar a planilha
df = pd.read_excel("BaseDadosNotas.xlsx")

# Remover coluna de ID
df_features = df.drop(columns=["ID"])

# Separar atributos e rótulo
X = df_features.drop(columns=["SITUAÇÃO"])
y = df_features["SITUAÇÃO"]

# Normalizar com Min-Max
scaler = MinMaxScaler()
X_normalized = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

# Arredondar para 3 casas decimais
X_normalized = X_normalized.round(3)

# Juntar com a coluna alvo
df_normalized = X_normalized.copy()
df_normalized["SITUAÇÃO"] = y.values

# Divisão estratificada: 2/3 treino, 1/3 teste
splitter = StratifiedShuffleSplit(n_splits=1, test_size=1/3, random_state=42)
for train_idx, test_idx in splitter.split(X_normalized, y):
    treino = df_normalized.iloc[train_idx]
    teste = df_normalized.iloc[test_idx]

# Salvar os arquivos com tabulação, sem índice, com acentuação compatível
treino.to_csv("treinamento.txt", sep="\t", index=False, encoding='utf-8')
teste.to_csv("teste.txt", sep="\t", index=False, encoding='utf-8')