import tkinter as tk
from tkinter import messagebox
import random

class Resolvedor8Rainhas:
    def __init__(self, k=10, maxIteracoes=50):
        self.k = k
        self.maxIteracoes = maxIteracoes

    def calcularConflitos(self, estado):
        contagem = 0
        for i in range(8):
            for j in range(i + 1, 8):
                if estado[i] == estado[j] or abs(estado[i] - estado[j]) == j - i:
                    contagem += 1
        return contagem

    def gerarVizinhos(self, estado):
        resultado = []
        for coluna in range(8):
            for linha in range(8):
                if estado[coluna] != linha:
                    novoEstado = estado[:]
                    novoEstado[coluna] = linha
                    resultado.append(novoEstado)
        return resultado

    def executarBusca(self):
        estados = [[random.randint(0, 7) for _ in range(8)] for _ in range(self.k)]
        detalhesPassos = []

        for iteracao in range(self.maxIteracoes):
            estados.sort(key=self.calcularConflitos)
            detalhesPassos.append({
                'iteracao': iteracao + 1,
                'melhorEstado': estados[0],
                'conflitos': self.calcularConflitos(estados[0]),
                'todosEstados': estados
            })

            if self.calcularConflitos(estados[0]) == 0:
                return estados[0], iteracao, detalhesPassos

            vizinhos = []
            for estado in estados[:self.k]:
                vizinhos.extend(self.gerarVizinhos(estado))

            estados = sorted(vizinhos, key=self.calcularConflitos)[:self.k]

        return None, self.maxIteracoes, detalhesPassos

class VisualizadorTabuleiro:
    def __init__(self, canvas):
        self.canvas = canvas
        self.tamanhoCelula = 50

    def desenharTabuleiro(self, solucao):
        self.canvas.delete("all")
        for linha in range(8):
            for coluna in range(8):
                self.desenharCelula(linha, coluna)
                if solucao and solucao[coluna] == linha:
                    self.desenharRainha(linha, coluna)

    def desenharCelula(self, linha, coluna):
        x1 = coluna * self.tamanhoCelula
        y1 = linha * self.tamanhoCelula
        x2 = x1 + self.tamanhoCelula
        y2 = y1 + self.tamanhoCelula
        cor = "white" if (linha + coluna) % 2 == 0 else "gray"
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor)

    def desenharRainha(self, linha, coluna):
        x = coluna * self.tamanhoCelula + self.tamanhoCelula // 2
        y = linha * self.tamanhoCelula + self.tamanhoCelula // 2
        self.canvas.create_text(x, y, text="♕", font=("Arial", 24), fill="red")

class ControladorInterface:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Problema das 8 Rainhas - Busca Local por Feixe")
        
        self.resolvedor = Resolvedor8Rainhas()
        self.visualizador = VisualizadorTabuleiro(tk.Canvas(self.raiz, width=400, height=400))
        self.visualizador.canvas.pack()
        
        self.criarComponentesInterface()
        self.detalhesPassos = None
        self.passoAtual = 0

    def criarComponentesInterface(self):
        self.botaoIniciar = tk.Button(self.raiz, text="Encontrar Solução", command=self.resolver)
        self.botaoIniciar.pack(pady=10)

        self.rotuloStatus = tk.Label(self.raiz, text="Clique em 'Encontrar Solução' para começar.")
        self.rotuloStatus.pack(pady=10)

        self.visualizador.desenharTabuleiro([None] * 8)

    def mostrarDetalhesPasso(self):
        if self.detalhesPassos and self.passoAtual < len(self.detalhesPassos):
            passo = self.detalhesPassos[self.passoAtual]
            melhorEstado = passo['melhorEstado']
            conflitos = passo['conflitos']

            self.rotuloStatus.config(
                text=f"Iteração {passo['iteracao']} - Melhor Estado: {melhorEstado} com {conflitos} conflitos"
            )
            self.visualizador.desenharTabuleiro(melhorEstado)

            self.passoAtual += 1

            if conflitos == 0:
                messagebox.showinfo("Sucesso", f"Solução encontrada na iteração {passo['iteracao']}!")
                return

            self.raiz.after(1000, self.mostrarDetalhesPasso)
        else:
            messagebox.showwarning("Falha", "Não foi encontrada solução após as iterações máximas.")
            self.rotuloStatus.config(text="Não foi encontrada solução após as iterações máximas.")

    def resolver(self):
        self.rotuloStatus.config(text="Buscando solução... aguarde.")
        solucao, iteracoes, self.detalhesPassos = self.resolvedor.executarBusca()
        self.passoAtual = 0
        self.mostrarDetalhesPasso()

if __name__ == "__main__":
    raiz = tk.Tk()
    app = ControladorInterface(raiz)
    raiz.mainloop()