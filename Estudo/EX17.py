import collections

queue = collections.deque([])

for _ in range(5):
    valor = input('insira o valor')
    queue.appendleft(valor)

print(queue)