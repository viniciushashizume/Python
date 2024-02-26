#projeto calculadora

class calc:
    def __init__(self, num1, num2):
        self.n1 = num1
        self.n2 = num2

    def soma(self):
        return self.n1+self.n2
    def subtr(self):
        return self.n1+self.n2
    def mult(self):
        return self.n1*self.n2
    def div(self):
        if (self.n2 == 0):
            return 0
        else:
            return self.n1/self.n2
        
a = calc(2,4)
b= a.soma()
c= a.subtr()
print(b)
print(c)