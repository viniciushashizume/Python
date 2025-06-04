import random

def local_beam_search(n_rainhas, tamanho_feixe=5, max_iteracoes=1000):
    """
    Resolve o problema das N-Rainhas usando Local Beam Search.
    
    Args:
        n_rainhas: Número de rainhas e tamanho do tabuleiro (n x n)
        tamanho_feixe: Quantidade de estados mantidos simultaneamente
        max_iteracoes: Número máximo de tentativas antes de desistir
    
    Returns:
        Uma lista representando as posições das rainhas ou None se não encontrar solução
    """
    
    # Função para criar um tabuleiro aleatório
    def criar_tabuleiro():
        return [random.randint(0, n_rainhas-1) for _ in range(n_rainhas)]
    
    # Função para contar quantos ataques existem no tabuleiro
    def contar_ataques(tabuleiro):
        ataques = 0
        for col1 in range(n_rainhas):
            for col2 in range(col1+1, n_rainhas):
                linha1, linha2 = tabuleiro[col1], tabuleiro[col2]
                # Rainhas se atacam se estão na mesma linha ou na mesma diagonal
                if linha1 == linha2 or abs(linha1 - linha2) == abs(col1 - col2):
                    ataques += 1
        return ataques
    
    # Função para gerar todos os vizinhos (pequenas modificações no tabuleiro)
    def gerar_vizinhos(tabuleiro):
        vizinhos = []
        for coluna in range(n_rainhas):
            for linha in range(n_rainhas):
                if linha != tabuleiro[coluna]:  # Ignora a posição atual da rainha
                    novo_tabuleiro = tabuleiro.copy()
                    novo_tabuleiro[coluna] = linha
                    vizinhos.append(novo_tabuleiro)
        return vizinhos
    
    # Passo 1: Inicializar com vários tabuleiros aleatórios
    tabuleiros_atuais = [criar_tabuleiro() for _ in range(tamanho_feixe)]
    
    for _ in range(max_iteracoes):
        # Passo 2: Verificar se algum tabuleiro atual é solução
        for tabuleiro in tabuleiros_atuais:
            if contar_ataques(tabuleiro) == 0:
                return tabuleiro
        
        # Passo 3: Gerar todos os vizinhos de todos os tabuleiros atuais
        todos_vizinhos = []
        for tabuleiro in tabuleiros_atuais:
            todos_vizinhos.extend(gerar_vizinhos(tabuleiro))
        
        # Passo 4: Ordenar os vizinhos pelo número de ataques (do melhor para o pior)
        todos_vizinhos.sort(key=lambda x: contar_ataques(x))
        
        # Passo 5: Selecionar os melhores vizinhos para a próxima iteração
        tabuleiros_atuais = todos_vizinhos[:tamanho_feixe]
    
    # Se chegou aqui, não encontrou solução
    return None

def imprimir_tabuleiro(tabuleiro):
    """Mostra o tabuleiro de forma visual"""
    if tabuleiro is None:
        print("Nenhuma solução encontrada")
        return
    
    n = len(tabuleiro)
    for linha in range(n):
        for coluna in range(n):
            print("Q " if tabuleiro[coluna] == linha else ". ", end="")
        print()

# Exemplo de uso:
if __name__ == "__main__":
    n = 8  # Número de rainhas (8 para o problema clássico)
    solucao = local_beam_search(n)
    
    print(f"\nSolução para {n}-rainhas:")
    imprimir_tabuleiro(solucao)