import pickle

# Especifique o caminho do seu arquivo .pkl
caminho_arquivo = 'C:/Users/Vinicius/Documents/GitHub/Python/model.pkl'

# Abra o arquivo em modo de leitura binária
with open(caminho_arquivo, 'rb') as arquivo:
    objeto = pickle.load(arquivo)

# Agora 'objeto' contém o que foi salvo no arquivo .pkl
print(objeto)
