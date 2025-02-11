from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configuración del dispositivo de control de acceso
DEVICE_IP = "10.0.0.196"  # Cambiar a la IP del equipo
DEVICE_PORT = "8080"  # Puerto del equipo

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
