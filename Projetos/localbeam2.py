import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Polygon
from collections import defaultdict

# Classe que define os estados do Brasil, suas conexões e heurísticas
class EstadosBrasil:
    def __init__(self):
        # Dicionário com sigla e nome dos estados
        self.estados = {
            'AC': {'nome': 'Acre'}, 'AL': {'nome': 'Alagoas'},'AM': {'nome': 'Amazonas'},
            'AP': {'nome': 'Amapá'},'BA': {'nome': 'Bahia'}, 'CE': {'nome': 'Ceará'},
            'DF': {'nome': 'Distrito Federal'},'ES': {'nome': 'Espírito Santo'},'GO': {'nome': 'Goiás'},
            'MA': {'nome': 'Maranhão'},'MG': {'nome': 'Minas Gerais'},'MS': {'nome': 'Mato Grosso do Sul'},
            'MT': {'nome': 'Mato Grosso'},'PA': {'nome': 'Pará'},'PB': {'nome': 'Paraíba'},
            'PE': {'nome': 'Pernambuco'},'PI': {'nome': 'Piauí'},'PR': {'nome': 'Paraná'},
            'RJ': {'nome': 'Rio de Janeiro'},'RN': {'nome': 'Rio Grande do Norte'},'RO': {'nome': 'Rondônia'},
            'RR': {'nome': 'Roraima'},'RS': {'nome': 'Rio Grande do Sul'},'SC': {'nome': 'Santa Catarina'},
            'SE': {'nome': 'Sergipe'},'SP': {'nome': 'São Paulo'},'TO': {'nome': 'Tocantins'}
        }
        # Dicionário de conexões entre estados com as distâncias em km
        self.conexoes = {
            ('AC', 'AM'): 1420, ('AC', 'RO'): 520,
            ('AM', 'RO'): 900, ('AM', 'MT'): 2500, ('AM', 'PA'): 5300, ('AM', 'RR'): 785,
            ('AP', 'PA'): 620,
            ('PA', 'MA'): 800, ('PA', 'TO'): 1100, ('PA', 'MT'): 2600,
            ('RO', 'MT'): 1450,
            ('RR', 'AM'): 785,
            ('AL', 'PE'): 280, ('AL', 'SE'): 290, ('AL', 'BA'): 630,
            ('BA', 'SE'): 350, ('BA', 'PE'): 840, ('BA', 'PI'): 1100, ('BA', 'TO'): 1500, 
            ('BA', 'MG'): 500, ('BA', 'ES'): 800,
            ('CE', 'RN'): 530, ('CE', 'PB'): 690, ('CE', 'PE'): 800, ('CE', 'PI'): 630,
            ('MA', 'PI'): 450, ('MA', 'TO'): 1100,
            ('PB', 'PE'): 120, ('PB', 'RN'): 185,
            ('PE', 'PI'): 800, ('PE', 'AL'): 280,
            ('PI', 'TO'): 900,
            ('DF', 'GO'): 200, ('DF', 'MG'): 700,
            ('GO', 'MT'): 900, ('GO', 'MS'): 800, ('GO', 'MG'): 900, ('GO', 'TO'): 800,
            ('MS', 'MT'): 700, ('MS', 'SP'): 1000, ('MS', 'PR'): 1250,
            ('MT', 'PA'): 2600, ('MT', 'TO'): 1100,
            ('ES', 'MG'): 500, ('ES', 'RJ'): 500, ('ES', 'BA'): 1200,
            ('MG', 'RJ'): 500, ('MG', 'SP'): 600, ('MG', 'BA'): 1400, ('MG', 'GO'): 900,
            ('RJ', 'SP'): 400,
            ('SP', 'PR'): 400,
            ('PR', 'SC'): 300, ('PR', 'MS'): 1250,
            ('RS', 'SC'): 480,
            ('SC', 'PR'): 300
        }
    def obterVizinhos(self, estado):
        return [(v, d) for (e1, e2), d in self.conexoes.items() 
                if estado in (e1, e2) and (v := e2 if e1 == estado else e1)]

class BuscadorCaminhos:
    def __init__(self, estadosBrasil, visualizador):
        self.estadosBrasil = estadosBrasil
        self.visualizador = visualizador

    def buscaFeixeLocal(self, inicio, objetivo, k=6, maxIter=27):
        # Inicializa com k caminhos começando no estado inicial
        estadosAtuais = [(0, inicio, [inicio])]  # (custo_acumulado, estado, caminho)
        
        for iteracao in range(1, maxIter+1):
            print(f"\n--- Iteração {iteracao} ---")
            print(f"Melhores candidatos (k={k}):")
            for i, (custo, estado, caminho) in enumerate(estadosAtuais, 1):
                print(f"{i}. {estado} (Custo: {custo}km, Caminho: {' → '.join(caminho)})")
            
            # Gera todos os vizinhos dos estados atuais
            proximosEstados = []
            for custo, estado, caminho in estadosAtuais:
                for vizinho, distancia in self.estadosBrasil.obterVizinhos(estado):
                    if vizinho not in caminho:  # Evita ciclos
                        novoCaminho = caminho + [vizinho]
                        proximosEstados.append((
                            custo + distancia,
                            vizinho,
                            novoCaminho
                        ))
            
            if not proximosEstados:
                print("Nenhum novo estado alcançável.")
                break
            
            # Ordena pelo custo acumulado e mantém apenas os k melhores
            proximosEstados.sort(key=lambda x: x[0])
            estadosAtuais = proximosEstados[:k]
            
            # Verifica se alcançamos o objetivo
            for custo, estado, caminho in estadosAtuais:
                if estado == objetivo:
                    print(f"\nObjetivo {objetivo} alcançado em {iteracao} iterações!")
                    return caminho
        
        # Se não encontrou, retorna o melhor caminho parcial
        if estadosAtuais:
            melhor_caminho = min(estadosAtuais, key=lambda x: x[0])[2]
            return melhor_caminho
        return None
    
class VisualizadorGrafo:
    def __init__(self, estadosBrasil):
        self.estadosBrasil = estadosBrasil
        self.coords = {
            'AC': (-9.11, -70.52), 'AL': (-9.57, -36.55), 'AM': (-3.47, -65.10),
            'AP': (1.41, -51.77), 'BA': (-12.96, -41.71), 'CE': (-5.20, -39.53),
            'DF': (-15.83, -47.86), 'ES': (-19.19, -40.34), 'GO': (-16.64, -49.31),
            'MA': (-5.42, -45.44), 'MG': (-18.10, -44.38), 'MS': (-20.51, -54.54),
            'MT': (-12.64, -55.42), 'PA': (-3.79, -52.48), 'PB': (-7.28, -36.72),
            'PE': (-8.38, -37.86), 'PI': (-7.72, -42.73), 'PR': (-24.89, -51.55),
            'RJ': (-22.25, -42.66), 'RN': (-5.81, -36.59), 'RO': (-10.83, -63.34),
            'RR': (1.99, -61.33), 'RS': (-30.17, -53.50), 'SC': (-27.45, -50.95),
            'SE': (-10.57, -37.45), 'SP': (-22.19, -48.79), 'TO': (-9.46, -48.26)
        }

    def visualizarMapaBrasileiro(self, caminho=None):
        plt.figure(figsize=(16, 16))
        contornoBr = [
            (-4, -50), (-7, -48), (-9, -46), (-11, -44), (-14, -42),
            (-17, -41), (-20, -40), (-23, -41), (-26, -43), (-28, -46),
            (-30, -50), (-30, -53), (-28, -56), (-25, -58), (-20, -60),
            (-15, -65), (-10, -70), (-5, -73), (0, -72), (3, -68),
            (4, -62), (4, -56), (2, -52), (0, -50), (-2, -52), (-4, -50)
        ]
        
        poligonoBr = Polygon(contornoBr, closed=True, fill=False, 
                           edgecolor='blue', linewidth=2, linestyle='--', alpha=0.5)
        plt.gca().add_patch(poligonoBr)
        
        for sigla, dados in self.estadosBrasil.estados.items():
            x, y = self.coords[sigla]
            plt.scatter(y, x, s=200, color='lightblue', edgecolor='black')
            plt.text(y, x+0.5, sigla, ha='center', va='center', fontsize=10,
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
            
            if caminho and sigla in caminho:
                plt.text(y, x-0.7, dados['nome'], ha='center', fontsize=8, 
                        bbox=dict(facecolor='white', alpha=0.8))
        
        for (e1, e2) in self.estadosBrasil.conexoes.keys():
            x1, y1 = self.coords[e1]
            x2, y2 = self.coords[e2]
            plt.plot([y1, y2], [x1, x2], 'gray', linewidth=1, alpha=0.5)
        
        if caminho:
            for i in range(len(caminho)-1):
                e1, e2 = caminho[i], caminho[i+1]
                x1, y1 = self.coords[e1]
                x2, y2 = self.coords[e2]
                plt.plot([y1, y2], [x1, x2], 'red', linewidth=2, alpha=0.8)
                plt.scatter([y1, y2], [x1, x2], s=250, color='red', edgecolor='black', zorder=3)
        
        plt.title("Mapa do Brasil com Estados", fontsize=16)
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.grid(True, alpha=0.3)
        plt.xlim(-75, -30)
        plt.ylim(-35, 5)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.tight_layout()
        plt.show()

class InterfaceUsuario:
    def __init__(self, estadosBrasil, buscadorCaminhos):
        self.estadosBrasil = estadosBrasil
        self.buscadorCaminhos = buscadorCaminhos

    def exibirInterface(self):
        print("\n" + "="*60)
        print("SISTEMA DE BUSCA DE CAMINHOS ENTRE ESTADOS BRASILEIROS".center(60))
        print("="*60)
        
        print("\nESTADOS BRASILEIROS DISPONÍVEIS (27 unidades federativas):")
        cols = 4
        estados = sorted(self.estadosBrasil.estados.items())
        for i in range(0, len(estados), cols):
            linha = [f"{sigla} - {dados['nome']: <20}" for sigla, dados in estados[i:i+cols]]
            print(" ".join(linha))
        
        inicio = self._obterEstado("-> Digite a sigla do estado de origem: ")
        objetivo = self._obterEstado("-> Digite a sigla do estado de destino: ")
        
        print(f"\nBuscando caminho de {self.estadosBrasil.estados[inicio]['nome']} para {self.estadosBrasil.estados[objetivo]['nome']}...")
        caminho = self.buscadorCaminhos.buscaFeixeLocal(inicio, objetivo)
        
        if caminho:
            self._mostrarResultado(caminho)
        else:
            print("Não foi possível encontrar um caminho entre os estados.")

    def _obterEstado(self, mensagem):
        estado = input(mensagem).upper()
        while estado not in self.estadosBrasil.estados:
            estado = input("Sigla inválida. Tente novamente: ").upper()
        return estado

    def _mostrarResultado(self, caminho):
        print("\nCAMINHO ENCONTRADO:")
        distanciaTotal = 0
        for i in range(len(caminho)-1):
            e1, e2 = caminho[i], caminho[i+1]
            distancia = next(d for (a,b), d in self.estadosBrasil.conexoes.items() 
                         if (a == e1 and b == e2) or (a == e2 and b == e1))
            distanciaTotal += distancia
            print(f"{i+1: >2}. {self.estadosBrasil.estados[e1]['nome']: <20} → {distancia: >4}km → {self.estadosBrasil.estados[e2]['nome']}")
        
        print(f"\n DISTÂNCIA TOTAL: {distanciaTotal}km")
        self.buscadorCaminhos.visualizador.visualizarMapaBrasileiro(caminho)

def main():
    estadosBrasil = EstadosBrasil()
    visualizador = VisualizadorGrafo(estadosBrasil)
    buscador = BuscadorCaminhos(estadosBrasil, visualizador)
    interface = InterfaceUsuario(estadosBrasil, buscador)
    interface.exibirInterface()

if __name__ == "__main__":
    main()