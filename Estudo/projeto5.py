#Banco de dados produtos

'''def registraproduto(listaprodutos):
    nome = str(input("Qual nome do produto?"))
    id = int(input("Insira o codigo de verificacao do produto"))
    produto={"Nome": nome, "ID": id}
    listaprodutos.append(produto)

def imprime(listaprodutos):
    print(listaprodutos)
    print("\n")

listaprodutos=[]
op=0
while True:
    print("\n1. Registrar Produto")
    print("2. Visualizar Produtos")
    print("3. Sair")
    
    op = input("Escolha uma opção: ")
    
    if op == "1":
        registraproduto(listaprodutos)
    elif op == "2":
        print(listaprodutos)
    elif op == "3":
        print("Saindo do programa...")
        break
    else:
        print("Opção inválida. Tente novamente.")'''

class produtos:
    def __init__(self, nome, id):
        self.nome=nome
        self.id = id

class operacoes:
    def __init__(self):
        self.lista=[]
    def registrar(self):
        nome = str(input("Qual nome do produto?"))
        id = int(input("Insira o codigo de verificacao do produto"))
        produto = produtos(nome,id)
        self.lista.append(produto)
    def imprimir (self):
        if self.lista:
            print(self.lista)
            '''for produto in self.lista:
                print("Nome do produto: ", produto.nome, "ID: ", produto.id)
                print("\n")'''
            
bd = operacoes()
while True:
    op = input("Selecione a operacao que deseja executar")
    if op == "1":
        bd.registrar()
    elif op == "2":
        bd.imprimir()
    elif op == "3":
        print("Saindo do programa...")
        break
    else:
        print("Opção inválida. Tente novamente.")


