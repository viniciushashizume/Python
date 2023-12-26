#Par ou impar
num = int (input('Insira um numero de 0 a 1000\n'))

while num >=0 and num <=1000:
    if num%2 == 0:
        print('O numero é par\n')
    elif num%2 == 1:
        print('O numero é impar\n')
    num = int (input('Insira um numero de 0 a 1000\n'))

