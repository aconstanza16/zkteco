import falcon
import json
import requests

# Configuración del equipo ZKTeco
ZKTECO_IP = "10.0.0.201"  # IP del equipo en la red
ZKTECO_PORT = 8080        # Puerto de comunicación del dispositivo

class ZKRequestHandler:
    def on_get(self, req, resp):
        """ Maneja solicitudes GET desde el equipo ZKTeco """
        try:
            params = req.params  # Captura los parámetros enviados en GET
            print(f"📡 GET recibido de ZKTeco con parámetros: {params}")

            # 📡 Verificar si el cliente solicita la lista de usuarios
            if req.get_param('action') == 'get_users':
                users = self.obtener_usuarios_zkteco()  # 🔹 Ejecuta la consulta a ZKTeco
                if users:
                    resp.status = falcon.HTTP_200
                    resp.text = json.dumps({
                        "status": "success",
                        "message": "Usuarios obtenidos correctamente.",
                        "users": users
                    })
                else:
                    resp.status = falcon.HTTP_500
                    resp.text = json.dumps({
                        "status": "error",
                        "message": "No se pudieron obtener los usuarios de ZKTeco."
                    })
            else:
                # 📡 Si no es una consulta de usuarios, devuelve los GET básicos como antes
                resp.status = falcon.HTTP_200
                resp.text = json.dumps({
                    "status":





