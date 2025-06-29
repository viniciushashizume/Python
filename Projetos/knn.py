import pandas as pd
import re
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np

# --- Configurações Iniciais ---
ARQUIVO_ENTRADA = 'Pedido_informacao_sei_23064.030111_2019_10_Versao02.xlsx'
ARQUIVO_SAIDA_UNIFICADO = 'base_dados_unificada.xlsx'
HEADER_ROW = 2

NOMES_ABAS = {
    'Relacao_Alunos': 'df_alunos',
    'Historico': 'df_historico',
    'Questionario_socioEconomico': 'df_questionario'
}

COLUNAS_SCALAR_ALUNOS = ['coeficiente', 'escore_vest', 'nota_enem', 'idade']
COLUNAS_SCALAR_HISTORICO = ['nota', 'freq_percentual', 'média_da_turma', 'qtd_de_alunos_turma']
COLUNAS_PARA_ONEHOT = ['forma_de_ingresso', 'escola_pública', 'sexo', 'grupo']
COLUNAS_A_MANTER = ['Período']

def padronizar_nomes_colunas(df, exclude=None):
    if exclude is None:
        exclude = []

    novas_colunas = {}
    for coluna in df.columns:
        if coluna in exclude:
            novas_colunas[coluna] = coluna
        else:
            nova_coluna = str(coluna).strip()
            nova_coluna = re.sub(r'[.\s\(\)%?:]+', '_', nova_coluna)
            nova_coluna = re.sub(r'_+$', '', nova_coluna)
            nova_coluna = nova_coluna.lower()
            novas_colunas[coluna] = nova_coluna

    df.rename(columns=novas_colunas, inplace=True)
    return df

def carregar_dados_excel(caminho_arquivo):
    """
    Carrega as abas especificadas de um arquivo Excel em dataframes.
    """
    try:
        todos_dfs = pd.read_excel(caminho_arquivo, sheet_name=list(NOMES_ABAS.keys()), header=HEADER_ROW)
        dataframes = {}
        for nome_aba, df in todos_dfs.items():
            df_padronizado = padronizar_nomes_colunas(df.copy(), exclude=COLUNAS_A_MANTER)
            if df.empty:
                print(f"AVISO: A aba '{nome_aba}' está vazia e será ignorada.")
                dataframes[NOMES_ABAS[nome_aba]] = pd.DataFrame()
                continue
            
            if 'id' not in df_padronizado.columns:
                sys.exit(f"ERRO CRÍTICO: Coluna 'id' não encontrada na aba '{nome_aba}'.")
            
            df_padronizado['id'] = df_padronizado['id'].astype(str)
            dataframes[NOMES_ABAS[nome_aba]] = df_padronizado
        return dataframes
    except FileNotFoundError:
        sys.exit(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
    except ValueError as e:
        sys.exit(f"Erro ao ler as abas do Excel. Verifique se os nomes {list(NOMES_ABAS.keys())} estão corretos no arquivo. Erro original: {e}")
    except Exception as e:
        sys.exit(f"Ocorreu um erro inesperado ao ler o arquivo Excel: {e}")

def escalar_colunas(df, colunas, scaler):
    colunas_existentes = [col for col in colunas if col in df.columns]
    if not colunas_existentes:
        return df

    df[colunas_existentes] = df[colunas_existentes].replace(',', '.', regex=True)
    df[colunas_existentes] = df[colunas_existentes].apply(pd.to_numeric, errors='coerce')

    for col in colunas_existentes:
        valores_nao_nulos = df[[col]].dropna()
        if not valores_nao_nulos.empty:
            df.loc[valores_nao_nulos.index, col] = scaler.fit_transform(valores_nao_nulos)

    return df

def normalizar_dados(dfs):
    df_alunos, df_historico, df_questionario = dfs['df_alunos'], dfs['df_historico'], dfs['df_questionario']
    colunas_a_remover = []

    if 'data_nascimento' in df_alunos.columns:
        df_alunos['data_nascimento'] = pd.to_datetime(df_alunos['data_nascimento'], dayfirst=True, errors='coerce')
        df_alunos['idade'] = (pd.to_datetime('2024-01-01') - df_alunos['data_nascimento']).dt.days / 365.25
        colunas_a_remover.append('data_nascimento')

    colunas_str_lowercase = ['escola_pública', 'sexo', 'grupo', 'situação_atual_do_aluno']
    for col in colunas_str_lowercase:
        if col in df_alunos.columns:
            df_alunos[col] = df_alunos[col].str.strip().str.lower()

    if 'freq' in df_historico.columns:
        df_historico.rename(columns={'freq': 'freq_percentual'}, inplace=True)
        df_historico['freq_percentual'] = df_historico['freq_percentual'].astype(str).str.replace('%', '', regex=False)

    if 'sigla_cota' in df_alunos.columns:
        df_alunos['is_cotista'] = (df_alunos['sigla_cota'].str.strip().str.lower() != 'não cotista').astype(int)
        colunas_a_remover.append('sigla_cota')

    if 'cidade' in df_alunos.columns:
        df_alunos['is_ponta_grossa'] = df_alunos['cidade'].str.lower().str.contains('ponta grossa', na=False).astype(int)
        colunas_a_remover.append('cidade')

    if 'estado' in df_alunos.columns:
        df_alunos['is_parana'] = df_alunos['estado'].str.lower().str.contains('pr|paraná', na=False, regex=True).astype(int)
        colunas_a_remover.append('estado')

    if 'situação_atual_do_aluno' in df_alunos.columns:
        status_evasao = ['desistente', 'transferido', 'jubilado', 'mudou de curso']
        df_alunos['evadiu'] = df_alunos['situação_atual_do_aluno'].isin(status_evasao).astype(int)
        colunas_a_remover.append('situação_atual_do_aluno')

    df_questionario_norm = normalizar_e_pivotar_questionario(df_questionario)

    scaler = MinMaxScaler()
    df_alunos = escalar_colunas(df_alunos, COLUNAS_SCALAR_ALUNOS, scaler)
    df_historico = escalar_colunas(df_historico, COLUNAS_SCALAR_HISTORICO, scaler)

    colunas_onehot_existentes = [col for col in COLUNAS_PARA_ONEHOT if col in df_alunos.columns]
    if colunas_onehot_existentes:
        df_alunos = pd.get_dummies(df_alunos, columns=colunas_onehot_existentes, dummy_na=True, dtype=int)

    df_alunos.drop(columns=colunas_a_remover, inplace=True, errors='ignore')

    return df_alunos, df_historico, df_questionario_norm

def normalizar_e_pivotar_questionario(df_questionario):
    if df_questionario.empty:
        return pd.DataFrame(columns=['id'])
        
    pergunta_renda_padronizada = "a_renda_total_mensal_de_sua_família_se_situa_na_faixa_de"
    mapa_renda = {
        'Menos de 1 salário mínimo.': 0, 'De um a dois salários mínimos.': 1,
        'De dois a cinco salários mínimos.': 2, 'De cinco a dez salários mínimos.': 3,
        'De dez a quinze salários mínimo.': 4, 'De vinte a quarenta salários mínimos.': 5,
        'Mais de quarenta salários mínimos.': 6
    }

    df_pivot = df_questionario.pivot_table(index='id', columns='pergunta', values='resposta', aggfunc='first').reset_index()
    df_pivot = padronizar_nomes_colunas(df_pivot, exclude=COLUNAS_A_MANTER)

    if pergunta_renda_padronizada in df_pivot.columns:
        df_pivot['renda_ordinal'] = df_pivot[pergunta_renda_padronizada].str.strip().map(mapa_renda)
        scaler_renda = MinMaxScaler()
        valores_validos = df_pivot[['renda_ordinal']].dropna()
        if not valores_validos.empty:
            df_pivot.loc[valores_validos.index, 'renda_normalizada'] = scaler_renda.fit_transform(valores_validos)

        df_pivot.drop(columns=[pergunta_renda_padronizada, 'renda_ordinal'], inplace=True, errors='ignore')

    return df_pivot

def unir_dataframes_finais(df_alunos, df_historico, df_questionario):
    df_final = df_alunos.copy()

    if not df_historico.empty:
        agregacoes_historico = {
            'nota': 'mean', 'freq_percentual': 'mean',
            'média_da_turma': 'mean', 'qtd_de_alunos_turma': 'mean'
        }
        agregacoes_existentes = {k: v for k, v in agregacoes_historico.items() if k in df_historico.columns}
        df_historico_agregado = df_historico.groupby('id').agg(agregacoes_existentes).reset_index()

        df_historico_agregado.rename(columns={
            'nota': 'nota_media_historico', 'freq_percentual': 'freq_media_historico',
            'média_da_turma': 'media_turma_historico', 'qtd_de_alunos_turma': 'qtd_alunos_media_historico'
        }, inplace=True)
        df_final = pd.merge(df_final, df_historico_agregado, on='id', how='left')

    if not df_questionario.empty:
        # Garante que a coluna 'id' do questionário é string para o merge
        df_questionario['id'] = df_questionario['id'].astype(str)
        df_final = pd.merge(df_final, df_questionario, on='id', how='left')

    return df_final

# --- APLICAÇÃO DO K-NN ---

def executar_analise_knn(df):
    """
    Função principal que executa toda a análise KNN.
    """
    print("\n--- Iniciando Análise com k-NN ---")

    if 'evadiu' not in df.columns:
        sys.exit("ERRO: A coluna 'evadiu' não foi encontrada no dataframe unificado.")

    features_para_remover = ['id', 'evadiu', '#', 'nome_do_curso', 'forma_de_ingresso_nan']
    X = df.drop(columns=[col for col in features_para_remover if col in df.columns])
    y = df['evadiu']

    for col in X.select_dtypes(include=np.number).columns:
        X[col].fillna(X[col].median(), inplace=True)
    
    X = X.apply(pd.to_numeric, errors='coerce').fillna(0)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    print(f"Dados divididos em {len(X_train)} para treino e {len(X_test)} para teste.")

    knn_25 = KNeighborsClassifier(n_neighbors=25)
    knn_25.fit(X_train, y_train)
    y_pred_25 = knn_25.predict(X_test)

    print("\n--- Resultados do Modelo KNN (K=25) ---")
    print("\nRelatório de Classificação:")
    print(classification_report(y_test, y_pred_25))
    
    acc_25 = accuracy_score(y_test, y_pred_25)
    print(f"Acurácia do Modelo: {acc_25:.2f}")

    cm = confusion_matrix(y_test, y_pred_25)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Não Evadiu', 'Evadiu'], yticklabels=['Não Evadiu', 'Evadiu'])
    plt.title('Matriz de Confusão (K=25)')
    plt.xlabel('Predito')
    plt.ylabel('Verdadeiro')
    plt.savefig('matriz_confusao_knn.png')
    plt.close()
    print("\nGráfico da matriz de confusão salvo como 'matriz_confusao_knn.png'")

    print("\n--- Análise de Vizinhos com K=5 ---")
    knn_5 = KNeighborsClassifier(n_neighbors=5)
    knn_5.fit(X_train, y_train)
    
    # Gera 5 análises de vizinhos para 5 alunos diferentes
    for i in range(5):
        # Seleciona um aluno aleatório diferente a cada iteração
        aluno_teste_idx = X_test.sample(1, random_state=i).index
        aluno_teste_features = X_test.loc[aluno_teste_idx]

        distancias, indices_vizinhos = knn_5.kneighbors(aluno_teste_features)
        
        df_vizinhos = X_train.iloc[indices_vizinhos[0]]

        # Lista expandida de colunas para dar mais contexto à análise dos vizinhos.
        colunas_para_exibir = [
            # Desempenho acadêmico
            'coeficiente', 
            'nota_media_historico', 
            'freq_media_historico',
            # Desempenho no ingresso
            'escore_vest',
            'nota_enem',
            # Dados demográficos e de origem
            'idade',
            'is_cotista',
            'is_ponta_grossa',
            'is_parana',
            # Dado socioeconômico
            'renda_normalizada' 
        ]

        # Filtra os dados para exibição, garantindo que a coluna exista no dataframe
        aluno_teste_display = aluno_teste_features[[col for col in colunas_para_exibir if col in aluno_teste_features.columns]]
        df_vizinhos_display = df_vizinhos[[col for col in colunas_para_exibir if col in df_vizinhos.columns]]

        # Aumenta o número de colunas que o pandas exibe por padrão no .to_string()
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        
        # Define um nome de arquivo único para cada análise
        nome_arquivo_analise = f'analise_vizinhos_k5_aluno_teste_{i+1}.txt'

        with open(nome_arquivo_analise, 'w', encoding='utf-8') as f:
            f.write(f"Análise para o aluno de índice: {aluno_teste_idx[0]}\n")
            status_real = "Evadiu" if y_test.loc[aluno_teste_idx[0]] == 1 else "Não Evadiu"
            f.write(f"Status de evasão real do aluno: {status_real}\n\n")

            f.write("Características selecionadas do aluno em teste:\n")
            # Transpõe o dataframe (troca linhas por colunas) para melhor legibilidade
            f.write(aluno_teste_display.T.to_string())
            f.write("\n\n")
            f.write("Características selecionadas dos seus 5 vizinhos mais próximos:\n")
            f.write(df_vizinhos_display.to_string())
        
        print(f"Análise de vizinhos salva em '{nome_arquivo_analise}'")

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
      plt.title('Dispersão no Conjunto de Teste: Média de Nota vs. Frequência')
      plt.xlabel('Nota Média Normalizada')
      plt.ylabel('Frequência Média Normalizada')
      plt.legend(title='Previsão de Evasão', labels=['Não Evadiu', 'Evadiu'])
      plt.grid(True)
      plt.savefig('scatter_teste_nota_freq.png')
      plt.close()
      print("Gráfico de dispersão (teste: nota vs. freq) salvo como 'scatter_teste_nota_freq.png'")


if __name__ == "__main__":
    print("Iniciando processo de leitura e unificação do arquivo Excel...")
    dataframes = carregar_dados_excel(ARQUIVO_ENTRADA)
    
    if dataframes:
        df_alunos_norm, df_historico_norm, df_questionario_norm = normalizar_dados({k: v.copy() for k, v in dataframes.items()})
        df_unificado = unir_dataframes_finais(df_alunos_norm, df_historico_norm, df_questionario_norm)
        
        df_unificado.to_excel(ARQUIVO_SAIDA_UNIFICADO, index=False, sheet_name='DadosUnificados')
        print(f"\nProcesso de unificação concluído! Arquivo final salvo como: '{ARQUIVO_SAIDA_UNIFICADO}'")
        
        executar_analise_knn(df_unificado)
        
        print("\n--- Análise Finalizada com Sucesso! ---")
    else:
        print("ERRO: Nenhum dado foi carregado do arquivo Excel.")
