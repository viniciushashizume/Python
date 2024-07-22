#gerador de senhas
import random

def gerador (tam):
    caracteres= ("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","1","2","3","4","5","6","7","8","9","0","!","@","#","$","%","&","*")
    senha = ''
    for _ in range (tam):
        senha += random.choice(caracteres)
    return senha

tam = int(input('Defina o tamanho da senha:'))
senha_gerada = gerador(tam)
print(f'A senha gerada é: {senha_gerada}')