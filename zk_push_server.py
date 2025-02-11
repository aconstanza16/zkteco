from flask import Flask, request, jsonify
import requests
import os
import logging

app = Flask(__name__)

# Configuración del dispositivo de control de acceso
DEVICE_IP = "10.0.0.201"  # Cambia a la IP del equipo
DEVICE_PORT = "8080"  # Puerto del equipo

# Configurar logs para depuración en Railway
logging.basicConfig(level=logging.DEBUG)

@app.route('/send_data', methods=['POST'])
def send_data():
    data = request.json
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400
    
    try:
        response = requests.post(f'http://{DEVICE_IP}:{DEVICE_PORT}/device_command', json=data)
        return jsonify({"status": "Success", "response": response.json()}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/device_status', methods=['GET'])
def device_status():
    try:
        response = requests.get(f'http://{DEVICE_IP}:{DEVICE_PORT}/status')
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/debug', methods=['GET'])
def debug():
    return jsonify({"message": "El servidor Flask en Railway está funcionando"}), 200


import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Servidor corriendo en el puerto: {port}")
    app.run(host='0.0.0.0', port=port)


