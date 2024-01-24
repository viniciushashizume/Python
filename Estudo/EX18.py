#self é o objeto que esta sendo construido, obtendo os valores passados
#passa self como parametro

class fracao:
    def __init__(self, num, den): #funcao construtor
        self.numerador = num
        if den == 0:
            self.denominador = 1
        else:
            self.denominador = den
        
    def inverter(self):
        return fracao(self.denominador, self.numerador)
    def multiplicar(self, other):
        numc=self.numerador * other.numerador
        denc=self.denominador * other.denominador
        return fracao(numc, denc)
    def somar(self, other):
        m1 = self.numerador * other.denominador
        m2 = self.denominador * other.numerador
        nums = m1+m2
        dens = self.denominador * other.denominador
        return fracao(nums,dens)

a = fracao(2,3)
b = a.inverter()
c = fracao(3,4)
d = a.multiplicar(c)
e = a.somar(c)

print("{}\n─\n{}".format(a.numerador, a.denominador))
print("──────────────────────────── ")
print("{}\n─\n{}".format(b.numerador, b.denominador))
print("──────────────────────────── ")
print("{}\n─\n{}".format(d.numerador, d.denominador))
print("──────────────────────────── ")
print("{}\n─\n{}".format(e.numerador, e.denominador))

