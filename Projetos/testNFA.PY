from graphviz import Digraph

# Estados e transições do NFA
states = {"q0", "q1", "q2"}
initial_state = "q0"
final_states = {"q0"}
transitions = {
    "q0": {"1": {"q1"}},
    "q1": {"0": {"q0", "q2"}, "1": {"q2"}},
    "q2": {},
}

# Criando o diagrama
dot = Digraph(format="png")
dot.attr(rankdir="LR")  # Layout da esquerda para a direita

# Adicionando estados
for state in states:
    if state in final_states:
        dot.node(state, shape="doublecircle")  # Estados finais
    else:
        dot.node(state, shape="circle")  # Outros estados

# Adicionando transições
for state, symbol_map in transitions.items():
    for symbol, dest_states in symbol_map.items():
        for dest in dest_states:
            dot.edge(state, dest, label=symbol)

# Marcando o estado inicial
dot.node("", shape="none")  # Estado inicial fictício
dot.edge("", initial_state)

# Gerando o diagrama
dot.render("nfa_diagram", view=True)  # Salva e exibe o diagrama
