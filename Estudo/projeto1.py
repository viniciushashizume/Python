#registrar alunos (nome, ra, nascimento, serie)
#buscar aluno por id
#registrar notas por bimestre
#calcular a media e determinar se o aluno foi aprovado ou reprovado media >=6

def registroaluno (lista_aluno, num_alunos):
    for _ in range(int(num_alunos)):
        name= input('Insira o nome do aluno\n')
        nascimento = input('Insira a data de nascimento do aluno\n')
        ra1 = input('Insira o RA do aluno\n')
        ser = input('Insira a série em que o aluno está\n')
        aluno={"Nome": name, "Data": nascimento, "Ra": ra1, "Serie": ser}
        lista_aluno.append(aluno)

def buscaaluno (lista_aluno, ra1):
    for aluno in lista_aluno:
        if aluno["Ra"] == ra1:
            print(aluno['Nome'], aluno['Data'], aluno['Ra'], aluno['Serie'])
        else: 
            print('Aluno não registrado no sistema\n')
def registra_nota(lista_aluno, ra1):
    


num_alunos = input('Quantos alunos deseja inserir no sistema? \n')
lista_aluno = []

registroaluno(lista_aluno, num_alunos)
#print(lista_aluno)
busca_ra=input('Qual RA do aluno a ser buscado no sistema?\n')
buscaaluno(lista_aluno, busca_ra)

