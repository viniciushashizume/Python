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
    'q17': 'Invalidar Operações'
}

alphabet = {'inserir_cartao', 'pin_incorreto', 'pin_correto', 'solicitar_saque', 'solicitar_deposito', 'consultar_saldo',
            'solicitar_transferencia', 'imprimir_recibo', 'saldo_insuficiente', 'erro', 'retirar_cartao', 'voltar', 'transferencia_invalida', 'operacao_concluida'}

transitions = {
    'q0': {'inserir_cartao': 'q1'},  
    'q1': {'pin_incorreto': 'q3', 'pin_correto': 'q2'},
    'q2': {'solicitar_saque': 'q4', 'consultar_saldo': 'q7', 'solicitar_transferencia': 'q9', 'solicitar_deposito': 'q15'},
    'q3': {'pin_incorreto': 'q3', 'pin_correto': 'q2'},
    'q4': {'saldo_insuficiente': 'q6', 'operacao_concluida': 'q5'},
    'q5': {'retirar_cartao': 'q14', 'imprimir_recibo': 'q12'},
    'q6': {'erro': 'q17'},
    'q7': {'operacao_concluida': 'q8'},
    'q8': {'retirar_cartao': 'q14'},
    'q9': {'operacao_concluida': 'q10', 'transferencia_invalida': 'q11'},
    'q10': {'retirar_cartao': 'q14', 'imprimir_recibo': 'q12'},
    'q11': {'erro': 'q17'},
    'q12': {'operacao_concluida': 'q13'},
    'q13': {'retirar_cartao': 'q14'},
    'q14': {'retirar_cartao': 'q0', 'voltar' : "q2"},
    'q15': {'operacao_concluida': 'q16'},
    'q16': {'retirar_cartao': 'q14'},
    'q17': {'voltar': 'q2'}
}

initial_state = 'q0'
accepting_states = {'q14'}

# Função para processar múltiplos testes
def process_tests(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        test_cases = f.read().split("\n\n")  # Separar os testes por linha em branco
    
    results = []
    for i, test_case in enumerate(test_cases):
        results.append(f"Teste {i + 1}:")
        current_state = initial_state
        inputs = test_case.strip().split('\n')
        for input_line in inputs:
            try:
                state, symbol = input_line.split(',')
                state = state.strip()
                symbol = symbol.strip()

                if state != current_state:
                    results.append(
                        f"Erro: Estado inesperado {state} ({states.get(state, 'Desconhecido')}). "
                        f"Esperado: {current_state} ({states.get(current_state, 'Desconhecido')})"
                    )
                    break

                if symbol in transitions.get(current_state, {}):
                    next_state = transitions[current_state][symbol]
                    results.append(f"({state} - {states[state]}, {symbol}) ⇒ {next_state} - {states[next_state]}")
                    current_state = next_state
                else:
                    results.append(f"Erro: Transição inválida para ({state} - {states.get(state, 'Desconhecido')}, {symbol})")
                    break
            except ValueError:
                results.append(f"Erro no formato da linha: {input_line}")
                break

        if current_state in accepting_states:
            results.append(f"Estado final alcançado: {current_state} - {states[current_state]}")
        else:
            results.append(f"Erro: Não chegou ao estado final. Estado atual: {current_state} - {states.get(current_state, 'Desconhecido')}")
        results.append("")  # Linha em branco entre os testes

    with open(output_file, 'w', encoding='utf-8') as f:
        for line in results:
            f.write(line + '\n')

# Exemplo de uso:
process_tests('input.txt', 'output.txt')

# Criando o objeto Digraph para o autômato
dot = Digraph(format="png")
dot.attr(rankdir="LR")  # Layout da esquerda para a direita

# Adicionando os estados com seus nomes traduzidos
for state, name in states.items():
    if state in accepting_states:
        dot.node(state, label=name, shape="doublecircle")  # Estados finais
    else:
        dot.node(state, label=name, shape="circle")  # Outros estados

# Adicionando as transições entre os estados
for state, symbol_map in transitions.items():
    for symbol, dest_state in symbol_map.items():
        dot.edge(state, dest_state, label=symbol)

# Adicionando o estado inicial fictício e a transição inicial
dot.node("", shape="none")  # Estado inicial fictício
dot.edge("", initial_state)  # Transição do estado inicial fictício para o estado inicial real

# Salvar e visualizar o diagrama
dot.render("automato_diagrama", view=True)
