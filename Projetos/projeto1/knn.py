import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import sys

# --- Constantes ---
ARQUIVO_DADOS_UNIFICADOS = 'base_dados_unificada.xlsx'

def executar_analise_knn(df):
    """
    Executa a análise KNN completa em um dataframe pré-processado.
    Gera relatórios, matriz de confusão e análises de vizinhos.
    """
    print("\n--- Iniciando Análise com k-NN ---")

    # Verifica se a coluna alvo 'evadiu' existe
    if 'evadiu' not in df.columns:
        sys.exit("ERRO: A coluna 'evadiu', que é o alvo da classificação, não foi encontrada no dataframe.")

    # --- Preparação dos Dados para o Modelo ---
    
    # Define as features (X) e o alvo (y)
    features_para_remover = ['id', 'evadiu', '#', 'nome_do_curso', 'forma_de_ingresso_nan', 'ano_desistência', 'período_desistências','período_do_aluno' ]
    X = df.drop(columns=[col for col in features_para_remover if col in df.columns])
    y = df['evadiu']

    # Garante que todas as colunas de features sejam numéricas
    for col in X.select_dtypes(include=np.number).columns:
        X[col] = X[col].fillna(X[col].median())
    
    # Converte colunas que possam não ser numéricas e preenche qualquer NaN restante com 0
    X = X.apply(pd.to_numeric, errors='coerce').fillna(0)

    # Divide os dados em conjuntos de treino e teste
    # 'stratify=y' garante que a proporção de evasão seja a mesma nos dois conjuntos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    print(f"Dados divididos em {len(X_train)} amostras para treino e {len(X_test)} para teste.")

    # --- Treinamento e Avaliação do Modelo KNN (K=25) ---
    knn_25 = KNeighborsClassifier(n_neighbors=25)
    knn_25.fit(X_train, y_train)
    y_pred_25 = knn_25.predict(X_test)

    print("\n--- Resultados do Modelo KNN (K=25) ---")
    print("\nRelatório de Classificação:")
    print(classification_report(y_test, y_pred_25, target_names=['Não Evadiu', 'Evadiu']))
    
    acc_25 = accuracy_score(y_test, y_pred_25)
    print(f"Acurácia do Modelo (K=25): {acc_25:.2%}")

    # Gera e salva a matriz de confusão
    cm = confusion_matrix(y_test, y_pred_25)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Não Evadiu', 'Evadiu'], yticklabels=['Não Evadiu', 'Evadiu'])
    plt.title('Matriz de Confusão (K=25)')
    plt.xlabel('Predito')
    plt.ylabel('Verdadeiro')
    plt.savefig('matriz_confusao_knn.png')
    plt.close()
    print("\nGráfico da matriz de confusão salvo como 'matriz_confusao_knn.png'")

    # --- Análise Detalhada dos Vizinhos (K=5) ---
    print("\n--- Análise de Vizinhos com K=5 ---")
    knn_5 = KNeighborsClassifier(n_neighbors=5)
    knn_5.fit(X_train, y_train)
    
    # Gera 5 análises de vizinhos para 5 alunos diferentes do conjunto de teste
    for i in range(5):
        # Seleciona um aluno aleatório a cada iteração para garantir variedade
        aluno_teste_idx = X_test.sample(1, random_state=i).index
        aluno_teste_features = X_test.loc[aluno_teste_idx]

        # Encontra os 5 vizinhos mais próximos no conjunto de treino
        distancias, indices_vizinhos = knn_5.kneighbors(aluno_teste_features)
        
        df_vizinhos = X_train.iloc[indices_vizinhos[0]]

        # Colunas selecionadas para dar um contexto claro à análise dos vizinhos
        colunas_para_exibir = [
            'coeficiente', 'nota_media_historico', 'freq_media_historico',
            'escore_vest', 'nota_enem', 'idade', 'is_cotista',
            'is_ponta_grossa', 'is_parana', 'renda_normalizada' 
        ]

        # Filtra os dados para exibição, garantindo que as colunas existam
        aluno_teste_display = aluno_teste_features[[col for col in colunas_para_exibir if col in aluno_teste_features.columns]]
        df_vizinhos_display = df_vizinhos[[col for col in colunas_para_exibir if col in df_vizinhos.columns]]

        # Configura o pandas para exibir todas as colunas
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        
        nome_arquivo_analise = f'analise_vizinhos_k5_aluno_{i+1}.txt'
        with open(nome_arquivo_analise, 'w', encoding='utf-8') as f:
            status_real = "Evadiu" if y_test.loc[aluno_teste_idx[0]] == 1 else "Não Evadiu"
            f.write(f"Análise para o aluno de índice: {aluno_teste_idx[0]} (Status Real: {status_real})\n\n")
            f.write("Características do Aluno em Teste:\n")
            f.write(aluno_teste_display.T.to_string(header=False)) # Transposto para melhor leitura
            f.write("\n\n" + "="*50 + "\n\n")
            f.write("Características dos Seus 5 Vizinhos Mais Próximos:\n")
            f.write(df_vizinhos_display.to_string())
        
        print(f"Análise de vizinhos salva em '{nome_arquivo_analise}'")

    if 'df_vizinhos' in locals() and 'aluno_teste_features' in locals():
        vizinhos_nota_media = df_vizinhos.get('nota_media_historico', pd.Series(dtype='float64'))
        aluno_teste_nota_media = aluno_teste_features.get('nota_media_historico', pd.Series(dtype='float64')).values[0]

        if not vizinhos_nota_media.empty:
            plt.figure(figsize=(10, 6))
            plt.scatter(range(len(vizinhos_nota_media)), vizinhos_nota_media, label='Vizinhos (k=5)')
            plt.scatter(-1, aluno_teste_nota_media, color='red', marker='*', s=200, label='Aluno em Teste (Último Analisado)')
            plt.xticks([])
            plt.ylabel('Nota Média Normalizada')
            plt.title('Comparação da Nota Média: Último Aluno de Teste vs. Seus 5 Vizinhos Mais Próximos')
            plt.legend()
            plt.grid(True)
            plt.savefig('scatter_vizinhos_nota_media.png')
            plt.close()
            print("\nGráfico de dispersão (vizinhos por nota) salvo como 'scatter_vizinhos_nota_media.png'")


    # --- Geração de Gráficos Adicionais ---
    df_teste_plot = X_test.copy()
    df_teste_plot['evadiu_predito'] = y_pred_25
    
    if 'nota_media_historico' in df_teste_plot.columns and 'freq_media_historico' in df_teste_plot.columns:
        plt.figure(figsize=(12, 8))
        sns.scatterplot(
            data=df_teste_plot, 
            x='nota_media_historico', 
            y='freq_media_historico', 
            hue='evadiu_predito', 
            palette={0: 'blue', 1: 'red'},
            alpha=0.7
        )
        plt.title('Dispersão: Média de Nota vs. Frequência (Previsões no Conjunto de Teste)')
        plt.xlabel('Nota Média Normalizada')
        plt.ylabel('Frequência Média Normalizada')
        plt.legend(title='Previsão de Evasão', labels=['Não Evadiu', 'Evadiu'])
        plt.grid(True)
        plt.savefig('scatter_teste_nota_vs_freq.png')
        plt.close()
        print("\nGráfico de dispersão (teste: nota vs. freq) salvo como 'scatter_teste_nota_vs_freq.png'")

def main():
    """
    Função principal que carrega os dados e orquestra a análise.
    """
    print(f"Carregando dados pré-processados do arquivo: '{ARQUIVO_DADOS_UNIFICADOS}'")
    try:
        df_unificado = pd.read_excel(ARQUIVO_DADOS_UNIFICADOS)
        print("Dados carregados com sucesso!")
        
        # Inicia a análise KNN com os dados carregados
        executar_analise_knn(df_unificado)
        
        print("\n--- Análise Finalizada com Sucesso! ---")

    except FileNotFoundError:
        print(f"\nERRO CRÍTICO: O arquivo '{ARQUIVO_DADOS_UNIFICADOS}' não foi encontrado.")
        print("Por favor, certifique-se de que o script de normalização foi executado e o arquivo está na mesma pasta que este script.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado ao ler o arquivo ou executar a análise: {e}")

if __name__ == "__main__":
    main()
