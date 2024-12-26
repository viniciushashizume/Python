import random
from colorama import Fore, Style

def gerarFeedback(palavra, tentativa):
    resultado = []
    for i, letra in enumerate(tentativa):
        if letra == palavra[i]:
            resultado.append(Fore.GREEN + letra + Style.RESET_ALL)
        elif letra in palavra:
            resultado.append(Fore.YELLOW + letra + Style.RESET_ALL)
        else:
            resultado.append(letra)
    return "".join(resultado)

def jogo():
    palavras = ["porta", "janta", "calvo"]
    palavra_aleatoria = random.choice(palavras)
    tentativas = 5

    print("Regras:\n- Letras na posição correta ficam verdes.\n- Letras na palavra, mas na posição errada, ficam amarelas.\n")
    print("Você tem 5 tentativas para adivinhar a palavra correta. Boa sorte!\n")

    for tentativa in range(1, tentativas + 1):
        resposta = input(f"Tentativa {tentativa}/{tentativas}: ").strip().lower()

        # Validação de entrada
        if len(resposta) != len(palavra_aleatoria):
            print(f"A palavra deve ter {len(palavra_aleatoria)} letras. Tente novamente.")
            continue

        # Gerar feedback
        resultado_feedback = gerarFeedback(palavra_aleatoria, resposta)
        print(f"Feedback: {resultado_feedback}\n")

        # Verificar se acertou
        if resposta == palavra_aleatoria:
            print(Fore.GREEN + "Parabéns! Você acertou a palavra!" + Style.RESET_ALL)
            break
    else:
        print(Fore.RED + f"Que pena! A palavra era: {palavra_aleatoria}." + Style.RESET_ALL)

jogo()
