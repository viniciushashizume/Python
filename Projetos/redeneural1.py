class Perceptron:
    """
    Implementação de um neurônio Perceptron com um único neurônio de entrada.
    (Esta classe permanece a mesma da implementação anterior)
    """
    def __init__(self, taxa_aprendizagem=0.1, usar_bias=False):
        self.taxa_aprendizagem = taxa_aprendizagem
        self.usar_bias = usar_bias
        self.peso = 0.0
        self.peso_bias = 0.0 if usar_bias else None

    def _funcao_ativacao(self, u):
        return 1 if u >= 0 else 0

    def prever(self, entrada):
        u = self.peso * entrada
        if self.usar_bias:
            u += self.peso_bias * 1
        return self._funcao_ativacao(u)

    def treinar(self, entrada, saida_desejada):
        saida_calculada = self.prever(entrada)
        erro = saida_desejada - saida_calculada
        if erro != 0:
            self.peso += self.taxa_aprendizagem * erro * entrada
            if self.usar_bias:
                self.peso_bias += self.taxa_aprendizagem * erro * 1
        return erro

def rodar_simulacao_para_arquivo(num_simulacao, params, arquivo_saida):
    """
    Função para executar uma simulação e ESCREVER os resultados em um arquivo.
    """
    arquivo_saida.write("-" * 30 + "\n")
    arquivo_saida.write(f"INICIANDO SIMULAÇÃO {num_simulacao}\n")
    arquivo_saida.write(f"Parâmetros: {params}\n")
    arquivo_saida.write("-" * 30 + "\n")

    usar_bias = 'peso_bias' in params
    p = Perceptron(taxa_aprendizagem=params['taxa_aprendizagem'], usar_bias=usar_bias)

    p.peso = params['peso']
    if usar_bias:
        p.peso_bias = params['peso_bias']

    epocas = 0
    limite_epocas = 100

    while epocas < limite_epocas:
        epocas += 1
        erro = p.treinar(params['entrada'], params['saida_desejada'])
        if erro == 0:
            arquivo_saida.write(f"\nConvergência atingida na Época {epocas}.\n")
            break
    
    if epocas == limite_epocas:
         arquivo_saida.write(f"\nA rede não convergiu após {limite_epocas} épocas.\n")

    epocas_resultado = '∞ (não converge)' if epocas == limite_epocas else epocas
    arquivo_saida.write(f"Épocas necessárias: {epocas_resultado}\n")
    arquivo_saida.write(f"Peso final do neurônio: {p.peso:.2f}\n")
    if usar_bias:
        arquivo_saida.write(f"Peso final do Bias: {p.peso_bias:.2f}\n")
    arquivo_saida.write("\n\n") # Adiciona espaço para a próxima simulação


# --- DEFINIÇÃO E EXECUÇÃO DAS SIMULAÇÕES PARA ARQUIVO ---

# NOME DO ARQUIVO DE SAÍDA
nome_arquivo = "resultados_simulacao.txt"

# PARÂMETROS DAS SIMULAÇÕES
sims = [
    # Sem Bias
    {'entrada': 1, 'peso': 0.5, 'taxa_aprendizagem': 0.1, 'saida_desejada': 0},
    {'entrada': 1, 'peso': 0.5, 'taxa_aprendizagem': 0.1, 'saida_desejada': 1},
    {'entrada': 0, 'peso': 0.5, 'taxa_aprendizagem': 0.1, 'saida_desejada': 1},
    {'entrada': 0, 'peso': 0.5, 'taxa_aprendizagem': 0.1, 'saida_desejada': 0},
    # Com Bias
    {'entrada': 1, 'peso': 0.5, 'peso_bias': 0.5, 'taxa_aprendizagem': 0.1, 'saida_desejada': 0},
    {'entrada': 1, 'peso': 0.5, 'peso_bias': 0.5, 'taxa_aprendizagem': 0.1, 'saida_desejada': 1},
    {'entrada': 0, 'peso': 0.5, 'peso_bias': 0.5, 'taxa_aprendizagem': 0.1, 'saida_desejada': 1},
    {'entrada': 0, 'peso': 0.5, 'peso_bias': 0.5, 'taxa_aprendizagem': 0.1, 'saida_desejada': 0}
]

try:
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        f.write("Resultados das Simulações da Rede Neural Perceptron\n")
        f.write("="*50 + "\n\n")
        for i, sim_params in enumerate(sims):
            rodar_simulacao_para_arquivo(i + 1, sim_params, f)
    
    print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")

except IOError as e:
    print(f"Ocorreu um erro ao escrever no arquivo: {e}")