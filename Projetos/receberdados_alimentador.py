from flask import Flask, request, jsonify
from datetime import datetime
import pandas as pd
import os

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
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
