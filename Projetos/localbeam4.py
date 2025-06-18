import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Polygon

class EstadosBrasil:
    def __init__(self):
        self.estados = {
            'AC': {'nome': 'Acre'}, 'AL': {'nome': 'Alagoas'}, 'AM': {'nome': 'Amazonas'},
            'AP': {'nome': 'Amapá'}, 'BA': {'nome': 'Bahia'}, 'CE': {'nome': 'Ceará'},
            'DF': {'nome': 'Distrito Federal'}, 'ES': {'nome': 'Espírito Santo'}, 
            'GO': {'nome': 'Goiás'}, 'MA': {'nome': 'Maranhão'}, 'MG': {'nome': 'Minas Gerais'},
            'MS': {'nome': 'Mato Grosso do Sul'}, 'MT': {'nome': 'Mato Grosso'}, 
            'PA': {'nome': 'Pará'}, 'PB': {'nome': 'Paraíba'}, 'PE': {'nome': 'Pernambuco'},
            'PI': {'nome': 'Piauí'}, 'PR': {'nome': 'Paraná'}, 'RJ': {'nome': 'Rio de Janeiro'},
            'RN': {'nome': 'Rio Grande do Norte'}, 'RO': {'nome': 'Rondônia'}, 
            'RR': {'nome': 'Roraima'}, 'RS': {'nome': 'Rio Grande do Sul'}, 
            'SC': {'nome': 'Santa Catarina'}, 'SE': {'nome': 'Sergipe'}, 
            'SP': {'nome': 'São Paulo'}, 'TO': {'nome': 'Tocantins'}
        }
        
        self.conexoes = [
            ('AC', 'AM'), ('AC', 'RO'), ('AM', 'RO'), ('AM', 'MT'), ('AM', 'PA'), ('AM', 'RR'),
            ('AP', 'PA'), ('PA', 'MA'), ('PA', 'TO'), ('PA', 'MT'), ('RO', 'MT'), ('RR', 'AM'),
            ('AL', 'PE'), ('AL', 'SE'), ('AL', 'BA'), ('BA', 'SE'), ('BA', 'PE'), ('BA', 'PI'),
            ('BA', 'TO'), ('BA', 'MG'), ('BA', 'ES'), ('CE', 'RN'), ('CE', 'PB'), ('CE', 'PE'),
            ('CE', 'PI'), ('MA', 'PI'), ('MA', 'TO'), ('PB', 'PE'), ('PB', 'RN'), ('PE', 'PI'),
            ('PE', 'AL'), ('PI', 'TO'), ('DF', 'GO'), ('DF', 'MG'), ('GO', 'MT'), ('GO', 'MS'),
            ('GO', 'MG'), ('GO', 'TO'), ('MS', 'MT'), ('MS', 'SP'), ('MS', 'PR'), ('MT', 'PA'),
            ('MT', 'TO'), ('ES', 'MG'), ('ES', 'RJ'), ('ES', 'BA'), ('MG', 'RJ'), ('MG', 'SP'),
            ('MG', 'BA'), ('MG', 'GO'), ('RJ', 'SP'), ('SP', 'PR'), ('PR', 'SC'), ('PR', 'MS'),
            ('RS', 'SC'), ('SC', 'PR')
        ]

    def obterVizinhos(self, estado):
        vizinhos = []
        for (e1, e2) in self.conexoes:
            if estado == e1:
                vizinhos.append(e2)
            elif estado == e2:
                vizinhos.append(e1)
        return vizinhos

class BuscadorCaminhos:
    def __init__(self, estadosBrasil, visualizador):
        self.estadosBrasil = estadosBrasil
        self.visualizador = visualizador

    def buscaFeixeLocal(self, inicio, objetivo, k=3, maxIter=100, delayVisualizacao=5.0):
        feixe = [[inicio]]
        self.visualizador.visualizarGrafoParcial([inicio], feixe, "Início", delayVisualizacao)
        
        for iteracao in range(maxIter):
            print(f"\n--- Iteração {iteracao} ---")
            print(f"Feixe atual (k={k}):")
            for i, caminho in enumerate(feixe, 1):
                print(f"{i}. {' → '.join(caminho)}")
            
            novos_caminhos = []
            for caminho in feixe:
                ultimo_estado = caminho[-1]
                for vizinho in self.estadosBrasil.obterVizinhos(ultimo_estado):
                    if vizinho not in caminho:
                        novos_caminhos.append(caminho + [vizinho])
            
            if not novos_caminhos:
                print("Nenhum novo estado alcançável.")
                break
            
            feixe = sorted(novos_caminhos, key=lambda x: len(x))[:k]
            
            for caminho in feixe:
                if caminho[-1] == objetivo:
                    print(f"\nObjetivo {objetivo} alcançado em {iteracao+1} iterações!")
                    self.visualizador.visualizarGrafoParcial(
                        caminho, feixe, f"Final ({iteracao+1})", delayVisualizacao*2)
                    return caminho
            
            self.visualizador.visualizarGrafoParcial(
                feixe[0] if feixe else [], feixe, f"Iteração {iteracao+1}", delayVisualizacao)
        
        if feixe:
            melhor_caminho = min(feixe, key=lambda x: len(x))
            self.visualizador.visualizarGrafoParcial(
                melhor_caminho, feixe, f"Final ({maxIter})", delayVisualizacao*2)
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

    def visualizarGrafoParcial(self, caminhoAtual, feixe, titulo, delay=1.0):
        plt.figure(figsize=(12, 12))
        G = nx.Graph()
        
        for sigla in self.estadosBrasil.estados:
            G.add_node(sigla, pos=(self.coords[sigla][1], self.coords[sigla][0]))
        
        for (e1, e2) in self.estadosBrasil.conexoes:
            G.add_edge(e1, e2)
        
        pos = nx.get_node_attributes(G, 'pos')
        
        nx.draw_networkx_nodes(G, pos, node_size=300, node_color='lightblue', alpha=0.7)
        nx.draw_networkx_edges(G, pos, edge_color='gray', width=1, alpha=0.3)
        nx.draw_networkx_labels(G, pos, font_size=10)
        
        if caminhoAtual:
            nx.draw_networkx_nodes(G, pos, nodelist=caminhoAtual, 
                                 node_size=500, node_color='red', alpha=0.8)
            path_edges = list(zip(caminhoAtual, caminhoAtual[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, 
                                 edge_color='red', width=2, alpha=0.8)
        
        estados_feixe = set()
        for caminho in feixe:
            estados_feixe.update(caminho)
        
        nx.draw_networkx_nodes(G, pos, nodelist=list(estados_feixe), 
                             node_size=400, node_color='yellow', alpha=0.5)
        
        plt.title(f"Local Beam Search - {titulo}\nCaminho: {' → '.join(caminhoAtual) if caminhoAtual else 'Nenhum'}")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.draw()
        plt.pause(delay)
        plt.close()

class InterfaceUsuario:
    def __init__(self, estadosBrasil, buscadorCaminhos):
        self.estadosBrasil = estadosBrasil
        self.buscadorCaminhos = buscadorCaminhos

    def exibirInterface(self):
        print("\n" + "="*60)
        print("LOCAL BEAM SEARCH - ESTADOS BRASILEIROS".center(60))
        print("="*60)
        
        print("\nESTADOS DISPONÍVEIS:")
        for sigla, dados in sorted(self.estadosBrasil.estados.items()):
            print(f"{sigla} - {dados['nome']}")
        
        inicio = input("\nDigite a sigla do estado de origem: ").upper()
        while inicio not in self.estadosBrasil.estados:
            inicio = input("Sigla inválida. Tente novamente: ").upper()
        
        objetivo = input("Digite a sigla do estado de destino: ").upper()
        while objetivo not in self.estadosBrasil.estados:
            objetivo = input("Sigla inválida. Tente novamente: ").upper()
        
        print(f"\nBuscando caminho de {self.estadosBrasil.estados[inicio]['nome']} para {self.estadosBrasil.estados[objetivo]['nome']}...")
        caminho = self.buscadorCaminhos.buscaFeixeLocal(inicio, objetivo)
        
        if caminho:
            print("\nCAMINHO ENCONTRADO:")
            for i, estado in enumerate(caminho):
                print(f"{i+1}. {self.estadosBrasil.estados[estado]['nome']}")
        else:
            print("\nNão foi possível encontrar um caminho entre os estados.")

def main():
    estados = EstadosBrasil()
    visualizador = VisualizadorGrafo(estados)
    buscador = BuscadorCaminhos(estados, visualizador)
    interface = InterfaceUsuario(estados, buscador)
    interface.exibirInterface()

if __name__ == "__main__":
    main()