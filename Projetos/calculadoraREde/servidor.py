import socket
import hashlib
import struct
import ipaddress

# Dados de autenticação (simulando um banco de dados)
usuarios = {
    "admin": hashlib.sha256("senha123".encode()).hexdigest(),
    "user1": hashlib.sha256("password1".encode()).hexdigest()
}

def autenticar_cliente(conn):
    """Autentica o cliente com login e senha"""
    conn.send(b"Bem-vindo ao servidor de calculadora de sub-redes!\n")
    
    # Receber login
    conn.send(b"Login: ")
    login = conn.recv(1024).decode().strip()
    
    # Receber senha
    conn.send(b"Senha: ")
    senha = conn.recv(1024).decode().strip()
    
    # Verificar credenciais
    if login in usuarios and usuarios[login] == hashlib.sha256(senha.encode()).hexdigest():
        conn.send(b"Autenticacao bem-sucedida!\n")
        return True
    else:
        conn.send(b"Falha na autenticacao. Credenciais invalidas.\n")
        return False

def calcular_subredes_ipv4(endereco, mascara_original, num_subredes):
    """Calcula sub-redes IPv4"""
    try:
        # Converter para objeto de rede
        rede = ipaddress.IPv4Network(f"{endereco}/{mascara_original}", strict=False)
        
        # Calcular nova máscara
        bits_necessarios = num_subredes.bit_length()
        nova_mascara = mascara_original + bits_necessarios
        
        if nova_mascara > 30:  # Limite prático para IPv4
            return None, "Mascara resultante muito grande para IPv4"
        
        # Dividir a rede
        subredes = list(rede.subnets(prefixlen_diff=bits_necessarios))
        
        resultados = []
        for subrede in subredes[:num_subredes]:
            # Endereço útil inicial é o primeiro host
            primeiro_host = subrede.network_address + 1
            # Endereço útil final é o último host
            ultimo_host = subrede.broadcast_address - 1
            
            resultados.append({
                'subrede': f"{subrede.network_address}/{nova_mascara}",
                'inicio': str(primeiro_host),
                'fim': str(ultimo_host)
            })
        
        return resultados, None
    
    except Exception as e:
        return None, str(e)

def calcular_subredes_ipv6(endereco, mascara_original, num_subredes):
    """Calcula sub-redes IPv6"""
    try:
        # Converter para objeto de rede
        rede = ipaddress.IPv6Network(f"{endereco}/{mascara_original}", strict=False)
        
        # Calcular nova máscara
        bits_necessarios = num_subredes.bit_length()
        nova_mascara = mascara_original + bits_necessarios
        
        if nova_mascara > 126:  # Limite prático para IPv6
            return None, "Mascara resultante muito grande para IPv6"
        
        # Dividir a rede
        subredes = list(rede.subnets(prefixlen_diff=bits_necessarios))
        
        resultados = []
        for subrede in subredes[:num_subredes]:
            # Endereço útil inicial é o primeiro host
            primeiro_host = subrede.network_address + 1
            # Endereço útil final é o último host (simplificado para IPv6)
            ultimo_host = subrede.broadcast_address - 1
            
            resultados.append({
                'subrede': f"{subrede.compressed}/{nova_mascara}",
                'inicio': f"{primeiro_host.compressed}",
                'fim': f"{ultimo_host.compressed}"
            })
        
        return resultados, None
    
    except Exception as e:
        return None, str(e)

def processar_requisicao(conn):
    """Processa a requisição do cliente"""
    try:
        # Receber tipo de IP (4 ou 6)
        conn.send(b"Escolha o tipo de IP (4 para IPv4, 6 para IPv6): ")
        tipo_ip = conn.recv(1024).decode().strip()
        
        if tipo_ip not in ['4', '6']:
            conn.send(b"Opcao invalida. Use 4 ou 6.\n")
            return
        
        # Receber endereço de rede
        conn.send(b"Digite o endereco de rede (ex: 192.168.0.0 ou 2001:db8:baba::): ")
        endereco = conn.recv(1024).decode().strip()
        
        # Receber máscara
        conn.send(b"Digite a mascara (ex: 24 para IPv4, 48 para IPv6): ")
        mascara = int(conn.recv(1024).decode().strip())
        
        # Validar máscara
        if tipo_ip == '4' and (mascara < 16 or mascara > 29):
            conn.send(b"Mascara invalida para IPv4. Deve ser entre /16 e /29.\n")
            return
        elif tipo_ip == '6' and (mascara < 48 or mascara > 62):
            conn.send(b"Mascara invalida para IPv6. Deve ser entre /48 e /62.\n")
            return
        
        # Receber número de sub-redes
        conn.send(b"Digite o numero de sub-redes desejadas: ")
        num_subredes = int(conn.recv(1024).decode().strip())
        
        # Calcular sub-redes
        if tipo_ip == '4':
            resultados, erro = calcular_subredes_ipv4(endereco, mascara, num_subredes)
        else:
            resultados, erro = calcular_subredes_ipv6(endereco, mascara, num_subredes)
        
        if erro:
            conn.send(f"Erro: {erro}\n".encode())
            return
        
        # Enviar resultados
        conn.send(b"\nResultados:\n")
        for res in resultados:
            linha = f"{res['subrede']} {res['inicio']} {res['fim']}\n"
            conn.send(linha.encode())
        
        conn.send(b"Calculo concluido.\n")
    
    except Exception as e:
        conn.send(f"Erro no processamento: {str(e)}\n".encode())

def iniciar_servidor():
    """Inicia o servidor socket"""
    host = '0.0.0.0'
    port = 12345
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Servidor ouvindo em {host}:{port}")
        
        while True:
            conn, addr = s.accept()
            print(f"Conexao estabelecida com {addr}")
            
            try:
                # Autenticar cliente
                if not autenticar_cliente(conn):
                    conn.close()
                    continue
                
                # Processar requisições
                while True:
                    processar_requisicao(conn)
                    
                    # Verificar se cliente quer continuar
                    conn.send(b"Deseja fazer outro calculo? (s/n): ")
                    resposta = conn.recv(1024).decode().strip().lower()
                    if resposta != 's':
                        break
                
            except Exception as e:
                print(f"Erro com cliente {addr}: {e}")
            finally:
                conn.close()
                print(f"Conexao com {addr} encerrada")

if __name__ == "__main__":
    iniciar_servidor()