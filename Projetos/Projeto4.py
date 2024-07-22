class Livro:
    def __init__(self, titulo, autor, ano):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano

    def exibirlivros(self):
        print(f'Titulo: {self.titulo} | Autor: {self.autor} | Ano: {self.ano}')

class Biblioteca:
    def __init__(self):
        self.livros = []
    def adicionarlivros(self, livro):
        self.livros.append(livro)
        print(f'Livro: "{livro.titulo}" adicionado')
    def removerlivros(self, titulo):
        for livro in self.livros:
            if livro.titulo == titulo:
                self.livros.remove(livro)
                print(f'Livro "{livro.titulo}" removido')
                return
            else:
                print("Livro não encontrado na biblioteca")
    def exibir_livros(self):
        for livro in self.livros:
            livro.exibirlivros()
            


livro1 = Livro("A", "AA", "1500")
livro2 = Livro("B", "AB", "1501")
livro3 = Livro("C", "AC", "1502")

biblioteca = Biblioteca()

biblioteca.adicionarlivros(livro1)
biblioteca.adicionarlivros(livro2)
biblioteca.adicionarlivros(livro3)

biblioteca.exibir_livros()





#livro1.exibirlivros()