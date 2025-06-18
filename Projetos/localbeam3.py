import random

def get_quadratic_function():
    print("Digite os coeficientes da função quadrática f(x) = ax² + bx + c:")
    a = float(input("a: "))
    b = float(input("b: "))
    c = float(input("c: "))
    
    def f(x):
        return a * x**2 + b * x + c
    
    return f, a, b, c

def generate_successors(x):
    delta = random.uniform(-0.5, 0.5)
    return x + delta

def local_beam_search(f, a, b, c, k=15, max_iterations=100):
    # Define o modo automaticamente com base em 'a'
    if a > 0:
        mode = "min"
    elif a < 0:
        mode = "max"
    else:
        mode = "max" if b < 0 else "min"  # Função linear: depende do coeficiente de b

    current_states = [random.uniform(-10, 10) for _ in range(k)]
    best_solution = None

    print("\nInício do Local Beam Search")
    print(f"Modo automático selecionado: {mode.upper()}")
    print(f"Estados iniciais: {[round(s, 3) for s in current_states]}")
    
    for iteration in range(1, max_iterations + 1):
        successors = []
        for state in current_states:
            for _ in range(3):
                new_state = generate_successors(state)
                score = f(new_state)
                if mode == "min":
                    score = -score
                successors.append((new_state, score))

                if best_solution is None or score > best_solution[1]:
                    best_solution = (new_state, score)

        successors.sort(key=lambda x: x[1], reverse=True)
        current_states = [s[0] for s in successors[:k]]

        print(f"\nIteração {iteration}")
        for i, x in enumerate(current_states):
            val = f(x)
            print(f"  Estado {i+1}: x = {x:.4f}, f(x) = {val:.4f}")
    
    best_x, best_score = best_solution
    best_f = f(best_x)

    # Solução teórica ótima
    if a != 0:
        optimal_x = -b / (2 * a)
        optimal_f = f(optimal_x)
    else:
        f_min = f(-10)
        f_max = f(10)
        if (mode == "max" and f_min > f_max) or (mode == "min" and f_min < f_max):
            optimal_x, optimal_f = -10, f_min
        else:
            optimal_x, optimal_f = 10, f_max
    
    print("\n=== Resultado Final ===")
    print(f"Melhor solução encontrada: x = {best_x:.4f}, f(x) = {best_f:.4f}")
    print(f"Solução teórica ótima: x = {optimal_x:.4f}, f(x) = {optimal_f:.4f}")

if __name__ == "__main__":
    f, a, b, c = get_quadratic_function()
    local_beam_search(f, a, b, c)
