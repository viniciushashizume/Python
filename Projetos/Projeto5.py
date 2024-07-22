class Funcionario:
    def __init__(self, nome, cargo, salario):
        self.nome = nome
        self.cargo = cargo
        self.salario = salario
    def exibir_informacoes(self):
        print(f'Nome do funcionario: {self.nome} | Cargo: {self.cargo} | Salario: {self.salario}')
    
class Empresa:
    def __init__(self, nome_empresa):
        self.nome_empresa = nome_empresa
        self.funcionarios = []
    def adicionar_funcionario(self, funcionario):
        self.funcionarios.append(funcionario)
        print(f'Funcionario {funcionario.nome} adicionado!')
    def aumentar_salario(self, funcionario, aumento):
        funcionario.salario += aumento
        print(f'Salario do funcionário {funcionario.nome} atualizado para {funcionario.salario}')
    def exibir_funcionarios(self):
        for funcionario in self.funcionarios:
            funcionario.exibir_informacoes()
            
funcionario1= Funcionario("A", "Caixa", 1500)
funcionario2= Funcionario("B", "Caixa", 4500)

empresa = Empresa("A")

empresa.adicionar_funcionario(funcionario1)
empresa.adicionar_funcionario(funcionario2)
empresa.exibir_funcionarios()
empresa.aumentar_salario(funcionario1, 200)
empresa.exibir_funcionarios()

