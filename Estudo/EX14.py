#inserindo no final

lista = []*5

"""for i in range(5):
    #num = input('Digite o numero ')
    lista.append(0)"""

for i in range(5):
    num = input('Digite o numero ')
    lista.insert(len(lista), num) #Inserir no final
    
print (lista)