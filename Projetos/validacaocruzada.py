import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, classification_report
import warnings

# Ignorar avisos de convergência para uma saída mais limpa
warnings.filterwarnings('ignore', category=UserWarning)

# --- 1. Carregar e Preparar os Dados ---
try:
    # Carrega o arquivo Excel original
    df = pd.read_excel("BaseDadosNotas.xlsx")
except FileNotFoundError:
    print("Erro: Arquivo 'BaseDadosNotas.xlsx' não encontrado.")
    exit()

# Separa as features (X) do rótulo (y)
X = df[['PROVA1', 'PROVA2', 'TRABALHO']].values
y = df['SITUAÇÃO'].values

# --- 2. Configurar o Modelo e a Validação ---

# Configuração do MLP que atingiu 100% (ex: uma camada com 10 neurônios)
# Você pode testar outras configurações alterando aqui
mlp_config = {
    'hidden_layer_sizes': (10,),
    'activation': 'relu',
    'solver': 'sgd',
    'learning_rate_init': 0.1,
    'momentum': 0.9,
    'max_iter': 100,  # Testando com 100 épocas
    'random_state': 42
}

# Inicializa o classificador MLP com a configuração definida
mlp = MLPClassifier(**mlp_config)

# Inicializa o normalizador de dados
scaler = MinMaxScaler()

# Configura a Validação Cruzada Estratificada
# Usaremos 5 "folds" (divisões). O modelo será treinado e testado 5 vezes.
n_splits = 5
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

# Lista para armazenar a acurácia de cada "fold"
fold_accuracies = []

print("="*70)
print(f"Iniciando Validação Cruzada com {n_splits} folds.")
print(f"Configuração do MLP: {mlp_config}")
print("="*70)

# --- 3. Executar a Validação Cruzada ---

# O loop irá iterar 5 vezes, a cada vez com um conjunto de treino/teste diferente
for i, (train_index, test_index) in enumerate(skf.split(X, y)):
    print(f"--- Fold {i+1}/{n_splits} ---")
    
    # Separa os dados de treino e teste para este fold
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    
    # IMPORTANTE: Ajusta (fit) o normalizador APENAS nos dados de TREINO
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Aplica (transform) a mesma normalização aos dados de TESTE
    X_test_scaled = scaler.transform(X_test)
    
    # Treina o modelo com os dados de treino do fold atual
    mlp.fit(X_train_scaled, y_train)
    
    # Faz as predições no conjunto de teste do fold atual
    predicoes = mlp.predict(X_test_scaled)
    
    # Calcula e armazena a acurácia do fold
    acuracia = accuracy_score(y_test, predicoes)
    fold_accuracies.append(acuracia)
    
    print(f"Acurácia do Fold: {acuracia:.4f}")
    # print(classification_report(y_test, predicoes, zero_division=0))

# --- 4. Apresentar Resultados Finais ---

print("\n" + "="*70)
print("Resultados Finais da Validação Cruzada")
print("="*70)
print(f"Acurácias de cada um dos {n_splits} folds: {np.round(fold_accuracies, 4)}")
print(f"\nAcurácia Média: {np.mean(fold_accuracies):.4f}")
print(f"Desvio Padrão da Acurácia: {np.std(fold_accuracies):.4f}")