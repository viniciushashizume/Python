from flask import Flask, request, jsonify
from datetime import datetime
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

app = Flask(__name__)
data = []

# Inicializa e treina o modelo (se não existir um arquivo de modelo salvo)
model = None

# Função para treinar o modelo
def train_model():
    global model
    df = pd.DataFrame(data)

    # Exemplo de feature engineering
    df['hour'] = df['timestamp'].dt.hour
    threshold = 10  # Defina um threshold adequado
    df['label'] = df['distance'] > threshold  # Defina o rótulo

    # Definindo variáveis de entrada e saída
    X = df[['hour']]
    y = df['label']

    # Dividindo os dados
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Treinando o modelo
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Salvando o modelo para uso posterior
    joblib.dump(model, 'model.pkl')

# Função para carregar o modelo
def load_model():
    global model
    if os.path.exists('model.pkl'):
        model = joblib.load('model.pkl')

@app.route('/data', methods=['POST'])
def receive_data():
    global data, model
    distancia = request.form.get('distancia')
    timestamp = request.form.get('timestamp')

    if distancia is None or timestamp is None:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        distancia = float(distancia)
        timestamp = datetime.fromtimestamp(int(timestamp))

        # Armazenar os dados recebidos
        data.append({'distance': distancia, 'timestamp': timestamp})

        # Treinar o modelo se houver dados suficientes
        if len(data) >= 10:  # Ajuste conforme necessário
            train_model()

        # Carregar o modelo se não estiver carregado
        if model is None:
            load_model()

        # Fazer a previsão
        df = pd.DataFrame(data)
        df['hour'] = df['timestamp'].dt.hour
        X_new = df[['hour']].iloc[-1:]  # Pegando a última entrada
        prediction = model.predict(X_new)

        # Retornar a previsão como resposta
        return jsonify({"message": "Data received", "distance": distancia, "timestamp": timestamp.isoformat(), "prediction": bool(prediction[0])}), 200

    except ValueError:
        return jsonify({"error": "Invalid data format"}), 400

def save_to_csv(distance, timestamp):
    filename = 'sensor_data.csv'
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a') as file:
        if not file_exists:
            file.write('timestamp,distance\n')  # Escreve o cabeçalho
        file.write(f"{timestamp.isoformat()},{distance}\n")  # Escreve os dados

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
