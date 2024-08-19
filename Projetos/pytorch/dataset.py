from typing import Any
from torch.utils.data import Dataset
import torchvision.datasets as datasets
from torch import nn, relu

class DataSet(Dataset):
    def __init__(self, train=False, transform = None):
        self.database = datasets.MNIST(root='./data', train = train, download = True, transform = transform) #se o diretorio nao existir, sera criado a partir do 'download'
        #transform indica as transformacoes que os dados inseridos serão submetidos
    def __getitem__(self, index):
        data, target = self.dataset[index] #conforme o indice passado como parametro, sera retornado o dado e a qual classe ele perterce
        return data, target
    def __len__(self): #retorna o tamanho do dataset
        return len(self.dataset)
    
class Model(nn.Module):
    def __init__(self, inputsize, hidden1, hidden2, outputsize):
        super(Model, self).__init__()
        self.input = nn.Linear(inputsize, hidden1)
        self.hidden = nn.Linear(hidden1,hidden2) 
        self.out = nn.Linear(hidden2,outputsize)
    def forward (self,x):
        out = relu(self.entry(x))
        out = relu(self.hidden(out))
        out = self.out(x)
        return out