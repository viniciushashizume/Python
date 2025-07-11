import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
import warnings

# Ignorar avisos sobre a não convergência para manter a saída limpa
warnings.filterwarnings('ignore', category=UserWarning)

def carregar_dados(caminho_arquivo):
    """
    Carrega os dados de um arquivo de texto, separando features (X) e rótulo (y).
    Assume que o delimitador é tabulação ('\t').
    """
    # CORREÇÃO: Alterado o separador para '\t' para corresponder ao arquivo salvo
    df = pd.read_csv(caminho_arquivo, sep='\t')
    
    # As três primeiras colunas são as features (entradas da rede)
    X = df[['PROVA1', 'PROVA2', 'TRABALHO']]
    
    # A última coluna é o rótulo/classe (saída da rede)
    y = df['SITUAÇÃO']
    
    return X, y

# --- 1. Carregar os dados de treinamento e teste ---
# Os arquivos já foram fornecidos pré-divididos conforme a especificação
try:
    X_train, y_train = carregar_dados('treinamento.txt')
    X_test, y_test = carregar_dados('teste.txt')
    print("Arquivos 'treinamento.txt' e 'teste.txt' carregados com sucesso.\n")
except FileNotFoundError as e:
    print(f"Erro: Arquivo não encontrado. Certifique-se de que '{e.filename}' está no mesmo diretório do script.")
    exit()

# --- 2. Definir as configurações da rede para os experimentos ---
# Requisito c: Testar pelo menos duas configurações de rede
configs_rede = [
    {'label': 'Config 1: Uma camada oculta com 10 neurônios', 'hidden_layer_sizes': (10,)},
    {'label': 'Config 2: Duas camadas ocultas com 10 e 5 neurônios', 'hidden_layer_sizes': (10, 5)}
]

# Requisito d: Treinar a rede com 30, 50 e 100 épocas
epocas = [30, 50, 100]

# --- 3. Executar os experimentos e apresentar os resultados ---
# Requisito e: Apresentar os experimentos realizados e os resultados obtidos

for config in configs_rede:
    for epoca in epocas:
        print("="*70)
        print(f"EXPERIMENTO: {config['label']} | Épocas: {epoca}")
        print("="*70)
        
        # CORREÇÃO: Parâmetros do MLP ajustados para um treinamento eficaz com 'sgd'
        mlp = MLPClassifier(
            hidden_layer_sizes=config['hidden_layer_sizes'],
            max_iter=epoca,
            random_state=42,
            solver='sgd',
            activation='relu',
            learning_rate_init=0.1,  # Taxa de aprendizado maior
            momentum=0.9             # Adicionado momentum para melhor convergência
        )
        
        # Treinar o modelo com os dados de treinamento
        mlp.fit(X_train, y_train)
        
        # Fazer predições com os dados de teste
        predicoes = mlp.predict(X_test)
        
        # Calcular a acurácia
        acuracia = accuracy_score(y_test, predicoes)
        
        # Gerar o relatório de classificação (precisão, recall, f1-score)
        relatorio = classification_report(y_test, predicoes, zero_division=0)
        
        # Apresentar os resultados para o relatório
        print(f"Resultados para a base de teste:\n")
        print(f"Acurácia: {acuracia:.2%}\n")
        print("Relatório de Classificação:")
        print(relatorio)
        print("\n")