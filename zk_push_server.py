import falcon
import json
import requests

# 📡 Configuración del equipo ZKTeco
ZKTECO_IP = "10.0.0.201"  # IP del equipo en tu red
ZKTECO_PORT = 8080        # Puerto del dispositivo

class ZKUserHandler:
    def on_get(self, req, resp):
        """ Maneja solicitudes GET para obtener la lista de usuarios del equipo ZKTeco """
        params = req.params
        print(f"📡 GET recibido de ZKTeco con parámetros: {params}")

        if 'action' in params and params['action'] == 'get_users':
            users = self.obtener_usuarios_zkteco()
            if users:
                resp.status = falcon.HTTP_200
                resp.text = json.dumps({"status": "success", "users": users})
            else:
                resp.status = falcon.HTTP_500
                resp.text = json.dumps({"status": "error", "message": "No se pudieron obtener los usuarios de ZKTeco."})
        else:
            resp.text = json.dumps({"status": "error", "message": "Parámetro 'action' no válido."})

        resp.status = falcon.HTTP_200

    def obtener_usuarios_zkteco(self):
        """
        📡 Envía la solicitud `QUERY USERINFO` al ZKTeco para obtener la lista de usuarios.
        """
        try:
            url = f"http://{ZKTECO_IP}:{ZKTECO_PORT}/iclock/cdata"
            payload = "QUERY USERINFO"  # Comando para obtener la lista de usuarios

            response = requests.post(url, data=payload, timeout=10)

            if response.status_code == 200:
                print(f"✅ Usuarios obtenidos correctamente desde ZKTeco.")
                return response.text  # Devuelve la respuesta del equipo
            else:
                print(f"❌ Error al obtener usuarios: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ No se pudo comunicar con ZKTeco: {e}")
            return None

# 🛠️ Crear la aplicación Falcon
app = falcon.App()
app.add_route('/iclock/cdata', ZKUserHandler())






