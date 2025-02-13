import falcon
import requests
import json

ZK_IP = "10.0.0.201"  # IP del dispositivo ZKTeco
ZK_PORT = "8080"  # Puerto del dispositivo
DEVICE_SN = "5430244500365"  # Número de serie del dispositivo

class GetUsers:
    def on_get(self, req, resp):
        """Solicita la lista de usuarios almacenados en el ZKTeco"""
        try:
            url = f"http://{ZK_IP}:{ZK_PORT}/iclock/getrequest?SN={DEVICE_SN}&action=USERINFO"
            print(f"📡 Enviando solicitud al dispositivo: {url}")

            response = requests.get(url)

            if response.status_code == 200:
                print(f"📡 Respuesta del ZKTeco: {response.text}")

                # Guardar la respuesta en un archivo
                with open("/tmp/zkteco_users.txt", "w") as file:
                    file.write(response.text)

                resp.status = falcon.HTTP_200
                resp.text = json.dumps({
                    "status": "success",
                    "message": "Usuarios almacenados correctamente",
                    "file": "/tmp/zkteco_users.txt"
                })

            else:
                print(f"❌ Error en la solicitud: {response.status_code} - {response.text}")
                resp.status = response.status_code
                resp.text = json.dumps({
                    "status": "error",
                    "message": f"Error al obtener usuarios: {response.text}"
                })

        except Exception as e:
            print(f"❌ Error al obtener usuarios: {e}")
            resp.status = falcon.HTTP_500
            resp.text = json.dumps({"status": "error", "message": "Error en el servidor"})

# 🛠️ Crear la aplicación Falcon
app = falcon.App()
app.add_route('/get_users', GetUsers())






