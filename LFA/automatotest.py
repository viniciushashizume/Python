from visual_automata.fa.dfa import VisualDFA

# Define os estados, alfabeto, transições, estado inicial e estados de aceitação
states = {'q0', 'q1', 'q2', 'q3'}
alphabet = {'0', '1'}
transitions = {
    'q0': {'0': 'q0', '1': 'q1'},
    'q1': {'0': 'q2', '1': 'q1'},
    'q2': {'0': 'q0', '1': 'q3'},
    'q3': {'0': 'q3', '1': 'q3'}
}
initial_state = 'q0'
accepting_states = {'q3'}

# Criação do DFA
dfa = VisualDFA(
    states=states,
    input_symbols=alphabet,
    transitions=transitions,
    initial_state=initial_state,
    final_states=accepting_states
)

# Visualizar o autômato
dfa.show_diagram(view=True)

# Testar o DFA com algumas entradas
print(dfa.input_check('101'))  # Deve retornar True
print(dfa.input_check('1001')) # Deve retornar False
