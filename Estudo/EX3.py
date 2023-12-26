#Informações biográficas

while True:
    nome = input('Digite o nome: \n')

    if isinstance(nome, str):
        break
    else:
        print('Tipo invalido para esta leitura, digite novamente: \n')

while True:
    idade = input('Digite a Idade: \n')

    if isinstance(idade, int):
        break
    else:
        print('Tipo invalido para esta leitura, digite novamente: \n')

print('Nome:', nome)
print('Idade:', idade)
    

        
