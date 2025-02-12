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
                return
            
            # 📡 Si no es una consulta de usuarios, solo devuelve el mensaje de conexión
            resp.status = falcon.HTTP_200
            resp.text = json.dumps({
                "status": "success",
                "message": "Servidor en Railway activo y listo para recibir datos."
            })
        except Exception as e:
            print(f"❌ Error en GET: {e}")
            resp.status = falcon.HTTP_500
            resp.text = json.dumps({"error": "Fallo en GET."})

    def obtener_usuarios_zkteco(self):
        """
        📡 Envía el comando QUERY USERINFO al dispositivo ZKTeco para obtener la lista de usuarios.
        """
        try:
            url = f"http://{ZKTECO_IP}:{ZKTECO_PORT}/iclock/cdata"
            payload = "QUERY USERINFO"

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
app.add_route('/iclock/cdata', ZKRequestHandler())




