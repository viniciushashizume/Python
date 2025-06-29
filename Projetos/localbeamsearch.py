<<<<<<< HEAD
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
=======
import tkinter as tk
from tkinter import messagebox
import random

def localBeamSearch(k=15, iteracoesMaximas=1000):
    def conflitos(estado):
        contador = 0
        for i in range(8):
            for j in range(i + 1, 8):
                if estado[i] == estado[j] or abs(estado[i] - estado[j]) == j - i:
                    contador += 1
        return contador

    def vizinhos(estado):
        resultado = []
        for coluna in range(8):
            for linha in range(8):
                if estado[coluna] != linha:
                    novoEstado = estado[:]
                    novoEstado[coluna] = linha
                    resultado.append(novoEstado)
        return resultado

    estados = [[random.randint(0, 7) for _ in range(8)] for _ in range(k)]

    for _ in range(iteracoesMaximas):
        estados.sort(key=conflitos)
        if conflitos(estados[0]) == 0:
            return estados[0]
        neighbors_pool = []
        for s in estados[:k]:
            neighbors_pool.extend(vizinhos(s))
        estados = sorted(neighbors_pool, key=conflitos)[:k]

    return None

# Interface com Tkinter
class appOitoRainhas:
    def __init__(self, root):
        self.root = root
        self.root.title("Problema das 8 Rainhas - Local Beam Search")
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        
        self.btn_start = tk.Button(self.root, text="Encontrar Solução", command=self.resolver)
        self.btn_start.pack(pady=10)

    def desenharTabuleiro(self, solution):
        self.canvas.delete("all")
        cell_size = 50
        for linha in range(8):
            for coluna in range(8):
                x1 = coluna * cell_size
                y1 = linha * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                fill = "white" if (linha + coluna) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill)
                if solution[coluna] == linha:
                    self.canvas.create_text(x1 + 25, y1 + 25, text="♕", font=("Arial", 24), fill="red")

    def resolver(self):
        solution = localBeamSearch()
        if solution:
            self.desenharTabuleiro(solution)
           #messagebox.showinfo("Sucesso", "Solução encontrada!")"""
        else:
            messagebox.showwarning("Falha", "Não foi encontrada solução.")

# Execução da interface
if __name__ == "__main__":
    root = tk.Tk()
    app = appOitoRainhas(root)
    root.mainloop()
>>>>>>> b1d0650287338fcd140d7d51fdeaf0390aaad811
