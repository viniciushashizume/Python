from graphviz import Digraph

dot = Digraph()
dot.node('A')
dot.node('B')
dot.edge('A', 'B')
dot.render('test-output', view=True)