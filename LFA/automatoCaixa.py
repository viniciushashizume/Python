from graphviz import Digraph

# Definir os estados, alfabeto, transições, estado inicial e estados finais
states = {
    'q0': 'Aguardar Cartão',
    'q1': 'Aguardar PIN Correto',
    'q2': 'Menu',
    'q3': 'PIN Incorreto',
    'q4': 'Solicitar Valor de Saque',
    'q5': 'Saque Concluído',
    'q6': 'Saldo Insuficiente',
    'q7': 'Solicitar Consulta de Saldo',
    'q8': 'Consulta de Saldo Concluída',
    'q9': 'Solicitar Transferência',
    'q10': 'Transferência Concluída',
    'q11': 'Erro na Transferência',
    'q12': 'Solicitar Recibo',
    'q13': 'Recibo Impresso',
    'q14': 'Retirar Cartão',
    'q15': 'Solicitar Valor Depósito',
    'q16': 'Depósito Concluído',
    'q17': 'Invalidar Operação',
    'q18': 'Verificação de Operação Saldo',
    'q19': 'Depósito Inválido',
    'q20': 'Verificação de Operação Transferência',
    'q21': 'Verificação de Operação Depósito',
}

alphabet = {
    'inserir_cartao', 'pin_incorreto', 'pin_correto', 'solicitar_saque',
    'solicitar_deposito', 'consultar_saldo', 'solicitar_transferencia',
    'imprimir_recibo_saldo', 'erro_saldo', 'erro', 'retirar_cartao',
    'voltar', 'terro_transferencia', 'concluir',
    'verificacao', 'verificacao_saldo', 'verificado_transferencia',
    'verificado_deposito', 'impressao_concluida', 'consulta_concluida', 'imprimir_recibo_transferencia'
}

transitions = {
    'q0': {'inserir_cartao': 'q1'},
    'q1': {'pin_incorreto': 'q3', 'pin_correto': 'q2'},
    'q2': {'solicitar_saque': 'q4', 'consultar_saldo': 'q7', 'solicitar_transferencia': 'q9', 'solicitar_deposito': 'q15', 'concluir': 'q14'},
    'q3': {'pin_incorreto': 'q3', 'pin_correto': 'q2'},
    'q4': {'verificacao': 'q18'},  
    'q5': {'concluir': 'q14', 'imprimir_recibo_saldo': 'q12'},
    'q6': {'erro': 'q17'},
    'q7': {'consulta_concluida': 'q8'},
    'q8': {'concluir': 'q14'},
    'q9': {'verificacao': 'q20'},  
    'q10': {'concluir': 'q14', 'imprimir_recibo_transferencia': 'q12'},
    'q11': {'erro': 'q17'},
    'q12': {'impressao_concluida': 'q13'},
    'q13': {'concluir': 'q14'},
    'q14': {'retirar_cartao': 'q0', 'voltar': "q2"},
    'q15': {'verificacao': 'q21'},  
    'q16': {'concluir': 'q14'},
    'q17': {'voltar': 'q2'},
    'q18': {'verificacao_saldo': 'q5', 'erro_saldo': 'q6'},  # Saída da verificação
    'q19': {'erro': 'q17'},
    'q20': {'erro_transferencia': 'q11', 'verificao_transferencia': 'q10'},
    'q21': {'erro_deposito': 'q19','verificacao_deposito': 'q16' }
}

initial_state = 'q0'
accepting_states = {'q0'}

# objeto digraph 
dot = Digraph(format="png")
dot.attr(rankdir="LR")  # formatação de esquerda para a direita

# adicionando os estados
for estado, nome in states.items():
    if estado in accepting_states:
        dot.node(estado, label=nome, shape="doublecircle")  # estados finais
    else:
        dot.node(estado, label=nome, shape="circle")  # outros estados

#adicionando as transições entre os estados
for estado, mapa_simbolos in transitions.items():
    for simbolo, estado_destino in mapa_simbolos.items():
        dot.edge(estado, estado_destino, label=simbolo)

# adicionando o estado inicial fictício e a transição inicial
dot.node("", shape="none")  # estado inicial fictício
dot.edge("", initial_state)  # transição do estado inicial fictício para o estado inicial real

#geração de imagem do diagrama
dot.render("automato_diagrama", view=True)

# função para processar uma sequência de entrada
def processarEntrada(Entrada):
    estadoAtual = initial_state
    entradas = Entrada.split(' - ')
    resultados = [f"Estado inicial: {estadoAtual} - {states[estadoAtual]}"]
    
    for simbolo in entradas:
        if simbolo in transitions.get(estadoAtual, {}):
            proximoEstado = transitions[estadoAtual][simbolo]
            resultados.append(f"({estadoAtual} - {states[estadoAtual]}, {simbolo}) ⇒ {proximoEstado} - {states[proximoEstado]}")
            estadoAtual = proximoEstado
        else:
            resultados.append(f"Erro: Transição inválida para ({estadoAtual} - {states[estadoAtual]}, {simbolo})")
            break
    
    if estadoAtual in accepting_states:
        resultados.append(f"Estado final alcançado: {estadoAtual} - {states[estadoAtual]}")
    else:
        resultados.append(f"Erro: Não chegou ao estado final. Estado atual: {estadoAtual} - {states[estadoAtual]}")
    
    return '\n'.join(resultados)

# função para ler entrada e gerar saida
def processarArquivo(arquivoEntrada, arquivoSaida):
    with open(arquivoEntrada, 'r', encoding='utf-8') as f:
        linhasEntrada = f.readlines()

    resultados = []
    for i, linha in enumerate(linhasEntrada):
        sequenciaEntrada = linha.strip()
        if sequenciaEntrada:  # ignorar linhas vazias
            resultados.append(f"Teste {i + 1}:")
            resultados.append(processarEntrada(sequenciaEntrada))
            resultados.append("")  # adicionar uma linha em branco entre os resultados

    with open(arquivoSaida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(resultados))

processarArquivo('entrada.txt', 'saida.txt')
