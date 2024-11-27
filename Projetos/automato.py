from visual_automata.fa.nfa import VisualNFA

# Define os estados do autômato (correspondem às etapas do ATM)
states = {
    'Inserir_Cartao', 
    'Validar_PIN', 
    'Menu_Principal', 
    'Saque', 
    'Saldo', 
    'Transferencia', 
    'Extrato', 
    'Erro_PIN', 
    'Cartao_Bloqueado', 
    'Saldo_Insuficiente', 
    'Confirmacao', 
    'Finalizacao'
}

# Alfabeto: simplificado para representar ações possíveis
alphabet = {'Inserir', 'PIN_OK', 'PIN_Errado', 'Saque', 'Saldo', 'Transferencia', 
            'Extrato', 'Saldo_OK', 'Saldo_Insuf', 'Encerrar'}

# Transições do NFA (usando `set` para mutabilidade)
transitions = {
    'Inserir_Cartao': {'Inserir': {'Validar_PIN'}},
    'Validar_PIN': {'PIN_OK': {'Menu_Principal'}, 'PIN_Errado': {'Erro_PIN'}},
    'Erro_PIN': {'PIN_OK': {'Menu_Principal'}, 'PIN_Errado': {'Cartao_Bloqueado'}},
    'Menu_Principal': {
        'Saque': {'Saque'}, 
        'Saldo': {'Saldo'}, 
        'Transferencia': {'Transferencia'}, 
        'Extrato': {'Extrato'}, 
        'Encerrar': {'Finalizacao'}
    },
    'Saque': {'Saldo_OK': {'Confirmacao'}, 'Saldo_Insuf': {'Saldo_Insuficiente'}},
    'Saldo': {'Encerrar': {'Finalizacao'}},
    'Transferencia': {'Saldo_OK': {'Confirmacao'}, 'Saldo_Insuf': {'Saldo_Insuficiente'}},
    'Extrato': {'Encerrar': {'Finalizacao'}},
    'Confirmacao': {'Encerrar': {'Finalizacao'}},
    'Saldo_Insuficiente': {'Encerrar': {'Finalizacao'}},
    'Cartao_Bloqueado': {'Encerrar': {'Finalizacao'}},
    'Finalizacao': {}  # Estado final, sem transições
}

# Estado inicial
initial_state = 'Inserir_Cartao'

# Estados de aceitação (onde o cliente finaliza ou ocorre bloqueio)
accepting_states = {'Finalizacao', 'Cartao_Bloqueado'}

# Criação do NFA
nfa = VisualNFA(
    states=states,
    input_symbols=alphabet,
    transitions=transitions,
    initial_state=initial_state,
    final_states=accepting_states
)

# Visualizar o autômato
nfa.show_diagram(view=True)

# Testar o NFA com algumas sequências de entrada
print("Entrada 'Inserir PIN_OK Saque Saldo_OK Encerrar':", 
      nfa.input_check(['Inserir', 'PIN_OK', 'Saque', 'Saldo_OK', 'Encerrar']))  # True

print("Entrada 'Inserir PIN_Errado PIN_Errado Encerrar':", 
      nfa.input_check(['Inserir', 'PIN_Errado', 'PIN_Errado', 'Encerrar']))  # True

print("Entrada 'Inserir PIN_OK Saque Saldo_Insuf Encerrar':", 
      nfa.input_check(['Inserir', 'PIN_OK', 'Saque', 'Saldo_Insuf', 'Encerrar']))  # True

print("Entrada 'Inserir PIN_Errado Encerrar':", 
      nfa.input_check(['Inserir', 'PIN_Errado', 'Encerrar']))  # False
