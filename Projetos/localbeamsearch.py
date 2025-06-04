import random
import math

def local_beam_search(n, k=5, max_iterations=1000):
    """
    Implementação do Local Beam Search para o problema das N-Rainhas
    
    Args:
        n: tamanho do tabuleiro (n x n) e número de rainhas
        k: número de estados mantidos simultaneamente (tamanho do feixe)
        max_iterations: número máximo de iterações permitidas
    
    Returns:
        Uma solução válida para o problema das N-Rainhas ou None se não encontrar
    """
    def random_state():
        """Gera um estado aleatório onde cada rainha está em uma coluna diferente"""
        return [random.randint(0, n-1) for _ in range(n)]
    
    def conflicts(state):
        """Calcula o número de pares de rainhas se atacando"""
        count = 0
        for i in range(n):
            for j in range(i+1, n):
                # Verifica se estão na mesma linha ou diagonais
                if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                    count += 1
        return count
    
    def get_neighbors(state):
        """Gera todos os vizinhos do estado atual (movendo cada rainha em sua coluna)"""
        neighbors = []
        for col in range(n):
            for row in range(n):
                if row != state[col]:
                    neighbor = list(state)
                    neighbor[col] = row
                    neighbors.append(neighbor)
        return neighbors
    
    # Inicializa k estados aleatórios
    current_states = [random_state() for _ in range(k)]
    current_costs = [conflicts(state) for state in current_states]
    
    for _ in range(max_iterations):
        # Verifica se encontramos uma solução (0 conflitos)
        for state in current_states:
            if conflicts(state) == 0:
                return state
        
        # Gera todos os vizinhos de todos os estados atuais
        all_neighbors = []
        for state in current_states:
            all_neighbors.extend(get_neighbors(state))
        
        # Seleciona os k melhores vizinhos
        all_neighbors.sort(key=lambda x: conflicts(x))
        current_states = all_neighbors[:k]
        current_costs = [conflicts(state) for state in current_states]
    
    # Se não encontrou solução, retorna o melhor estado encontrado
    best_state = min(current_states, key=lambda x: conflicts(x))
    return best_state if conflicts(best_state) == 0 else None

# Exemplo de uso para o problema das 8 rainhas
n = 8
solution = local_beam_search(n)
if solution:
    print(f"Solução encontrada para {n}-rainhas:")
    for row in range(n):
        line = ["Q" if solution[col] == row else "." for col in range(n)]
        print(" ".join(line))
else:
    print(f"Não foi encontrada solução para {n}-rainhas dentro do número máximo de iterações.")