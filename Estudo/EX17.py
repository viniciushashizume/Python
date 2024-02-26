import collections

queue = collections.deque([])
queue2 = collections.deque([])

for _ in range(5):
    valor = input('insira o valor')
    queue.appendleft(valor) #insere fim

for _ in range(5):
    valor = input('insira o valor')
    queue2.append(valor) #insere inicio

print(queue)
print(queue2)