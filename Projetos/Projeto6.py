class Estudante:
    def __init__(self, nome, serie):
        self.nome = nome
        self.serie = serie
        self.notas = []
    def inserir_nota(self, nota):
        self.notas.append(nota)
    def exibir_informacao (self):
        print(f'Nome do aluno: {self.nome} | Serie do aluno: {self.serie} | Notas do aluno {self.notas}')
       
class Escola:
    def __init__(self):
        self.alunos = []
    def adicionar_aluno(self, aluno):
        self.alunos.append(aluno)
        print(f'Aluno {aluno.nome} inserido no sistema!')
    def calcularmedia(self, aluno):
        soma = sum(aluno.notas)
        media = soma/len(aluno.notas)
        return media

            

estudante1= Estudante ("A", "1A")
estudante1.inserir_nota(8.5)
estudante1.inserir_nota(8.0)
escola = Escola()
escola.adicionar_aluno(estudante1)
media = escola.calcularmedia(estudante1)
print(f'Media do aluno é: {media}')
estudante1.exibir_informacao()
