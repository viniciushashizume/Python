import random

def f(x):
    return -x**2 + 4*x

def generate_successors(x):
    delta = random.uniform(-0.5, 0.5)
    return max(0, min(4, x + delta))  # Limita no intervalo [0, 4]

def local_beam_search(k=3, max_iterations=10):
    current_states = [random.uniform(0, 4) for _ in range(k)]
    best_solution = None

    print("Início do Local Beam Search")
    print(f"Estados iniciais: {[round(s, 3) for s in current_states]}")
    
    for iteration in range(1, max_iterations + 1):
        successors = []
        for state in current_states:
            for _ in range(3):  # 3 sucessores por estado
                new_state = generate_successors(state)
                score = f(new_state)
                successors.append((new_state, score))

                if best_solution is None or score > best_solution[1]:
                    best_solution = (new_state, score)

        # Selecionar os k melhores
        successors.sort(key=lambda x: x[1], reverse=True)
        current_states = [s[0] for s in successors[:k]]

        print(f"\nIteração {iteration}")
        for i, x in enumerate(current_states):
            print(f"  Estado {i+1}: x = {x:.4f}, f(x) = {f(x):.4f}")
    
    print("\n=== Resultado Final ===")
    print(f"Melhor solução encontrada: x = {best_solution[0]:.4f}, f(x) = {best_solution[1]:.4f}")
    print(f"Solução teórica ótima: x = 2.0, f(x) = 4.0")

if __name__ == "__main__":
    local_beam_search()
