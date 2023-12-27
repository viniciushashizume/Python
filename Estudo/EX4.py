nome = input('Qual nome deseja inserir: ')
palavras = nome.split()
sigla = '' #String vazia 

for palavra in palavras:
    sigla += palavra[0].upper()

print('A sigla é:', sigla)
