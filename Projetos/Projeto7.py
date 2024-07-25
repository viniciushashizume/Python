class Veiculo:
    def __init__(self, marca, placa, ano):
        self.marca = marca
        self.placa = placa
        self.ano = ano
    def detalhes(self):
        print(f'Marca: {self.marca} | Modelo: {self.modelo} | Ano: {self.ano}')

class Garagem:
    def __init__(self):
        self.carros = []
    def adicionar(self, carro):
        self.carros.append(carro)
        print(f'Carro {carro.marca} Placa {carro.placa} adicionado!')
    def remover(self, placa):
        for carro in self.carros:
            if carro.placa == placa:
                self.carros.remove(carro)
                return
        print('Carro nao registrado no sistema')
    def busca(self, placa):
        for carro in self.carros:
            if carro.placa == placa:
                print(f'Placa {carro.placa} Modelo {carro.modelo} Ano {carro.ano}')
                return
        print('Carro não encontrado no sistema')

v1 = Veiculo("A", "AAA", "1")
v2 = Veiculo("B", "BBB", "2")
v3 = Veiculo("C", "CCC", "3")

garage = Garagem()
garage.adicionar(v1)
garage.adicionar(v2)
garage.adicionar(v3)

