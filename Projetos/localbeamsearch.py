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
