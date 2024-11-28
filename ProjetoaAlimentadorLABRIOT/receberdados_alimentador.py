from flask import Flask, request, jsonify
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)
data = []

@app.route('/data', methods=['POST']) 
def receive_data():
    distancia = request.form.get('distancia') 
    tempo = request.form.get('timestamp')

    if distancia is None or tempo is None:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        distancia = float(distancia)
        tempo = datetime.fromtimestamp(int(tempo)) 
        data.append({'distance': distancia, 'tempo': tempo})

        save_to_csv(distancia, tempo)

        return jsonify({"message": "Data received", "distance": distancia, "tempo": tempo.isoformat()}), 200
    except ValueError:
        return jsonify({"error": "Invalid data format"}), 400

def save_to_csv(distance, tempo):
    filename = 'sensor_data.csv'
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a') as file:
        if not file_exists:
            file.write('tempo,distance\n')
        file.write(f"{tempo.isoformat()},{distance}\n")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
