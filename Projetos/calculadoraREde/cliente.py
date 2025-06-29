import socket

def conectar_servidor():
    """Conecta ao servidor e inicia a interação"""
    host = input("Digite o endereço do servidor: ")
    port = 12345
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            print(s.recv(1024).decode())  # Mensagem de boas-vindas
            
            while True:
                # Receber e exibir mensagens do servidor
                data = s.recv(1024).decode()
                if not data:
                    break
                
                print(data, end='')
                
                # Se o servidor espera entrada, enviar
                if data.endswith(": "):
                    entrada = input()
                    s.send(entrada.encode())
                
        except Exception as e:
            print(f"Erro na conexao: {e}")
        finally:
            print("Conexao encerrada")

if __name__ == "__main__":
    print("Cliente da Calculadora de Sub-redes")
    conectar_servidor()