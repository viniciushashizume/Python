from flask import Flask, request, jsonify
from datetime import datetime
import pandas as pd
import os
from sklearn.cluster import KMeans
import numpy as np

app = Flask(__name__)
data = []

@app.route('/data', methods=['POST']) 
def receive_data():
    distancia = request.form.get('distancia') 
    timestamp = request.form.get('timestamp')

    if distancia is None or timestamp is None:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        distancia = float(distancia)
        timestamp = datetime.fromtimestamp(int(timestamp)) 
        data.append({'distance': distancia, 'timestamp': timestamp})

        save_to_csv(distancia, timestamp)

        return jsonify({"message": "Data received", "distance": distancia, "timestamp": timestamp.isoformat()}), 200
    except ValueError:
        return jsonify({"error": "Invalid data format"}), 400

def save_to_csv(distance, timestamp):
    filename = 'sensor_data.csv'
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a') as file:
        if not file_exists:
            file.write('timestamp,distance\n')
        file.write(f"{timestamp.isoformat()},{distance}\n")

@app.route('/analyze', methods=['GET'])
def analyze_data():
    # Carregar os dados do arquivo CSV
    df = pd.read_csv('sensor_data.csv', parse_dates=['timestamp'])
    df['hour'] = df['timestamp'].dt.hour  # Extrair a hora do timestamp
    
    # Agrupar os dados por hora e contar as leituras
    hourly_counts = df.groupby('hour')['distance'].count().reset_index()
    
    # Aplicar KMeans para identificar os picos
    kmeans = KMeans(n_clusters=3)  # Você pode ajustar o número de clusters conforme necessário
    hourly_counts['hour'] = hourly_counts['hour'].values.reshape(-1, 1)  # Reformatar para KMeans
    kmeans.fit(hourly_counts[['hour']])
    
    hourly_counts['cluster'] = kmeans.labels_

    # Retornar os dados de análise
    return jsonify(hourly_counts.to_dict(orient='records')), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
